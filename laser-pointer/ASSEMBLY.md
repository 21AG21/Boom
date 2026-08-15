# LASER-POINTER — complete beginner's build guide

An **on/off Bluetooth laser** you control from a **button** on the device
and from your **phone or laptop**. No motors, no patterns (those can come
later). This assumes you have **nothing** and have **never** done
electronics. Follow it top to bottom — every step is small on purpose.

Hands-on time once parts arrive: about **30–40 minutes**, no soldering.

Read the **Safety** box at the very bottom before you switch on the laser.

---

## PART 1 — What to buy

Four things plus a USB-C cable you probably own. Get the "pre-soldered
pins" board and you need no soldering iron.

| # | Thing | Buy this (example) | Why |
|---|---|---|---|
| 1 | **ESP32-C3 SuperMini** (*pre-soldered pins*) | [3-pack, pins pre-soldered](https://www.amazon.com/ESP32-C3-Development-Supermini-Bluetooth-Pre-Soldered/dp/B0F12JS872) | The brain + Bluetooth. |
| 2 | **KY-008 laser module** (3-pack) | [KY-008 3-pack](https://www.amazon.com/KY-008-650nm-Sensor-Module-Arduino/dp/B0786BLLXD) | The red laser dot. |
| 3 | **Tactile pushbutton** | search **"tactile push button kit 12mm"** | The on/off button. |
| 4 | **Breadboard + jumper wires kit** | [4 breadboards + wires](https://www.amazon.com/Solderless-Breadboard-Boards-Flexible-Jumper/dp/B0GVD11LSS) | Connect everything, no solder. |
| — | **USB-C cable** | you already own one | Powers it and loads the software. |

> **Simpler alternative:** an "Arduino starter kit" (~$25) includes the
> breadboard, wires, and buttons together — then you only add the
> ESP32-C3 and the KY-008 laser.

When it arrives, check you have: 1 small blue board, at least 1 laser
module (small board with a silver tube), 1 button, 1 breadboard, and a
bundle of jumper wires.

---

## PART 2 — Install the software (do this while parts ship)

You'll set up the free **Arduino IDE** — the program that loads code onto
the board. Do this on a **laptop/desktop**, not a phone.

**Step 2.1 — Install the Arduino IDE**
1. Go to **arduino.cc/en/software**.
2. Download **Arduino IDE 2.x** for your operating system.
3. Run the installer with defaults, then open the program once. You'll see
   a code area and, top-left, a check mark (Verify) and a right-arrow
   (Upload).

**Step 2.2 — Teach it about the ESP32**
1. Menu: **File → Preferences** (Mac: **Arduino IDE → Settings**).
2. In **"Additional boards manager URLs"**, paste this and click **OK**:
   ```
   https://espressif.github.io/arduino-esp32/package_esp32_index.json
   ```
3. Open **Tools → Board → Boards Manager…**
4. Search **esp32**, find **"esp32 by Espressif Systems"**, click
   **Install** (big download — wait a few minutes).

**Step 2.3 — Install the one library**
1. Open **Sketch → Include Library → Manage Libraries…**
2. Search **NimBLE-Arduino** → find it (by h2zero) → **Install**.

Software is ready.

---

## PART 3 — Build the hardware (no soldering)

Keep the board **unplugged** the whole time. There are only three
connections.

**Step 3.1 — Know your parts**
- The **board** has tiny pin labels along its edges. You'll use **GPIO4**,
  **GPIO10**, **GND**, and (optional) **GPIO5**. They may be printed as
  just `4`, `10`, `G`, `5`.
- The **KY-008 laser** is a small board with a silver tube and 3 pins,
  usually marked **`S`**, a blank middle pin, and **`−`**.
- The **button** has legs on two sides.

**Step 3.2 — Put the board on the breadboard**
Press the ESP32-C3 into the breadboard so its two rows of pins straddle
the center gap. (If it won't fit, leave it out and use female-to-male
jumper wires straight onto its pins instead.)

**Step 3.3 — Wire the laser (2 wires)**
- laser **`S`** → board **GPIO4**
- laser **`−`** → board **GND**
- middle pin → leave unconnected

**Step 3.4 — Wire the button (2 wires)**
- one leg → board **GPIO10**
- the opposite leg → board **GND**

(GND is shared — you can run both the laser `−` and a button leg into any
GND pin, or into a breadboard `−` rail that you jumper once to the board's
GND.)

**Step 3.5 — (Optional) status LED**
- board **GPIO5** → the **220Ω resistor** → LED **long leg (+)**
- LED **short leg (−)** → **GND**

That's the whole circuit. Double-check the laser `S` goes to GPIO4 and its
`−` to GND. Take a photo so you can compare later.

---

## PART 4 — Load the software onto the board

**Step 4.1 — Get the code**
1. On this project's GitHub page: green **Code** button → **Download ZIP** →
   unzip.
2. Open **`laser-pointer/firmware/laserpointer/`** and double-click
   **`laserpointer.ino`** — it opens in the Arduino IDE. (If it offers to
   put it in a folder of the same name, click OK.)

**Step 4.2 — Plug in the board** with the USB-C cable. A small light comes
on.

**Step 4.3 — Pick the board:** **Tools → Board → esp32 → "ESP32C3 Dev
Module."**

**Step 4.4 — Pick the port:** **Tools → Port →** choose the new entry that
appeared when you plugged in (Windows `COM4/5…`, Mac `/dev/cu.usbmodem…`).
Unsure? Unplug, look, plug back in, pick the new one.

**Step 4.5 — Upload:** click the **right-arrow (→)**, top-left. Wait for
**"Done uploading."**
- *If it hangs at "Connecting…":* unplug, hold the board's **BOOT** button
  while plugging USB back in, release after 2 seconds, click Upload again.

The laser is now controllable. The status light does a slow blink when the
laser is off.

---

## PART 5 — Turn it on and off

### The button
Press it → laser **on**. Press again → **off**. Done — no phone needed.

### Your phone or laptop
1. Open **`laser-pointer/app/laser-remote.html`** from the downloaded
   folder:
   - **Laptop:** double-click it — opens in your browser. Use **Chrome or
     Edge**.
   - **Android phone:** open it in **Chrome** (email the file to yourself
     and open the attachment, or host it on GitHub Pages).
   - **iPhone:** Safari can't do this — install the free **Bluefy** browser
     and open the file there. (Or use "the other way" below.)
2. Click **Connect**.
3. In the little pop-up, click **LASER-PT** → **Pair/Connect**.
4. The status line turns green and the big round button lights up. Tap it
   to turn the laser on/off. If you press the physical button, the app
   updates to match.

### The other way — any phone, no app
1. Install **nRF Connect** (free, iPhone or Android).
2. **Scan** → tap **LASER-PT** → **Connect**.
3. Find the **Nordic UART** service, tap the write/up-arrow icon, and send
   as *Text*: `L1` = on, `L0` = off, `T` = toggle.

---

## If something doesn't work

| Problem | Fix |
|---|---|
| Upload fails at "Connecting…" | Hold **BOOT** while plugging in USB, then Upload again. |
| No **Port** appears | Try a different USB-C cable — many are charge-only with no data wires. |
| Laser won't light | Check `S` → **GPIO4** and `−` → **GND**; the middle pin stays empty. Try `L1` from the app or press the button. |
| `Connect` in the app does nothing | You're not on Chrome/Edge (laptop/Android) or Bluefy (iPhone). Plain Safari/iOS can't do Web Bluetooth. |
| App won't find the device | Make sure the board is powered and you flashed the firmware; only one device can be connected to it at a time. |

---

## SAFETY — read this

- It's a **5 mW class-3R** laser. **Never aim it at anyone's eyes**, your
  own included, and never at pets' faces.
- Never point it at **mirrors, windows, glossy screens, or shiny metal** —
  a reflection can bounce into an eye.
- There's no motor, so **you** choose where it points: aim the whole unit
  so the dot stays on the **floor and low walls**.
- To kill it fast: tap the button, tap the app, or unplug it. The laser
  also shuts off by itself if the Bluetooth connection drops.
- It's a toy for chasing a dot around the floor — treat it like one.
