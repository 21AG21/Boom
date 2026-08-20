# Provisional Patent Application — DRAFT

**Title:** Handheld Tactile Respiratory-Pacing Device with a Localized
Reciprocating Pad and Silent Hold Operation

**Applicant / Inventor:** _[your name]_
**Prepared:** August 2026
**Status:** DRAFT for the applicant's review. This is a working draft to
support a U.S. provisional filing (USPTO micro-entity fee ~$65 in 2026). It
is **not legal advice.** Before spending on a non-provisional, commission a
professional prior-art search — a close commercial product (Moonbird) exists
and is discussed candidly in the Background and in the Patentability Notes at
the end.

---

## Cross-Reference to Related Applications
None.

## Field of the Invention
The invention relates to handheld devices for guiding human breathing, and
more particularly to a pocket-carried tactile object that paces a user's
respiration through a localized, silently-actuated pad contacted by a single
digit, without a visual display, audible tone, or required companion
application.

## Background of the Invention

**The need.** Paced or "slow" breathing (typically 4–7 breaths per minute)
is a well-supported technique for down-regulating the autonomic nervous
system, reducing acute anxiety, and improving heart-rate variability. In
practice, people reach for it exactly when they are least able to operate a
screen: mid-panic, in public, at 3 a.m., in a waiting room, or as a child or
non-verbal user who cannot follow an app.

**Existing approaches and their limitations.**

1. *Software pacers (e.g., meditation and breathing apps).* These require a
   phone, add another illuminated screen and notification surface to a user
   who is often over-stimulated already, and demand visual or auditory
   attention. They are unsuitable in the dark, in social settings, or for
   users who cannot read a screen.

2. *Whole-body vibratory relaxation devices (e.g., chest-placed infrasonic
   units; wrist/ankle haptic wearables).* These deliver vibration rather
   than a paced expansion the user actively follows, are comparatively
   expensive, and are session- or wearable-oriented rather than a
   grab-and-hold object.

3. *Handheld tactile breathing pacers that expand and contract as a whole in
   the hand (e.g., the Moonbird device).* Such devices pace breathing by
   physically changing the volume/shape of the entire gripped body, require
   a particular full-hand grip and orientation to work, are priced as
   clinical wellness gadgets (on the order of US$150–229 at retail), and
   typically pair with a companion application for biofeedback. Because the
   whole body deforms, the device reads as a purpose-built medical gadget
   rather than an unremarkable everyday-carry object, and its size and cost
   preclude bulk, disposable, or ambient-object deployments.

**The unmet need** is a low-cost, everyday-carry object that (a) is
indistinguishable at rest from an ordinary tactile comfort object such as a
worry stone; (b) paces breathing through a *localized* moving pad a single
digit rests on, rather than deforming the whole gripped body; (c) operates
with **no visual or audible output at all**, so it does not itself become an
alerting stimulus; (d) can be made effectively silent, including through the
long breath-hold phases used in techniques such as 4-7-8 and box breathing;
and (e) admits a battery-free embodiment for always-ready use and reduced
electronic waste, and a very-low-cost embodiment suitable for bulk or
institutional distribution.

## Summary of the Invention

The invention is a handheld respiratory-pacing device comprising a
hand-sized body, substantially rigid over most of its exterior, that
presents a single **localized reciprocating pad** on one face. The pad rises
and falls along a path transverse to that face over a repeating cadence
corresponding to a target breathing pattern. A user rests one digit —
typically the thumb — on the pad and entrains their inhalation and
exhalation to its motion. The device produces **no visual and no audible
pacing output**; the pad's tactile motion, optionally punctuated by a
discrete haptic "apex" cue at the top of inhalation, is the sole channel.

In a first, electromechanical embodiment, a rotary actuator (e.g., a micro
servo or geared motor) drives a **motion converter** — a cam, crank, or
inclined/swash face — that transforms rotation into reciprocating travel of
a piston carrying the pad. A controller drives the actuator along a
smoothly-eased (e.g., smootherstep or sinusoidal) profile so pad motion is
organic rather than mechanical. During isometric **hold** phases of a
cadence, the controller **de-energizes or mechanically decouples the
actuator** so the device emits substantially no acoustic noise while the pad
dwells — a "silent hold." A mechanical, detented selector chooses among
plural cadences (for example 5-5 coherence, 4-7-8, and 4-4-4-4 box
breathing).

In a second embodiment, the actuator is a **shape-memory-alloy element**
(e.g., nitinol wire) that contracts on heating to drive the pad, permitting
a thinner, silent, near-solid-state device.

In a third embodiment, the device contains **no electronics**: a user winds
a spring that, released through a mechanical escapement or governor, paces
the pad through a fixed number of breathing cycles before coming to rest.
This battery-free embodiment is always ready, generates no electronic waste,
and can be produced at very low cost for bulk or institutional distribution.

