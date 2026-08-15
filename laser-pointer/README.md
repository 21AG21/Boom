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
- **Fail-safe** — the laser turns off by itself if Bluetooth drops.

It's small — roughly a **matchbox**. See [How big it is](#how-big-it-is).

```
   phone / laptop                 ESP32-C3              laser diode
  ┌───────────────┐   BLE (NUS)  ┌──────────┐   GPIO4  ┌──────────┐
  │ laser-remote  │ ───────────► │ firmware │ ───────► │  KY-008  │
  │  ON / OFF     │ ◄─────────── │ (NimBLE) │          │  5mW red │
  └───────────────┘  on/off sync └────┬─────┘          └──────────┘
                                       │ GPIO10
                                  [ push button ]  press = on/off
```

## Parts

See [SHOPPING.md](SHOPPING.md) — about **$8**. A microcontroller, a laser
module, a button, and a USB cable (add a small battery to go cordless).
No servos, no bracket.

Full beginner walkthrough: **[ASSEMBLY.md](ASSEMBLY.md)**.

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

## How big it is

- **ESP32-C3 SuperMini:** ~22 × 18 × 3 mm
- **KY-008 laser:** ~15 × 24 mm board, 6 mm tube
- **Button:** ~6–12 mm

On a breadboard it's dominated by the breadboard. Tidied into a little
case with a small LiPo, the whole thing is about **40 × 25 × 18 mm — a
matchbox**, or smaller if you skip the battery and run it off USB. Want a
printed matchbox-size case (beam window + button hole + USB-C notch)? Ask
and I'll add it to [`../hardware/generate_stls.py`](../hardware/generate_stls.py).

## Safety

Even a 5 mW class-3R diode must never hit an eye. Since there's no motor,
**you** decide where it points — aim the unit so the dot lands on the
floor / low walls, never at people, pets' faces, mirrors, or glass. The
laser also switches off automatically if the Bluetooth connection drops.
