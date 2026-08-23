# Lull — Build a Prototype

A weekend build. You print five parts, drop in a motor + a few electronics,
seat a foam dome and a gel lobe, and calibrate. Two tiers: **Tier A** is a
5-minute "does it breathe at all" proof with no code; **Tier B** is the real
prototype with good torque and feel. Do A first if you're impatient, then B.

Everything here matches `hardware/lull.py` (the parts) and
`firmware/lull/lull.ino` (Tier B). Read `mechanism.md` first if you haven't.

---

## Bill of materials

| Part | Qty | ~Cost | Where / notes |
|---|---:|---:|---|
| **N20 gearmotor**, 6 V, **slow + high-torque** (pick 10–30 RPM) | 1 | $4–8 | Amazon/AliExpress "N20 6V 15RPM". Slow = more torque; you'll PWM it slower still. |
| **3.7 V LiPo** (250–500 mAh) + **TP4056** USB-C charger | 1 | $7 | Powers motor *and* MCU cleanly. (Production intent is 2×AAA + a boost; LiPo is simplest for a proto.) |
| **ESP32-C3 SuperMini** | 1 | $4 | Tier B only. Or a $1 ATtiny. |
| **N-MOSFET**, logic-level (AO3400 / IRLML2502) **or** a **DRV8833** driver board | 1 | $1–3 | DRV8833 is easiest — it includes flyback protection. |
| **1N5819** flyback diode | 1 | $0.10 | Only if using a bare MOSFET (not needed with DRV8833). |
| **Compression spring assortment** | 1 | $6 | The "authority spring" — you'll pick one ~10–20 N. Reusable. |
| **Closed-cell silicone / EVA foam** disc, ~Ø32×12 mm | 1 | $5 | The breathing dome. A firm craft-foam disc works for v0; cast Ecoflex over it for the real feel. |
| **A NeeDoh** (or similar gel squish ball) | 1 | $5 | Cut/seat it as the gel lobe — the fastest leak-proof fidget you can get. |
| Tactile button or slide switch | 1 | $0.5 | |
| PLA filament | — | ~$0.50 | The five printed parts (~25 g). |
| Wire, M2 screws, super glue, silicone adhesive | — | $3 | |

**~$30–40** in parts for one, most of it reusable across builds.

**Tools:** 3D printer, soldering iron, hobby knife, small screwdriver, calipers,
a phone/watch (to time breaths), and — for calibration — a **kitchen scale**.

---

## 1 · Print the parts
```bash
pip install trimesh manifold3d scipy numpy matplotlib shapely
python3 hardware/lull.py            # -> hardware/stl/
python3 hardware/render_preview.py  # optional
```

| Part | Material | Orientation | Layer | Walls | Infill | Supports |
|---|---|---|---|---|---|---|
| `lull_base` | PLA/PETG | cavity up (as modelled) | 0.20 | 4 | 25% | under the motor-cradle bridge |
| `lull_lid` | PLA | top face down | 0.20 | 4 | 20% | light, under the dome collar |
| `lull_cam` | **PETG/nylon** | flat, disc on bed | 0.16 | 4 | 40% | none |
| `lull_follower` | PLA/PETG | upright, foot down | 0.16 | 3 | 40% | none |
| `lull_platen` | PLA | flat | 0.20 | 3 | 30% | none |

Print the cam and follower in PETG/nylon — they carry the load. The foam dome
and gel lobe are **not** printed (they're the bought foam + NeeDoh).

---

## 2 · Wiring (Tier B, recommended)

```
LiPo + ──┬──────────────► motor terminal A
         │
       [TP4056]        motor terminal B ──► DRV8833 OUT
         │              DRV8833 IN  ◄── GPIO2 (PWM)
LiPo - ──┴── GND ──────► DRV8833 GND, ESP32-C3 GND
                         ESP32-C3 3V3 ◄── LiPo + (via C3's own regulator)
         button: GPIO9 ── button ── GND
```
Bare-MOSFET variant: motor between LiPo+ and MOSFET drain; MOSFET source to
GND; gate to GPIO2 with a 100 kΩ gate-to-GND pulldown; **1N5819 across the
motor**, cathode to LiPo+.

Flash `firmware/lull/lull.ino` (Arduino IDE, board "ESP32C3 Dev Module").

**Tier A (no code):** skip the MCU. Wire `LiPo+ → slide switch → series
resistor (~15–47 Ω 0.5 W) → motor → LiPo-`. It'll spin slow and breathe. This
proves motion but loses torque at low speed — that's why Tier B (PWM) is the
real prototype.

---

## 3 · Assembly

1. **Motor + cam.** Press the N20 into the base cradle, shaft pointing at the
   follower bore. Slide `lull_cam` onto the shaft; set-screw or a dab of glue.
   Spin by hand — the lumpy edge should sweep just under the follower bore.
2. **Follower.** Drop `lull_follower` into its guide bore, rounded foot resting
   on top of the cam. It should rise/fall ~3 mm as you turn the cam by hand.
3. **Authority spring.** Set a compression spring on the follower's top seat.
4. **Platen + dome.** Seat `lull_platen` on the spring (locating boss down).
   Bond the **foam dome** onto the platen's top. Press the dome's lip into the
   groove around the lid's big opening.
5. **Gel lobe.** Seat the NeeDoh (or a cast gel blob) into the lid's **separate**
   side opening; its lip catches the groove. Nothing connects it to the
   mechanism — that's the point.
6. **Electronics.** Tuck the LiPo, charger, and driver into the bays; run the
   motor leads; mount the button/switch in the side slot.
7. **Close up.** Screw the lid to the base (M2 into the three bosses).

---

## 4 · Calibrate (the important 10 minutes)

**Cadence.** Run it. Time ten breaths; one breath should take ~12 s (5/min).
Adjust `DUTY_5BPM` in the firmware up/down until it lands. (Open-loop, so it
drifts a little with battery level — fine for a proto.)

**Authority / feel — this is the answer to "enough torque?"** Press the dome
straight down onto a **kitchen scale** while it's inhaling and read the peak
force. That peak ≈ the authority spring's preload:
- **Target ~1.5–2 kg (≈15–20 N).** Below that, a hard clench simply compresses
  the spring and the motor keeps turning — it never stalls.
- Too weak (dome barely pushes a resting palm) → fit a **stiffer** spring.
- Too strong (fights your hand, motor lugs) → fit a **softer** spring.

Swapping the spring is the whole tuning knob. The firm foam means that even
when a grip stops the dome rising, you still feel the breath as a **pressure
pulse** in your palm.

---

## 5 · Test it

- Rest your palm on the dome, breathe with it for two minutes. It should feel
  like a slow, calm swell — and be quiet (a faint motor whir is OK; an
  *irregular* tick means the cam/follower needs a smoother contact or a gel
  motor mount).
- Knead the gel lobe with your fingers while your palm stays on the dome — two
  behaviors at once.
- **Clench the whole thing hard.** The dome should stop rising but the motor
  should keep turning smoothly (the spring is slipping) — no stall, no grind.
  If it stalls, your authority spring is too stiff or the motor too weak.

---

## Where to go next
- Swap the craft-foam dome for **cast Ecoflex 00-30 over a closed-cell core**
  for the real "breathing skin" feel.
- Add the soft **exhale "shhh"** (a small felt-damped port) to mask motor whine
  and turn it into a pacing cue.
- If motor-noise quality fights you, jump to the **nitinol** drive in
  `../breathe-stone/hardware-v2/` (silent, no motor) with this same two-zone body.
