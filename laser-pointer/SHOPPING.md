# LASER-POINTER — shopping list

Everything for the Bluetooth on/off laser. It's short now — no servos, no
bracket. Prices are rough (Amazon/AliExpress); multipacks are cheaper per
unit.

## Required

| # | Part | Buy this (example) | ~Price | Notes |
|---|---|---|---|---|
| 1 | **ESP32-C3 SuperMini** (get *pre-soldered pins*) | [3-pack, pins pre-soldered](https://www.amazon.com/ESP32-C3-Development-Supermini-Bluetooth-Pre-Soldered/dp/B0F12JS872) | $4 | The brain + Bluetooth LE + USB-C. Pre-soldered = no iron needed. |
| 2 | **KY-008 laser module** (3-pack) | [KY-008 3-pack](https://www.amazon.com/KY-008-650nm-Sensor-Module-Arduino/dp/B0786BLLXD) | $2 | The 5 mW red dot. |
| 3 | **Momentary pushbutton** | search **"tactile push button kit 12mm"** | ~$0 | Any normally-open button. Assortment packs are cheapest. |
| 4 | **Breadboard + jumper wires** | [4 boards + M-M/F-M/F-F wires](https://www.amazon.com/Solderless-Breadboard-Boards-Flexible-Jumper/dp/B0GVD11LSS) | $2 | Connect everything, no soldering. |
| — | **USB-C cable** | you own one | — | Power + flashing. |

**Subtotal: ~$8.**

> **Cheaper/simpler alternative:** an "Arduino starter kit" (~$25) bundles
> the breadboard, jumper wires, buttons, LEDs, and resistors in one box —
> then you only add the ESP32-C3 and the KY-008 laser.

## Optional

| Part | Search | ~Price | Notes |
|---|---|---|---|
| Green LED + 220Ω resistor | "5mm green LED" / "220 ohm resistor" | ~$0 | Status light (on = laser on). The build works fine without it. |

## Compact build (Tier B — thumbnail size)

Swaps for shrinking it down; see [COMPACT.md](COMPACT.md) for the full
plan, sizes, and deep-sleep runtime math.

| Part | Search | ~Price | Notes |
|---|---|---|---|
| **Bare 6 mm laser diode** | "6mm 650nm 5mW laser diode module" | $1 | Replaces the KY-008 board. **Add a ~100 Ω resistor** in series (the KY-008 had one built in). |
| **~100 Ω resistor** | "100 ohm resistor" | ~$0 | In series with the bare diode — don't skip it. |
| **SMD tactile button** | "2x4mm SMD tactile switch" | ~$0 | Tiny replacement for the through-hole button. |
| **100 mAh slim LiPo** *or* **LIR2032 coin + holder** | "401220 lipo 100mah" / "LIR2032 rechargeable + holder" | $3–5 | LiPo = best runtime; coin = flattest. Both feed the 3.7 V board directly, no booster. |
| **TP4056 USB-C** (if recharging in place) | "TP4056 Type-C" | $1 | ~26 × 17 mm, so it sits beside the MCU. Skip it and swap/charge the cell externally to stay smallest. |

Deep sleep (~10 µA idle) is already in the firmware, so even the little
coin cell lasts months of standby.

## If you want it cordless (optional, later)

| Part | Search | ~Price | Notes |
|---|---|---|---|
| TP4056 USB-C charge board | "TP4056 Type-C" | $1 | Charging + battery protection. |
| 3.7 V LiPo, 300–500 mAh | "3.7v lipo 502030" | $5 | No motors here, so even a tiny cell lasts a long time. |
| Slide switch | "mini slide switch SS12D00" | ~$0 | Hard on/off for the battery. |

The board runs happily on 3.7 V, so unlike the motorized version you do
**not** need a 5 V booster — the LiPo can feed it directly.

## Control app — nothing to buy

The phone/laptop remote is [`app/laser-remote.html`](app/laser-remote.html)
in this repo — open it in Chrome/Edge. On iPhone, get the free **Bluefy**
browser (App Store), or use the free **nRF Connect** app with the text
commands in the README.

## Tools

- Arduino IDE (free) to flash the firmware.
- Nothing else for a breadboard build. (Soldering iron only if you later
  make it permanent — about 3 joints.)

---

**Bottom line:** ESP32-C3 + KY-008 laser + a button + a breadboard ≈ **$8**,
plus a USB-C cable you already own.
