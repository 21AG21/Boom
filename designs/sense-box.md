# Design 3 — The ENV-SENSE Box (recommended)

**Difficulty: easiest print of the three. The strongest disguise.**
The pouch and bottle imitate *your* belongings — objects the people around
you know intimately, sitting at *your* seat, with the beam tracing back to
*you*. This design abandons all three weaknesses: it imitates **office
infrastructure**, lives **across the room**, and works while your hands
are visibly on the table.

## Why it beats the others

- Nobody inspects an official-looking box. A labeled "sensor" is part of
  the building, and buildings are someone else's job.
- Not attributed to you: it sits on a shelf/wall far from your seat, and
  WiFi doesn't care about distance across a conference room.
- The geometry exonerates you: when the dot appears, sight-lines point at
  a shelf — while you're demonstratively not touching anything.
- Worst case is survivable: a discovered mystery box goes to facilities.
  That's a very different conversation than *your* bottle with a laser
  inside.

## The object

A 111 × 87 × 61 mm wall/shelf box in the visual language of a CO₂ monitor:

```
   ┌──────────────────────────────┐
   │ ≡ vents        (side walls)  │   ← 3 vent slots each side (decoys)
   │ ░░░░░░░░ window ░░░░░░░  ● ← green "status" LED (heartbeat blink)
   │ ┌──────────────────────┐     │
   │ │ ENV-SENSE 2  ▍▍▍▍▍▍ │     │   ← printed label in a recess
   │ └──────────────────────┘     │
   └──────────────────────────────┘
      back: 2 keyhole slots (wall mount) + USB notch (optional mains power)
```

- **Window**: an 80 × 12 mm opening behind dark tint film — reads as the
  sensor's optical intake. The full pan-tilt turret sits behind it:
  ~±45° pan and enough tilt for shelf-height placement.
- **Status LED**: a real green LED on GPIO5 doing a slow heartbeat blink.
  It monitors nothing. It is the single most convincing component.
- **Label**: print `hardware/label_env_sense.pdf` (60 × 18 mm) on plain
  paper, glue it into the recess. Fake asset number and barcode included.
- **Mounting**: keyhole slots for a wall screw, flat base for a shelf.
  Battery-powered (a 1000 mAh LiPo runs ~a week of meeting duty), so no
  cable to explain; the rear USB notch is there if you ever want to run
  it from mains like real hardware.

## Parts

Reuses the pouch turret internals — same electronics, same firmware
(`BUILD_POUCH 1`), same tilt bracket and laser clip prints:

| Printed part | Job |
|---|---|
| **sense_case** | Body: window, vents, LED hole, label recess, trays, servo well |
| **sense_lid** | Friction-fit top lid |
| **pouch_tilt_bracket** | Tilt servo carrier (shared part) |
| **laser_clip** | Laser holder (shared part) |

## Build steps

1. Print case + lid (black or beige PLA — beige+texture reads even more
   "institutional"), plus the shared bracket and clip.
2. Pan servo into the floor well, bracket on its horn, tilt servo in,
   laser clipped, exactly like the pouch build.
3. ESP32-C3, TP4056, LiPo into their trays; green LED into the front
   hole (long leg → GPIO5 via 220 Ω, short leg → GND).
4. Tint film behind the window; label into the recess.
5. Press the lid on. Place it on a shelf with sight-lines to the room.
   Start patrol mode *before* the meeting and don't touch your phone.

## Placement notes

- Shelf height beats desk height: the beam tilts downward onto walls and
  tables naturally, and people rarely study objects above eye level.
- Set the tilt safety ceiling (firmware `TILT_MAX`) after placing it:
  aim the beam at the highest point you want reachable, note the angle,
  clamp there.
- Give it a "history": a strip of old tape or a smudge makes hardware
  look like it's been installed for years.
