#!/usr/bin/env python3
"""Render Boom turret parts + assembled models to STL.

Requires: pip install trimesh manifold3d scipy numpy
Edit the measurements below, run, and fresh STLs land in hardware/stl/.
"""
import numpy as np
import trimesh
from trimesh.creation import box as _box, cylinder as _cyl

# ================= MEASUREMENTS (edit these) =================
# Pencil case: 4 x 8 x 3 inch boxy case, interior in mm
POUCH_L = 203      # interior length  (8")
POUCH_W = 102      # interior width   (4")
BEAM_H  = 42       # beam axis height above case floor (case is 76mm tall)

# Bottle: 1.2 L / 40 oz ThermoFlask
BOTTLE_OD = 92     # body outer diameter at the shoulder
MOUTH_ID  = 54     # mouth inner diameter — VERIFY with the plug test print!

import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stl")
os.makedirs(OUT, exist_ok=True)

# ---------------- helpers ----------------
def box(l, w, h, at=(0, 0, 0)):
    b = _box(extents=[l, w, h])
    b.apply_translation([at[0] + l / 2, at[1] + w / 2, at[2] + h / 2])
    return b

def cyl(d, h, at=(0, 0, 0), sections=96):
    c = _cyl(radius=d / 2, height=h, sections=sections)
    c.apply_translation([at[0], at[1], at[2] + h / 2])
    return c

def frustum(d1, d2, h, at=(0, 0, 0), sections=96):
    a = cyl(d1, 0.01, at=at, sections=sections)
    b = cyl(d2, 0.01, at=(at[0], at[1], at[2] + h - 0.01), sections=sections)
    return trimesh.util.concatenate([a, b]).convex_hull

def rot(m, deg, axis, point=(0, 0, 0)):
    m.apply_transform(trimesh.transformations.rotation_matrix(
        np.radians(deg), axis, point))
    return m

def union(ms):
    return trimesh.boolean.union(ms, engine="manifold")

def diff(base, cuts):
    return trimesh.boolean.difference([base] + cuts, engine="manifold")

def save(mesh, name, check=True):
    if check:
        assert mesh.is_watertight, f"{name} not watertight"
    mesh.export(f"{OUT}/{name}.stl")
    vol = f"vol={mesh.volume/1000:.1f}cm3" if check else "assembly"
    print(f"{name}.stl  {vol}  tris={len(mesh.faces)}")

# ================= POUCH CHASSIS =================
base_l, base_w = POUCH_L - 12, POUCH_W - 12
base_t, rim_h, rim_t = 3, 12, 2
laser_d = 6.4
sv_l, sv_w, sv_well_h = 23.2, 12.6, 17
sv_flange = 32.5
well_at = (base_l - sv_flange - 14, (base_w - sv_w - 5) / 2, base_t)

def tray(l, w, at, wall=1.6, h=6):
    return diff(box(l + 2 * wall, w + 2 * wall, h, at),
                [box(l, w, h, (at[0] + wall, at[1] + wall, at[2] + 1))])

def pen_clip(at):
    body = cyl(13, 8, at)
    return diff(body, [cyl(10, 10, (at[0], at[1], at[2] - 1)),
                       box(14, 8, 10, (at[0] - 7, at[1], at[2] - 1))])

def chassis():
    plate = box(base_l, base_w, base_t)
    rim = diff(box(base_l, base_w, rim_h),
               [box(base_l - 2 * rim_t, base_w - 2 * rim_t, rim_h + 2,
                    (rim_t, rim_t, -1))])
    # nose post + alignment ring at beam height (aim out the zipper corner)
    post = box(4, 14, BEAM_H, (base_l - 4, base_w / 2 - 7, 0))
    nose = rot(cyl(laser_d + 5, 6), 90, [0, 1, 0])
    nose.apply_translation([base_l - 1 + 3, base_w / 2, BEAM_H])
    well = box(sv_flange + 4, sv_w + 5, sv_well_h, well_at)
    trays = [tray(52, 35, (6, (base_w - 35) / 2 - 1.6, base_t)),
             tray(28, 18, (68, 8, base_t)),
             tray(23.5, 19, (68, base_w - 19 - 12, base_t))]
    clips = [pen_clip((x, base_w - 8, rim_h)) for x in (30, 75, 120)]
    solid = union([plate, rim, post, nose, well] + trays + clips)

    cuts = []
    for fx in (0.25, 0.6):   # washer weight pockets
        cuts.append(cyl(25.8, 3.6, (base_l * fx, base_w / 2, base_t - 2.6)))
    bore = rot(cyl(laser_d + 2, 16), 90, [0, 1, 0])   # beam bore
    bore.apply_translation([base_l - 4 + 8, base_w / 2, BEAM_H])
    cuts.append(bore)
    cuts.append(box(sv_l, sv_w, sv_well_h + 2,        # servo pocket
                    (well_at[0] + (sv_flange + 4 - sv_l) / 2,
                     well_at[1] + 2.5, well_at[2] - 1)))
    cx = well_at[0] + (sv_flange + 4) / 2
    for dx in (-(sv_flange / 2 - 2), sv_flange / 2 - 2):
        cuts.append(cyl(2.2, 10, (cx + dx, well_at[1] + 2.5 + sv_w / 2,
                                  well_at[2] + sv_well_h - 8)))
    return diff(solid, cuts)

