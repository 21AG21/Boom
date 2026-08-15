/*
 * LASER-POINTER — Bluetooth remote laser, on/off + deep sleep
 * ------------------------------------------------------------------
 * A tiny fixed laser you switch on/off from a physical button and from
 * your phone/laptop over Bluetooth. No motors, no patterns yet.
 *
 * POWER / SLEEP (the important part for the compact build):
 *   The ESP32-C3 has two states.
 *     AWAKE  — Bluetooth is live, button + phone both work. ~40-80 mA.
 *     ASLEEP — deep sleep, everything off but the button. ~10 uA.
 *   It auto-sleeps after SLEEP_AFTER_MS of being idle (laser off AND no
 *   phone connected). Pressing the button WAKES it and turns the laser
 *   on in one action. While asleep the phone can't reach it — press the
 *   button once to wake it, then connect. This is what lets a ~100 mAh
 *   cell last months of standby instead of an hour.
 *
 * The ESP32-C3 does Bluetooth Low Energy (BLE), not classic Bluetooth —
 * the phone side is any "BLE UART" app or the included web app.
 *
 * Arduino IDE setup:
 *   1. Boards manager: install "esp32" (Espressif), pick "ESP32C3 Dev Module"
 *   2. Library manager: install "NimBLE-Arduino"
 *   3. Flash over USB-C.
 *
 * Phone commands (Nordic UART; case-insensitive, one per line):
 *   L1  laser on      L0  laser off      T  toggle
 *
 * Wiring (the whole circuit):
 *   GPIO4  -> laser diode signal (KY-008 "S" pin, or a bare 6mm diode +)
 *   GND    -> laser "-"  ·  button leg  ·  (optional LED -)
 *   GPIO10 -> button -> GND      (internal pull-up; also the wake pin)
 *   GPIO5  -> status LED (optional, via 220Ohm to GND)
 *   3V3/battery or USB -> powers the board
 *
 * NOTE: the wake button MUST be on an RTC-capable pin. GPIO10 works on
 * the ESP32-C3. If you move it, pick another GPIO the C3 can wake from.
 *
 * SAFETY: even a 5mW class-3R laser must never hit an eye. Aim the unit
 * so the dot lands on the floor / low walls, never at people, pets'
 * faces, mirrors, or glass.
 */
#include <NimBLEDevice.h>
#include "esp_sleep.h"
#include "driver/gpio.h"

// ---------------- config ----------------
const char *BLE_NAME = "LASER-PT";

// Nordic UART Service (NUS) UUIDs — the de-facto BLE serial standard.
#define NUS_SERVICE   "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
#define NUS_RX        "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"  // phone -> device
#define NUS_TX        "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"  // device -> phone

const int PIN_LASER = 4;                  // laser signal
const int PIN_LED   = 5;                  // status LED (optional)
const int PIN_BTN   = 10;                 // momentary button to GND + wake pin

// Go to deep sleep after this long idle (laser off AND no phone connected).
const uint32_t SLEEP_AFTER_MS = 120000;   // 2 minutes

// ---------------- state ----------------
NimBLECharacteristic *txChar = nullptr;
volatile bool connected = false;
bool laserOn = false;
uint32_t lastActivity = 0;                // millis() of the last thing we did
bool consumeRelease = false;              // swallow the release of the wake-press

void touch() { lastActivity = millis(); } // "something happened, stay awake"

void applyLaser() { digitalWrite(PIN_LASER, laserOn ? HIGH : LOW); }

void notify(const char *s) {
  if (txChar && connected) { txChar->setValue((uint8_t *)s, strlen(s)); txChar->notify(); }
}

void setLaser(bool on) {
  laserOn = on;
  applyLaser();
  touch();
  notify(on ? "on\n" : "off\n");          // lets the app mirror button presses
}

// ---------------- deep sleep ----------------
void goToSleep() {
  digitalWrite(PIN_LASER, LOW);
  digitalWrite(PIN_LED, LOW);
  // keep the pull-up on the button alive through deep sleep, then wake
  // when the button pulls the pin LOW.
  gpio_set_direction((gpio_num_t)PIN_BTN, GPIO_MODE_INPUT);
  gpio_pullup_en((gpio_num_t)PIN_BTN);
  gpio_pulldown_dis((gpio_num_t)PIN_BTN);
  esp_deep_sleep_enable_gpio_wakeup(1ULL << PIN_BTN, ESP_GPIO_WAKEUP_GPIO_LOW);
  esp_deep_sleep_start();                 // chip halts here; wakes via full reboot
}

