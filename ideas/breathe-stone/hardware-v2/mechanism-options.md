# Breathe Stone — Mechanism Options

Four ways to make a dome breathe. v1 shipped the servo. v2 ships nitinol.
Here's the whole decision, so the choice is legible and the others stay on
the table for the versions they're actually best for.

## The comparison

| | **Servo + crank** (v1) | **Nitinol wire** (v2) ✅ | Slow gearmotor + cam | Wound spring + escapement |
|---|---|---|---|---|
| Silent? | No — servos hunt/buzz when holding | **Yes** — no motor at all | Nearly — a slow motor still whirs faintly | **Yes** — purely mechanical |
| Thickness | ~38 mm (upright servo) | **~24 mm** | ~30 mm | ~26 mm |
| Electronics | MCU + servo | MCU + one MOSFET | MCU + motor driver | **None** |
| Power draw | Low, but holding wastes current | Pulsed heating; fine for slow breathing | Continuous while running | **Zero** |
| Cost @ volume | ~$12 | ~$11 | ~$10 | **~$5** |
| Build difficulty | Easiest to prototype | Wire crimping + duty tuning | Cam profiling | Hardest — real horology |
| Cadence change | Firmware | Firmware | Firmware (speed) or swap cam | Swap escapement / disc |
| Best for | A first working prototype tonight | **The daily-carry retail unit** | A quiet mid-tier | The battery-free B2B / bulk unit |

## Why v2 is nitinol

The objection to shape-memory alloy is always the same: *it's slow* — it's
cooling-limited, so you can't cycle it fast. But **a breath is slow.** At
4–8 breaths per minute, an inhale is 4–5 seconds and an exhale 5–8. That is
squarely inside nitinol's comfortable range, so the actuator's one real
weakness simply doesn't apply here. In exchange you get the three things the
product most needs:

- **True silence.** No motor means nothing to hunt, hold, or gear. This
  matters more than anything for a 3 a.m. anxiety object — the whole point of
  v1's "detach the servo during holds" firmware trick was to chase a silence
  that v2 gets for free.
- **Thinness.** No upright servo drops the body from 38 mm to 24 mm — the
  difference between a hockey puck and a worry stone you'd actually pocket.
- **Solid-state simplicity.** One wire, one MOSFET, a return spring. Fewer
  moving parts to wear or rattle.

The costs are honest: nitinol is open-loop (heating-to-travel is nonlinear
and hysteretic, so `PULL_DUTY`/`HOLD_DUTY` need calibrating), the wire must be
kept off bare PLA (see the print profile's heat note), and exhale speed is set
by cooling physics, not firmware — so the cadence's exhale can't be shorter
than the wire's natural cool time. None of these is a dealbreaker; all are
documented and tunable.

## When each alternative wins

- **Servo + crank (v1)** — still the right *first* build. Cheapest parts to
  source, no wire crimping, no duty tuning. Prove the effect on someone's
  thumb with v1, then move to v2 for the product. It stays in
  [`../hardware/`](../hardware/).
- **Slow gearmotor + breathing-cam** — if nitinol tuning proves finicky in
  the field, a slow N20 gearmotor turning a *profiled cam* (whose shape
  encodes the whole breath waveform) is a robust middle path: the motor spins
  at constant speed and never holds a position, so it doesn't buzz like a
  servo. Bonus: different cadences become **swappable cam discs** — a physical
  "cadence library" that doubles as a collectible.
- **Wound spring + escapement** — the endgame for the **kinetic / B2B
  version**: no battery, no electronics, ~$5 COGS. You wind it, an escapement
  meters the release, and it paces ~10 breaths before resting. It's the
  hardest to engineer (it's a little clock), but it's the only option that can
  go, by the thousand, into waiting rooms and airline kits that will never
  charge anything. This is the natural v3 for the Calm Kit channel.

## Roadmap read
**v1 servo** → prove the effect. **v2 nitinol** (this folder) → the silent,
thin, retail daily-carry. **v3 wound-spring** → the battery-free bulk unit
for institutions. Same dome, same feel, three actuators for three jobs.
