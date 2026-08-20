# Breathe Stone 🫧

> *A worry stone that breathes with you — so you breathe with it.*

A palm-sized stone with a domed pad on top that slowly rises and falls on a
breathing cadence. Rest your thumb on it and, without thinking, your breath
entrains to the rise and fall. No screen. No notification. Near-silent. It
just breathes, and you follow.

This folder is the **#1 flagship from the [Idea Vault](../README.md), built
out from a page into a startable project** — real printable parts, working
firmware, a provisional-patent draft, and grounded unit economics.

---

## Why this one first
- **Highest fidget score** in the vault, clearest B2B revenue, strongest
  patent.
- The market is **de-risked**: *Moonbird*, a ~$199 handheld device that
  paces breathing by expanding in your hand, already sells into this
  category. Breathe Stone takes that proven demand down-market and into
  everyday carry — **⅕ the price, pocketable, no app**, and into bulk
  channels a $199 gadget can't reach.

## What's in here

| Folder | What it is | Status |
|---|---|---|
| [`hardware/`](hardware/) | Parametric STL generator (this repo's trimesh idiom), 5 watertight printable parts + assembly, and a preview render | ✅ generates & prints |
| [`firmware/`](firmware/) | ESP32-C3 sketch: silent 5-5 / 4-7-8 / box cadences, sine-eased, servo detaches through holds | ✅ flash-ready |
| [`patent/`](patent/) | Full provisional draft, 20 claims, candid Moonbird prior-art analysis | ✅ file-ready (~$65) |
| [`business/`](business/) | BOM across 3 build tiers, unit economics, and a phased go-to-market | ✅ |

## How it works (the mechanism)
A micro servo turns a **crank**; the crank pin lifts a **piston** guided in
the lid bore; the piston carries a soft **dome** your thumb rests on. The
firmware drives the servo along a smootherstep-eased breathing waveform, and
— the key trick — **detaches the servo during the breath-holds** so the
stone is dead silent while the pad dwells (a commanded servo otherwise buzzes,
which is unacceptable at 3 a.m.).

Three actuation paths, cheapest-to-quietest:
1. **Servo + crank** (the prototype here) — easiest to build tonight.
2. **Nitinol wire** — silent, solid-state, thins the stone to ~22 mm.
3. **Wound spring + escapement** — *no electronics at all*; the bulk / B2B
   hero at ~$5 COGS.

## Build it (four weekends, ~$100 — see [`../one-month-ship-plan.md`](../one-month-ship-plan.md))
```bash
# 1. Generate the printable parts
pip install trimesh manifold3d scipy numpy matplotlib
python3 hardware/breathe_stone.py          # STLs -> hardware/stl/
python3 hardware/render_preview.py         # optional preview PNG

# 2. Print: base, lid, piston, crank in PLA; dome in TPU
# 3. Drop in an SG90/MG90S + ESP32-C3 + 300mAh LiPo + TP4056
# 4. Flash firmware/breathe_stone/breathe_stone.ino (Arduino IDE, ESP32 core)
# 5. Calibrate SERVO_DOWN / SERVO_UP in the sketch to your crank
```
Prototype dimensions are **78 × 58 × 38 mm** (chunky, to fit an SG90); the
nitinol/kinetic versions shrink it to worry-stone size.

## The numbers (grounded, Aug 2026)
- **COGS** ~$12 electronic / ~$5 kinetic at volume → **~64% DTC margin** at
  $34 / $14 retail.
- **Break-even** ~550 units against ~$12k tooling; fund it with a
  1,000–2,000-unit crowdfunding pre-sale.
- **Upside case**: the fidget spinner did ~$2.2 B at peak. Underwrite the
  base case; keep the option on the breakout.

## Honest risks
Moonbird is close prior art (see the patent notes) — compete on price, form,
and B2B, not on features. Avoid medical claims (comfort/wellness, not
treatment). Guard against commoditization with brand + B2B contracts + the
collectible dome-skin restock loop + IP.

---
*Built out overnight from the Idea Vault. The mechanism, firmware, patent,
and economics are all real and startable — the next move is the ten-hands
test and the provisional filing.*
