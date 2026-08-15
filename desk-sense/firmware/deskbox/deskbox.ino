/*
 * DESK-SENSE — the bit box
 * ------------------------------------------------------------------
 * A desk gadget that reads the room with total authority. Real BME280
 * temperature / humidity / pressure on a little OLED, plus a few
 * derived "readings" that are played straight for laughs. It sits out
 * in the open, it's obviously yours, and people pick it up to read it.
 * No laser, no hiding — that's the whole joke.
 *
 * Arduino IDE setup:
 *   1. Boards manager: install "esp32" (Espressif), pick "ESP32C3 Dev Module"
 *   2. Library manager, install:
 *        - "Adafruit BME280 Library"   (pulls in Adafruit Unified Sensor)
 *        - "Adafruit SSD1306"          (pulls in Adafruit GFX)
 *   3. Flash over USB-C. No WiFi, nothing to join — it just runs.
 *
 * Wiring (I2C, both devices share the same two pins):
 *   ESP32-C3        BME280        SSD1306 OLED
 *   -----------------------------------------------
 *   3V3     ------> VIN/VCC ----> VCC
 *   GND     ------> GND     ----> GND
 *   GPIO8   ------> SDA     ----> SDA      (I2C data)
 *   GPIO9   ------> SCL     ----> SCL      (I2C clock)
 *   GPIO5   --[220Ω]--> green LED --> GND  (heartbeat)
 *
 * Default I2C addresses: BME280 = 0x76 (some boards 0x77),
 *                        SSD1306 = 0x3C. Change below if yours differ.
 */
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// ---------------- config ----------------
#define I2C_SDA        8
#define I2C_SCL        9
#define PIN_LED        5        // heartbeat LED — looks official, does nothing

#define BME_ADDR       0x76     // try 0x77 if the sensor isn't found
#define OLED_ADDR      0x3C
#define OLED_W         128
#define OLED_H         64

#define USE_FAHRENHEIT 1        // 1 = °F, 0 = °C

// The bit box cycles through screens. Real data first, then the jokes.
const uint32_t SCREEN_MS = 3500;

Adafruit_BME280 bme;
Adafruit_SSD1306 oled(OLED_W, OLED_H, &Wire, -1);

bool haveBME = false;
uint32_t lastScreen = 0, lastBeat = 0;
int screen = 0;
const int NUM_SCREENS = 4;

// ---------------- helpers ----------------
void centerText(const char *s, int y, int size) {
  int16_t x1, y1; uint16_t w, h;
  oled.setTextSize(size);
  oled.getTextBounds(s, 0, y, &x1, &y1, &w, &h);
  oled.setCursor((OLED_W - w) / 2, y);
  oled.print(s);
}

void header(const char *label) {
  oled.drawLine(0, 12, OLED_W, 12, SSD1306_WHITE);
  oled.setTextSize(1);
  oled.setCursor(0, 2);
  oled.print(label);
}

// Barometric "trend" arrow from a rolling reference pressure.
float pressRef = 0;
const char *pressureArrow(float hpa) {
  if (pressRef == 0) pressRef = hpa;
  float d = hpa - pressRef;
  pressRef += (hpa - pressRef) * 0.02;   // slow drift toward current
  if (d > 0.4) return "RISING";
  if (d < -0.4) return "FALLING";
  return "STEADY";
}

// ---------------- joke metrics (derived from REAL data, played straight) --
// Everything below is computed from genuine sensor readings, so the box
// isn't lying — it's just deeply committed to the bit.

// "Meeting Density" — warmer + more humid + more people breathing = higher.
int meetingDensity(float tempC, float hum) {
  float idx = (tempC - 19.0) * 6.0 + (hum - 35.0) * 1.1;
  if (idx < 0) idx = 0; if (idx > 100) idx = 100;
  return (int)idx;
}

// "Circle-Back Index (ppm)" — rises with stuffiness. Pure vibes, real math.
int circleBackPPM(float tempC, float hum) {
  return 400 + (int)((tempC - 18.0) * 55.0 + (hum - 30.0) * 9.0);
}

