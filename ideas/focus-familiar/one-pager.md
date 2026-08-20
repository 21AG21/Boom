# Focus Familiar 🐣 — Deep-Dive One-Pager

> *Feed it your phone. It glows while you focus — and wilts the second you
> cave.*

Flagship #2 from the [Idea Vault](../README.md). A desk creature with a slot
in its belly: slide your phone in and it wakes up and glows and starts a
focus timer; pull the phone out early and it visibly **wilts** (head droops,
light fades). *Forest*, the focus app, turned into a physical companion
you'd feel guilty abandoning.

---

## Why it can be huge (the numbers)
The collectible engine underneath it is one of the biggest consumer stories
of the decade:

| Signal | Figure | Year |
|---|---|---|
| Pop Mart revenue | **RMB 37.1 B (~$5.4 B), +185% YoY** | 2025 |
| Labubu ("The Monsters") franchise alone | **RMB 14.2 B, +366% YoY** | 2025 |
| Global blind-box market | **~$14.7 B** | 2025 |

Focus Familiar marries that proven **collect-them-all** mania to a behavior
parents actively *want* to buy (put the phone down). Parents buy the first
one; the blind-box loop makes kids want the rest.

## Mechanism & BOM (volume tier)
The trick is a **cheap electronic "core" + interchangeable collectible
skins** — razor-and-blades.

- **Phone-presence sensing** — simplest & privacy-safe: a mechanical tact
  switch (or hall sensor + magnet) under the slot floor. No camera, no data.
- **Reaction** — one micro-servo for the head wilt/perk; a warm LED for the
  glow; a mechanical flip-timer or e-ink dot for the countdown.
- **Brain** — a $0.5–1 MCU (no radio needed); optional NFC tap to log streaks
  for kids who want gamification.
- **Power** — USB-powered desk object (drop the battery entirely) or a small
  LiPo.

| Part | COGS (volume) |
|---|---|
| Molded body + head linkage | $2.00 |
| Micro-servo | $1.50 |
| MCU + LED + phone-switch | $1.30 |
| Timer (flip or e-ink) | $1.00 |
| USB power / cable (no battery) | $0.60 |
| PCB, wiring, assembly | $2.20 |
| Blind-box packaging | $1.20 |
| **Core COGS** | **~$9.80** |
| Collectible **skin** (molded shell only) | **~$1.50** |

## Unit economics
| SKU | Retail | COGS | Gross margin |
|---|---|---:|---:|
| Base creature (core) | **$35** | $9.80 | **72%** |
| Blind-box skin / seasonal creature | **$11** | $1.50 | **86%** |
| Multipack (family/classroom) | $89 | ~$28 | 69% |

The base creature is the beachhead; **the profit is the endless $11 skins at
86% margin**, sold as blind-box drops with manufactured scarcity and "rares."

## Patent claim skeleton
- **Independent:** *A desk companion device whose expressive mechanical state
  (posture, illumination, and/or displayed timer) is driven by the continuous
  presence or absence of a stowed personal electronic device in a receptacle,
  and which transitions to a penalty state upon removal of the stowed device
  before a target interval elapses.*
- **Dependent:** the sensing modality (mechanical/hall/capacitive); the
  head-droop actuation; timer integration and completion animation; **a
  common electronic core accepting interchangeable decorative skins**; NFC
  streak logging; the early-removal "wilt" specifically as a negative
  reinforcement cue.
- *Design patents* on each creature form. The behavioral-penalty mechanic is
  the defensible core; the character IP is the durable moat (Pop Mart's real
  moat is characters, not tech).

## Go-to-market
- **Audiences:** parents-of-teens, students, the focus/productivity crowd, and
  designer-toy collectors.
- **Launch:** base creature + a first set of ~6 skins, with blind-box drops
  from day one.
- **Content:** the product films itself — "my focus creature wilted because I
  checked Instagram" is native short-video. Seed to study-tok and
  parenting creators.
- **Retail:** bookstores, stationery, gift, and toy — the same shelves
  Smiskis and Sonny Angels own.

## Risks & mitigations
| Risk | Mitigation |
|---|---|
| Existing phone-lockboxes / Brick / Unpluq / Forest | Differentiate on *emotional companion + collectible loop*, not on locking; those are utilities, this is a character you bond with |
| Commoditization / knockoffs | Character IP + design patents + blind-box scarcity (the Pop Mart playbook) |
| Screen-time efficacy skepticism | Keep it playful, not clinical — a nudge and a companion, not a therapeutic claim |
| Single-IP dependence (Pop Mart's own stumble) | Launch a *family* of creatures; don't bet the brand on one character |

## First build (this week)
A cardboard-and-servo puppet whose head droops when a magnet leaves a slot.
If it makes *you* not want to grab your phone, build the cute version. Reuse
the servo + sine-easing patterns from the Breathe Stone firmware for the
wilt/perk motion.

---
**Fidget score:** ●●●●○ · Biggest upside of the three flagships, most
competition. The vault's recommendation: film Seed Fidget for reach, build
Breathe Stone first, and let Focus Familiar be the swing.
