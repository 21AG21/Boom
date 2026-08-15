# LASER-POINTER — shopping list

Everything for the Bluetooth pan/tilt laser pointer. Prices are rough
(AliExpress/Amazon); multipacks are cheaper per unit.

## Required

| # | Part | Search for | ~Price | Notes |
|---|---|---|---|---|
| 1 | **ESP32-C3 SuperMini** | "ESP32-C3 SuperMini" | $4 | The brain. Has Bluetooth LE + USB-C on board. |
| 2 | **SG90 or MG90S micro servo** | "MG90S metal gear servo" | $3 ea | One for pan, one for tilt. MG90S (metal gear) is quieter and sturdier — worth it. |
| 1 | **Pan-tilt servo bracket kit** | "SG90 pan tilt bracket" | $2 | The little 2-servo gimbal. Or print `pouch_tilt_bracket` from this repo. |
| 1 | **5 mW red laser module (KY-008)** | "KY-008 laser module" | $2 | 6 mm diode on a 3-pin board. Class-3R. |
| 1 | **Momentary pushbutton** | "6x6 tactile pushbutton" or "12mm momentary button" | ~$0 | The physical laser/patrol button. Any normally-open button. |
| 1 | **Green LED + 220Ω resistor** | "5mm green LED" / "220 ohm resistor" | ~$0 | Optional status light. |
| — | **Jumper wires** | "dupont jumper wires" | $2 | Female-female for a no-solder prototype. |
| 1 | **USB-C cable** | you own one | — | Power + flashing. |

**Subtotal: ~$13–15.**

## Power — pick one

Two micro servos can spike more current than the ESP32-C3's 3V3 pin
likes, so give them a proper 5V source.

| Option | Parts | ~Price | Notes |
|---|---|---|---|
| **Tethered (simplest)** | a 5V USB-C wall charger / power bank | you own one | Feed 5V to the servo rail and the board's 5V pin. Zero extra parts. |
| **Cordless** | TP4056 USB-C charger + 3.7V LiPo (1000 mAh) + a small **5V boost or 5V BEC** + slide switch | ~$8 | LiPo is 3.7V; servos want ~5V, so add a tiny boost converter. Same battery parts as the other builds in this repo, plus the booster. |

If you only ever run it plugged in, skip the whole cordless row.

## Control app — nothing to buy

The phone/computer remote is [`app/laser-remote.html`](app/laser-remote.html)
in this repo — just open it in Chrome/Edge. On iPhone you'll want the free
**Bluefy** browser (App Store) since Safari can't do Web Bluetooth, or use
the free **nRF Connect** app with the text commands in the README.

## Tools

- Arduino IDE (free) to flash firmware.
- Soldering iron for the permanent build (~8 joints). Breadboard/jumpers
  work for prototyping with no solder.
- Small screwdriver for the servo bracket.

## Enclosure (optional)

It's a visible desk toy, so it doesn't need a case — the bare pan-tilt
bracket on a small base is fine. If you want a printed open stand, reuse
`pouch_tilt_bracket.stl` + `laser_clip.stl` from
[`../hardware/stl/`](../hardware/stl/), or ask and I'll generate a
dedicated `pointer_base` with a button hole and USB-C notch.

---

**Bottom line:** ESP32-C3 + two micro servos + a pan/tilt bracket + a
KY-008 laser + a pushbutton ≈ **$15**, plus a USB charger you already own.