def tilt_bracket():
    fl, fw = sv_l + 6, sv_w + 6
    solid = union([box(fl, fw, 3),
                   box(3, fw, sv_well_h),
                   box(3, fw, sv_well_h, (fl - 3, 0, 0))])
    cuts = [box(sv_l, sv_w, 5, (3, 3, -1)),
            cyl(2.2, 5, (fl / 2, fw / 2, -1)),
            cyl(1.8, 5, (fl / 2 + 4, fw / 2, -1)),
            cyl(1.8, 5, (fl / 2 - 4, fw / 2, -1))]
    return diff(solid, cuts)

def laser_clip():
    solid = union([cyl(laser_d + 4, 10),
                   box(8, 3, 10, (-4, -(laser_d + 4) / 2 - 3, 0))])
    screw = rot(cyl(1.8, 8), 90, [1, 0, 0])
    screw.apply_translation([0, -(laser_d + 4) / 2 - 2, 5])
    cuts = [cyl(laser_d, 12, (0, 0, -1)),
            box(4, laser_d, 12, (-2, 0, -1)),
            screw]
    return diff(solid, cuts)

# ================= BOTTLE TOP — LOW PROFILE =================
# The servo sinks into the bottle neck inside a "bucket" so the visible
# shell is only ~26mm tall (a normal-looking chug cap). z=0 = bottle rim.
od, wall = BOTTLE_OD, 2.4
band_h, dome_h, cap_t = 16, 8, 2.5     # shell: 16 + 8 + 2.5 ≈ 26mm visible
slot_h, slot_z, spine = 6, 3.5, 60     # slot in shell-local z
tilt_down, fit_tol = 5, 0.4
top_d = od * 0.72
bucket_depth = 40                       # how far the bucket hangs into the neck
opening_d = 32                          # rotation opening in the bucket flange

def shell():
    """Shell-local z: base at 0 (sits on the bucket flange at abs z=3)."""
    outer = union([cyl(od, band_h, sections=128),
                   frustum(od, top_d, dome_h, (0, 0, band_h), sections=128),
                   cyl(top_d, cap_t, (0, 0, band_h + dome_h - 0.5), sections=128)])
    inner = union([cyl(od - 2 * wall, band_h + 1, (0, 0, -1), sections=128),
                   frustum(od - 2 * wall, top_d - 2 * wall, dome_h,
                           (0, 0, band_h), sections=128)])
    half_w = (od / 2 + 2) * np.sin(np.radians(spine / 2))
    slot = diff(cyl(od + 4, slot_h, (0, 0, slot_z), sections=128),
                [box(od / 2 + 3, half_w * 2, slot_h + 2,
                     (0, -half_w, slot_z - 1))])
    return diff(outer, [inner, slot])

def bucket():
    """Plug + servo carrier in one part. Flange rests on the bottle rim,
    stem hangs into the neck, servo stands at the bottom, shaft up."""
    stem_d = MOUTH_ID - fit_tol
    solid = union([
        cyl(od, 3, sections=128),                                  # rim flange
        # register ring the shell friction-fits over
        diff(cyl(od - 2 * wall - 0.6, 2, (0, 0, 3), sections=128),
             [cyl(od - 2 * wall - 7, 2.4, (0, 0, 2.9), sections=128)]),
        cyl(stem_d, bucket_depth, (0, 0, -bucket_depth), sections=128),
        frustum(stem_d - 2, stem_d, 2, (0, 0, -bucket_depth), sections=128),
    ])
    cuts = [
        # hollow interior (floor 2.4 stays; flange underside is the ceiling)
        cyl(stem_d - 2 * wall, bucket_depth - 2.4,
            (0, 0, -bucket_depth + 2.4), sections=128),
        # central rotation opening through the flange
        cyl(opening_d, 6, (0, 0, -1), sections=128),
        # servo pocket: shaft lands on the center axis
        box(sv_l, sv_w, 5, (-sv_l + 17.4, -sv_w / 2, -bucket_depth + 5.4)),
    ]
    # hollow first, then add the servo mount block on the fresh floor
    solid = diff(solid, [cuts[0]])
    solid = union([solid,
                   box(sv_l + 6, sv_w + 6, 6, (-8.8, -(sv_w + 6) / 2,
                                               -bucket_depth + 2.4))])
    return diff(solid, cuts[1:])

