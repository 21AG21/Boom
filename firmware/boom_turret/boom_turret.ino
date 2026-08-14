/*
 * Boom turret firmware — ESP32-C3 SuperMini
 * ------------------------------------------
 * Creates a WiFi access point and serves a phone joystick page.
 *
 * Arduino IDE setup:
 *   1. Boards manager: install "esp32" (Espressif), pick "ESP32C3 Dev Module"
 *   2. Library manager: install "ESP32Servo"
 *   3. Flash, join WiFi "BOOM-net" (password below), open http://192.168.4.1
 *
 * Wiring (matches the build docs):
 *   GPIO2 -> pan servo signal      GPIO3 -> tilt servo signal (pouch only)
 *   GPIO4 -> laser module signal   5V/GND -> servo + laser power rails
 */
#include <WiFi.h>
#include <WebServer.h>
#include <ESP32Servo.h>

// ---------------- build config ----------------
#define BUILD_POUCH 1        // 1 = pencil case (pan + tilt), 0 = bottle (pan only)

const char *AP_SSID = "BOOM-net";
const char *AP_PASS = "pewpew123";   // change me

const int PIN_PAN = 2, PIN_TILT = 3, PIN_LASER = 4;

// Servo angle limits. TILT: 90 = level. The MAX below is the SAFETY
// CEILING — beam can never rise above it. Calibrate for your room so the
// beam stays below chest height at the wall.
const float PAN_MIN = 10, PAN_MAX = 170;
const float TILT_MIN = 55;           // steepest downward aim
const float TILT_MAX = 88;           // safety ceiling (< 90 = below level)

const float EASE = 0.08;             // per-tick easing (smaller = smoother)
const uint32_t TICK_MS = 20;         // 50 Hz motion loop

// ---------------- state ----------------
Servo panServo, tiltServo;
WebServer server(80);

enum Mode { MANUAL, PATROL, FROZEN };
Mode mode = MANUAL;
float panNow = 90, tiltNow = 75, panTgt = 90, tiltTgt = 75;
bool laserOn = false;
uint32_t lastTick = 0, patrolUntil = 0;

float clampf(float v, float lo, float hi) {
  return v < lo ? lo : (v > hi ? hi : v);
}