Because only a small pad moves while the body stays rigid, the body can be
shaped and finished as an ordinary worry stone, pebble, or comfort object;
the respiratory-pacing function is concealed until the pad is touched.

## Brief Description of the Drawings
The following informal figures accompany this draft (see the rendered
prototype image `hardware/parts_preview.png` and the parametric source
`hardware/breathe_stone.py`, which generate the referenced parts):

- **FIG. 1** — perspective view of the assembled device (an ovoid pebble
  body with a domed pad on the upper face).
- **FIG. 2** — the lower body shell, showing an actuator well, a battery
  bay, a controller shelf, a cadence-selector aperture, and ballast pockets.
- **FIG. 3** — the upper body shell, showing the pad aperture with a capture
  groove and an internal guide bore.
- **FIG. 4** — the piston, showing a travel-limiting shoulder, an
  anti-rotation key, and a drive socket.
- **FIG. 5** — the crank/motion-converter that mounts on the actuator output
  and lifts the piston.
- **FIG. 6** — the compliant pad (dome), a thin elastomeric spherical cap
  with a peripheral lip captured by the upper shell.
- **FIG. 7** — a cadence timing diagram plotting pad displacement versus time
  for 5-5, 4-7-8, and box cadences, showing eased transitions and dwell
  ("hold") intervals during which the actuator is de-energized.

## Detailed Description

### Overall structure
A body (**10**) sized to be held in one hand — in one prototype approximately
78 mm × 58 mm × 38 mm, with a flat, weighted base for stability — comprises a
lower shell (**20**) and an upper shell (**30**) that join to enclose the
mechanism. The body's exterior is substantially rigid and, apart from the
pad, continuous, so that at rest it presents as an ordinary tactile comfort
object. A localized pad (**40**) is exposed through an aperture (**32**) in
an upper face of the body and is the only moving external surface.

### The pad and its guidance
The pad (**40**) is, in one embodiment, a thin compliant elastomeric dome
(e.g., silicone or thermoplastic polyurethane), 30–40 mm in diameter, having
a peripheral lip (**42**) captured in a groove (**33**) around the aperture,
so its edge is sealed and fixed while its center translates. The pad is
carried by, or bears upon, a piston (**50**) constrained to reciprocate along
an axis transverse to the upper face by a guide bore (**34**) in the upper
shell. The piston includes an anti-rotation feature (**52**), e.g., a key or
flat, so the pad does not twist, and a shoulder (**54**) that limits maximum
travel. Full pad stroke in the prototype is approximately 3–6 mm.

### Electromechanical drive (first embodiment)
A rotary actuator (**60**) — for example a hobby micro servo (SG90/MG90S
class) or a small geared DC or stepper motor — is seated in a well (**22**)
in the lower shell with its output directed toward the piston. A motion
converter (**70**) coupled to the actuator output transforms rotation into
reciprocation of the piston. The converter may be:

- a **crank** with a pin engaging a socket or slot in the piston (a
  scotch-yoke-type coupling), giving pad displacement approximately
  proportional to the sine of the actuator angle;
- an **eccentric or profiled cam** bearing on a follower on the piston; or
- an **inclined or "swash" face** on a rotating member on which the piston
  foot rides, giving sinusoidal lift as the member turns.

A controller (**80**) — e.g., a small microcontroller such as an ESP32-C3
class module on a shelf (**24**) in the lower shell, powered by a rechargeable
cell (**90**) in a bay (**26**) with an associated charge port (**28**) —
commands the actuator to follow a displacement-versus-time profile
corresponding to a selected cadence. Transitions between inhale and exhale
are **eased** (e.g., by a smootherstep function s(t) = t³(t(6t−15)+10) or a
raised-cosine), so pad velocity is zero at each turning point and the motion
feels organic and produces no snap.

### Silent hold (a distinguishing method)
Several breathing techniques include isometric **hold** phases (e.g., the
7-count hold of 4-7-8; the two 4-count holds of box breathing) during which
the pad should remain stationary. A servo or motor commanded to maintain a
loaded static position typically hunts and emits an audible buzz, which is
objectionable in the bedtime and anxiety contexts the device targets. In the
present invention, upon entering a hold phase and after the pad has settled,
the controller **de-energizes and/or mechanically decouples the actuator**
(for example by detaching drive to a servo, cutting motor current, or
releasing a clutch), allowing the pad to dwell under the mechanism's residual
friction and/or a light detent, so that the device is substantially silent
throughout the hold. The controller re-energizes the actuator immediately
before the next moving phase. The same de-energization is applied during
extended pauses and before a sleep state, minimizing both noise and power.

