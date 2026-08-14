# Design 2 — The Bottle Top Module ("Boom Flask")

**Difficulty: moderate — needs a well-fitting print. The cooler build.**
Your ThermoFlask stays a completely real, functional, water-filled bottle.
The turret lives in a 3D-printed **fake lid module** that replaces the real
lid during deployment. Anyone who picks the bottle up feels cold water
slosh. That's checkmate on suspicion.

## Concept

The printed module looks like a chunky matte-black insulated lid — the kind
half the bottles in any office already have. Between the "lid" dome and its
base ring runs a **6 mm dark window slot** that reads as a decorative seam.
Behind that slot, a laser on a rotating carriage covers **300° of the room
without the bottle ever moving.**

```
        ┌────────────┐   ← dome: battery + ESP32-C3 + charge board
        │   ▒▒▒▒▒▒   │
        ├────────────┤
        │ ░░░░░░░░░░ │   ← 300° window slot (tinted film) — beam exits here
        ├────────────┤      inside: pan servo + hanging laser carriage
        │  ═══╦═══   │   ← plug boss: press-fits into the bottle mouth
   ╔════╧════╩═══╧════╗
   ║                  ║  ← your actual ThermoFlask, actually full of water
```

## Why it works as a disguise

- **The object is real.** Weight, temperature, condensation, slosh — every
  sense confirms "water bottle." The module only has to survive a glance,
  and matte black PLA + a plasti-dip coat looks exactly like molded lid
  plastic.
- **The window slot** is covered with dark tinted acrylic film (sold as
  automotive tint; a 5 mW red laser passes through light tint with plenty
  of punch). From a metre away it's a styling groove.
- **360°-ish coverage** means you place the bottle once, anywhere on the
  table, and never touch it again. No aiming behavior to get caught doing.
- **One servo, fixed downward tilt.** The carriage holds the laser at a
  fixed ~5° downward angle — mechanically incapable of reaching faces at
  conference-table height, and one servo is quieter than two. Panning uses
  slow eased sweeps.

## The parts (see [`hardware/bottle_top.scad`](../hardware/bottle_top.scad))

| Printed part | Job |
|---|---|
| **Shell** | Dome + window band, the visible "lid" |
| **Bulkhead** | Disc that carries the pan servo, shaft pointing down |
| **Carriage** | Hangs from the servo horn, clips the laser at 5° down |
| **Plug ring** | Press-fits into the bottle mouth; shell snaps onto it |

Electronics: ESP32-C3 SuperMini + slim 502030 LiPo (250 mAh ≈ a full
meeting week of patrol duty) + TP4056. The USB-C charge port hides in a
cutout on the slot's blind spine — the 60° of arc with no window.

## Critical measurements (edit at the top of the .scad)

1. `bottle_od` — outer diameter of your ThermoFlask body at the shoulder
   (24 oz ThermoFlask ≈ 73 mm — verify with calipers or a paper strip:
   circumference ÷ π).
2. `mouth_id` — inner diameter of the bottle mouth (≈ 55 mm on wide-mouth
   models). The plug ring uses this minus 0.4 mm tolerance; wrap one turn
   of electrical tape for a snug, removable fit.
3. Print the plug ring **first, alone** — it's a 20-minute test print that
   validates both fits before you commit to the 3-hour shell.

## Build steps

1. Calibrate: print plug ring, test-fit, adjust tolerance, reprint if needed.
2. Print shell, bulkhead, carriage (black PLA, 0.2 mm layers, supports on
   for the shell dome).
3. Servo into the bulkhead pocket (shaft down through the center hole),
   carriage onto the horn, laser into the carriage clip.
4. ESP32 + TP4056 + LiPo foam-taped into the dome cavity; wires down
   through the bulkhead notch.
5. Tinted film strip glued inside the window slot.
6. Bulkhead snaps into the shell; shell onto plug ring; module onto bottle.
7. Real lid goes in your bag. Swap back after the meeting and take a drink.

## Field notes

- Condensation on a cold bottle can fog the tint film from outside — wipe
  the slot band when you set it down, or deploy with room-temp water.
- Park mode points the laser at the blind spine, so even the tint slot
  shows nothing when idle.
- If someone asks about the chunky lid: "it's a filter cap." Nobody has a
  follow-up question about a filter cap.
