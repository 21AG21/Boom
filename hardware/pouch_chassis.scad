// ============================================================
// Boom Pouch — internal turret chassis for a fabric pencil pouch
// Open in OpenSCAD (openscad.org) → F6 → Export STL
//
// Print: PLA, 0.2mm layers, 3 walls, 15% infill, no supports.
// Parts are laid out side by side; set `part` to print individually.
// ============================================================

// -------- MEASURE YOUR POUCH AND EDIT THESE --------
pouch_inner_l = 190;   // interior length of your pouch (mm)
pouch_inner_w = 70;    // interior width at the base (mm)

// -------- part selector: "all", "chassis", "tilt", "clip" --------
part = "all";

// -------- tuning --------
clearance   = 12;      // gap between chassis and pouch walls (fabric slack)
base_t      = 3;       // base plate thickness
rim_h       = 12;      // perimeter rim height
rim_t       = 2;       // rim wall thickness
laser_d     = 6.4;     // laser module barrel diameter + clearance

// SG90/MG90S micro servo body + flange
servo_l = 23.2;  servo_w = 12.6;  servo_well_h = 17;
servo_flange_l = 32.5;  servo_screw_d = 2.2;

// component trays (L x W)
esp_l = 23.5;  esp_w = 19;    // ESP32-C3 SuperMini
chg_l = 28;    chg_w = 18;    // TP4056 USB-C board
bat_l = 52;    bat_w = 35;    // 503450-ish LiPo — edit to your battery

washer_d = 25.8;  washer_t = 2.6;   // M8 fender washer / quarter pockets

base_l = pouch_inner_l - clearance;
base_w = pouch_inner_w - clearance;

$fn = 64;

// ============================================================
module tray(l, w, wall=1.6, h=6) {          // open-top holder
  difference() {
    cube([l + 2*wall, w + 2*wall, h]);
    translate([wall, wall, 1]) cube([l, w, h]);
  }
}

module servo_well() {                        // vertical servo pocket
  difference() {
    cube([servo_flange_l + 4, servo_w + 5, servo_well_h]);
    // body pocket, centered
    translate([(servo_flange_l + 4 - servo_l)/2, 2.5, -1])
      cube([servo_l, servo_w, servo_well_h + 2]);
    // flange screw holes
    for (x = [ (servo_flange_l+4)/2 - servo_flange_l/2 + 2,
               (servo_flange_l+4)/2 + servo_flange_l/2 - 2 ])
      translate([x, 2.5 + servo_w/2, servo_well_h - 8])
        cylinder(d = servo_screw_d, h = 10);
  }
}

module pen_clip() {                          // C-clip that holds a real pen
  difference() {
    cylinder(d = 13, h = 8);
    translate([0, 0, -1]) cylinder(d = 10, h = 10);
    translate([-7, 0, -1]) cube([14, 8, 10]);   // opening
  }
}

module chassis() {
  difference() {
    union() {
      cube([base_l, base_w, base_t]);                       // base plate
      difference() {                                        // perimeter rim
        cube([base_l, base_w, rim_h]);
        translate([rim_t, rim_t, -1])
          cube([base_l - 2*rim_t, base_w - 2*rim_t, rim_h + 2]);
      }
      // nose alignment ring: laser's neutral axis exits here.
      // Line this ring up with the open zipper corner.
      translate([base_l - 1, base_w/2, base_t + 16])
        rotate([0, 90, 0]) cylinder(d = laser_d + 5, h = 6);

      // pan servo well at the nose end
      translate([base_l - servo_flange_l - 14, (base_w - servo_w - 5)/2, base_t])
        servo_well();

      // trays back to front: battery, charger, ESP32
      translate([6, (base_w - bat_w)/2 - 1.6, base_t]) tray(bat_l, bat_w);
      translate([bat_l + 16, 6, base_t])               tray(chg_l, chg_w);
      translate([bat_l + 16, base_w - esp_w - 10, base_t]) tray(esp_l, esp_w);

      // pen clips along one rim — the decoy layer
      for (x = [30, 75, 120])
        translate([x, base_w - 8, rim_h]) pen_clip();
    }
    // washer weight pockets sunk into the base
    for (x = [base_l * 0.25, base_l * 0.6])
      translate([x, base_w/2, base_t - washer_t])
        cylinder(d = washer_d, h = washer_t + 1);
    // beam exit through the nose ring
    translate([base_l - 3, base_w/2, base_t + 16])
      rotate([0, 90, 0]) cylinder(d = laser_d + 2, h = 10);
  }
}

// U-bracket: presses onto the pan servo horn, carries the tilt servo
module tilt_bracket() {
  horn_w = 8;
  difference() {
    union() {
      cube([servo_l + 6, servo_w + 6, 3]);              // floor
      cube([3, servo_w + 6, servo_well_h]);              // side wall
      translate([servo_l + 3, 0, 0]) cube([3, servo_w + 6, servo_well_h]);
    }
    translate([3, 3, -1]) cube([servo_l, servo_w, 5]);   // servo drops in
    // horn screw holes in the floor center
    translate([(servo_l + 6)/2, (servo_w + 6)/2, -1]) {
      cylinder(d = 2.2, h = 5);
      translate([horn_w/2, 0, 0]) cylinder(d = 1.8, h = 5);
      translate([-horn_w/2, 0, 0]) cylinder(d = 1.8, h = 5);
    }
  }
}

// snap ring for the laser barrel, mounts on the tilt servo horn
module laser_clip() {
  difference() {
    union() {
      cylinder(d = laser_d + 4, h = 10);
      translate([-4, -(laser_d + 4)/2 - 3, 0]) cube([8, 3, 10]); // horn tab
    }
    translate([0, 0, -1]) cylinder(d = laser_d, h = 12);
    translate([-2, 0, -1]) cube([4, laser_d, 12]);               // snap slot
    translate([0, -(laser_d + 4)/2 - 4, 5])
      rotate([90, 0, 0]) cylinder(d = 1.8, h = 6);               // horn screw
  }
}

// ============================================================
if (part == "all" || part == "chassis") chassis();
if (part == "all" || part == "tilt")
  translate([0, base_w + 15, 0]) tilt_bracket();
if (part == "all" || part == "clip")
  translate([50, base_w + 15, 0]) laser_clip();
