/*
 * Breathe Stone v2 firmware — ESP32-C3 + nitinol (shape-memory) wire
 * -----------------------------------------------------------------
 * No motor. A MOSFET pulses current through a nitinol wire; the wire warms
 * and CONTRACTS, pulling a bell crank that lifts the dome (inhale). Cut the
 * current and the wire cools and a return spring lowers the dome (exhale).
 * There is nothing to hunt, hold, or gear — so the stone is truly silent.
 *
 * Two facts drive this firmware:
 *   1. INHALE is active (we heat the wire); EXHALE is passive (we stop
 *      heating and physics does the rest). We can shape the rise precisely
 *      but the fall rate is set by how fast the wire cools — so pick a wire
 *      gauge whose natural cooling time ≈ your exhale seconds (thin = fast).
 *   2. Nitinol degrades if cooked. Holding full contraction at full current
 *      overheats it. So a HOLD uses a reduced maintenance duty, and a global
 *      THERMAL BUDGET forces a cool-down if we've been driving too hard.
 *
 * Wiring:
 *   GPIO2 -> MOSFET gate (logic-level N-ch, e.g. AO3400/IRLML2502)
 *            wire in series with the MOSFET drain; source to battery -.
 *   GPIO9 -> button to GND (BOOT button, internal pull-up)
 *   GPIO8 -> optional dim LED
 *   Size the wire current with its own resistance + a small series resistor;
 *   PWM sets the AVERAGE heating power. Never drive DC at 100%.
 *
 * Arduino IDE: install "esp32" (Espressif), board "ESP32C3 Dev Module".
 * Controls: tap = next cadence · double-tap = pause · hold 1.5s = sleep.
 */
#include "esp_sleep.h"

// ---------------- pins ----------------
const int PIN_SMA = 2;      // MOSFET gate (PWM)
const int PIN_BTN = 9;      // to GND, INPUT_PULLUP
const int PIN_LED = 8;      // optional
const bool USE_LED = false;

// ---------------- PWM ----------------
const int   PWM_CH   = 0;
const int   PWM_FREQ = 500;     // Hz through the MOSFET
const int   PWM_BITS = 10;      // 0..1023
const int   PWM_MAX  = (1 << PWM_BITS) - 1;

// ---------------- SMA drive (CALIBRATE to your wire) ----------------
// Duty is a fraction 0..1 of full current. These are the safe knobs.
const float PULL_DUTY = 0.90;   // peak heating while actively contracting (inhale)
const float HOLD_DUTY = 0.32;   // maintenance to *stay* contracted through a hold
const float DUTY_CAP  = 0.95;   // hard ceiling — never exceed
// Thermal budget: integrate duty over time; if we exceed the budget, force a
// cool-down so the wire never bakes. Units are "duty-seconds".
const float THERM_MAX   = 14.0; // allowed heat debt before a forced cool
const float THERM_COOL  = 6.0;  // resume once debt falls back under this
const float THERM_LEAK  = 0.55; // debt bleeds off at this many units/sec when cool

const uint32_t TICK_MS = 20;
const uint32_t SESSION_MIN = 20;

// ---------------- cadence library ----------------
// level 0 = exhaled (dome down), 1 = inhaled (dome up).
struct Seg { float a, b; uint32_t ms; };
struct Cadence { const char *name; const Seg *seg; uint8_t n; };
// NOTE: exhale segments (b < a) command cooling — their *minimum* duration is
// the wire's cool time. Keep exhale >= inhale so physics can keep up.
const Seg COHERENCE[] = {{0,1,5000},{1,0,5500}};
const Seg C478[]      = {{0,1,4000},{1,1,7000},{1,0,8000}};
const Seg BOX[]       = {{0,1,4000},{1,1,4000},{1,0,5000},{0,0,4000}};
const Cadence CADENCES[] = {{"coherence",COHERENCE,2},{"4-7-8",C478,3},{"box",BOX,4}};
const uint8_t N_CAD = 3;

// ---------------- state ----------------
bool paused = false;
uint8_t cad = 0, segI = 0;
uint32_t segStart = 0, lastTick = 0, sessionStart = 0;
float levelNow = 0;
float thermDebt = 0;      // accumulated heat
bool cooling = false;     // forced cool-down latch