def carriage():
    """Screws onto the servo horn (~z-8); riser climbs through the flange
    opening; laser rides just above the flange at slot height, 5° down."""
    ring = rot(cyl(laser_d + 4, 12, (0, 0, -6)), 90 + tilt_down, [0, 1, 0])
    ring.apply_translation([17.5, 0, 9.5])
    solid = union([cyl(16, 2.5, (0, 0, -8)),           # horn plate
                   box(4, 3, 17, (5.5, -1.5, -8)),     # riser
                   box(12, 3, 3, (5.5, -1.5, 6)),      # jib out to the laser
                   ring])
    bore = rot(cyl(laser_d, 15, (0, 0, -7.5)), 90 + tilt_down, [0, 1, 0])
    bore.apply_translation([17.5, 0, 9.5])
    cuts = [bore, cyl(2.4, 6, (0, 0, -8.5))]
    for a in (0, 90, 180, 270):
        r = np.radians(a)
        cuts.append(cyl(1.8, 6, (5 * np.cos(r), 5 * np.sin(r), -8.5)))
    return diff(solid, cuts)

# ================= MOCK COMPONENTS (assembly views only) =================
def mock_servo(at, upright=True):
    """SG90 body 22.5x11.8x22.7 + shaft."""
    if upright:
        body = box(22.5, 11.8, 22.7, at)
        shaft = cyl(4.8, 4, (at[0] + 5.9, at[1] + 5.9, at[2] + 22.7))
        return trimesh.util.concatenate([body, shaft])
    body = box(22.5, 22.7, 11.8, at)   # lying on its side
    shaft = rot(cyl(4.8, 4), 90, [1, 0, 0])
    shaft.apply_translation([at[0] + 5.9, at[1] - 0.1, at[2] + 5.9])
    return trimesh.util.concatenate([body, shaft])

def mock_laser(at, along="x", length=28):
    m = cyl(6, length, (0, 0, -length / 2))
    if along == "x":
        rot(m, 90, [0, 1, 0])
    m.apply_translation(list(at))
    return m

def pouch_assembly():
    parts = [chassis()]
    sx = well_at[0] + (sv_flange + 4 - sv_l) / 2
    sy = well_at[1] + 2.9
    parts.append(mock_servo((sx, sy, base_t + 0.5)))                 # pan servo
    tb = tilt_bracket()
    tb.apply_translation([sx - 3, sy - 3, base_t + 28])              # bracket on horn
    parts.append(tb)
    parts.append(mock_servo((sx, sy - 5, base_t + 31.5), upright=False))
    parts.append(mock_laser((base_l - 20, base_w / 2, BEAM_H), "x", 44))
    lc = laser_clip()
    rot(lc, 90, [0, 1, 0])
    lc.apply_translation([base_l - 34, base_w / 2, BEAM_H])
    parts.append(lc)
    parts.append(box(50, 34, 10, (7.6, (base_w - 34) / 2, base_t + 1)))   # LiPo
    parts.append(box(28, 18, 4, (69.6, 9.6, base_t + 1)))                 # TP4056
    parts.append(box(23.5, 19, 4, (69.6, base_w - 19 - 10.4, base_t + 1)))  # ESP32
    for fx in (0.25, 0.6):
        parts.append(cyl(25.4, 2.4, (base_l * fx, base_w / 2, base_t - 2.5)))
    return parts

def bottle_assembly():
    """Assembled on a mock bottle top; shell is listed last (render it
    translucent). z=0 is the bottle rim."""
    bottle = trimesh.util.concatenate([
        cyl(od, 70, (0, 0, -95), sections=96),
        frustum(od, MOUTH_ID + 8, 20, (0, 0, -25), sections=96),
        cyl(MOUTH_ID + 8, 5, (0, 0, -5), sections=96)])
    parts = [bottle, bucket()]
    parts.append(mock_servo((-5.65, -5.9, -bucket_depth + 5.4)))   # in the bucket
    parts.append(carriage())
    lm = mock_laser((27, 0, 8.7), "x", 18)
    rot(lm, tilt_down, [0, 1, 0], point=(27, 0, 8.7))
    parts.append(lm)
    # slim electronics standing in the bucket crescents beside the servo
    parts.append(box(3.5, 22.5, 18, (-20, -11, -bucket_depth + 4)))  # ESP32-C3
    parts.append(box(4, 30, 12, (16, -15, -bucket_depth + 4)))       # LiPo 401230
    parts.append(box(23, 3.5, 16, (-11.5, 18, -bucket_depth + 4)))   # TP4056
    sh = shell(); sh.apply_translation([0, 0, 3]);                  parts.append(sh)
    return parts

# ================= build everything =================
if __name__ == "__main__":
    save(chassis(), "pouch_chassis")
    save(tilt_bracket(), "pouch_tilt_bracket")
    save(laser_clip(), "laser_clip")
    save(shell(), "bottle_shell")
    save(bucket(), "bottle_bucket")
    save(carriage(), "bottle_carriage")
    save(trimesh.util.concatenate(pouch_assembly()), "ASSEMBLED_pouch",
         check=False)
    save(trimesh.util.concatenate(bottle_assembly()), "ASSEMBLED_bottle",
         check=False)
    print("done")
