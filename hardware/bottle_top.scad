// ============================================================
// Boom Flask — fake lid module for a ThermoFlask-style bottle
// Open in OpenSCAD (openscad.org) → F6 → Export STL
//
// PRINT ORDER: set part="plug" first — a 20-min test print that
// validates the bottle-mouth fit before the 3-hour shell.
// Shell prints dome-up with supports; others need no supports.
// ============================================================

// -------- MEASURE YOUR BOTTLE AND EDIT THESE --------
bottle_od = 73;    // body outer diameter at the shoulder (24oz ≈ 73)
mouth_id  = 55;    // bottle mouth inner diameter (wide mouth ≈ 55)

// -------- part selector: "all", "shell", "bulkhead", "carriage", "plug" --------
part = "all";

// -------- tuning --------
wall      = 2.4;
band_h    = 30;    // straight window-band section height
dome_h    = 18;    // tapered top height
slot_h    = 6;     // laser window slot height
slot_z    = 12;    // slot bottom, from band bottom
spine_deg = 60;    // blind arc (structure + hidden USB-C port)
tilt_down = 5;     // fixed downward beam angle (safety: keep >= 4)
laser_d   = 6.4;

servo_l = 23.2;  servo_w = 12.6;  servo_h = 26;  // SG90/MG90S w/ shaft
plug_h  = 12;
fit_tol = 0.4;

$fn = 96;

// ============================================================
// wedge cutter: pie slice of `angle` degrees centered on +X axis
module wedge(angle, r, h) {
  linear_extrude(h)
    polygon(concat([[0, 0]],
      [for (a = [-angle/2 : 3 : angle/2]) [r*cos(a), r*sin(a)]],
      [[r*cos(angle/2), r*sin(angle/2)]]));
}

// The visible "lid": straight band + tapered dome, hollow
module shell() {
  difference() {
    union() {
      cylinder(h = band_h, d = bottle_od);
      translate([0, 0, band_h])
        cylinder(h = dome_h, d1 = bottle_od, d2 = bottle_od * 0.66);
      translate([0, 0, band_h + dome_h - 0.5])
        cylinder(h = 3, d = bottle_od * 0.66);          // flat lid top
    }
    // hollow interior
    translate([0, 0, -1]) {
      cylinder(h = band_h + 1, d = bottle_od - 2*wall);
      translate([0, 0, band_h + 1])
        cylinder(h = dome_h, d1 = bottle_od - 2*wall,
                              d2 = bottle_od * 0.66 - 2*wall);
    }
    // window slot: full circle minus the blind spine (spine faces +X)
    translate([0, 0, slot_z])
      rotate([0, 0, spine_deg/2])
        wedge(360 - spine_deg, bottle_od, slot_h);
    // USB-C port cutout on the spine, near the bottom
    translate([bottle_od/2 - wall - 1, -5, 3])
      cube([wall + 2, 10, 4]);
    // bulkhead snap groove inside the band top
    translate([0, 0, band_h - 4])
      difference() {
        cylinder(h = 2.4, d = bottle_od - 2*wall + 1.6);
        cylinder(h = 2.4, d = bottle_od - 2*wall - 2);
      }
  }
}

// Disc that carries the pan servo, shaft pointing DOWN through center.
// Snaps into the shell groove; electronics ride on top of it.
module bulkhead() {
  d = bottle_od - 2*wall - 0.6;
  difference() {
    union() {
      cylinder(h = 3, d = d);
      // snap lip
      translate([0, 0, 0.3])
        difference() {
          cylinder(h = 2, d = d + 2);
          cylinder(h = 2, d = d - 2);
        }
    }
    // servo body drops through, centered on its output shaft
    translate([-servo_l + 17.4, -servo_w/2, -1])   // shaft ~5.9mm from body end
      cube([servo_l, servo_w, 5]);
    // wire pass-through
    translate([d/2 - 8, 0, -1]) cylinder(d = 8, h = 5);
    // zip-tie slots to strap the servo down
    for (y = [-servo_w/2 - 4, servo_w/2 + 4])
      translate([-3, y - 1.5, -1]) cube([6, 3, 5]);
  }
}

// Hangs from the servo horn below the bulkhead; holds the laser
// at a fixed slight downward angle so the beam can't reach eye level.
module carriage() {
  difference() {
    union() {
      cylinder(d = 16, h = 3);                       // horn plate
      translate([-2, -8, 0]) cube([4, 3, 18]);        // drop arm
      translate([0, -8 + 1.5, 14])                    // laser ring, tilted
        rotate([90 + tilt_down, 0, 0])
          cylinder(d = laser_d + 4, h = 12, center = true);
    }
    translate([0, 0, -1]) cylinder(d = 2.4, h = 5);   // horn center screw
    for (r = [0, 90, 180, 270])                       // horn arm screws
      rotate([0, 0, r]) translate([5, 0, -1]) cylinder(d = 1.8, h = 5);
    // laser barrel bore
    translate([0, -8 + 1.5, 14])
      rotate([90 + tilt_down, 0, 0])
        cylinder(d = laser_d, h = 14, center = true);
  }
}

// Press-fits into the bottle mouth; the shell sits on its flange.
module plug() {
  difference() {
    union() {
      cylinder(h = 3, d = bottle_od);                            // flange
      translate([0, 0, -plug_h]) {
        cylinder(h = plug_h, d = mouth_id - fit_tol);
        cylinder(h = 2, d1 = mouth_id - fit_tol - 2,             // entry chamfer
                         d2 = mouth_id - fit_tol);
      }
    }
    translate([0, 0, -plug_h - 1])                               // hollow it
      cylinder(h = plug_h + 5, d = mouth_id - fit_tol - 2*wall);
  }
}

// ============================================================
if (part == "all" || part == "shell") shell();
if (part == "all" || part == "bulkhead")
  translate([bottle_od + 20, 0, 0]) bulkhead();
if (part == "all" || part == "carriage")
  translate([bottle_od + 20, bottle_od, 0]) carriage();
if (part == "all" || part == "plug")
  translate([0, bottle_od + 25, plug_h]) plug();
