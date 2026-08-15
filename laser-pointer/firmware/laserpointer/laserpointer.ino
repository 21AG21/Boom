/*
 * LASER-POINTER — Bluetooth (BLE) pan/tilt laser pointer
 * ------------------------------------------------------------------
 * A visible desk toy / cat toy. The ESP32-C3 advertises a BLE UART
 * service; connect from your phone and send short text commands to aim,
 * toggle the laser, or start patrol. Nothing hidden — it sits out in the
 * open and it's obviously yours.
 *
 * The ESP32-C3 supports Bluetooth Low Energy (BLE), not classic
 * Bluetooth SPP. So you control it with any "BLE UART" / "BLE terminal"
 * phone app rather than the old pair-as-a-serial-port method.
 *
 * Arduino IDE setup:
 *   1. Boards manager: install "esp32" (Espressif), pick "ESP32C3 Dev Module"
 *   2. Library manager: install "ESP32Servo" and "NimBLE-Arduino"
 *   3. Flash over USB-C.
 *
 * Connect from your phone:
 *   - Install a BLE UART app: "nRF Connect" (iOS/Android) or
 *     "Serial Bluetooth Terminal" (Android, enable BLE mode).
 *   - Scan, connect to "LASER-PT", open the Nordic UART service, and
 *     send the commands below to the RX characteristic.
 *
 * Commands (case-insensitive, one per line):
 *   P<0-100>   pan to a percent of travel      e.g.  P50  (center)
 *   T<0-100>   tilt to a percent of travel     e.g.  T30
 *   J<px>,<py> joystick: two 0-100 values      e.g.  J50,80
 *   L1 / L0    laser on / off
 *   M1 / M0    patrol on / off
 *   X          all off: laser off + park level
 *
 * Wiring:
 *   GPIO2 -> pan servo signal
 *   GPIO3 -> tilt servo signal
 *   GPIO4 -> laser module signal (KY-008 style, 5mW class-3R)
 *   5V / GND -> servo power rails + laser power
 *   GPIO5 -> status LED (slow blink idle, solid while laser on)
 *
 * SAFETY: even a 5mW pointer must never hit an eye. TILT_MAX below is a
 * hard firmware ceiling — the beam physically cannot rise above it. Set
 * it so the dot stays on the floor / low walls for your setup, and don't
 * aim at mirrors or glass. It's a cat toy, not a prank on people.
 */
#include <ESP32Servo.h>
#include <NimBLEDevice.h>

// ---------------- config ----------------
const char *BLE_NAME = "LASER-PT";

// Nordic UART Service (NUS) UUIDs — the de-facto BLE serial standard.
#define NUS_SERVICE   "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
#define NUS_RX        "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"  // phone -> device
#define NUS_TX        "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"  // device -> phone

const int PIN_PAN = 2, PIN_TILT = 3, PIN_LASER = 4, PIN_LED = 5;

// Physical button (momentary, wired GPIO10 -> button -> GND; uses the
// chip's internal pull-up). Short press: toggle laser. Long press
// (>600 ms): toggle patrol. Lets you run the toy without a phone.
const int PIN_BTN = 10;
const uint32_t LONG_PRESS_MS = 600;

// Servo travel. TILT: 90 = level beam. TILT_MAX < 90 keeps the beam
// pointed DOWNWARD — that's your eye-safety ceiling. Calibrate for the
// spot the toy sits in.
const float PAN_MIN = 10, PAN_MAX = 170;
const float TILT_MIN = 55;              // steepest downward aim
const float TILT_MAX = 88;              // safety ceiling (< 90 = below level)

const float EASE = 0.14;                // per-tick easing (smaller = smoother)
const uint32_t TICK_MS = 20;            // 50 Hz motion loop

// ---------------- state ----------------
Servo panServo, tiltServo;
NimBLECharacteristic *txChar = nullptr;
volatile bool connected = false;

enum Mode { MANUAL, PATROL };
Mode mode = MANUAL;
float panNow = 90, tiltNow = 75, panTgt = 90, tiltTgt = 75;
bool laserOn = false;
uint32_t lastTick = 0, patrolUntil = 0;

float clampf(float v, float lo, float hi) {
  return v < lo ? lo : (v > hi ? hi : v);
}

// ---------------- physical button ----------------
bool btnDown = false;
uint32_t btnSince = 0;
bool btnLongFired = false;

void toggleLaser() {
  laserOn = !laserOn;
  digitalWrite(PIN_LASER, laserOn ? HIGH : LOW);
}

