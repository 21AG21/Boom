/*
 * Breathe Stone firmware — ESP32-C3 SuperMini
 * -------------------------------------------
 * Drives the crank servo so the thumb pad rises and falls on a paced
 * breathing cadence. No screen, no app, no notifications: one button
 * cycles cadence, the motion itself is the whole interface.
 *
 * The design goal is SILENCE. A servo that is constantly re-commanded
 * hunts and buzzes; here the motion is slow and sine-eased, and the servo
 * is DETACHED during the long breath-holds so the stone is dead quiet in a
 * dark room. (An MG90S metal-gear servo is quieter than an SG90 — worth it.)
 *
 * Arduino IDE setup:
 *   1. Boards manager: install "esp32" (Espressif), pick "ESP32C3 Dev Module"
 *   2. Library manager: install "ESP32Servo"
 *   3. Flash. First power-on starts in COHERENCE (5-5). Tap to cycle.
 *
 * Wiring:
 *   GPIO2  -> crank servo signal      5V / GND -> servo power rails
 *   GPIO9  -> button to GND           (BOOT button; internal pull-up)
 *   GPIO8  -> optional dim LED        (leave unpopulated for a pure-analog stone)
 *
 * Controls:
 *   tap            -> next cadence  (Coherence -> 4-7-8 -> Box -> Pause -> ...)
 *   double-tap     -> pause / resume (park the pad down, go quiet)
 *   hold 1.5 s     -> deep sleep (park down, detach, ~0 mA; tap wakes)
 */
#include <ESP32Servo.h>
#include "esp_sleep.h"

// ---------------- hardware config ----------------
const int PIN_SERVO = 2;
const int PIN_BTN   = 9;     // to GND, INPUT_PULLUP
const int PIN_LED   = 8;     // optional; onboard LED is active-LOW on many C3s
const bool USE_LED  = false; // true for a faint glow synced to the breath

// Servo travel that maps to the pad's full down..up stroke. Calibrate to
// YOUR crank so the pad moves ~4 mm and never binds at the ends.
const int SERVO_DOWN = 18;   // exhaled: pad at rest, lowest
const int SERVO_UP   = 92;   // inhaled: pad raised
const int SERVO_MIN_US = 500, SERVO_MAX_US = 2400;

const uint32_t TICK_MS      = 20;     // 50 Hz motion loop
const uint32_t QUIET_HOLD_MS = 600;   // detach the servo after this still-time
const uint32_t SESSION_MIN  = 20;     // auto-sleep after N minutes of use

// ---------------- cadence library ----------------
// A cadence is a ring of segments. Each segment eases the pad "openness"
// (0 = exhaled/down, 1 = inhaled/up) from a->b over ms milliseconds.
struct Seg { float a, b; uint32_t ms; };
struct Cadence { const char *name; const Seg *seg; uint8_t n; };

// 5-5 coherence breathing (calm, the default resting cadence)
const Seg COHERENCE[] = {{0, 1, 5000}, {1, 0, 5000}};
// 4-7-8 (sleep / down-regulation): inhale 4, hold 7, exhale 8
const Seg C478[]      = {{0, 1, 4000}, {1, 1, 7000}, {1, 0, 8000}};
// box breathing 4-4-4-4 (focus): inhale, hold in, exhale, hold out
const Seg BOX[]       = {{0, 1, 4000}, {1, 1, 4000}, {1, 0, 4000}, {0, 0, 4000}};

const Cadence CADENCES[] = {
  {"coherence", COHERENCE, 2},
  {"4-7-8",     C478,      3},
  {"box",       BOX,       4},
};
const uint8_t N_CAD = sizeof(CADENCES) / sizeof(CADENCES[0]);

// ---------------- state ----------------
Servo servo;
bool attached = false;
bool paused   = false;
uint8_t cad = 0;                 // current cadence index
uint8_t segI = 0;                // current segment
uint32_t segStart = 0, lastTick = 0, sessionStart = 0;
float levelNow = 0, levelCmd = 0, lastWritten = -1;
uint32_t stillSince = 0;

// smootherstep: zero velocity at both ends -> no robotic jerk, no servo snap
float ease(float t) {
  t = t < 0 ? 0 : (t > 1 ? 1 : t);
  return t * t * t * (t * (t * 6 - 15) + 10);
}

