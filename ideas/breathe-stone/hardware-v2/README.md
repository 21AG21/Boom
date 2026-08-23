# Breathe Stone v2 — silent nitinol build

The retail-intent version. v1 proved the effect with a servo; **v2 removes
the motor entirely** and drives the dome with a shape-memory (nitinol) wire.
The result is silent, solid-state, and **24 mm thick — 14 mm thinner than
v1** — a stone you'd actually keep in a pocket.

> The trick: a breath is slow (4–8/min), and nitinol is "slow" only because
> it's cooling-limited — so the one thing that makes SMA a poor general
> actuator makes it a perfect one here.

## What's here
| File | What it is |
|---|---|
| `breathe_stone_v2.py` | Parametric generator (repo idiom). Five watertight parts + assembly. |
| `stl/` | Printable parts: `v2_base`, `v2_lid`, `piston`, `crank` (bell crank), `dome`. |
| `render_preview_v2.py` · `parts_preview_v2.png` | The labelled render. |
| `firmware/breathe_stone_v2/` | ESP32-C3 + MOSFET SMA driver — thermally-safe, silent. |
| `print-profile.md` | Slicer-ready settings, filament/time estimates, the wire-heat caveat. |
| `mechanism-options.md` | Servo vs nitinol vs gearmotor-cam vs wound-spring — the full decision. |

## How it works
A nitinol wire, anchored in the base and routed as a hairpin, **contracts when
a MOSFET pulses current through it**, pulling the short arm of a **bell crank**.
The long arm lifts the piston that carries the dome — that's the inhale. Cut
the current, the wire cools, and a **return spring** lowers the dome — the
exhale. The firmware shapes the current to the 5-5 / 4-7-8 / box cadences;
exhale is passive, so its speed is set by how fast the wire cools (pick the
wire gauge to match).

## Build it
```bash
pip install trimesh manifold3d scipy numpy matplotlib
python3 breathe_stone_v2.py          # -> stl/
python3 render_preview_v2.py         # -> parts_preview_v2.png
```
Then follow [`print-profile.md`](print-profile.md) to print, wire the MOSFET +
ESP32-C3 + LiPo, flash [`firmware/breathe_stone_v2/`](firmware/breathe_stone_v2/),
and calibrate the two duty constants so the dome travels ~4 mm and holds
without the wire getting hot.

## Two things to respect
- **Wire heat vs PLA** — the wire hits ~60–90 °C; keep it off bare PLA (air
  gap + a thin PTFE sleeve, or print the base in PETG). Details in the profile.
- **Open-loop tuning** — SMA heating-to-travel is nonlinear; start
  `PULL_DUTY`/`HOLD_DUTY` low and raise slowly. A future rev adds a hall/flex
  position sensor for closed-loop.

See [`mechanism-options.md`](mechanism-options.md) for why nitinol, and when the
servo (v1), a gearmotor-cam, or a battery-free wound-spring (the v3 bulk unit)
each win instead.