// A verdict line for the room, chosen from real comfort ranges.
const char *roomVerdict(float tempC, float hum) {
  if (tempC > 25.5) return "TOO WARM. SPEAK UP.";
  if (tempC < 19.0) return "BRISK. BLAME FACILITIES.";
  if (hum > 60)     return "SWAMP CONDITIONS.";
  if (hum < 25)     return "DESERT. HYDRATE.";
  return "NOMINAL. SUSPICIOUS.";
}

// ---------------- screens ----------------
void drawClimate(float tempC, float hum, float hpa) {
  oled.clearDisplay();
  header("ENV-SENSE  DESK-1");
  float t = USE_FAHRENHEIT ? tempC * 9.0 / 5.0 + 32.0 : tempC;
  char buf[24];
  snprintf(buf, sizeof(buf), "%.1f%c", t, USE_FAHRENHEIT ? 'F' : 'C');
  centerText(buf, 22, 2);
  oled.setTextSize(1);
  snprintf(buf, sizeof(buf), "RH %.0f%%   %.0f hPa", hum, hpa);
  centerText(buf, 46, 1);
  centerText(pressureArrow(hpa), 56, 1);
  oled.display();
}

void drawMeeting(float tempC, float hum) {
  oled.clearDisplay();
  header("MEETING DENSITY");
  int d = meetingDensity(tempC, hum);
  char buf[16];
  snprintf(buf, sizeof(buf), "%d%%", d);
  centerText(buf, 20, 3);
  // bar
  int w = (OLED_W - 8) * d / 100;
  oled.drawRect(4, 52, OLED_W - 8, 10, SSD1306_WHITE);
  oled.fillRect(4, 52, w, 10, SSD1306_WHITE);
  oled.display();
}

void drawCircleBack(float tempC, float hum) {
  oled.clearDisplay();
  header("CIRCLE-BACK LEVEL");
  char buf[20];
  snprintf(buf, sizeof(buf), "%d", circleBackPPM(tempC, hum));
  centerText(buf, 22, 3);
  centerText("ppm", 54, 1);
  oled.display();
}

void drawVerdict(float tempC, float hum) {
  oled.clearDisplay();
  header("ROOM VERDICT");
  const char *v = roomVerdict(tempC, hum);
  // wrap the verdict onto two centered lines at size 1
  centerText(v, 30, 1);
  oled.display();
}

void drawNoSensor() {
  oled.clearDisplay();
  header("ENV-SENSE  DESK-1");
  centerText("SENSOR OFFLINE", 26, 1);
  centerText("check BME280 wiring", 42, 1);
  oled.display();
}

// ---------------- setup / loop ----------------
void setup() {
  pinMode(PIN_LED, OUTPUT);
  Wire.begin(I2C_SDA, I2C_SCL);

  oled.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
  oled.clearDisplay();
  oled.setTextColor(SSD1306_WHITE);
  centerText("ENV-SENSE", 18, 2);
  centerText("booting...", 44, 1);
  oled.display();

  haveBME = bme.begin(BME_ADDR);
  delay(900);
}

void loop() {
  uint32_t now = millis();

  // heartbeat: slow official-looking pulse
  if (now - lastBeat > 1500) { lastBeat = now; digitalWrite(PIN_LED, HIGH); }
  if (now - lastBeat > 80)   { digitalWrite(PIN_LED, LOW); }

  if (!haveBME) { drawNoSensor(); delay(500); return; }

  float tempC = bme.readTemperature();
  float hum   = bme.readHumidity();
  float hpa   = bme.readPressure() / 100.0;

  if (now - lastScreen > SCREEN_MS) {
    lastScreen = now;
    screen = (screen + 1) % NUM_SCREENS;
  }

  switch (screen) {
    case 0: drawClimate(tempC, hum, hpa); break;
    case 1: drawMeeting(tempC, hum);      break;
    case 2: drawCircleBack(tempC, hum);   break;
    case 3: drawVerdict(tempC, hum);      break;
  }
  delay(30);
}
