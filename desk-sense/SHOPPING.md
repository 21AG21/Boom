# DESK-SENSE — shopping list

Everything you need for the bit box. Prices are rough (AliExpress/Amazon,
mid-2020s); buying multipacks is usually cheaper per unit.

## Required

| # | Part | What to search for | ~Price | Notes |
|---|---|---|---|---|
| 1 | **ESP32-C3 SuperMini** | "ESP32-C3 SuperMini" | $4 | The brain. USB-C on board. Any ESP32-C3 dev board works if pins differ. |
| 1 | **BME280 sensor board** | "BME280 module I2C" | $3 | Temp + humidity + pressure. Make sure it's **BME**280 (humidity), not **BMP**280 (no humidity). |
| 1 | **0.96" OLED, I2C, SSD1306** | "0.96 OLED I2C SSD1306 128x64" | $3 | 4-pin (VCC/GND/SDA/SCL) version. White or blue, your call. |
| 1 | **Green LED (5mm or 3mm)** | "5mm green LED" | ~$0 | Any color; green sells the "official" look. |
| 1 | **220–330Ω resistor** | "220 ohm resistor" | ~$0 | Current-limits the LED. |
| — | **Jumper wires** | "dupont jumper wires female-female" | $2 | For a no-solder breadboard build. |
| 1 | **USB-C cable** | you already own one | — | Power + flashing. |

**Subtotal: ~$12–14.**

## If you want it solid (recommended)

| Part | Search | ~Price | Notes |
|---|---|---|---|
| Small perfboard **or** mini breadboard | "mini breadboard 170" / "perfboard 4x6cm" | $1–2 | Breadboard = zero solder. Perfboard = permanent. |
| Solder + iron | — | — | ~6 joints if you go permanent. Borrow one if you don't have it. |

## If you want it cordless (optional)

Reuse the exact battery setup from the other builds in this repo:

| Part | Search | ~Price | Notes |
|---|---|---|---|
| TP4056 USB-C charge board | "TP4056 Type-C" | $1 | Charging + battery protection. |
| 3.7V LiPo, 500–1000 mAh | "3.7v lipo 502030" | $6 | No servos/radio here, so even a small cell lasts days. |
| Slide switch | "mini slide switch SS12D00" | ~$0 | On/off. |

## Enclosure (optional — you can run it bare on the desk)

- **3D printed:** use `sense_case.stl` + `sense_lid.stl` already in this
  repo ([`../hardware/stl/`](../hardware/stl/)) and open the front window
  to frame the OLED (~26 × 15 mm). No printer? Any online print service
  takes the STL as-is.
- **No printer, no service:** a small project box, an Altoids-style tin,
  or even a folded cardstock shell all work. It's a desk gag, not a
  spacecraft.

## Tools

- Arduino IDE (free) to flash the firmware.
- A wire stripper / small screwdriver is handy but not required for the
  breadboard version.

---

**Bottom line:** the three required chips (ESP32-C3, BME280, SSD1306) plus
an LED and a resistor. If you have a junk drawer with jumper wires and a
USB-C cable, you're looking at about **$10 of new parts**.
