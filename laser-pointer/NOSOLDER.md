# LASER-POINTER v1 — the no-soldering build

This is the version to build first. **Zero soldering.** Everything pushes
into a breadboard or clips on with jumper wires, and it's powered by a USB
cable. You get the full thing: a laser you turn on/off from a **button**
and from your **phone or laptop** over Bluetooth.

The only trade for skipping solder is **size** — it lives on a small
breadboard, so it's about a **deck of cards**, not a matchbox. You can
shrink it later ([COMPACT.md](COMPACT.md)) once you're comfortable; the
board and firmware carry straight over.

Hands-on time once parts arrive: **~20 minutes.**

---

## PART 1 — What to buy (nothing needs soldering)

| # | Thing | Buy this (example) | Why |
|---|---|---|---|
| 1 | **ESP32-C3 SuperMini — _pre-soldered pins_** | [3-pack, pins pre-soldered](https://www.amazon.com/ESP32-C3-Development-Supermini-Bluetooth-Pre-Soldered/dp/B0F12JS872) | The brain + Bluetooth. **The "pre-soldered pins" part matters** — it means the pins are already attached, so you don't touch an iron. |
| 2 | **KY-008 laser module** (3-pack) | [KY-008 3-pack](https://www.amazon.com/KY-008-650nm-Sensor-Module-Arduino/dp/B0786BLLXD) | Comes with pins that push into a breadboard. |
| 3 | **Tactile pushbutton** (breadboard type, 4-leg) | search **"12mm tactile push button breadboard"** | Legs push straight into the breadboard. |
| 4 | **Breadboard + jumper wire kit** | [4 breadboards + M-M/F-M/F-F wires](https://www.amazon.com/Solderless-Breadboard-Boards-Flexible-Jumper/dp/B0GVD11LSS) | Holds everything, no solder. Get one with **male-to-male** and **female-to-female** wires. |
| — | **USB-C cable + phone charger or power bank** | you already own one | Powers it and loads the software. |

That's it — about **$8**. No battery, no charge board, no soldering iron.

> **Even simpler:** an "Arduino starter kit" (~$25) has the breadboard,
> wires, and buttons in one box — then you just add the ESP32-C3 and the
> KY-008 laser.

When it arrives, check you have: 1 small blue board, at least 1 laser
module (small board with a silver tube and pins), 1 button, 1 breadboard,
and a bundle of jumper wires in a few colors.

---

## PART 2 — Install the software (while parts ship)

Do this on a **laptop/desktop**. It's the same for every version of this
project.

**2.1 — Arduino IDE**
1. Go to **arduino.cc/en/software**, download **Arduino IDE 2.x** for your
   OS, install with defaults, open it once.

**2.2 — Add ESP32 support**
1. **File → Preferences** (Mac: **Arduino IDE → Settings**).
2. In **"Additional boards manager URLs"**, paste this and click **OK**:
   ```
   https://espressif.github.io/arduino-esp32/package_esp32_index.json
   ```
3. **Tools → Board → Boards Manager…**, search **esp32**, install
   **"esp32 by Espressif Systems"** (big download, wait a few minutes).

**2.3 — Add the one library**
1. **Sketch → Include Library → Manage Libraries…**
2. Search **NimBLE-Arduino**, click **Install**.

---

## PART 3 — Understand the breadboard (30-second primer)

A breadboard is a grid of holes that grip wires. Two things to know:

- **The long rails** down the sides (marked **+** red and **−** blue) each
  connect all the way along. We'll use the **−** rail as shared ground.
- **The short rows** in the middle: each row of 5 holes is connected side
  to side, but the two halves are split by the center trench. Push a chip's
  pins so they **straddle that center trench** and each pin gets its own
  row.

You never need to know more than that for this build.

---

## PART 4 — Plug it together (no soldering)

Work with the USB cable **unplugged**.

**4.1 — Seat the main board**
Push the **ESP32-C3 SuperMini** into the breadboard so its two rows of
pins straddle the center trench, near one end. Press gently until it's
seated. Each of its pins now lands in its own row.

**4.2 — Make a ground rail**
Take a **male-to-male jumper**. Put one end in a row touching the board's
**GND** pin, and the other end in the blue **−** rail. Now the whole −
rail is ground.

**4.3 — Add the laser**
The **KY-008** has 3 pins underneath, usually marked **`S`**, a blank
middle, and **`−`**. Push it into the breadboard (away from the main
board) so each pin is in its own row. Then:
- **male-to-male jumper:** laser **`−`** row → blue **−** rail.
- **male-to-male jumper:** laser **`S`** row → the board's **GPIO4** pin
  row.
- leave the middle pin alone.

**4.4 — Add the button**
Push the **tactile button** so it straddles the center trench (its legs
land on both sides). Then:
- **male-to-male jumper:** one button leg row → the board's **GPIO10** pin
  row.
- **male-to-male jumper:** the leg on the **other side** → blue **−** rail.

**4.5 — Double-check**
- Laser `S` → GPIO4? Laser `−` → − rail?
- Button between GPIO10 and − rail?
- Board GND → − rail?

Take a photo so you can compare if something misbehaves.

> **No breadboard? The even-simpler way:** because the SuperMini's pins and
> the KY-008's pins are both exposed metal, you can connect them directly
> with **female-to-female jumper wires** (laser `S`→GPIO4, laser `−`→a GND
> pin). The button is the only fiddly part without a breadboard, so the
> breadboard is still the friendlier route.

---

## PART 5 — Load the software

**5.1 — Get the code**
1. On this project's GitHub page: green **Code** button → **Download ZIP**,
   unzip it.
2. Open **`laser-pointer/firmware/laserpointer/`** and double-click
   **`laserpointer.ino`** — it opens in the Arduino IDE. (If it offers to
   move it into a same-named folder, click OK.)

**5.2 — Turn OFF sleep for the USB build (one small edit)**
Near the top of the file you'll see:
```
#define ENABLE_SLEEP 1
```
Change the `1` to `0` and save. On USB power there's no battery to save,
and this keeps it **always reachable from your phone** (with sleep on, it
would go quiet after 2 minutes until you pressed the button). Later, for
the battery build, set it back to `1`.

**5.3 — Plug in** the board with the USB-C cable to your computer.

**5.4 — Pick the board:** **Tools → Board → esp32 → "ESP32C3 Dev Module."**

**5.5 — Pick the port:** **Tools → Port →** choose the new entry that
appeared when you plugged in (Windows `COM4/5…`, Mac `/dev/cu.usbmodem…`).
Unsure which? Unplug, look, plug back in, pick the new one.

**5.6 — Upload:** click the **right-arrow (→)**, top-left. Wait for **"Done
uploading."**
- *If it hangs at "Connecting…":* unplug, hold the board's **BOOT** button
  while plugging USB back in, release after 2 seconds, click Upload again.

---

## PART 6 — Use it

Power it from any **USB-C charger or power bank** (or just leave it in the
computer). Then:

**The button:** press → laser on, press again → off. No phone needed.

**Your phone or laptop:**
1. Open **`laser-pointer/app/laser-remote.html`** from the download:
   - **Laptop:** double-click → opens in your browser. Use **Chrome/Edge**.
   - **Android:** open in **Chrome** (email yourself the file, or host it).
   - **iPhone:** install the free **Bluefy** browser and open it there.
2. Click **Connect** → pick **LASER-PT** → **Pair**.
3. The big round button lights up — tap to toggle. Press the physical
   button and the app updates to match.

**No-app option (any phone):** install **nRF Connect**, Scan → **LASER-PT**
→ Connect → find the **Nordic UART** service → send text `L1` (on), `L0`
(off), `T` (toggle).

---

## If something doesn't work

| Problem | Fix |
|---|---|
| Upload hangs at "Connecting…" | Hold **BOOT** while plugging in USB, then Upload again. |
| No **Port** appears | Your USB-C cable might be charge-only — try another; it needs data wires. |
| Laser won't light | Re-check laser `S` → **GPIO4** and `−` → **− rail**; middle pin stays empty. Try `L1` from the app or press the button. |
| It goes quiet after ~2 min | You didn't set `ENABLE_SLEEP` to `0` — do step 5.2 and re-upload. |
| App `Connect` does nothing | Use Chrome/Edge (laptop/Android) or Bluefy (iPhone); plain Safari can't. |
| Wires keep popping out | Push them fully in; breadboard holes grip better near the center rows. |

---

## SAFETY

- It's a **5 mW class-3R** laser. **Never aim at eyes** (yours or others')
  or at pets' faces.
- Never point it at **mirrors, windows, glossy screens, or shiny metal** —
  reflections can reach an eye.
- No motor here, so **you** choose where it points: keep the dot on the
  **floor and low walls**.
- Kill it fast: tap the button, tap the app, or unplug it. It also turns
  off by itself if the Bluetooth connection drops.

---

When you're ready to make it small and battery-powered, go to
**[COMPACT.md](COMPACT.md)** — that's the version with soldering and deep
sleep. Same board, same firmware (just set `ENABLE_SLEEP` back to `1`).