void togglePatrol() {
  mode = (mode == PATROL) ? MANUAL : PATROL;
  if (mode == PATROL) patrolUntil = 0;
}

void serviceButton() {
  bool pressed = digitalRead(PIN_BTN) == LOW;   // active-low with pull-up
  uint32_t now = millis();
  if (pressed && !btnDown) {                     // edge: just pressed
    btnDown = true; btnSince = now; btnLongFired = false;
  } else if (pressed && btnDown && !btnLongFired && now - btnSince > LONG_PRESS_MS) {
    togglePatrol();                              // long press
    btnLongFired = true;
  } else if (!pressed && btnDown) {              // edge: released
    btnDown = false;
    if (!btnLongFired && now - btnSince > 30) toggleLaser();  // short press (debounced)
  }
}

void notify(const char *s) {
  if (txChar && connected) { txChar->setValue((uint8_t *)s, strlen(s)); txChar->notify(); }
}

// map a 0-100 percent to a servo range
float pct(float p, float lo, float hi) {
  return lo + clampf(p, 0, 100) / 100.0 * (hi - lo);
}

// ---------------- command parser ----------------
void handleLine(String cmd) {
  cmd.trim();
  if (cmd.length() == 0) return;
  char c = toupper(cmd.charAt(0));
  String rest = cmd.substring(1);

  switch (c) {
    case 'P':
      panTgt = pct(rest.toFloat(), PAN_MIN, PAN_MAX);
      if (mode == PATROL) mode = MANUAL;
      break;
    case 'T':
      tiltTgt = pct(rest.toFloat(), TILT_MIN, TILT_MAX);
      if (mode == PATROL) mode = MANUAL;
      break;
    case 'J': {                          // "J<px>,<py>"
      int comma = rest.indexOf(',');
      if (comma > 0) {
        panTgt  = pct(rest.substring(0, comma).toFloat(), PAN_MIN, PAN_MAX);
        tiltTgt = pct(rest.substring(comma + 1).toFloat(), TILT_MIN, TILT_MAX);
        if (mode == PATROL) mode = MANUAL;
      }
      break;
    }
    case 'L':
      laserOn = rest.toInt() == 1;
      digitalWrite(PIN_LASER, laserOn ? HIGH : LOW);
      break;
    case 'M':
      mode = (rest.toInt() == 1) ? PATROL : MANUAL;
      if (mode == PATROL) patrolUntil = 0;
      break;
    case 'X':                            // all off + park level
      mode = MANUAL;
      laserOn = false;
      digitalWrite(PIN_LASER, LOW);
      panTgt = 90;
      tiltTgt = TILT_MIN + (TILT_MAX - TILT_MIN) * 0.5;
      break;
    default:
      notify("? unknown cmd\n");
      return;
  }
  notify("ok\n");
}

// ---------------- BLE callbacks ----------------
class ServerCB : public NimBLEServerCallbacks {
  void onConnect(NimBLEServer *, NimBLEConnInfo &) override { connected = true; }
  void onDisconnect(NimBLEServer *s, NimBLEConnInfo &, int) override {
    connected = false;
    laserOn = false;                     // fail safe: laser off if phone drops
    digitalWrite(PIN_LASER, LOW);
    NimBLEDevice::startAdvertising();    // allow reconnect
  }
};

class RxCB : public NimBLECharacteristicCallbacks {
  void onWrite(NimBLECharacteristic *chr, NimBLEConnInfo &) override {
    std::string v = chr->getValue();
    // a single write may carry several newline-separated commands
    String buf = String(v.c_str());
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

  panServo.setPeriodHertz(50);
  panServo.attach(PIN_PAN, 500, 2400);
  tiltServo.setPeriodHertz(50);
  tiltServo.attach(PIN_TILT, 500, 2400);

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
  uint32_t now = millis();
  digitalWrite(PIN_LED, laserOn ? HIGH : ((now % 2400) < 70 ? HIGH : LOW));
  if (now - lastTick < TICK_MS) return;
  lastTick = now;

  if (mode == PATROL && now > patrolUntil) {
    // slow random drift, then a long natural pause — good for a cat
    panTgt = random((int)PAN_MIN, (int)PAN_MAX);
    tiltTgt = random((int)TILT_MIN, (int)TILT_MAX);
    patrolUntil = now + random(3000, 11000);
  }

  panNow += (panTgt - panNow) * EASE;
  tiltNow += (tiltTgt - tiltNow) * EASE;
  tiltNow = clampf(tiltNow, TILT_MIN, TILT_MAX);   // hard safety clamp

  panServo.write(panNow);
  tiltServo.write(tiltNow);
}
