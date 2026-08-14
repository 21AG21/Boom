# Design 1 — The Pencil Pouch Turret ("Boom Pouch")

**Difficulty: easiest. Best first build.** Fabric is the perfect turret skin:
it muffles servo noise, hides all internals, slouches naturally so nothing
looks rigid, and a pencil pouch with its zipper 2 inches open is the least
suspicious object in any meeting room.

## Concept

A 3D-printed chassis "boat" sits inside your black pouch and gives it a
secret skeleton. The pan-tilt turret is mounted at one end, aimed out the
**partially open zipper corner** — a dark opening nobody ever registers.
A few real pens and a highlighter sit clipped along the top of the chassis,
so if anyone glances inside the open corner, they see... pens.

```
        zipper opened ~50mm at this corner
              ▼
   ┌──────────░░─────────────────────────┐
   │  [laser]▷░░   pens laid on top      │   ← fabric pouch
   │  [tilt-servo]                       │
   │  [pan-servo] [ESP32] [chg] [battery]│   ← printed chassis inside
   │  (washer weights under base)        │
   └─────────────────────────────────────┘
```

## Why it works as a disguise

- **Noise**: two layers of fabric + foam tape on the chassis = servo buzz
  becomes inaudible past ~1 m. This is the quietest of the two designs.
- **Movement**: the beam moves; the pouch doesn't. The turret is decoupled
  from the fabric (chassis is weighted, turret only swings a light laser).
- **Inspection-proof**: unzip it fully for a doubter and tilt it — pens and
  a highlighter dominate the view; the electronics read as "power bank."
  A TP4056 board with a USB-C port literally *is* half a power bank.
- **Charging story**: plugging USB-C into a pouch looks odd, so charge it
  at home. A 1000 mAh LiPo runs the ESP32 + lazy servo duty cycle for
  several work days.

## Aiming

The zipper corner gives roughly a **70° horizontal arc and 25° vertical**.
You aim the *center* of the arc by how you casually set the pouch down —
the turret handles the rest. The chassis nose has an alignment ring so the
laser's neutral position always matches the zipper opening.

## Build steps

1. Measure your pouch's interior (length × width at the base). Edit the two
   numbers at the top of [`hardware/pouch_chassis.scad`](../hardware/pouch_chassis.scad)
   and export/print the three parts (chassis, tilt bracket, laser clip).
   ~3 h print, any black PLA.
2. Drop two M8 fender washers (or quarters) into the base pockets — the
   weight keeps the pouch planted while servos move.
3. Screw the pan servo into its well, press the tilt bracket onto the pan
   horn, clip the laser into the tilt horn ring.
4. Stick the ESP32-C3, TP4056 and battery into their trays (double-sided
   foam tape — also damps vibration).
5. Wire: battery → TP4056 → slide switch → ESP32 5V/GND; servo signals to
   GPIO 2 & 3; laser module to GPIO 4 via its transistor pin.
6. Foam tape on the chassis underside, slide it into the pouch, lay 3–4
   real pens in the top clips, zip until ~50 mm stays open at the nose.

## Field notes

- Set the pouch on a folder or notebook — raising it 10–15 mm off the table
  widens the usable downward angle.
- The "freeze" button in the app blacks out the laser and parks the servos
  center — hit it the moment someone starts visually hunting.
- Keep one real pen *in use* from the pouch during the meeting. Ownership
  established, suspicion zero.