### Haptic apex cue
Optionally, at the top of the inhalation phase, the mechanism provides a
discrete tactile cue — for example a slight over-travel-and-settle, a light
detent the piston crosses, or a brief low-amplitude oscillation — so the user
perceives a defined "top of breath" without any light or sound.

### Shape-memory embodiment (second embodiment)
The rotary actuator and converter are replaced by one or more shape-memory-
alloy (SMA) elements (e.g., nitinol wire) arranged to shorten on resistive
heating and thereby raise the pad, and to relax (lowering the pad) on
cooling, the controller modulating heating current to follow the cadence
profile. This embodiment is silent, has no gear train, and permits a thinner
body (on the order of 22 mm).

### Battery-free kinetic embodiment (third embodiment)
The device contains no electronics. A user winds a spring (**100**) via an
external knob or by squeezing the body; the spring drives the pad through the
motion converter, and a mechanical **escapement or governor** (**110**) meters
the release so the pad reciprocates at the target respiratory rate for a
fixed number of cycles (e.g., ten breaths) before the spring is spent and the
pad returns to rest. A mechanical detented selector may change the escapement
rate to select among cadences. This embodiment is always ready, requires no
charging, produces no electronic waste, and is inexpensive to manufacture in
volume for bulk or institutional distribution.

### Cadence selection
A user-accessible selector (**120**) — e.g., a detented slide or rotary
switch exposed through an aperture (**23**) in the body wall — chooses among
plural stored or mechanically-defined cadences, including without limitation
5-5 coherence breathing, 4-7-8 breathing, and 4-4-4-4 box breathing. In an
electronic embodiment the selector may be a single button that cycles
cadences and, by multi-press or hold, pauses the device or places it in a
low-power sleep from which a press wakes it.

### Body, materials, and concealment
Because only the pad moves, the body may be finished as an ordinary comfort
object — a river-stone pebble, an egg, a coin, or a figurine — of wood-filled
or mineral-filled polymer, cast resin, ceramic, or metal, optionally weighted
with internal ballast (**130**) to give the reassuring heft of a worry stone.
The pad may be color- and texture-matched to the body so the pacing function
is not apparent until the pad is touched and set in motion. A soft-touch or
elastomeric overmold may cover part or all of the body.

### Operation
A user selects a cadence, rests a thumb (or other digit) on the pad, and
breathes so that inhalation tracks the pad's rise and exhalation tracks its
fall, holding the breath while the pad dwells. No screen is consulted and no
sound is emitted; the user may keep their eyes closed or attend to a
conversation while using the device.

---

## Claims

What is claimed is:

1. A handheld respiratory-pacing device comprising: a hand-sized body having
   an exterior that is substantially rigid over a majority of its area; a pad
   exposed at a localized region of a face of the body and movable relative
   to the body along a path transverse to said face; and a drive operable to
   reciprocate the pad along said path over a repeating cadence corresponding
   to a target breathing pattern, such that a user resting a single digit on
   the pad entrains breathing to the pad's motion; wherein the device is
   configured to pace breathing without emitting a visual or audible pacing
   output.

2. The device of claim 1, wherein the body, apart from the pad, presents at
   rest as an ordinary tactile comfort object such that the respiratory-pacing
   function is not apparent until the pad is contacted.

3. The device of claim 1, wherein the pad comprises a compliant elastomeric
   dome having a peripheral portion fixed to the body and a central portion
   that translates along said path.

4. The device of claim 1, further comprising a piston constrained by a guide
   in the body to reciprocate along said path and carrying or bearing upon
   the pad, the piston including an anti-rotation feature that prevents the
   pad from rotating.

5. The device of claim 1, wherein the drive comprises a rotary actuator and a
   motion converter that transforms rotation of the actuator into
   reciprocation of the pad.

6. The device of claim 5, wherein the motion converter comprises one of: a
   crank having a pin engaging the piston; an eccentric or profiled cam
   bearing on a follower; and an inclined face on which a follower rides.

7. The device of claim 5, further comprising a controller that drives the
   actuator along a displacement-versus-time profile in which transitions
   between inhalation and exhalation are eased such that pad velocity
   approaches zero at each turning point.

8. The device of claim 7, wherein the cadence includes at least one hold
   phase during which the pad is nominally stationary, and wherein the
   controller de-energizes or mechanically decouples the actuator during the
   hold phase so that the device is substantially acoustically silent while
   the pad dwells.

9. The device of claim 8, wherein the controller re-energizes or re-couples
   the actuator immediately prior to a subsequent moving phase of the cadence.

10. The device of claim 1, wherein the drive comprises a shape-memory-alloy
    element that changes length in response to applied heating to move the
    pad.

