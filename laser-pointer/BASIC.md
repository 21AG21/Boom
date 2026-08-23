# LASER-POINTER — the basic wireless button build (~$13, no code, no solder)

A laser dot you toggle from across the room with a **physical button on a
little wireless remote**. **No microcontroller, no phone, no app, no code,
and no soldering.** Nothing hidden — it's a laser plugged into a wireless
relay, sitting out in the open.

It works with a ready-made **433 MHz RF relay kit**: a remote (the button)
and a matchbox-size **receiver** with a relay in it. The laser and battery
screw into the receiver. Press the remote → the relay closes the circuit →
the laser lights. Press again → off.

```
   your hand                     across the room
  ┌──────────┐   433 MHz radio   ┌───────────────────────────────┐
  │  remote  │ ) ) ) ) ) ) ) ) ) │  receiver + relay             │
  │ (button) │                   │   battery ─┬─ VCC     COM ─┐   │
  └──────────┘                   │            │  (jumper)     │   │
                                 │   battery +─┴─ COM     NO ─┼─ laser +
                                 │   battery − ── GND ────────┴─ laser −
                                 └───────────────────────────────┘
   press remote → relay COM–NO closes → battery reaches the laser → dot on
```

Build time once parts arrive: **~10 minutes** with a small screwdriver.

---

## PART 1 — What to buy (~$13, two things + AAs you already have)

The relay receiver has **screw terminals**, so wires clamp down with a
screwdriver — no soldering. You reuse AA batteries you already own.