// ---------------- physical button ----------------
bool btnDown = false;
uint32_t btnSince = 0;

void serviceButton() {
  bool pressed = digitalRead(PIN_BTN) == LOW;   // active-low with pull-up
  uint32_t now = millis();
  if (pressed && !btnDown) {                     // just pressed
    btnDown = true; btnSince = now;
  } else if (!pressed && btnDown) {              // released
    btnDown = false;
    if (consumeRelease) { consumeRelease = false; touch(); return; }  // wake-press
    if (now - btnSince > 30) setLaser(!laserOn); // debounced toggle
  }
}

// ---------------- command parser ----------------
void handleLine(String cmd) {
  cmd.trim();
  if (cmd.length() == 0) return;
  touch();
  char c = toupper(cmd.charAt(0));
  switch (c) {
    case 'L': setLaser(cmd.substring(1).toInt() == 1); break;  // L1 / L0
    case 'T': setLaser(!laserOn); break;                        // toggle
    case 'X': setLaser(false); break;                           // off
    default:  notify("? unknown cmd\n"); return;
  }
}

// ---------------- BLE callbacks ----------------
class ServerCB : public NimBLEServerCallbacks {
  void onConnect(NimBLEServer *, NimBLEConnInfo &) override { connected = true; touch(); }
  void onDisconnect(NimBLEServer *s, NimBLEConnInfo &, int) override {
    connected = false;
    setLaser(false);                    // fail safe: laser off if phone drops
    NimBLEDevice::startAdvertising();
  }
};

class RxCB : public NimBLECharacteristicCallbacks {
  void onWrite(NimBLECharacteristic *chr, NimBLEConnInfo &) override {
    String buf = String(chr->getValue().c_str());
    int nl;
    while ((nl = buf.indexOf('\n')) >= 0) {
      handleLine(buf.substring(0, nl));
      buf = buf.substring(nl + 1);
    }
    if (buf.length()) handleLine(buf);
  }
};

// ---------------- setup / loop ----------------
void setup() {
  pinMode(PIN_LASER, OUTPUT);
  digitalWrite(PIN_LASER, LOW);
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_BTN, INPUT_PULLUP);

  // If we woke because the button was pressed, treat it as "turn on":
  // light the laser now and swallow the button's release so it doesn't
  // immediately toggle back off.
  if (esp_sleep_get_wakeup_cause() == ESP_SLEEP_WAKEUP_GPIO) {
    laserOn = true;
    consumeRelease = true;
    btnDown = true;
    btnSince = millis();
  }
  applyLaser();

  NimBLEDevice::init(BLE_NAME);
  NimBLEServer *server = NimBLEDevice::createServer();
  server->setCallbacks(new ServerCB());

  NimBLEService *svc = server->createService(NUS_SERVICE);
  txChar = svc->createCharacteristic(NUS_TX, NIMBLE_PROPERTY::NOTIFY);
  NimBLECharacteristic *rxChar =
      svc->createCharacteristic(NUS_RX, NIMBLE_PROPERTY::WRITE | NIMBLE_PROPERTY::WRITE_NR);
  rxChar->setCallbacks(new RxCB());
  svc->start();

  NimBLEAdvertising *adv = NimBLEDevice::getAdvertising();
  adv->addServiceUUID(NUS_SERVICE);
  adv->setName(BLE_NAME);
  NimBLEDevice::startAdvertising();

  touch();
}

void loop() {
  serviceButton();
  uint32_t now = millis();

  // status LED: solid while the laser is on, slow heartbeat when idle
  digitalWrite(PIN_LED, laserOn ? HIGH : ((now % 2400) < 70 ? HIGH : LOW));

  // auto-sleep when there's nothing to stay awake for
  if (!laserOn && !connected && now - lastActivity > SLEEP_AFTER_MS) {
    goToSleep();
  }

  delay(5);
}