float clampf(float v, float lo, float hi){ return v<lo?lo:(v>hi?hi:v); }
float ease(float t){ t=clampf(t,0,1); return t*t*t*(t*(t*6-15)+10); }

void driveDuty(float duty){
  duty = clampf(duty, 0, DUTY_CAP);
  ledcWrite(PWM_CH, (int)(duty * PWM_MAX));
  if (USE_LED) analogWrite(PIN_LED, 255 - (int)(duty*40)); // faint, optional
}

// ---------------- button ----------------
uint32_t btnDownAt=0, lastTapAt=0; bool btnPrev=true, holdFired=false;

void goSleep(){
  driveDuty(0);                                  // wire cools, spring parks the dome
  delay(300);
  if (USE_LED) analogWrite(PIN_LED, 255);
  esp_deep_sleep_enable_gpio_wakeup(1ULL<<PIN_BTN, ESP_GPIO_WAKEUP_GPIO_LOW);
  esp_deep_sleep_start();
}
void nextCadence(){ cad=(cad+1)%N_CAD; segI=0; segStart=millis(); }

void handleButton(){
  bool b=digitalRead(PIN_BTN); uint32_t now=millis();
  if (btnPrev && !b){ btnDownAt=now; holdFired=false; }
  else if (!b && !holdFired && now-btnDownAt>1500){ holdFired=true; goSleep(); }
  else if (!btnPrev && b){
    if (holdFired){}
    else if (now-lastTapAt<350){ paused=!paused; if(!paused){segI=0; segStart=now; sessionStart=now;} lastTapAt=0; }
    else lastTapAt=now;
  }
  if (lastTapAt && now-lastTapAt>=350 && b){ nextCadence(); lastTapAt=0; }
  btnPrev=b;
}

// ---------------- setup / loop ----------------
void setup(){
  pinMode(PIN_BTN, INPUT_PULLUP);
  if (USE_LED){ pinMode(PIN_LED, OUTPUT); analogWrite(PIN_LED,255); }
  ledcSetup(PWM_CH, PWM_FREQ, PWM_BITS);
  ledcAttachPin(PIN_SMA, PWM_CH);
  driveDuty(0);
  uint32_t now=millis(); segStart=sessionStart=lastTick=now;
}

void loop(){
  handleButton();
  uint32_t now=millis();
  if (now-lastTick < TICK_MS) return;
  float dt=(now-lastTick)/1000.0f; lastTick=now;

  if (!paused && (now-sessionStart) > SESSION_MIN*60000UL) goSleep();

  // --- desired breath level from the cadence ---
  float levelCmd = 0; bool holding = false;
  if (!paused){
    const Cadence &C = CADENCES[cad]; const Seg &S = C.seg[segI];
    float t=(now-segStart)/(float)S.ms;
    if (t>=1.0f){ segI=(segI+1)%C.n; segStart=now; t=0; }
    holding = (S.a==S.b) && S.a>0.5f;      // a real "hold in" phase
    levelCmd = S.a + (S.b-S.a)*ease(t);
  }
  levelNow += (levelCmd-levelNow)*0.5f;

  // --- map level -> heating duty (open-loop; calibrate the two dutys) ---
  // Rising/holding needs current; falling commands zero and lets it cool.
  float duty;
  if (levelCmd <= levelNow + 0.001f){        // at target or exhaling
    duty = holding ? HOLD_DUTY*levelNow : 0.0f;
  } else {                                    // actively inhaling
    duty = PULL_DUTY * levelCmd;
  }

  // --- thermal budget: protect the wire ---
  thermDebt += duty*dt;                       // heat we're adding
  thermDebt -= THERM_LEAK*dt;                 // heat bleeding off
  if (thermDebt < 0) thermDebt = 0;
  if (thermDebt > THERM_MAX) cooling = true;  // too hot -> force a cool-down
  if (cooling && thermDebt < THERM_COOL) cooling = false;
  if (cooling) duty = 0;                       // safety wins over the cadence

  driveDuty(duty);
}
