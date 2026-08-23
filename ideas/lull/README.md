# Lull 🫧

> A breathing squishy: a palm pad that slowly swells so you match your breath
> to it, plus a separate gel lobe you knead. Two loved behaviors, two separate
> parts.

Lull is the design that came out of the adversarial pass on the Breathe Stone
idea — the winner, and the one that fixed the flaw every earlier concept shared
(putting the fidget gel in the breathing load path). It moves only the palm
pad, not the whole body — deliberately unlike Moonbird.

## What's here
| File | What it is |
|---|---|
| [`mechanism.md`](mechanism.md) | How it works + the **Force & Feel** section (torque, the slip-clutch, "enough torque?") |
| [`hardware/lull.py`](hardware/) | Parametric generator — 5 watertight printable parts + assembly + render |
| [`firmware/lull/`](firmware/lull/) | Constant-speed motor driver (the waveform lives in the cam, not the code) |
| [`build-guide.md`](build-guide.md) | BOM + wiring + step-by-step assembly + calibration — build one this weekend |
| [`lull-3d.html`](lull-3d.html) | The interactive 3D viewer (drag to rotate; watch the dome breathe) |

## The idea in one paragraph
A slow gearmotor turns a **cam whose edge shape *is* the breath curve** (4-1-6),
so a dumb constant-speed motor produces an organic breath with no waveform code.
The cam lifts a **follower**, which pushes a **platen** through an **authority
spring** (the slip-clutch — it sets the max push force, ~15–20 N, and gives way
to a hard clench instead of stalling). The platen drives a **sealed foam dome**
your palm rests on. Off to the side, a **separate sealed gel lobe** is there to
knead. 2×AAA, no pump, no liquid, no charge anxiety.

## Build it
```bash
pip install trimesh manifold3d scipy numpy matplotlib shapely
python3 hardware/lull.py            # -> hardware/stl/
```
Then follow [`build-guide.md`](build-guide.md): print, wire an N20 + LiPo +
driver, seat a foam disc (dome) and a NeeDoh (lobe), flash the firmware, and
calibrate the cadence + the authority spring. ~$30–40 in parts, most reusable.

## Status
Prototype-ready: geometry generates and prints watertight, firmware is
flash-ready, the build guide is complete. Physically unbuilt/untested — the
next real step is to build one and do the ten-hands test.
