# Lull — Mechanism

Lull is the breathing-squishy that came out of the adversarial design pass.
Its one structural idea: **two jobs, two separate parts.** The breathing and
the fidgeting never share the same piece of material — which is what lets each
be good, and what kept killing every earlier concept that tried to make one
gel blob do both.

## The two zones

**1 · The breath (a dry cam-riser under a sealed foam dome).**
A small geared motor turns at a slow, constant speed. On its shaft is a
**cam** — an off-round disc whose edge profile *is* the breath curve: shaped so
one full rotation = inhale (~4s rise), hold (~1s), exhale (~6s fall). A dumb
constant-speed motor therefore produces a correct, organic breath with no
waveform electronics; a slide switch changes only the motor's *speed* to pick
5 or 4 breaths/min, or OFF.

The cam lifts a **follower**, which pushes a **platen** bonded under the
breathing surface — a **sealed closed-cell silicone-foam dome**. It's a solid
springy block, so it can't leak (nothing fluid inside) and it springs back on
its own each cycle. The dome swells into your resting palm on inhale and
settles on exhale.

**2 · The fidget (a separate sealed gel lobe).**
A NeeDoh-style knead-zone on the rim: an injection-moulded TPE skin filled with
non-Newtonian silicone dough, heat-welded shut at one nub. Nobody actuates
through it; it's never pressurised; it just sits there to be squeezed. Because
the two zones never share a boundary, a fidget failure and a mechanism failure
can't reach each other.

No air pump, no liquid, no dynamic seal, no charge port. Power is 2×AAA.

## Force & Feel

*The question this answers: can the mechanism push the dome up against someone
gripping it hard — like a stressed person clenching?*

**Short answer: yes against a resting palm, no against a hard clench — and it's
built not to try.**

### The numbers
A small gearmotor (N20 class, high ratio) delivers roughly **0.3–0.5 N·m** of
stall torque. Through a cam of ~8 mm radius:

    force ≈ torque / radius = 0.4 N·m / 0.008 m ≈ 50 N (theoretical)

After cam friction and pressure-angle losses, usable push is more like
**15–25 N**. For comparison:

| Load | Resistance | Overpowered? |
|---|---|---|
| Palm resting on the pad (intended use) | a few N | ✅ easily |
| Light cupped grip | ~5–10 N | ✅ yes |
| Firm, deliberate clench | 50–150 N+ | ❌ no |

So the breath is felt clearly by a hand that's *resting* on the dome, which is
the intended posture — you rest a palm on it like a worry stone, you don't
crush it.

### Why it must NOT beat a fist
A motor strong enough to push out against a clenched fist would be large, loud,
power-hungry, and expensive — it breaks the ~$25–32 retail target and the
quiet-not-silent goal. Fighting the hand is the wrong objective.

### The slip-clutch, done with a spring
Between the follower and the platen sits a **series compression spring** — the
"authority spring." It is the slip-clutch:

- Palm resistance **below** the spring's preload → the spring transmits the
  full push and the dome rises. Breath felt.
- Palm resistance **above** preload (a clench) → the spring simply compresses
  and the platen stops rising. The cam keeps turning; **the motor never
  stalls, overheats, or strips gears** — the spring absorbs the motion.

So the spring's preload *is* the maximum force the dome will ever exert. That's
the design knob.

**Authority target: comfortably lift against ~15–20 N, slip above it.** Tune
three things to hit it: cam radius, gearmotor ratio (torque), and the authority
spring's rate + preload.

### Under grip, feel is pressure, not travel
Because the dome is **firm foam**, even when a moderate grip stops it from
visibly rising, the cam pushing the platen up **raises the pressure the foam
presses back into your palm** — you feel the breath as a rhythmic
firmness/pressure change, like a slow pulse, not as displacement. It doesn't
have to win a movement contest to be felt.

### And the two-zone design sidesteps the fight entirely
The clencher's energy has somewhere to go: the **gel lobe**. You knead the lobe
with your fingers (it takes any force you want) while your palm rests on the
breathing dome. The breather is never the thing being crushed — which is the
whole reason the zones are split.

## Actuation roadmap
Same two-zone body, three drives for three price points:
- **Electric cam-riser** (this doc) — the retail unit, ~$25–32.
- **Nitinol wire** (see `../breathe-stone/hardware-v2/`) — silent, thin, if
  motor-noise quality proves hard.
- **Wound spring + escapement** — battery-free bulk/B2B unit for waiting-room
  Calm Kits.