11. The device of claim 1, wherein the drive comprises a user-wound spring
    and a mechanical escapement or governor that meters release of the spring
    so as to reciprocate the pad at the target breathing rate for a finite
    number of cycles, and wherein the device is free of electronic components.

12. The device of claim 1, further comprising a user-operable selector that
    selects among a plurality of cadences including at least two of: a
    coherence cadence with equal inhalation and exhalation intervals; a
    4-7-8 cadence; and a box-breathing cadence.

13. The device of claim 1, wherein the drive is configured to provide, at a
    peak-inhalation point of the cadence, a discrete tactile cue distinct
    from the reciprocating motion, without any visual or audible output.

14. The device of claim 1, further comprising internal ballast weighting the
    body to a mass giving the tactile character of a worry stone.

15. The device of claim 1, wherein the device omits any illuminated display
    and any audible transducer used for pacing, such that the pad's motion is
    the sole pacing channel.

16. A method of pacing human breathing, comprising: presenting, at a
    localized region of a face of a hand-sized body whose exterior is
    otherwise substantially rigid, a pad that reciprocates transverse to said
    face; driving the pad through a repeating cadence corresponding to a
    target breathing pattern; and, during a hold phase of the cadence in which
    the pad is nominally stationary, de-energizing or mechanically decoupling
    an actuator that drives the pad so that the body emits substantially no
    acoustic noise during the hold phase; wherein the cadence is conveyed to a
    user by tactile motion of the pad without a visual or audible pacing
    output.

17. The method of claim 16, further comprising easing transitions between
    inhalation and exhalation phases such that pad velocity approaches zero at
    each turning point.

18. The method of claim 16, further comprising selecting, via a user-operable
    selector, among a plurality of cadences differing in the number and
    duration of inhalation, hold, and exhalation phases.

19. The method of claim 16, wherein driving the pad comprises releasing a
    user-wound spring through a mechanical escapement, the method being
    performed without electrical power.

20. The device of claim 1, wherein the body is dimensioned to be carried in a
    pocket and the pad is dimensioned to be covered by a single thumb.

---

## Abstract
A handheld device paces a user's breathing through touch alone. A hand-sized
body, rigid over most of its exterior and shaped like an ordinary comfort
object such as a worry stone, presents a single localized pad on one face. A
drive reciprocates the pad along a path transverse to that face over a
repeating cadence (e.g., 5-5 coherence, 4-7-8, or box breathing); a user
rests a thumb on the pad and matches inhalation and exhalation to its rise
and fall. The device emits no visual or audible pacing output. In an
electromechanical embodiment a rotary actuator and motion converter drive a
guided piston that carries the pad, transitions are smoothly eased, and the
actuator is de-energized during breath-hold phases so the device is silent
while the pad dwells. Shape-memory-alloy and battery-free spring-and-
escapement embodiments are also disclosed.

---

## Patentability Notes (for the applicant — not part of the filing)

**Known close prior art.** *Moonbird* is a commercially available handheld
device that paces breathing by expanding and contracting **as a whole** in
the hand. Treat it as the primary reference. General "tactile/haptic
breathing guide" concepts also appear in patent literature and apps. Do a
professional search before a non-provisional.

**Where the defensible whitespace appears to be** (claims above are drafted
to lean here):

1. **Localized pad vs. global deformation.** Moonbird deforms the entire
   gripped body; here a *single small pad on an otherwise rigid comfort-object
   body* moves, with the function concealed until touched (claims 1–3, 20).
   This is the strongest structural distinction — keep it central.
2. **Silent-hold method.** De-energizing/decoupling the actuator through
   isometric hold phases for silence (claims 8–9, 16) is a specific, testable
   method that Moonbird's whole-body pneumatic actuation does not present in
   the same way.
3. **Battery-free spring/escapement embodiment** (claims 11, 19) — a genuinely
   different actuation class aimed at bulk/institutional and zero-e-waste use.
4. **Strictly no visual/audible output** as an affirmative limitation (claims
   1, 15) — a deliberate design constraint framed as a feature.

**Weak spots to expect.** "Pace breathing with a moving tactile surface" is
close to Moonbird and may be deemed obvious in the abstract; survival will
depend on the *specific mechanism and method* limitations, not the broad
idea. Independent claim 1 may need narrowing toward the localized-pad-on-
rigid-body structure if the examiner reads Moonbird broadly.

**Recommended next steps.** (1) File this provisional now to secure a date and
12 months of "patent pending" for ~$65. (2) Within that year, commission a
professional prior-art search (~$1–2k) focused on Moonbird's patent family
and haptic-breathing-guide art. (3) Build and film the prototype (the repo's
`hardware/` and `firmware/` folders) to support enablement and any later
design-patent filings on the specific pebble form. (4) Decide on a
non-provisional only if the search supports the mechanism/method claims.
