# Design 2 — The Bottle Top Module ("Boom Flask", low-profile v2)

**Difficulty: moderate — needs a well-fitting print. The cooler build.**
Your 1.2 L ThermoFlask stays a completely real, functional, water-filled
bottle. The turret lives in a 3D-printed module that replaces the real lid
during deployment. Anyone who picks the bottle up feels cold water slosh.
That's checkmate on suspicion.

## v2: the shrunk design

v1 stacked the whole mechanism *above* the bottle and stood ~53 mm tall —
conspicuously chunky. v2 sinks the mechanism **into the bottle neck**: the
Ø54 mm wide mouth comfortably swallows the Ø53.6 mm "bucket" that carries
the servo, ESP32, charger, and battery. Only the shell shows, and it's now
**~26 mm tall** — the proportions of a normal chug cap.

```
      ┌───────────────┐  ← shell dome (~26mm total visible)
      │░░░░░░░░░░░░░░░│  ← 300° window slot — the laser fires from here
   ╔══╧═══╤═══════╤═══╧══╗  ← bucket flange sits on the bottle rim
   ║      │ ┌─┐ ▲ │      ║
   ║ neck │ │s│ █ │ neck ║  ← bucket hangs into the neck: servo (s),
   ║      │ └─┘   │      ║    riser █ climbs up to the laser
   ║      └───────┘      ║
   ║   ~~~ water ~~~     ║  ← bottle still holds water below
```

- The **bucket** press-fits into the mouth like a giant cork. The servo
  stands on its floor, shaft up, landing exactly on the bottle's center
  axis. Slim electronics (ESP32-C3, TP4056, a 401230 LiPo) stand in the
  crescents beside the servo. Water sits below the bucket floor.
- The **carriage** screws onto the servo horn and climbs through a Ø32 mm
  opening in the flange; its jib holds the laser just above the flange,
  right behind the shell's window slot, fixed at **5° downward** — the
  module physically cannot aim at eye level from table height.
- The **shell** friction-fits over a register ring on the flange. Lift it
  off to charge or flip the power switch; press it back on. No visible
  ports. The 6 mm slot is covered with dark tint film and covers **300°**
  of the room without the bottle ever moving.

## The parts (see [`hardware/generate_stls.py`](../hardware/generate_stls.py))

| Printed part | Job |
|---|---|
| **bottle_bucket** | Cork + servo carrier; hangs 40 mm into the neck |
| **bottle_carriage** | Horn plate → riser → jib → laser clip at 5° down |
| **bottle_shell** | The visible "lid": window band + shallow dome |

## Critical measurements

1. `MOUTH_ID` — inner diameter of the bottle mouth. **Default is 54 mm
   (estimated).** Print the bucket FIRST at 25% height scale (a quick
   ring) or measure with calipers before committing — the press-fit
   depends on it. One turn of electrical tape fine-tunes a loose fit.
2. `BOTTLE_OD` — body diameter at the shoulder (default 92 mm). The shell
   should match the bottle body so the silhouette reads as one object.
3. Regenerate after editing: `python3 hardware/generate_stls.py`.

## Build steps

1. Validate the mouth fit (see above), then print all three parts —
   black PLA, 0.2 mm layers; supports only under the shell dome.
2. Servo into the bucket-floor pocket (shaft up), foam-tape the ESP32,
   TP4056 and LiPo into the crescents, wire it up (GPIO2 pan, GPIO4 laser).
3. Screw the carriage onto the servo horn, clip the laser into the ring,
   route its two wires down the riser with a spiral of thread or tape —
   leave slack: the carriage sweeps ~300°.
4. Glue tint film inside the shell's window slot; press the shell onto
   the register ring.
5. Fill the bottle, push the bucket into the mouth, deploy. Real lid goes
   in your bag; swap back after the meeting.

## Field notes

- Park mode points the laser at the blind spine, so even the tint slot
  shows nothing when idle.
- Wire slack is the #1 mechanical gotcha: test full sweep before closing
  the shell. If wires snag, reduce the pan range in the firmware
  (PAN_MIN/PAN_MAX).
- Condensation on a cold bottle can fog the tint film — wipe the band
  when you set it down, or deploy with room-temp water.
- If someone asks about the cap: "it's a filter lid." Nobody has a
  follow-up question about a filter lid.
