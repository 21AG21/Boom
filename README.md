# Boom — Covert Desk Laser Turret

A tiny pan-tilt laser turret disguised as everyday desk objects, controlled
from your phone. Two enclosure designs are included:

| Design | Disguise | Coverage | Difficulty | Docs |
|---|---|---|---|---|
| **Pencil Pouch** | Black fabric pencil pouch (yours) | ~70° aimable arc | ★ Easiest | [designs/pencil-pouch.md](designs/pencil-pouch.md) |
| **Bottle Top Module** | ThermoFlask water bottle (yours) | 300° panoramic | ★★ Needs a decent 3D print | [designs/bottle-top.md](designs/bottle-top.md) |

3D-printable models (parametric OpenSCAD) live in [`hardware/`](hardware/).
Open a `.scad` file in [OpenSCAD](https://openscad.org) (free), tweak the
measurements at the top to match your actual pouch/bottle, press F6, and
export STL for printing.

## Shared electronics (both designs)

| Part | Approx. cost | Notes |
|---|---|---|
| ESP32-C3 SuperMini | ~$4 | Tiny (18×22 mm) WiFi microcontroller |
| SG90 / MG90S micro servo ×1–2 | ~$3 ea | MG90S metal-gear is quieter — worth it |
| 5 mW red laser diode module (6 mm) | ~$2 | KY-008 style |
| 3.7 V LiPo battery (500–1000 mAh) | ~$6 | Pouch fits a big one; bottle needs slim 401230/502030 |
| TP4056 USB-C charge board | ~$1 | Charge port + battery protection |
| Slide switch, jumper wires | ~$2 | |

Total: **under $20**. No soldering strictly required to prototype (breadboard
first), but the final compact builds want ~6 solder joints.

## How it works

The ESP32 creates its own WiFi access point (or joins your phone's hotspot)
and serves a one-page web joystick. Your phone controls pan/tilt/laser over
WebSocket. Firmware features planned:

- Smooth sine-eased motion (no robotic jerks, less servo noise)
- Auto-patrol mode: slow random drifts with long pauses
- **Freeze button**: instantly parks and blacks out when eyes start hunting
- **Tilt ceiling enforced in firmware**: the beam physically cannot rise
  above a configured angle, so it can never reach faces/eyes

## Safety (real talk)

Even a 5 mW class-3R diode should never hit an eye. Both mechanical designs
have a built-in downward tilt bias and the firmware clamps the tilt range.
Configure the ceiling for your room so the beam stays on floors, walls
below chest height, and ceilings only if aimed from a high shelf. Don't
point at reflective surfaces near faces. Entertain responsibly.
