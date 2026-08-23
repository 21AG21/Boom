/*
 * Lull firmware — ESP32-C3 (or any small MCU) + one N-MOSFET
 * ---------------------------------------------------------
 * The breath WAVEFORM lives in the cam's shape, so the firmware's only job is
 * to spin the motor at a slow, steady speed — one cam rotation per breath.
 * That's it. A button cycles: OFF -> 5 breaths/min -> 4 breaths/min -> OFF.
 *
 * Because the cam does the shaping, there is deliberately no waveform code
 * here. (You could even run Lull with no MCU at all — a switch picking two
 * dropper resistors to the motor — but a tiny PWM makes speed adjustable.)
 *
 * Wiring:
 *   GPIO2 -> gate of a logic-level N-MOSFET (AO3400 / IRLML2502).
 *            Motor across battery+ and the MOSFET drain; source to battery-.
 *            A flyback diode (1N5819) across the motor, cathode to battery+.
 *   GPIO9 -> button to GND (BOOT button; internal pull-up).
 *   GPIO8 -> optional dim LED.
 *   Power: 2xAAA (3V) or a 3.7V LiPo. Keep the MCU on its own regulated rail.
 *
 * CALIBRATE ONCE: the duty->RPM relationship depends on your exact motor,
 * gearbox, battery, and mechanism friction (it's open-loop). Print the cam,
 * assemble, then adjust DUTY_5BPM / DUTY_4BPM until a full breath takes 12 s
 * (5/min) or 15 s (4/min) — time ten breaths and divide.
 */
#include "esp_sleep.h"

const int PIN_MOTOR = 2;
const int PIN_BTN   = 9;
const int PIN_LED   = 8;
const bool USE_LED  = false;

const int PWM_CH=0, PWM_FREQ=20000, PWM_BITS=10, PWM_MAX=(1<<PWM_BITS)-1;

// --- calibrate these to hit the cadence (see header) ---
const float DUTY_5BPM = 0.52;   // ~5 breaths/min  (12 s per cam revolution)
const float DUTY_4BPM = 0.44;   // ~4 breaths/min  (15 s per revolution)
const float START_DUTY_BOOST = 0.85;   // brief kick to break static friction
const uint32_t BOOST_MS = 250;

const uint32_t SESSION_MIN = 20;        // auto-off so a pocketed unit never drains

enum Mode { OFF, BPM5, BPM4 };
Mode mode = BPM5;
float duty = 0, dutyTgt = 0;
uint32_t modeStart = 0, lastTick = 0, sessionStart = 0;

void setDuty(float d){
  d = d<0?0:(d>1?1:d);
  ledcWrite(PWM_CH, (int)(d*PWM_MAX));
  if(USE_LED) analogWrite(PIN_LED, 255-(int)(d*45));
}
void applyMode(Mode m){
  mode=m; modeStart=millis(); sessionStart=millis();
  dutyTgt = (m==BPM5)?DUTY_5BPM : (m==BPM4)?DUTY_4BPM : 0;
}

// --- button: tap cycles modes, hold sleeps ---
uint32_t downAt=0; bool prev=true, held=false;
void goSleep(){ setDuty(0); delay(60); if(USE_LED) analogWrite(PIN_LED,255);
  esp_deep_sleep_enable_gpio_wakeup(1ULL<<PIN_BTN, ESP_GPIO_WAKEUP_GPIO_LOW); esp_deep_sleep_start(); }
void button(){
  bool b=digitalRead(PIN_BTN); uint32_t now=millis();
  if(prev && !b){ downAt=now; held=false; }
  else if(!b && !held && now-downAt>1200){ held=true; goSleep(); }
  else if(!prev && b && !held){ applyMode(mode==BPM5?BPM4:(mode==BPM4?OFF:BPM5)); }
  prev=b;
}

void setup(){
  pinMode(PIN_BTN, INPUT_PULLUP);
  if(USE_LED){ pinMode(PIN_LED,OUTPUT); analogWrite(PIN_LED,255); }
  ledcSetup(PWM_CH,PWM_FREQ,PWM_BITS); ledcAttachPin(PIN_MOTOR,PWM_CH);
  applyMode(BPM5);
  lastTick=millis();
}

void loop(){
  button();
  uint32_t now=millis();
  if(now-lastTick<15) return; lastTick=now;

  if(mode!=OFF && now-sessionStart > SESSION_MIN*60000UL) applyMode(OFF);

  // soft ramp toward target duty; brief boost at start to overcome stiction
  if(mode!=OFF && now-modeStart<BOOST_MS) setDuty(START_DUTY_BOOST);
  else { duty += (dutyTgt-duty)*0.05; setDuty(duty); }
}
