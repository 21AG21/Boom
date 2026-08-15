# LASER-POINTER — Bluetooth pan/tilt laser pointer

A visible desk toy / cat toy: a little pan-tilt laser you aim from your
phone or computer over Bluetooth, with a physical button on the device
itself. It sits out in the open — obviously yours, nothing hidden.

- **Bluetooth (BLE)** control — no WiFi, no accounts, no internet.
- **Phone or computer app** — a single HTML file with a joystick pad.
- **Physical button** — short press toggles the laser, long press starts
  patrol, so it works with no phone at all.
- **Patrol mode** — slow random drifts and pauses; good cat entertainment.
- **Firmware tilt clamp** — the beam physically can't rise above a set
  angle, keeping the dot low. It's a toy, not something to point at people.

```
   phone / laptop                 ESP32-C3                servos + laser
  ┌───────────────┐   BLE (NUS)  ┌──────────┐   GPIO     ┌────────────┐
  │ laser-remote  │ ───────────► │ firmware │ ─────────► │ pan / tilt │
  │  joystick UI  │ ◄─────────── │ (NimBLE) │            │  + diode   │
  └───────────────┘   "ok"       └────┬─────┘            └────────────┘
                                       │ GPIO10
                                  [ push button ]  short=laser  long=patrol
```

## Parts

See [SHOPPING.md](SHOPPING.md) — about **$15**. Servos, an ESP32-C3, a
laser module, a pushbutton, and a battery if you want it cordless.

## 1. Wire it

```
  ESP32-C3 SuperMini
  ------------------
  GPIO2  ──► pan servo   signal (orange)
  GPIO3  ──► tilt servo  signal (orange)
  GPIO4  ──► laser module signal (S / +)
  GPIO5  ──► status LED  (optional, via 220Ω to GND)
  GPIO10 ──► pushbutton ──► GND      (other button leg)
  5V     ──► servo V+  ·  laser V+
  GND    ──► servo GND · laser GND · button · LED

  Servos are happiest on a real 5V supply (USB 5V or a 5V BEC). Powering
  two servos straight off the C3's 3V3 pin will brown it out — use the 5V
  rail / battery path in SHOPPING.md.
```

The pushbutton is just a momentary switch from GPIO10 to GND; the chip's
internal pull-up does the rest (no resistor needed).

## 2. Flash the firmware

Open [`firmware/laserpointer/laserpointer.ino`](firmware/laserpointer/laserpointer.ino)
in the Arduino IDE.

1. Board: **ESP32C3 Dev Module** (install the "esp32" boards package).
2. Libraries (Library Manager): **ESP32Servo** and **NimBLE-Arduino**.
3. Plug in over USB-C, Upload.

On boot it advertises as **`LASER-PT`** over Bluetooth LE.

## 3. Control it

### Option A — the app (recommended)

Open [`app/laser-remote.html`](app/laser-remote.html) in a browser and hit
**Connect**. You get a joystick pad, Laser / Patrol / Center buttons, and a
big "Laser off + park".

| Platform | Browser that works |
|---|---|
| Windows / Mac / Linux | **Chrome** or **Edge** |
| Android | **Chrome** |
| iPhone / iPad | Safari/iOS-Chrome do **not** support Web Bluetooth — use the **Bluefy** browser app, or Option B |

Easiest way to get it on your phone: push this repo and open the file via
GitHub Pages, or just email/AirDrop the single HTML file to yourself.

### Option B — any BLE terminal app

No install of ours needed. Use **nRF Connect** (iOS/Android) or **Serial
Bluetooth Terminal** (Android, BLE mode), connect to `LASER-PT`, and send
these text commands to the Nordic UART RX characteristic:

| Command | Does |
|---|---|
| `P50` | pan to 50% of travel (center) |
| `T30` | tilt to 30% of travel |
| `J50,80` | joystick: pan 50%, tilt 80% |
| `L1` / `L0` | laser on / off |
| `M1` / `M0` | patrol on / off |
| `X` | everything off + park level |

### Option C — the physical button

No phone at all: **short press** toggles the laser, **long press (>0.6 s)**
toggles patrol mode.

## 4. Tune it

Everything adjustable is at the top of the `.ino`:

- `TILT_MAX` — the safety ceiling. Lower it until the highest the beam
  ever points is still safely below eye level for where the toy sits.
- `PAN_MIN` / `PAN_MAX` — how far it sweeps left/right.
- `EASE` — motion smoothness (smaller = slower, smoother).
- `BLE_NAME` — rename the device if you build more than one.

## Enclosure

Reuse the visible pan-tilt hardware already in this repo
([`../hardware/stl/`](../hardware/stl/)): `pouch_tilt_bracket` +
`laser_clip` carry the servo and diode. Mount them on any small base or
in the pouch chassis — no need for a disguise, it's a desk toy. If you
want a purpose-made open stand (servo well + button hole + USB-C notch),
say so and I'll add a `pointer_base` to `../hardware/generate_stls.py`.

## Safety

Even a 5 mW class-3R diode must never hit an eye. The firmware clamps
tilt so the beam stays low, and the laser auto-off's if the Bluetooth
connection drops. Keep it aimed at the floor / low walls / a target on
your own desk, never at people or pets' faces, and never at mirrors or
glass that could bounce it upward.
