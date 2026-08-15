# LASER-POINTER — compact build (Tier B) + deep sleep

This is the "shrink it as much as possible without a custom PCB" plan. It
takes the working on/off laser and squeezes it to about a **thumbnail**,
running for **months** on a tiny battery thanks to deep sleep.

If you haven't built the basic version yet, do that first on a breadboard
([ASSEMBLY.md](ASSEMBLY.md)) so you know the circuit works — then shrink.

---

## 1. The size ladder (where this sits)

| Tier | What changes | Size | Difficulty |
|---|---|---|---|
| A — basic | SuperMini board + KY-008 board + button + LiPo | ~40 × 25 × 18 mm (matchbox) | easy |
| **B — compact (this doc)** | bare diode, SMD button, coin/slim cell, deep sleep | **~24 × 20 × 10 mm (thumbnail)** | medium, hand-solder |
| C — custom PCB | raw ESP32-C3-MINI-1 module on a fabbed board | ~16 × 16 × 7 mm (shirt button) | hard, needs reflow |
| floor | diode + radio module + battery, stacked | ~15 × 14 × 7 mm | — |

Tier B keeps every part hand-solderable — no PCB fab, no hot-air. The
**ESP32-C3 SuperMini board (22.5 × 18 mm) becomes the footprint**, and
everything else hides in its shadow or stacks under it.

---

## 2. What makes it small

Three swaps from the basic build:

1. **Laser: drop the KY-008 carrier board.** The KY-008 is just a bare
   **6 mm laser diode** (6 mm Ø × ~10 mm) on a little PCB with one
   resistor. Desolder the diode from its board (or buy a bare "6mm 650nm
   5mW laser diode module") and wire it directly:
   - diode **+** → GPIO4 (through a **~100 Ω resistor** — the KY-008 board
     had one built in; the bare diode needs it added back)
   - diode **−** → GND
   This removes the single biggest part.

2. **Button: 2 × 4 mm SMD tactile** instead of the 6–12 mm through-hole
   one. Still just "GPIO10 ↔ GND". Any tiny momentary switch works.

3. **Battery: a small cell tucked under the board.** Two choices:
   - **~100 mAh slim LiPo** (e.g. 401220, ~20 × 12 × 4 mm) — best runtime,
     rechargeable with a TP4056.
   - **LIR2032 rechargeable coin** (20 mm Ø × 3.2 mm) — flattest, ~40 mAh,
     shorter runtime.

Optional: skip the status LED to save a hair more space; the firmware
doesn't need it.

---

## 3. Deep sleep — how the power plan works

A BLE radio that's always listening would flatten a coin cell in an hour.
So the firmware uses two states:

```
        ┌─────────── press button ───────────┐
        │                                     ▼
   ┌──────────┐   idle 2 min (off + no phone)   ┌──────────┐
   │  ASLEEP  │ ◄────────────────────────────── │  AWAKE   │
   │ ~10 uA   │                                  │ 40-80 mA │
   │ button   │ ─────── press button ──────────► │ BLE live │
   │ only     │        (wakes + laser ON)        │ btn+phone│
   └──────────┘                                  └──────────┘
```

- **AWAKE:** Bluetooth advertises/connects; both the button and the phone
  work. Draws ~40–80 mA while the radio is active.
- **ASLEEP (deep sleep):** everything off except the button pin. Draws
  ~10 µA (that's 0.01 mA).
- **Falling asleep:** after `SLEEP_AFTER_MS` (default **2 minutes**) with
  the laser **off** and **no phone connected**, it deep-sleeps itself.
- **Waking:** press the button → it boots, **turns the laser on**, and
  starts advertising so your phone can connect again.

The one thing to know: **while it's asleep, your phone can't see it.**
Press the button once to wake it, then hit Connect in the app. That's the
tradeoff that buys the huge standby life.

Tune it: change `SLEEP_AFTER_MS` at the top of the `.ino` (bigger = stays
awake/reachable longer, shorter battery; smaller = sleeps sooner, longer
battery).

---

## 4. Runtime math (so you can pick a battery)

Rough numbers — real life varies with how much you actually use it.

| Battery | Standby (asleep) | Active use (laser + BLE) |
|---|---|---|
| LIR2032 coin (~40 mAh) | ~months* | ~30 min |
| 100 mAh slim LiPo | ~months* | ~1.25 hr |
| 250 mAh LiPo | ~months* | ~3 hr |

\* Standby is dominated by the cell's own self-discharge, not the ~10 µA
draw — at 10 µA a 100 mAh cell would in theory last over a year; in
practice self-discharge sets the limit at several months. Either way, for
a toy that sits idle between uses, deep sleep means it's essentially always
ready without charging.

Since the ESP32-C3 runs happily at 3.7 V, the LiPo (or 3.6 V LIR coin)
feeds it **directly** — no 5 V booster needed.

---

## 5. Charging

Pick based on how small you want it:

- **Rechargeable in place (recommended):** a **TP4056 USB-C** charge board
  between the cell and the circuit. It's ~26 × 17 mm — a bit bigger than
  the MCU — so the two boards sit side by side, making the finished pack
  more like **26 × 40 × 10 mm** ("half a matchbox"). Plug in USB-C to
  charge; unplug to run.
- **Smallest, swap to charge:** a **coin-cell holder** and no charger on
  board — pop the LIR2032 out and charge it in a coin charger. This is the
  true thumbnail size but less convenient.

You still flash the firmware over the SuperMini's own USB-C either way.

---

## 6. Wiring (compact)

Same three logical connections as the basic build, just with the bare
diode and its resistor:

```
  ESP32-C3 SuperMini
  ------------------
  GPIO4  ──[~100Ω]──► laser diode (+)
  GND    ─────────────► laser diode (−)  ·  button leg
  GPIO10 ─────────────► button (other leg)      (wake pin)

  battery (+) ──► board 5V/VBAT-in path (see your board's pinout)
  battery (−) ──► board GND
  (via TP4056 if you're charging in place)
```

> The ~100 Ω resistor matters: the KY-008 board included one, but a bare
> diode wired straight to 3.3 V can burn out. Keep it in series with the
> diode.

Everything else — flashing, the app, the button behavior — is exactly as
in [README.md](README.md) and [ASSEMBLY.md](ASSEMBLY.md).

---

## 7. Build order

1. Build and test on a breadboard first (basic version).
2. Flash the deep-sleep firmware (already in
   `firmware/laserpointer/laserpointer.ino`).
3. Confirm it sleeps: leave it 2 min with the laser off and unconnected —
   the status LED stops blinking. Press the button — it wakes and the
   laser comes on.
4. Confirm phone reconnect: after it sleeps, the app can't find it; press
   the button, then Connect — it appears.
5. Once happy, solder the bare diode + resistor + SMD button, add the
   battery (+ TP4056 if charging in place), and pack it into a case.

Want the enclosure? I can add a **`pointer_micro` case** to
[`../hardware/generate_stls.py`](../hardware/generate_stls.py): a
thumbnail shell with a 6 mm beam hole, a button hole, and a USB-C slot —
just ask.

---

## Safety

Even a 5 mW class-3R diode must never hit an eye. There's no motor, so
**you** decide where it points — aim the unit so the dot lands on the
floor / low walls, never at people, pets' faces, mirrors, or glass. The
laser switches off automatically if the Bluetooth connection drops, and
the device powers the beam down before sleeping.
