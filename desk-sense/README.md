# DESK-SENSE — the bit box

A desk gadget that reads the room with total authority. It shows **real**
temperature, humidity, and pressure on a little OLED — then cycles into a
few extra "readings" delivered with a completely straight face: Meeting
Density, Circle-Back Level (ppm), and a one-line Room Verdict. Every joke
number is computed from genuine sensor data, so it never actually lies.
It just takes itself very seriously.

It sits out in the open on your desk. It's obviously yours. People pick it
up to read it — that's the whole payoff. No laser, no radio, nothing hidden.

```
        ┌────────────────────────────┐
        │  ENV-SENSE  DESK-1      ●   │   ← heartbeat LED
        │  ────────────────────────  │
        │         72.4°F             │   ← real reading
        │     RH 41%   1013 hPa      │
        │          STEADY            │
        └────────────────────────────┘
            (cycles every ~3.5 s)

   MEETING DENSITY 68%   ·   CIRCLE-BACK 512 ppm   ·   "NOMINAL. SUSPICIOUS."
```

## What it actually measures

| Screen | Source | Honest? |
|---|---|---|
| Temp / Humidity / Pressure | BME280 sensor | 100% real |
| Pressure trend (RISING/STEADY/FALLING) | BME280, rolling reference | real |
| Meeting Density % | warmth + humidity (a crowded room *is* warmer & damper) | plausible-real |
| Circle-Back Level (ppm) | stuffiness proxy | a bit (a joke) |
| Room Verdict | real comfort ranges → deadpan line | real data, editorial delivery |

## Build it

### 1. Get the parts

See [SHOPPING.md](SHOPPING.md). Total is roughly **$12–16**. Everything is
I2C, so the whole thing is four wires plus an LED — no soldering strictly
required if you use a tiny breadboard, but it's ~6 easy joints to make it
solid.

### 2. Wire it

Both the sensor and the screen sit on the same two I2C lines. Wire them in
parallel (SDA to SDA to SDA, SCL to SCL to SCL).

```
  ESP32-C3 SuperMini        BME280            SSD1306 OLED (0.96")
  ---------------------------------------------------------------
  3V3   ───────────────────► VIN ───────────────► VCC
  GND   ───────────────────► GND ───────────────► GND
  GPIO8 (SDA) ─────────────► SDA ───────────────► SDA
  GPIO9 (SCL) ─────────────► SCL ───────────────► SCL

  GPIO5 ──[220Ω]──► (+)green LED(−) ──► GND      (heartbeat)
```

Power the board from any USB-C cable/charger. Want it cordless? Add a
TP4056 + a small LiPo exactly like the other builds in this repo — it'll
run for days since there are no servos or radio drawing current.

### 3. Flash the firmware

Open [`firmware/deskbox/deskbox.ino`](firmware/deskbox/deskbox.ino) in the
Arduino IDE. Header comment has the full setup, but in short:

1. Board: **ESP32C3 Dev Module** (install the "esp32" boards package).
2. Libraries (Library Manager): **Adafruit BME280 Library** and
   **Adafruit SSD1306** — accept the extra dependencies each pulls in
   (Adafruit Unified Sensor, Adafruit GFX).
3. Plug in over USB-C, hit Upload.

That's it. On boot it shows `ENV-SENSE booting...`, then starts cycling
screens.

### 4. Tune the bit (optional)

Everything you'd want to change is at the top of the `.ino`:

- `USE_FAHRENHEIT` — `1` for °F, `0` for °C.
- `SCREEN_MS` — how long each screen holds.
- `BME_ADDR` — flip to `0x77` if the serial/OLED says the sensor is offline
  (some BME280 boards use the other address).
- The joke functions (`meetingDensity`, `circleBackPPM`, `roomVerdict`)
  are plain C near the middle of the file — rewrite the labels and verdict
  lines to whatever fits your office. That's where the comedy lives.

## Enclosure

The `sense_case` / `sense_lid` prints from [`../hardware/stl/`](../hardware/stl/)
fit this board perfectly — but for the bit box you want the front
**window opened up to frame the OLED** instead of hiding a lens behind
tint. Two ways to get there:

- **Fast:** print `sense_case.stl` as-is and just cut/file the window
  open to ~26 × 15 mm so the screen shows through. Skip the tint film.
- **Clean:** regenerate from [`../hardware/generate_stls.py`](../hardware/generate_stls.py)
  with a proper OLED cutout. If you want, I can add a `deskbox_case`
  variant to that generator with the exact 0.96" OLED window and a USB-C
  side notch — just ask.

Keep the printed label if you like — a fake asset number reading
`ENV-SENSE DESK-1  ▍▍▍▍▍▍` leans into the joke rather than hiding anything,
because the thing is sitting on your desk in plain sight.

## Why this and not the other thing

The original enclosure in this repo is built to look like anonymous
building infrastructure so a laser can't be traced back to whoever's
running it. This is the opposite: same aesthetic, played as a gag, with
your name effectively on it. Real data, out in the open, funnier — and
nobody gets a beam in the eye.
