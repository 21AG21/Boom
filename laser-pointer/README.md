# LASER-POINTER — Bluetooth remote laser (on/off)

A tiny fixed laser you switch **on and off** two ways:

1. a **physical button** on the device, and
2. your **phone or laptop** over Bluetooth.

No motors, no aiming, no patterns yet — you point the whole gadget where
you want the dot (prop it on the floor for a cat, clip it to a shelf) and
toggle the beam. (Light-pattern modes can be added later.)

- **Bluetooth (BLE)** — no WiFi, no accounts, no internet.
- **Phone or laptop app** — a single HTML file with one big on/off button.
- **Button and app stay in sync** — press the device button and the app
  updates, and vice-versa.
- **Deep sleep** — idles at ~10 µA and wakes on the button, so a tiny
  battery lasts months. See [Power & sleep](#power--sleep).
- **Fail-safe** — the laser turns off by itself if Bluetooth drops.

It's small — a **matchbox** as built, a **thumbnail** in the compact
build. See [How big it is](#how-big-it-is) and the full shrink plan in
**[COMPACT.md](COMPACT.md)**.

```
   phone / laptop                 ESP32-C3              laser diode
  ┌───────────────┐   BLE (NUS)  ┌──────────┐   GPIO4  ┌──────────┐
  │ laser-remote  │ ───────────► │ firmware │ ───────► │  KY-008  │
  │  ON / OFF     │ ◄─────────── │ (NimBLE) │          │  5mW red │
  └───────────────┘  on/off sync └────┬─────┘          └──────────┘
                                       │ GPIO10
                                  [ push button ]  press = on/off
```

## Start here — pick your version

- **Simplest, no code, wireless button: [BASIC.md](BASIC.md).** A ready-made
  433 MHz remote + relay receiver toggles the laser from across the room.
  No microcontroller, no app, no soldering (screw terminals). ~$13 (reuses
  AAs you own). **This is the one to build if you just want a
  button-controlled laser.**
- **Phone control, no soldering: [NOSOLDER.md](NOSOLDER.md).** Adds a tiny
  ESP32-C3 so your phone/laptop controls it over Bluetooth. Breadboard +
  USB, ~$8.
- **General Bluetooth walkthrough:** [ASSEMBLY.md](ASSEMBLY.md).
- **Shrink the Bluetooth build (needs soldering):** [COMPACT.md](COMPACT.md)
  — thumbnail size + battery + deep sleep.

The rest of this file describes the **Bluetooth** version.

## Parts

See [SHOPPING.md](SHOPPING.md) — about **$8**. A microcontroller, a laser
module, a button, and a USB cable (add a small battery to go cordless).
No servos, no bracket.

## 1. Wire it (the whole circuit — 3 connections)

```
  ESP32-C3 SuperMini
  ------------------
  GPIO4  ──► laser "S" pin  (KY-008 signal)
  GND    ──► laser "−" pin  ·  one button leg  ·  LED (−) if used
  GPIO10 ──► other button leg   (internal pull-up, no resistor)
  GPIO5  ──► status LED ──[220Ω]──► GND   (optional)
  USB-C  ──► powers the board
```

The KY-008 draws little enough to run straight off the GPIO pin, so
there's no separate power rail — nothing to solder for a breadboard test.

## 2. Flash the firmware

Open [`firmware/laserpointer/laserpointer.ino`](firmware/laserpointer/laserpointer.ino)
in the Arduino IDE.

1. Board: **ESP32C3 Dev Module** (install the "esp32" boards package).
2. Library (Library Manager): **NimBLE-Arduino**.
3. Plug in over USB-C, Upload.

On boot it advertises over Bluetooth LE as **`LASER-PT`**.

## 3. Control it

### The button
Press it: laser on. Press again: off. Works with no phone at all.

### The app (phone or laptop)
Open [`app/laser-remote.html`](app/laser-remote.html), hit **Connect**,
pick `LASER-PT`, tap the big power button.

| Where | Browser |
|---|---|
| Windows / Mac / Linux laptop | **Chrome** or **Edge** |
| Android phone | **Chrome** |
| iPhone / iPad | **Bluefy** app (Safari can't do Web Bluetooth) or the option below |

### Or any BLE terminal app
**nRF Connect** / **Serial Bluetooth Terminal** → connect to `LASER-PT` →
send to the Nordic UART RX characteristic:

| Command | Does |
|---|---|
| `L1` | laser on |
| `L0` | laser off |
| `T` | toggle |

## Power & sleep

The ESP32-C3 has two states:

- **Awake** — Bluetooth live, button + phone both work (~40–80 mA).
- **Asleep** — deep sleep, everything off but the button (~10 µA).

It auto-sleeps after **2 minutes** idle (laser off and no phone
connected). **Press the button to wake it** — that also turns the laser
on. While asleep the phone can't see it, so press the button first, then
Connect. This is what lets a ~100 mAh cell last months of standby instead
of an hour. Adjust the timeout via `SLEEP_AFTER_MS` in the `.ino`.

## How big it is

- **ESP32-C3 SuperMini:** ~22 × 18 × 3 mm
- **KY-008 laser:** ~15 × 24 mm board, 6 mm tube (or a bare 6 mm diode)
- **Button:** ~2–12 mm

As built (SuperMini + KY-008 board + LiPo) it tidies to about **40 × 25 ×
18 mm — a matchbox**. The **compact build** (bare diode, SMD button, coin/
slim cell) shrinks to about **24 × 20 × 10 mm — a thumbnail**; the full
shrink ladder, runtime math, and charging options are in
**[COMPACT.md](COMPACT.md)**.

Want a printed case (beam hole + button hole + USB-C notch, matchbox or
thumbnail size)? Ask and I'll add it to
[`../hardware/generate_stls.py`](../hardware/generate_stls.py).

## Safety

Even a 5 mW class-3R diode must never hit an eye. Since there's no motor,
**you** decide where it points — aim the unit so the dot lands on the
floor / low walls, never at people, pets' faces, mirrors, or glass. The
laser also switches off automatically if the Bluetooth connection drops.