| # | Thing | Buy this | What to check |
|---|---|---|---|
| 1 | **433 MHz RF relay + remote kit** (1 channel) | [DC 3.7–12 V mini latching relay + remote — B08D3GXXQ1](https://www.amazon.com/DC-3-7V-Wireless-Latching-Transmitter/dp/B08D3GXXQ1) · alt: [B077ZQMQDZ](https://www.amazon.com/Wireless-Control-Controller-Receiver-Transmitter/dp/B077ZQMQDZ) | Listing must literally say **DC 3.7–12 V** (so 4.5 V works) and **latching / self-locking** — **NOT** 12 V-only, **NOT** momentary-only. ~$7 |
| 2 | **Red laser module, 5 mW, with leads** | [farhop 650 nm 5 mW 3 V, 5-pack — B00VCR036Q](https://www.amazon.com/farhop-650nm-Laser-Diode-Module/dp/B00VCR036Q) · or [HiLetgo 10-pack — B071FT9HSV](https://www.amazon.com/HiLetgo-10pcs-650nm-Diode-Laser/dp/B071FT9HSV) | 3–5 V, red (+) / black (−) wires, built-in driver — **no resistor needed.** ~$6 |
| — | **3 × AA batteries** | you already have these | Fresh **alkaline** (not rechargeable — NiMH's 3.6 V is too low to click the relay). |

**Total: about $13.** Only need a battery holder if you don't own one:
[3×AA holder w/ switch — B0C5M9XGGV](https://www.amazon.com/Jstincal-Battery-Holder-4-5-5V-3%C3%971-5V/dp/B0C5M9XGGV) (~$5).

> **Why 4.5 V (3×AA):** it's inside the laser's 3–5 V range *and* inside
> this relay's 3.7–12 V range, so one battery pack safely runs both. Don't
> use 6 V (4×AA) — that can over-drive a 5 V laser.

> **Cheaper if you can wait:** the same relay is ~$3 and the laser ~$1 on
> AliExpress/eBay (2–3 week shipping), bringing the whole build near **$6**.
> On Prime, ~$13 is the honest floor — the relay kit alone is ~$7 and it's
> the one part you can't cheap out on.

> **One button or two:** set the receiver to **latching / self-locking** and
> one button turns the laser on/off. (Some kits also offer a **two-button**
> latched mode — one on, one off.) Avoid **momentary** mode, where the laser
> is only on while you hold the button.

---

## PART 2 — Identify the terminals

On the **receiver** you'll have two little screw-terminal blocks:

- **Power in:** **VCC / +** and **GND / −** — powers the receiver.
- **Relay out:** **COM**, **NO**, **NC** — the switch contacts. You use
  **COM** and **NO** ("normally open" = open until the remote closes it).

On the **battery holder / pack**: **red** = + , **black** = −.
On the **laser**: **red** = + , **black/blue** = −.

---

## PART 3 — Wire it (all screw terminals, no solder)

Strip ~5 mm of bare wire, loosen each screw, slip the wire in, tighten.
Five connections:

1. Battery **red (+)** → receiver **VCC**.
2. Battery **black (−)** → receiver **GND**.
3. A short jumper wire from **VCC → COM** (so battery + also feeds the
   relay's common contact). *Many boards bridge this internally — check the
   wiring slip; if it's already bridged, skip this wire.*
4. Laser **red (+)** → receiver **NO**.
5. Laser **black/blue (−)** → receiver **GND** (same terminal as the battery
   −; twist the two − wires together and clamp them in together).

Now the laser only gets power when the remote tells the relay to connect
COM→NO.

> **Test the laser first (30 seconds, saves the part):** touch the laser's
> red wire to **+** and black to **−** of a *single* AA (1.5 V) before wiring
> anything. It should glow faintly. This confirms the laser works **and**
> which wire is +/− — reversed polarity at 4.5 V can kill the diode
> instantly and silently.

---

## PART 4 — Pair the remote and test

1. Put the 3 AA batteries in; switch power **ON**. The receiver's LED lights.
2. Most kits are **pre-paired** — if not, the receiver has a small **"learn"
   button**: tap it, then press the remote button once to pair (one tap;
   follow the kit's slip of paper).
3. Set the mode to **latching / self-locking** (its learn button — the slip
   shows the tap pattern). One press on = next press off.
4. **Point the laser at a wall or the floor — never at anyone.**
5. Press the remote. **Dot on.** Press again. **Dot off.** Walk across the
   room and try again — that's the wireless range.

---

## PART 5 — Make it tidy (optional)

- **Fast:** tuck the receiver + battery pack into a small box or tin, with a
  hole for the laser to shine out one end. The remote stays in your pocket.
- **Nicer:** I can generate a small 3D-printable case (a slot for the
  battery pack, a window for the beam) — ask and I'll add it to
  [`../hardware/generate_stls.py`](../hardware/generate_stls.py).

---

## If it doesn't work

| Problem | Fix |
|---|---|
| Remote does nothing | Batteries in right way? Power ON? The remote has its own little battery (often a 12 V A23 or a coin) — check/replace it. |
| Laser never lights | You may be on **NC** instead of **NO** — move the laser + wire to **NO**. Also confirm the VCC→COM jumper (step 3). |
| Laser always on, remote won't turn it off | You're likely in **momentary** mode or wired to **NC**. Switch the receiver to **latching** and use **NO**. |
| Works only up close | The remote battery is weak, or something metal is blocking it — fresh remote battery and line-of-sight help. |
| Laser dim / flaky | A battery is low (use fresh alkalines, not NiMH), or a screw terminal is gripping insulation not bare wire — strip back ~5 mm and re-clamp. |
| Receiver drains batteries overnight | Normal — it listens all the time. Flip the pack's switch (or pull a battery) when done. |

---

## SAFETY — read this

- It's a **5 mW class-3R** laser (cheap modules often run brighter — treat
  it as stronger). **Never aim it at anyone's eyes**, your own included, and
  never at pets' faces.
- Never point it at **mirrors, windows, glossy screens, or shiny metal** — a
  reflection can bounce into an eye.
- Because a stray remote press can light it when you're not looking, **aim
  the whole unit somewhere safe permanently** — dot on the floor or a target.
- Flip the master switch off (or pull a battery) when it's not in use,
  especially around kids.

---

## Want phone control later?

This is the no-code wireless build. If you ever want to drive it from your
phone instead of a remote, that's the Bluetooth version — same laser, plus a
tiny microcontroller: see [README.md](README.md) and [NOSOLDER.md](NOSOLDER.md).