// ---------------- control page ----------------
const char PAGE[] PROGMEM = R"HTML(
<!doctype html><meta name=viewport content="width=device-width,initial-scale=1">
<title>BOOM</title>
<style>
 body{margin:0;background:#111;color:#eee;font-family:system-ui;
      display:flex;flex-direction:column;align-items:center;gap:14px;padding:16px}
 #pad{width:82vw;max-width:340px;aspect-ratio:1;background:#1d1f24;
      border:2px solid #333;border-radius:16px;position:relative;touch-action:none}
 #dot{width:34px;height:34px;background:#e03131;border-radius:50%;
      position:absolute;left:calc(50% - 17px);top:calc(50% - 17px)}
 button{font-size:17px;padding:12px 22px;border-radius:12px;border:0;
        background:#2b2f36;color:#eee}
 button.on{background:#2f6db4}
 #freeze{background:#7a1f1f;font-weight:700;font-size:20px;width:82vw;max-width:340px}
 #row{display:flex;gap:12px}
</style>
<h3>BOOM turret</h3>
<div id=pad><div id=dot></div></div>
<div id=row>
 <button id=laser>Laser</button>
 <button id=patrol>Patrol</button>
 <button id=center>Center</button>
</div>
<button id=freeze>FREEZE</button>
<script>
const pad=document.getElementById('pad'),dot=document.getElementById('dot');
let px=0.5,py=0.5,laser=0,dirty=false;
function move(e){const r=pad.getBoundingClientRect();
 const t=e.touches?e.touches[0]:e;
 px=Math.min(1,Math.max(0,(t.clientX-r.left)/r.width));
 py=Math.min(1,Math.max(0,(t.clientY-r.top)/r.height));
 dot.style.left=(px*r.width-17)+'px';dot.style.top=(py*r.height-17)+'px';
 dirty=true;e.preventDefault();}
pad.addEventListener('pointerdown',move);pad.addEventListener('pointermove',
 e=>{if(e.buttons||e.touches)move(e)});pad.addEventListener('touchmove',move);
setInterval(()=>{if(!dirty)return;dirty=false;
 fetch(`/cmd?pan=${(1-px).toFixed(3)}&tilt=${(1-py).toFixed(3)}`).catch(()=>{});},120);
const L=document.getElementById('laser');
L.onclick=()=>{laser^=1;L.classList.toggle('on',laser);
 fetch('/cmd?laser='+laser).catch(()=>{});};
const P=document.getElementById('patrol');
P.onclick=()=>{P.classList.toggle('on');
 fetch('/mode?m='+(P.classList.contains('on')?'patrol':'manual')).catch(()=>{});};
document.getElementById('center').onclick=()=>{px=py=0.5;dirty=true;};
document.getElementById('freeze').onclick=()=>{laser=0;L.classList.remove('on');
 P.classList.remove('on');fetch('/mode?m=freeze').catch(()=>{});};
</script>
)HTML";

// ---------------- handlers ----------------
void handleCmd() {
  if (mode == FROZEN && !server.hasArg("laser")) { server.send(200, "text/plain", "frozen"); return; }
  if (server.hasArg("pan"))    // joystick sends 0..1
    panTgt = PAN_MIN + clampf(server.arg("pan").toFloat(), 0, 1) * (PAN_MAX - PAN_MIN);
  if (server.hasArg("tilt"))
    tiltTgt = TILT_MIN + clampf(server.arg("tilt").toFloat(), 0, 1) * (TILT_MAX - TILT_MIN);
  if (server.hasArg("laser")) {
    laserOn = server.arg("laser") == "1" && mode != FROZEN;
    digitalWrite(PIN_LASER, laserOn ? HIGH : LOW);
  }
  if (mode == PATROL) mode = MANUAL;   // touching the stick takes over
  server.send(200, "text/plain", "ok");
}

void handleMode() {
  String m = server.arg("m");
  if (m == "freeze") {                 // park + blackout, instantly
    mode = FROZEN;
    laserOn = false;
    digitalWrite(PIN_LASER, LOW);
    panTgt = 90; tiltTgt = TILT_MIN + (TILT_MAX - TILT_MIN) * 0.5;
  } else if (m == "patrol") {
    mode = PATROL; patrolUntil = 0;
  } else {
    mode = MANUAL;
  }
  server.send(200, "text/plain", "ok");
}

void setup() {
  pinMode(PIN_LASER, OUTPUT);
  digitalWrite(PIN_LASER, LOW);
  panServo.setPeriodHertz(50);
  panServo.attach(PIN_PAN, 500, 2400);
#if BUILD_POUCH
  tiltServo.setPeriodHertz(50);
  tiltServo.attach(PIN_TILT, 500, 2400);
#endif
  WiFi.softAP(AP_SSID, AP_PASS);
  server.on("/", []() { server.send_P(200, "text/html", PAGE); });
  server.on("/cmd", handleCmd);
  server.on("/mode", handleMode);
  server.begin();
}

void loop() {
  server.handleClient();
  uint32_t now = millis();
  if (now - lastTick < TICK_MS) return;
  lastTick = now;

  if (mode == PATROL && now > patrolUntil) {
    // slow random drift, then a long natural pause
    panTgt = random((int)PAN_MIN, (int)PAN_MAX);
    tiltTgt = random((int)TILT_MIN, (int)TILT_MAX);
    patrolUntil = now + random(3000, 11000);
  }

  // eased motion: fast enough to feel live, slow enough to look organic
  panNow += (panTgt - panNow) * EASE;
  tiltNow += (tiltTgt - tiltNow) * EASE;
  tiltNow = clampf(tiltNow, TILT_MIN, TILT_MAX);   // hard safety clamp

  panServo.write(panNow);
#if BUILD_POUCH
  tiltServo.write(tiltNow);
#endif
}
