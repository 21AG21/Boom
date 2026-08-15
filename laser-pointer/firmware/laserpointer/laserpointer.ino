/*
 * LASER-POINTER — Bluetooth remote laser, on/off only
 * ------------------------------------------------------------------
 * A tiny fixed laser you switch on and off two ways:
 *   1. a physical button on the device, and
 *   2. your phone / computer over Bluetooth.
 * No motors, no aiming, no patterns (those can come later) — you point
 * the whole gadget where you want the dot and toggle the beam.
 *
 * The ESP32-C3 does Bluetooth Low Energy (BLE), not classic Bluetooth —
 * so the phone side is any "BLE UART" app or the included web app.
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
 *   GPIO4  -> laser module signal (KY-008 "S" pin)
 *   GND    -> laser "-" pin  ·  button leg  ·  (optional LED -)
 *   GPIO10 -> button -> GND      (internal pull-up; no resistor needed)
 *   GPIO5  -> status LED (optional, via 220Ohm to GND)
 *   5V/USB -> powers the board
 *
 * SAFETY: even a 5mW class-3R laser must never hit an eye. Aim the unit
 * so the dot lands on the floor / low walls, never at people, pets'
 * faces, mirrors, or glass.
 */
#include <NimBLEDevice.h>

// ---------------- config ----------------
const char *BLE_NAME = "LASER-PT";

// Nordic UART Service (NUS) UUIDs — the de-facto BLE serial standard.
#define NUS_SERVICE   "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
#define NUS_RX        "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"  // phone -> device
#define NUS_TX        "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"  // device -> phone

const int PIN_LASER = 4;                  // KY-008 signal
const int PIN_LED   = 5;                  // status LED (optional)
const int PIN_BTN   = 10;                 // momentary button to GND

// ---------------- state ----------------
NimBLECharacteristic *txChar = nullptr;
volatile bool connected = false;
bool laserOn = false;

void applyLaser() { digitalWrite(PIN_LASER, laserOn ? HIGH : LOW); }

void notify(const char *s) {
  if (txChar && connected) { txChar->setValue((uint8_t *)s, strlen(s)); txChar->notify(); }
}

void setLaser(bool on) {
  laserOn = on;
  applyLaser();
  notify(on ? "on\n" : "off\n");     // lets the app reflect button presses
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
    if (now - btnSince > 30) setLaser(!laserOn); // debounced toggle
  }
}

// ---------------- command parser ----------------
void handleLine(String cmd) {
  cmd.trim();
  if (cmd.length() == 0) return;
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
  void onConnect(NimBLEServer *, NimBLEConnInfo &) override { connected = true; }
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
}

void loop() {
  serviceButton();
  // status LED: solid while the laser is on, slow heartbeat when idle
  uint32_t now = millis();
  digitalWrite(PIN_LED, laserOn ? HIGH : ((now % 2400) < 70 ? HIGH : LOW));
  delay(5);
}
