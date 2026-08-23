# Breathe Stone v2 — Slicer-Ready Print Profile

Settings you can punch straight into PrusaSlicer / OrcaSlicer / Cura. A
0.4 mm nozzle and 0.2 mm layers throughout. No slicer was available to
generate a true G-code preview here, so filament and time are **estimates
computed from the actual mesh volumes** — confirm in your slicer before a
long run.

## Per-part settings

| Part | Material | Orientation on bed | Layer | Walls | Infill | Supports | Notes |
|---|---|---|---|---|---|---|---|
| `v2_base` | PLA (or **PETG** — see heat note) | floor down, cavity up (as modelled) | 0.20 | 4 | 20% | Only under the pivot-pin cross-hole (a short bridge) | Brim if bed adhesion is marginal |
| `v2_lid` | PLA | **top face down** (dome rim on the glass) | 0.20 | 4 | 20% | Light, under the inner guide tube | Top-down gives a glass-smooth dome rim |
| `v2_piston` | PLA (or PETG) | axis vertical, shoulder up | 0.16 | 3 | 30% | None | Fine layers so it slides cleanly in the bore |
| `v2_crank` | **PETG or nylon** | L laid flat on the bed | 0.16 | 4 | 40% | None | It carries the load — tougher material, denser fill |
| `v2_dome` | **TPU 95A** | convex side up | 0.20 | 2 | 0% (gyroid 5% if it feels flimsy) | None | The only flexible part; the touch surface |

## Global settings
- Nozzle 0.4 mm · first layer 0.24 mm · 4 top / 4 bottom layers.
- PLA 205 °C / bed 60 °C · PETG 240 °C / bed 80 °C · TPU 225 °C / bed 40 °C, slow (~20 mm/s).
- Seam: rear/`-y` side (away from the label window) so the front stays clean.
- Print the two shells and the piston in one PLA job; swap to PETG for the
  crank and TPU for the dome.

## Estimated filament & time (one full set)

| Part | Solid vol | ~Printed | Filament | Mass | ~Time |
|---|--:|--:|--:|--:|--:|
| v2_base | 17.1 cm³ | 9.4 cm³ | 3.9 m | 11.6 g | ~101 min |
| v2_lid | 11.0 cm³ | 6.0 cm³ | 2.5 m | 7.5 g | ~67 min |
| v2_piston | 3.7 cm³ | 2.2 cm³ | 0.9 m | 2.8 g | ~29 min |
| v2_crank | 0.4 cm³ | 0.3 cm³ | 0.1 m | 0.3 g | ~10 min |
| v2_dome | 2.2 cm³ | 1.8 cm³ | 0.8 m | 2.3 g | ~25 min |
| **Set** | | **19.8 cm³** | **~8.2 m** | **~25 g** | **~3.9 h** |

Material cost per set ≈ **$0.49** at a $20/kg spool. "Printed" volume assumes
typical infill; "Solid" is the model volume (100% infill upper bound).
Throughput assumed ~6 cm³/h for small detailed parts — your printer may
differ ±40%.

## ⚠️ The one real constraint: wire heat vs. PLA
The nitinol wire reaches roughly **60–90 °C** while actuating. **PLA softens
around 55–60 °C.** So the wire must never bear on a PLA wall:
- The generator routes the wire through an **air-gapped channel** — keep it
  that way, and add a thin **PTFE (Teflon) sleeve** over the wire where it
  passes any wall. PTFE is cheap, slick, and heat-proof.
- If you'd rather not fuss with a sleeve, **print `v2_base` in PETG** (softens
  ~80 °C) and keep the air gap. That's the safe default for a daily-carry unit.
- The dome, lid, and outer shell never get hot — PLA is fine there.

## Assembly order
1. Crimp the nitinol wire as a hairpin sized from the travel formula in
   `breathe_stone_v2.py` (a≈5, b≈14 → ~36 mm), anchor one end in the base post.
2. Drop the **bell crank** onto the pivot fork; pin it (1.75 mm filament
   offcut or a 2 mm brass rod).
3. Hook the wire's moving end to the crank's input-arm hole; set the other
   crimp so the wire is just taut with the dome at rest.
4. Seat the **return spring** in its pocket; drop in the **piston**, tip of
   the crank's output arm under the piston.
5. Wire the MOSFET board (gate→GPIO2, wire in series with drain), ESP32-C3,
   LiPo + charge board into their bays.
6. Press the **TPU dome** lip into the lid groove; screw the lid to the base.
7. Flash `firmware/breathe_stone_v2/`, then **calibrate** `PULL_DUTY` /
   `HOLD_DUTY` so the dome travels ~4 mm on inhale and holds without the wire
   getting too hot to touch. Start low and raise slowly.
