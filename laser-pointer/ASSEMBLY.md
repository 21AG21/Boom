# LASER-POINTER — complete beginner's build guide

This assumes you have **nothing** and have **never** done electronics.
Follow it top to bottom. Every step is small on purpose. Total hands-on
time once parts arrive: about **1–1.5 hours**, no soldering.

Read the **Safety** box at the very bottom before you switch on the laser.

---

## PART 1 — What to buy

You need six things plus a USB-C charger you probably already own. Buy the
"pre-soldered pins" board and you won't need a soldering iron at all.

| # | Thing | Buy this (example) | Why |
|---|---|---|---|
| 1 | **ESP32-C3 SuperMini** (get the *pre-soldered pins* version) | [3-pack, pins pre-soldered](https://www.amazon.com/ESP32-C3-Development-Supermini-Bluetooth-Pre-Soldered/dp/B0F12JS872) | The brain + Bluetooth. Pre-soldered = no iron needed. |
| 2 | **2× MG90S micro servos** (comes as a 2-pack with horns + screws) | [Miuzei MG90S 2-pack](https://www.amazon.com/Miuzei-Geared-Helicopter-Arduino-Project/dp/B0BWJ41FZB) | The two motors that pan and tilt. |
| 3 | **Pan/tilt servo bracket** | [SG90/MG90S PT bracket](https://www.amazon.com/Bracket-Platform-Anti-Vibration-Aircraft-Dedicated/dp/B07VS7DN1T) | The little frame the two servos bolt into. |
| 4 | **KY-008 laser module** (3-pack) | [KY-008 3-pack w/ demo](https://www.amazon.com/KY-008-650nm-Sensor-Module-Arduino/dp/B0786BLLXD) | The 5 mW red laser dot. |
| 5 | **Breadboard + jumper wires kit** | [4 breadboards + M-M/F-M/F-F wires](https://www.amazon.com/Solderless-Breadboard-Boards-Flexible-Jumper/dp/B0GVD11LSS) | Lets you connect everything with no soldering. |
| 6 | **Tactile pushbutton** | search **"tactile push button kit 12mm"** (any momentary button) | The physical on/off button. A cheap assortment pack is fine. |
| — | **USB-C cable + phone charger** | you already own one | Powers it and loads the software. |

> **Cheaper/simpler alternative:** an "Arduino starter kit" (~$25) usually
> bundles the breadboard, jumper wires, LEDs, resistors, **and** pushbuttons
> in one box — then you only add the ESP32-C3, the 2 servos, the bracket,
> and the KY-008 laser separately. If you want an LED status light, that's
> where you'd get the LED + resistor too (optional; the build works without).

When it all arrives, lay the parts on a table and check you have: 1 small
blue board, 2 servos (each with a bag of little plastic arms + tiny screws),
1 bracket kit, at least 1 laser module (small board with a silver tube),
1 breadboard, a bundle of wires, and 1 button.

---

## PART 2 — Install the software (do this while parts ship)

You'll set up the free **Arduino IDE** on your computer. This is the program
that loads code onto the board. **Do these on a laptop/desktop**, not a phone.

**Step 2.1 — Install the Arduino IDE**
1. Go to **arduino.cc/en/software**.
2. Download **Arduino IDE 2.x** for your operating system (Windows/Mac/Linux).
3. Run the installer, click through with defaults, open the program once.
   You'll see a window with a code area and, top-left, a green check (Verify)
   and a right-arrow (Upload).

**Step 2.2 — Teach it about the ESP32**
1. In the IDE menu: **File → Preferences** (on Mac: **Arduino IDE → Settings**).
2. Find the box labeled **"Additional boards manager URLs"**.
3. Paste this line into it, then click **OK**:
   ```
   https://espressif.github.io/arduino-esp32/package_esp32_index.json
   ```
4. Open **Tools → Board → Boards Manager…** (a panel opens on the left).
5. In its search box type **esp32**.
6. Find **"esp32 by Espressif Systems"** and click **Install**. It's a big
   download — wait for it to finish (a few minutes).

**Step 2.3 — Install the two libraries**
1. Open **Sketch → Include Library → Manage Libraries…** (a panel opens).
2. Search **ESP32Servo** → find "ESP32Servo" → click **Install**.
3. Search **NimBLE-Arduino** → find "NimBLE-Arduino" (by h2zero) → **Install**.

Software is ready. Leave the IDE installed; you'll come back to it in Part 4.

---

## PART 3 — Build the hardware (no soldering)

Do this with the board **unplugged** from power the whole time.

### 3.1 — Mount the servos in the bracket
The bracket kit is a small pile of plastic plates + screws. There are lots
of these kits and they assemble slightly differently, but the goal is always
the same shape:

1. **Bottom servo = PAN** (turns left/right). It sits in the base plate,
   shaft pointing **up**.
2. **Top servo = TILT** (nods up/down). It bolts into the U-shaped bracket
   that sits on top of the pan servo, shaft pointing **sideways**.
3. Use the tiny screws that came **with the servos** to hold them in, and
   the bracket's own screws to join the plates. Snap a plastic servo "horn"
   (the little arm) onto each shaft where the bracket calls for it.
4. Don't force anything and don't fully tighten yet — leave it so the
   servos can still be re-centered in step 4.6.

> If the bracket instructions are confusing, search YouTube for
> **"SG90 pan tilt bracket assembly"** — it's a 3-minute watch and the
> MG90S mounts identically.

### 3.2 — Attach the laser
1. The **KY-008** is a small board with a silver tube (the laser) on it and
   3 pins underneath.
2. Tape or zip-tie the laser board to the **top (tilt) servo's** horn/arm so
   the silver tube points **forward and slightly down**. Hot glue works too
   if you have it. It just needs to move when the top servo moves.

### 3.3 — Understand the board's pins
Look at your ESP32-C3 SuperMini. Along the edges the pins are labeled in
tiny print. You'll use these:

- **5V** (sometimes "5" or "VBUS") — power out
- **GND** (sometimes "G") — ground, there may be more than one
- **GPIO2, GPIO3, GPIO4, GPIO10** — signal pins (may be printed as just
  "2", "3", "4", "10")

### 3.4 — Set up the breadboard power rails
A breadboard has two long rows down each side marked **+** (red) and **−**
(blue/black). These are your power rails.

1. Plug the board into the breadboard so its pins straddle the center gap
   (or, if it won't fit, just use female-to-male jumper wires to reach it).
2. Run a **jumper from the board's `5V` pin → the red `+` rail.**
3. Run a **jumper from the board's `GND` pin → the blue `−` rail.**

Now anything plugged into the + rail gets 5V, and the − rail is ground.

### 3.5 — Wire the two servos
Each servo has a 3-wire plug: **brown/black = ground, red = power,
orange/yellow = signal.** Using male-to-male jumpers pushed into the
breadboard next to each servo wire (or female-to-male straight onto the
servo plug):

**Pan servo (bottom):**
- brown  → **−** rail
- red    → **+** rail (5V)
- orange → board **GPIO2**

**Tilt servo (top):**
- brown  → **−** rail
- red    → **+** rail (5V)
- orange → board **GPIO3**

### 3.6 — Wire the laser
The KY-008 has 3 pins, usually marked **`S`**, a middle pin, and **`−`**.
- **`−`** → **−** rail
- **`S`** → board **GPIO4**
- middle pin → leave it unconnected

### 3.7 — Wire the button
A tactile button has legs on two sides. It doesn't matter which way round:
- one leg → board **GPIO10**
- the opposite leg → **−** rail

That's the whole circuit. Double-check nothing on the **+ (5V)** rail is
accidentally touching the **− rail**. Take a photo before moving on so you
can compare later.

---

## PART 4 — Load the software onto the board

### 4.1 — Get the code onto your computer
1. On this project's GitHub page, click the green **Code** button →
   **Download ZIP**. Unzip it.
2. Open the folder **`laser-pointer/firmware/laserpointer/`** and
   double-click **`laserpointer.ino`** — it opens in the Arduino IDE.
   (If it asks to move it into a folder of the same name, click OK.)

### 4.2 — Plug in the board
Connect the ESP32-C3 to your computer with the **USB-C cable**. A small
light on the board should come on.

### 4.3 — Pick the board type
In the Arduino IDE menu: **Tools → Board → esp32 →** scroll to and click
**"ESP32C3 Dev Module."**

### 4.4 — Pick the port
**Tools → Port →** choose the new entry that appeared when you plugged in
(Windows: `COM4`, `COM5`… / Mac: `/dev/cu.usbmodem…`). If you're unsure,
unplug, look at the list, plug back in, and pick the one that's new.

### 4.5 — Upload
1. Click the **right-arrow (→) Upload** button, top-left.
2. It will compile (progress bar) then flash. Wait for **"Done uploading."**
   at the bottom.
3. *If it fails or hangs at "Connecting…":* unplug, hold the little **BOOT**
   button on the board while you plug the USB back in, release after 2
   seconds, and click Upload again.

The laser pointer is now running. The status light will do a slow blink.

### 4.6 — Center the servos (one-time mechanical fix)
When it first powers on, the firmware parks near center. If the bracket is
aimed weirdly, **unplug**, gently pop the servo horn off its spline, rotate
the bracket to point roughly straight/level, and press the horn back on.
Re-tighten the bracket screws now.

---

## PART 5 — Control it from your phone or computer

### The easy way — the app
1. From the same downloaded folder, open **`laser-pointer/app/laser-remote.html`**.
   - **On a computer:** just double-click it — it opens in your browser.
     Use **Chrome or Edge**.
   - **On an Android phone:** open it in **Chrome** (easiest: email the file
     to yourself and open the attachment, or view it on GitHub Pages).
   - **On an iPhone:** Safari can't do this. Install the free **Bluefy**
     browser from the App Store and open the file in that. (Or use the
     "other way" below.)
2. Click the big **Connect** button.
3. A little window pops up listing Bluetooth devices — click **LASER-PT**,
   then **Pair/Connect**.
4. The status line turns green. Now:
   - **Drag inside the square pad** to aim the dot.
   - **Laser** button turns the beam on/off.
   - **Patrol** makes it drift on its own (cat mode).
   - **Center** re-centers. **LASER OFF + PARK** is your panic-off.

### The other way — no app, any phone
1. Install **nRF Connect** (free, iPhone or Android).
2. Open it, **Scan**, tap **LASER-PT**, tap **Connect**.
3. Find the service with a **"TX/RX"** or **"Nordic UART"** characteristic,
   tap the up-arrow/write icon, and send these typed commands (as *Text*):
   - `L1` = laser on, `L0` = laser off
   - `J50,80` = aim (first number left↔right, second up↔down, each 0–100)
   - `M1` = patrol on, `M0` = off
   - `X` = everything off

### The no-phone way — the button
- **Short press** the button = laser on/off.
- **Hold it ~1 second** = patrol mode on/off.

---

## PART 6 — Aim it safely (do this once)

The firmware already stops the beam from pointing up, but tune it for your
desk:

1. Put the toy where it'll live.
2. Turn the laser on and sweep it around with the app.
3. If the highest the dot ever goes is still too high, open
   `laserpointer.ino`, find the line `const float TILT_MAX = 88;` near the
   top, **lower** that number (e.g. `82`), and re-upload (Part 4.5). Bigger
   number = higher beam; you want the dot to stay on the floor and low walls.

---

## If something doesn't work

| Problem | Fix |
|---|---|
| Upload fails at "Connecting…" | Hold **BOOT** while plugging in USB, then Upload again. |
| No **Port** appears | Try a different USB-C cable — many are charge-only with no data wires. |
| Servos jitter or the board keeps resetting | Servos need real power. Use a **USB wall charger**, not a laptop port, and make sure servo **red** wires are on the **5V** rail. |
| Laser won't light | Check `S` → GPIO4 and `−` → `−` rail; the middle pin stays empty. Try `L1` from the app. |
| `Connect` in the app does nothing | You're not on Chrome/Edge (computer/Android) or Bluefy (iPhone). Safari/regular iOS can't do Web Bluetooth. |
| Button does the wrong thing | Short vs long press: a quick tap = laser; a held press = patrol. |

---

## SAFETY — read this

- It's a **5 mW class-3R** laser. **Never aim it at anyone's eyes**, your
  own included, and never at pets' faces.
- Never point it at **mirrors, windows, glossy screens, or shiny metal** —
  a reflection can bounce into an eye.
- Keep the dot on the **floor and low walls**. The `TILT_MAX` clamp helps,
  but *you* set where the whole thing points.
- If you lose control, hit **LASER OFF + PARK** in the app, tap the button,
  or just unplug it. The laser also shuts off by itself if the Bluetooth
  connection drops.
- It's a toy for chasing a dot around the floor — treat it like one.
