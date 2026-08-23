# LASER-POINTER — the basic wireless button build (no code)

A laser dot you toggle from across the room with a **physical button on a
little wireless remote**. **No microcontroller, no phone, no app, no code,
and no soldering.** Nothing hidden — it's a laser plugged into a wireless
relay, sitting out in the open.

It works with a ready-made **433 MHz RF remote kit**: a keyfob (the button)
and a matchbox-size **receiver** with a relay in it. The laser and battery
screw into the receiver. Press the fob → the relay closes the circuit →
the laser lights. Press again → off.

```
   your hand                     across the room
  ┌──────────┐   433 MHz radio   ┌───────────────────────────────┐
  │  keyfob  │ ) ) ) ) ) ) ) ) ) │  receiver + relay             │
  │ (button) │                   │   battery ─┬─ COM      NO ─ laser +
  └──────────┘                   │            └─ powers receiver │
                                 │   battery − ── GND ── laser − │
                                 └───────────────────────────────┘
   press fob → relay COM–NO closes → battery reaches the laser → dot on
```

Build time once parts arrive: **~15 minutes** with a small screwdriver.

---

## PART 1 — What to buy

Three things plus batteries. The relay receiver has **screw terminals**,
so wires clamp down with a screwdriver — no soldering.

| # | Thing | Buy this (example) | What to check |
|---|---|---|---|
| 1 | **433 MHz RF relay + keyfob kit** (1 channel) | [DieseRC 5/12/24 V RF relay, 2 keyfobs, dry contacts](https://www.amazon.com/DieseRC-Wireless-Transmitters-Potential-Free-Controller/dp/B0B19N81RD) — or [mini 3.5–12 V, momentary/**toggle**/latched](https://www.amazon.com/DC-3-7V-Wireless-Momentary-Transmitter/dp/B08F7CTDWT) | Must run at **~5 V or "wide voltage 3.5–12 V"** — **NOT** a 12 V-only unit. Wants a **toggle** or separate **on/off** mode. |
| 2 | **Red laser module, 5 mW, with wire leads** | [HiLetgo 650 nm 5 mW dot, with leads (10-pack)](https://www.amazon.com/HiLetgo-10pcs-650nm-Diode-Laser/dp/B071FT9HSV) | 3–5 V, has red (+) / black (−) wires and a built-in driver — **no resistor needed.** |
| 3 | **3 × AA battery holder with leads + switch** | [Raogoodcx 3×AA (4.5 V) holder w/ leads & switch](https://www.amazon.com/Raogoodcx-Battery-Holder-Bundle-Switch/dp/B0C28CZC8P) | 4.5 V suits both the receiver and the laser. Its own slide switch is a handy master power cut-off. |
| — | **3 × AA batteries** | any store | — |

**Cost: about $18.** (If your relay module has bare wire ends instead of
screw terminals, grab a few **"Wago 221 lever connectors"** too, for
no-solder joins.)

> **Why 4.5 V (3×AA):** it's inside the laser's 3–5 V range *and* inside
> the receiver's range, so one battery pack safely runs both. Don't use
> 6 V (4×AA) — that can over-drive a 5 V laser.

> **One button or two:** most fobs have several buttons. Set the receiver
> to **toggle** mode and one button turns the laser on/off. Or use
> **latched** mode with two buttons — one on, one off. Both are just
> physical buttons; pick whichever the kit makes easy.

---

## PART 2 — Identify the terminals

On the **receiver** you'll have screw terminals labeled roughly:

- **VCC / +** and **GND / −** — power for the receiver.
- **COM**, **NO**, **NC** — the relay's switch contacts. You use **COM**
  and **NO** ("normally open" = open until the fob closes it).

On the **battery holder**: **red** = + , **black** = −.
On the **laser**: **red** = + , **black/blue** = −.

---

## PART 3 — Wire it (all screw terminals, no solder)

Loosen each screw, slip the bare wire end in, tighten. Five connections:

1. Battery **red (+)** → receiver **VCC**.
2. Battery **black (−)** → receiver **GND**.
3. A short jumper wire from **VCC → COM** (so the battery + also feeds the
   relay's common contact). *(Some kits bridge this internally — check
   their wiring picture; if so, skip this.)*
4. Laser **red (+)** → receiver **NO**.
5. Laser **black/blue (−)** → receiver **GND** (same terminal as the
   battery −; twist the two − wires together into it, or use a lever
   connector).

Now the laser only gets power when the fob tells the relay to connect
COM→NO.

---

## PART 4 — Pair the fob and test

1. Put the 3 AA batteries in the holder; switch the holder's slide switch
   **ON**.
2. Most kits are **pre-paired** — if not, the receiver has a small
   **"learn" button**: tap it, then press the fob button once to pair
   (follow the kit's slip of paper; it's one tap).
3. Set the mode if there's a jumper/button for it: **toggle** for
   one-button on/off.
4. **Point the laser at a wall or the floor — never at anyone.**
5. Press the fob. **Dot on.** Press again. **Dot off.** Walk across the
   room and try again — that's the wireless range.

---

## PART 5 — Make it tidy (optional)

- **Fast:** tuck the receiver + battery box into a small box or tin, with a
  hole for the laser to shine out one end. The fob stays loose in your
  pocket.
- **Nicer:** I can generate a small 3D-printable case (a slot for the
  battery box, a window for the beam) — ask and I'll add it to
  [`../hardware/generate_stls.py`](../hardware/generate_stls.py).

---

## If it doesn't work

| Problem | Fix |
|---|---|
| Fob does nothing | Batteries in right way? Holder switch ON? The fob has its own little battery (often a 12 V A23 or a coin) — check/replace it. |
| Laser never lights | You may be on **NC** instead of **NO** — move the laser + wire to **NO**. Also confirm the VCC→COM jumper (step 3). |
| Laser is always on, fob won't turn it off | You're likely in **momentary** or wired to **NC**. Switch the receiver to **toggle** mode and use **NO**. |
| Works only up close | The fob battery is weak, or something metal is blocking it — fresh fob battery and line-of-sight help. |
| Laser dim | A battery is low, or a screw terminal is gripping insulation not bare wire — strip back ~5 mm and re-clamp. |
| Receiver drains batteries overnight | Normal — the receiver listens all the time. Flip the holder's slide switch OFF when you're done. |

---

## SAFETY — read this

- It's a **5 mW class-3R** laser. **Never aim it at anyone's eyes**, your
  own included, and never at pets' faces.
- Never point it at **mirrors, windows, glossy screens, or shiny metal** —
  a reflection can bounce into an eye.
- Keep the dot on the **floor, walls, or a target** — treat it like the
  laser pointer it is.
- Flip the master switch off (or pull a battery) when it's not in use,
  especially around kids.

---

## Want phone control later?

This is the no-code wireless build. If you ever want to drive it from your
phone instead of a fob, that's the Bluetooth version — same laser, plus a
tiny microcontroller: see [README.md](README.md) and [NOSOLDER.md](NOSOLDER.md).
