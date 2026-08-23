# LASER-POINTER — the basic wireless button build (~$16, no code, no solder)

A laser dot you toggle from across the room with a **physical button on a
little wireless remote**. **No microcontroller, no phone, no app, no code,
and no soldering.** Nothing hidden — it's a laser wired to a tiny wireless
relay, sitting out in the open.

It works with a ready-made **433 MHz RF relay kit**: a remote (the button)
and a thumb-size **relay module** with wires already attached. The laser and
battery wires twist onto the relay's wires (held with tape). Press the remote
→ the relay closes the circuit → the laser lights. Press again → off.

```
   your hand                     across the room
  ┌──────────┐   433 MHz radio   ┌────────────────────────────────┐
  │  remote  │ ) ) ) ) ) ) ) ) ) │  relay module (pigtail wires)  │
  │ (button) │                   │   red  ─ power +               │
  └──────────┘                   │   black─ power −               │
                                 │   out1 ─┐  (the switch,        │
                                 │   out2 ─┘   no polarity)       │
                                 └────────────────────────────────┘
   press remote → the two output wires connect → laser gets power → dot on
```

Build time once parts arrive: **~10 minutes** with a stripper/scissors and tape.

---

## PART 1 — What to buy (~$16, two things + AAs you already have)

Both parts come with **wires already attached** (no screw terminals, no
soldering). You join wire-to-wire by twisting and taping.

