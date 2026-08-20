# Ship One in a Month

You already own the hardest asset most idea-guys lack: **a working
parametric 3D-print pipeline** (`hardware/generate_stls.py`, the STL
toolchain, the OpenSCAD sources). That's a physical-product prototyping lab.
This plan turns the #1 flagship — **Breathe Stone** — into something real in
four weekends, reusing exactly what's already in this repo.

The point isn't the specific idea; it's proving to yourself that you can go
from a page in the vault to an object in your hand in 30 days. Do it once and
every other idea in here gets cheaper.

---

## Week 1 — Prove the effect (no electronics)

**Goal:** confirm that a swelling dome actually calms *your* breathing.
- Print a plain pebble shell + a domed cap from the repo's pipeline
  (`python3 hardware/generate_stls.py`, edit dimensions at the top).
- Drive the dome by hand or with a cheap hobby servo + the sine-eased
  motion code pattern already in `firmware/` (the turret firmware literally
  does smooth sine easing — reuse the easing math, not the aiming).
- Sit with it for 5 minutes. If your breathing entrains, continue. If not,
  fix the cadence/travel *before spending another dollar.*

**Deliverable:** a video of the dome breathing at 4-7-8. That's your first
proof and your first marketing asset.

---

## Week 2 — Make it standalone

**Goal:** a self-contained unit anyone can hold.
- ESP32-C3 or a smaller ATtiny; one micro-servo or a nitinol wire; one AAA
  or a small LiPo + TP4056 (all parts already spec'd in the repo's BOM).
- Add the physical cadence switch (4-7-8 / box / coherence).
- Silence check: it must be inaudible in a quiet room. Swap to a metal-gear
  servo or a cam-and-spring if not.

**Deliverable:** one unit that runs untethered for a week on a charge.

---

## Week 3 — Ten units + ten hands

**Goal:** find out if strangers feel it too.
- Print 10 shells. Hand them to 10 people, say nothing but "hold this."
- Watch: do they keep holding it? Does their breathing slow? Would they pay $29?
- Log every reaction. This is your real product research — cheaper and
  truer than any survey.

**Deliverable:** 10 data points and at least 3 unprompted "where can I buy this."

---

## Week 4 — Protect it and post it

**Goal:** a defensible position and a public signal.
- **Provisional patent:** file a US provisional (~$130 micro-entity) on the
  tactile-only respiratory pacer claim from the deep dive. It's cheap, buys
  you 12 months of "patent pending," and forces you to write the invention
  down precisely.
- **One video:** the Seed-Fidget-style arc but for Breathe Stone — anxious
  person, hand on stone, breathing visibly slows. Post it. Gauge reach.
- **Decide:** the responses tell you whether to tool up for injection
  molding, list on a crowdfunder, or pivot to a different vault page.

**Deliverable:** a provisional filing number and one public post you can
point investors/partners to.

---

## The reusable playbook

Every physical idea in the vault runs the same loop:

1. **Print the mechanism** on this repo's pipeline (days, not weeks).
2. **Steal the firmware patterns** already here (sine easing, AP web UI,
   safety clamps) instead of writing them again.
3. **Ten hands** before any tooling money.
4. **Provisional patent** the one defensible claim while it's cheap.
5. **One video** to test reach before committing capital.

You're not starting from zero on any of them. You're starting from a lab.

---

## Cost to first real unit

| Item | Cost |
|---|---|
| Filament + prints (10 shells) | ~$15 |
| ESP32-C3 / servo / LiPo / charger (from repo BOM) | ~$20 |
| US provisional patent (micro-entity) | ~$130 |
| **Total to a patent-pending object in your hand** | **~$165** |

That's the whole bar. $165 and four weekends separates "I have ideas" from
"I have a patent-pending product and footage of strangers wanting it."
