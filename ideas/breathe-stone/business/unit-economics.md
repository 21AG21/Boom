# Breathe Stone — Unit Economics

All component figures are grounded in the August 2026 market-research pass
(sources at the bottom). Where a figure is a bulk-quote estimate it is
marked **[est]** — get real LCSC/Alibaba quotes before committing a costing
model. Currency is USD.

## The market it sits in

| Market | Size | Year | Why it matters |
|---|---|---|---|
| Global fidget-toy market | ~$8–9 B | 2024–25 | The impulse-object channel; grows ~6–8%/yr |
| Fidget-spinner craze **peak** | ~$2.2 B, ~300 M units | 2017 | The upside case — a single simple object can go vertical |
| Anxiety/depression **app** segment | ~$2.4 B | 2025 | Proves people pay to self-regulate anxiety |
| Digital mental-health market | ~$24–28 B → ~$59 B by 2030 (16% CAGR) | 2025 | The tailwind Breathe Stone rides *against* (anti-app) |

**The incumbent that de-risks demand: Moonbird.** A handheld silicone device
that expands/contracts in the hand to pace breathing, retailing **~$199**
(street $150–229), no subscription. It proves a real market exists for a
*handheld tactile breathing pacer*. Breathe Stone's whole strategy is to
take that proven demand and win on **price (⅕ the cost), form (an
everyday-carry stone, not a gadget), and channels Moonbird can't reach
(bulk/institutional).**

## Bill of materials — three build tiers

### Tier A — Maker / crowdfunding pilot (first ~500 units, 3D-printed)
Purpose: validate and film, not to make margin.

| Part | Cost | Note |
|---|---|---|
| Printed shell set (base, lid, piston, crank) | $4.00 | filament + machine time, this repo's STLs |
| Dome (printed TPU or cast silicone) | $1.50 | |
| MG90S micro servo | $3.00 | metal-gear, quieter; retail small-qty |
| ESP32-C3 SuperMini | $3.00 | |
| LiPo 300 mAh | $5.00 | |
| TP4056 USB-C charge board | $1.00 | |
| Button, slide switch, wires, screws, ballast washers | $2.00 | |
| Packaging + insert card | $1.50 | |
| **COGS (materials)** | **~$21** | + your assembly labor (~15 min/unit) |

At a **$39** pilot price this is thin but positive; the pilot's job is proof,
not profit.

### Tier B — Tooled electronic version (5k+ units)

| Part | Cost | Note |
|---|---|---|
| Injection-molded shell set | $1.50 | amortized; tooling ~$10–15k one-time **[est]** |
| Cast silicone dome | $0.50 | **[est]** |
| Coreless/MG90-class actuator | $2.00 | bulk **[est]** |
| MCU (ESP32-C3-class, or a $0.5 no-radio MCU) | $1.00 | drop Wi-Fi to cut cost |
| LiPo | $2.00 | bulk **[est]** |
| Charge circuit (TP4056-class) | $0.40 | |
| Button/PCB/misc/ballast | $1.50 | |
| Contract assembly | $2.00 | **[est]** |
| Packaging | $1.00 | |
| **Landed COGS** | **~$12** | |

### Tier C — Battery-free kinetic version (the bulk / B2B hero)
No electronics: molded shells + a wound spring and escapement drive the pad.

| Part | Cost | Note |
|---|---|---|
| Molded shells | $1.50 | |
| Spring + molded escapement/governor | $1.00 | **[est]** |
| Silicone dome | $0.50 | |
| Ballast + assembly + packaging | $2.00 | |
| **Landed COGS** | **~$5** | and it never needs charging |

## Pricing & margin

| Version | Retail (DTC) | COGS | DTC gross margin | Wholesale (keystone) | Wholesale margin |
|---|---|---:|---:|---:|---:|
| Electronic (Tier B) | **$34** | $12 | **65%** | $17 | 29% |
| Kinetic (Tier C) | **$14** | $5 | **64%** | $7 | 29% |
| vs. Moonbird | $199 | — | — | — | — |

Keystone wholesale margins are thin on purpose — the model leans **DTC +
B2B**, using retail wholesale mainly for reach/brand. To lift wholesale
margin, drive electronic COGS under $9 (drop the radio, integrate the PCB) or
lead with the kinetic version in bulk channels.

## Revenue model (four legs)

1. **DTC** (Shopify + Amazon) — $34 electronic / $14 kinetic, ~64% margin.
   The core.
2. **Retail wholesale** — gift shops, pharmacies, museum & bookstore counters,
   airport shops. Reach and impulse placement.
3. **B2B / institutional (the differentiator)** — the kinetic **Calm Kit**:
   airlines (fear-of-flying kits), ER & dental waiting rooms, therapists &
   school counselors, DMV-style waiting areas. Volume, low-touch, reorders.
   Moonbird at $199 structurally cannot serve this; a $5-COGS kinetic stone
   can.
4. **Restock loop** — seasonal/collectible silicone dome "skins," scented
   domes, a weighted "night" edition, a kids edition. Gift-driven Q4 spikes.

## Break-even (illustrative, electronic Tier B)

- One-time: tooling ~$12k **[est]** + provisional patent $65 + first
  inventory.
- Contribution per DTC unit: $34 − $12 = **$22**.
- Tooling break-even ≈ **~550 units** of contribution (before marketing/CAC).
- Practical path: a crowdfunding pre-sale of **1,000–2,000 units** funds the
  tooling and the first production run before you spend on inventory at risk.

## TAM / SAM / SOM (kept honest)

- **TAM** — anti-screen tactile wellness + impulse comfort objects, a slice of
  the ~$8–9 B fidget market plus the anxiety-self-care spend. Large and
  growing.
- **SAM** — handheld tactile breathing/anxiety objects. Small today but
  *proven* — Moonbird sells into it at $199. A cheaper, broader-form entrant
  expands it.
- **SOM (3-yr, conservative)** — even **0.02–0.05%** of the fidget market is
  **$1.6–4 M/yr** in revenue: a healthy small business at 60% margins. The
  **upside case** is the spinner's own history — the right object at the
  right moment did $2.2 B. Underwrite the base case; keep the option on the
  breakout.

## What kills the margin (watch these)

- **Actuator noise** forcing an expensive quiet actuator — mitigated by the
  silent-hold firmware and/or the kinetic version.
- **CAC** on DTC — mitigate with organic short-video reach (the product films
  itself) and B2B where CAC is a sales conversation, not ad spend.
- **Knockoffs** — the spinner got commoditized in months. Defenses: the
  provisional/design IP, brand, B2B contracts, and the collectible restock
  loop that a generic copy can't replicate.

---

### Sources (2026 research pass)
Fidget market — Fortune Business Insights, Cognitive Market Research,
SkyQuest. Spinner peak — Business of Business / Accio. App & digital
mental-health — GM Insights, The Business Research Company. Moonbird price —
PureWow / Cybernews / Tom's Guide (street $150–229; ~$199 most-cited).
Components — ProtoSupplies, SparkFun, Adafruit, Tinkersphere, AliExpress
wiki, Alibaba. Provisional fee — USPTO 2026 schedule ($65 micro-entity). Full
URLs are in the research appendix of the founder's brief.