| # | Thing | Buy this | What to check |
|---|---|---|---|
| 1 | **433 MHz RF relay + remote kit** (mini, pigtail wires) | [ZABLL DC 3.7–12 V mini RF relay + remote — B08F7CTDWT](https://www.amazon.com/DC-3-7V-Wireless-Momentary-Transmitter/dp/B08F7CTDWT) | Listing must say **DC 3.7–12 V** (so 4.5 V works). Confirm one of its **"five working modes"** is **self-locking / toggle** — set it to that (not momentary). ~$10 |
| 2 | **Red laser module, 5 mW, with leads** | [DTOL 650 nm 5 mW 5 V, 10-pack — Amazon's Choice, ~$6](https://www.amazon.com/HiLetgo-10pcs-650nm-Diode-Laser/dp/B071FT9HSV) | 3–5 V, has two lead wires and a built-in driver — **no resistor needed.** On the DTOL, leads are **red (+) / blue (−)**. ~$6 |
| 3 | **Electrical tape** | any tape you have | Holds each twisted joint. A roll is ~$3 if you don't own any. |
| — | **3 × AA batteries** | you already have these | Fresh **alkaline** (not rechargeable — NiMH's 3.6 V is too low to click the relay). |

**Total: about $16** (plus tape you probably own). Only need a battery holder
if you don't own one: [3×AA holder w/ switch — B0C5M9XGGV](https://www.amazon.com/Jstincal-Battery-Holder-4-5-5V-3%C3%971-5V/dp/B0C5M9XGGV) (~$5).

> **Why 4.5 V (3×AA):** it's inside the laser's 3–5 V range *and* inside this
> relay's 3.7–12 V range, so one battery pack safely runs both. Don't use 6 V
> (4×AA) — that can over-drive a 5 V laser.

> **Sturdier joints (optional):** twist + tape is fine for this 4.5 V, tiny-
> current circuit. If you want reusable, tape-free joints, add
> [WAGO 221 lever connectors](https://www.amazon.com/Wago-Lever-Nut-Assortment-Pocket-Pack/dp/B01N0LRTXZ) (~$8) and skip the tape.

---

## PART 2 — Identify the wires

This relay module has **loose wires ("pigtails"), not screw terminals.** The
kit's slip of paper labels them. The standard layout is:

- **Red** = power **+** (VCC in).
- **Black** = power **−** (GND in).
- **Two output wires** (often yellow + blue/white) = the **switch**. These are
  a "dry contact" — a plain on/off switch with **no polarity**, so it doesn't
  matter which output wire goes where.

On the **battery holder / pack**: **red** = + , **black** = −.
On the **laser**: **red** = + , **blue/black** = − (blue on the DTOL).

> **Check the slip.** If your slip shows the output as a **single** switched
> wire (not a pair), use that scheme instead: see the note at the end of Part 3.

---

## PART 3 — Wire it (twist + tape, no solder)

Strip ~5 mm of bare wire on each end. For every joint: hold the bare ends
together, twist them tightly, fold the twist over, and wrap it in tape.

**Test the laser first (30 seconds, saves the part):** touch the laser's
**red** wire to **+** and **blue/black** to **−** of a *single* AA (1.5 V). It
should glow faintly. This confirms the laser works **and** which wire is +/− —
reversed polarity at 4.5 V can kill the diode instantly and silently.

**Three taped joints:**

1. **Power + / feed the switch** — twist together three wires: battery **red
   (+)**, relay **red (power +)**, and **one relay output wire**. Tape.
2. **Switch → laser** — twist the relay's **other output wire** to the laser
   **red (+)**. Tape.
3. **Ground** — twist together three wires: battery **black (−)**, relay
   **black (power −)**, and laser **blue/black (−)**. Tape.

That's it. The laser now only gets power when the remote tells the relay to
connect its two output wires.

> **If your slip shows a single switched-output wire** (module outputs power
> itself, no separate pair): then — battery **red +** → relay **red**;
> battery **black −** → relay **black** + laser **−** (joint 3 above);
> relay **output wire** → laser **red +**. Two joints instead of three.

---

## PART 4 — Pair the remote and test

1. Put the 3 AA batteries in; switch power **ON**. The relay's LED lights.
2. Most kits are **pre-paired** — if not, the receiver has a small **"learn"
   button**: tap it, then press the remote once to pair (follow the slip).
3. Set the mode to **self-locking / toggle** (its learn button — the slip
   shows the tap pattern). One press on = next press off. Avoid **momentary**
   (laser only on while you hold the button).
4. **Point the laser at a wall or the floor — never at anyone.**
5. Press the remote. **Dot on.** Press again. **Dot off.** Walk across the
   room and try again — that's the wireless range.

---

## PART 5 — Make it tidy (optional)

- **Fast:** tuck the relay + battery pack into a small box or tin, with a hole
  for the laser to shine out one end. The remote stays in your pocket.
- **Nicer:** I can generate a small 3D-printable case (a slot for the battery
  pack, a window for the beam) — ask and I'll add it to
  [`../hardware/generate_stls.py`](../hardware/generate_stls.py).

---

## If it doesn't work

| Problem | Fix |
|---|---|
| Remote does nothing | Batteries in right way? Power ON? The remote has its own little battery (often a 12 V A23 or a coin) — check/replace it. |
| Laser never lights | Re-check the laser is in series through **both** output wires (joints 1 → 2). Re-do the single-AA test to confirm the laser + which wire is +/−. |
| Laser always on, remote won't turn it off | You're in **momentary** mode — switch the receiver to **self-locking / toggle** (Part 4, step 3). |
| A joint feels loose / intermittent | Re-twist tighter with more bare copper contact and re-tape, or use a WAGO connector. |
| Works only up close | The remote battery is weak, or something metal is blocking it — fresh remote battery and line-of-sight help. |
| Laser dim / flaky | A battery is low (use fresh alkalines, not NiMH), or a joint is gripping insulation not bare wire — strip back ~5 mm and re-twist. |
| Relay drains batteries overnight | Normal — it listens all the time. Flip the pack's switch (or pull a battery) when done. |

---

## SAFETY — read this

- It's a **5 mW class-3R** laser (cheap modules often run brighter — treat it
  as stronger). **Never aim it at anyone's eyes**, your own included, and
  never at pets' faces.
- Never point it at **mirrors, windows, glossy screens, or shiny metal** — a
  reflection can bounce into an eye.
- Because a stray remote press can light it when you're not looking, **aim the
  whole unit somewhere safe permanently** — dot on the floor or a target.
- Flip the master switch off (or pull a battery) when it's not in use,
  especially around kids.

---

## Want phone control later?

This is the no-code wireless build. If you ever want to drive it from your
phone instead of a remote, that's the Bluetooth version — same laser, plus a
tiny microcontroller: see [README.md](README.md) and [NOSOLDER.md](NOSOLDER.md).