void attachServo() {
  if (!attached) { servo.attach(PIN_SERVO, SERVO_MIN_US, SERVO_MAX_US); attached = true; }
}
void detachServo() {
  if (attached) { servo.detach(); attached = false; }
}

void writePad(float level) {
  int ang = SERVO_DOWN + (int)roundf(level * (SERVO_UP - SERVO_DOWN));
  if ((float)ang == lastWritten) return;      // don't re-command: kills buzz
  attachServo();
  servo.write(ang);
  lastWritten = ang;
  stillSince = millis();
}

void ledGlow(float level) {
  if (!USE_LED) return;
  // active-LOW onboard LED; faint so it never becomes a "notification"
  int duty = (int)(level * 40);               // cap at ~16% brightness
  analogWrite(PIN_LED, 255 - duty);
}

// ---------------- button (tap / double-tap / hold) ----------------
uint32_t btnDownAt = 0, lastTapAt = 0;
bool btnPrev = HIGH, holdFired = false;

void goSleep() {
  writePad(0);                                // park the pad down
  delay(400);
  detachServo();
  if (USE_LED) analogWrite(PIN_LED, 255);
  esp_deep_sleep_enable_gpio_wakeup(1ULL << PIN_BTN, ESP_GPIO_WAKEUP_GPIO_LOW);
  esp_deep_sleep_start();                     // tap on PIN_BTN wakes -> setup()
}

void nextCadence() {
  cad = (cad + 1) % N_CAD;
  segI = 0; segStart = millis();
}

void handleButton() {
  bool b = digitalRead(PIN_BTN);
  uint32_t now = millis();
  if (btnPrev == HIGH && b == LOW) {          // press
    btnDownAt = now; holdFired = false;
  } else if (b == LOW && !holdFired && now - btnDownAt > 1500) {
    holdFired = true;                         // long hold -> sleep
    goSleep();
  } else if (btnPrev == LOW && b == HIGH) {   // release
    if (holdFired) { /* consumed by sleep */ }
    else if (now - lastTapAt < 350) {         // second tap -> pause toggle
      paused = !paused;
      if (!paused) { segI = 0; segStart = now; sessionStart = now; }
      lastTapAt = 0;
    } else {
      lastTapAt = now;                        // provisional single tap
    }
  }
  // commit a lone single-tap once the double-tap window closes
  if (lastTapAt && now - lastTapAt >= 350 && b == HIGH) {
    nextCadence();
    lastTapAt = 0;
  }
  btnPrev = b;
}

// ---------------- setup / loop ----------------
void setup() {
  pinMode(PIN_BTN, INPUT_PULLUP);
  if (USE_LED) { pinMode(PIN_LED, OUTPUT); analogWrite(PIN_LED, 255); }
  servo.setPeriodHertz(50);
  attachServo();
  writePad(0);                                // start exhaled/at rest
  uint32_t now = millis();
  segStart = sessionStart = lastTick = now;
}

void loop() {
  handleButton();
  uint32_t now = millis();
  if (now - lastTick < TICK_MS) return;
  lastTick = now;

  // auto-sleep after a full session so a pocketed stone never drains
  if (!paused && (now - sessionStart) > SESSION_MIN * 60000UL) goSleep();

  if (paused) {                               // quiet hold at rest
    levelCmd = 0;
    if (levelNow > 0.01f) levelNow += (0 - levelNow) * 0.08f;   // ease down once
    else if (now - stillSince > QUIET_HOLD_MS) { detachServo(); ledGlow(0); return; }
    writePad(levelNow);
    return;
  }

  // advance the cadence ring
  const Cadence &C = CADENCES[cad];
  const Seg &S = C.seg[segI];
  float t = (now - segStart) / (float)S.ms;
  if (t >= 1.0f) {                            // next segment
    segI = (segI + 1) % C.n;
    segStart = now;
    t = 0;
  }
  levelCmd = S.a + (S.b - S.a) * ease(t);     // sine-eased breath waveform

  // detach during a genuine hold (a == b) once the pad has settled: silence
  bool holding = (S.a == S.b);
  if (holding && now - stillSince > QUIET_HOLD_MS) {
    detachServo();                            // dead quiet through the hold
    ledGlow(levelCmd);
    return;
  }

  levelNow += (levelCmd - levelNow) * 0.5f;   // light smoothing on top of ease
  writePad(levelNow);
  ledGlow(levelNow);
}
