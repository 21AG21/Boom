#!/usr/bin/env python3
"""Breathe Stone — parametric prototype geometry -> STL.

A palm-sized worry stone whose top pad rises and falls on a breathing
cadence. A micro servo turns a crank that lifts a piston; the piston
carries a soft dome your thumb rests on. Match your breath to the dome and
your nervous system follows.

This generator is written in the same idiom as the repo's
`hardware/generate_stls.py` (trimesh + manifold booleans, watertight
checks). Edit the measurements block, run, and fresh STLs land in
`ideas/breathe-stone/hardware/stl/`.

    pip install trimesh manifold3d scipy numpy
    python3 ideas/breathe-stone/hardware/breathe_stone.py

Printable parts:
    stone_base    – lower shell: servo well, battery bay, PCB shelf, switch
    stone_lid     – upper shell: dome aperture, piston guide, label window
    piston        – rides the guide bore, carries the dome
    crank         – presses on the servo spline, lifts the piston via a pin
    dome          – thin spherical cap (print in TPU); the touch surface
    ASSEMBLED_stone – all of the above in place (visualization only)

Production note: the SG90 is a stand-in. A flat coreless pager motor or a
nitinol (shape-memory) wire actuator shrinks the whole stone to ~22 mm thick
and makes it silent — see patent/provisional-draft.md.
"""
import os
import numpy as np
import trimesh
from trimesh.creation import box as _box, cylinder as _cyl, icosphere as _ico

# ================= MEASUREMENTS (edit these) =================
STONE_L = 78          # length  (x) – long axis of the pebble
STONE_W = 58          # width   (y)
STONE_H = 38          # total thickness (z). Prototype is chunky; the
                      # production actuator drops this to ~22 mm.
WALL    = 2.4
PART_Z  = 15          # parting plane: base is z<PART_Z, lid is above

DOME_D    = 36        # breathing dome diameter (thumb pad)
DOME_RISE = 9         # dome height (cap sagitta)
TRAVEL    = 4         # how far the pad travels between exhale and inhale
PISTON_D  = 24        # piston / guide-bore diameter

# SG90 stand-in envelope
SV_L, SV_W, SV_H = 22.8, 12.2, 22.9   # body, standing upright, shaft up
SV_SHAFT_Z       = 22.9               # shaft top above the servo floor
FIT = 0.35                             # generic clearance

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stl")
os.makedirs(OUT, exist_ok=True)

# ---------------- helpers (same style as the turret generator) ----------
def box(l, w, h, at=(0, 0, 0)):
    b = _box(extents=[l, w, h])
    b.apply_translation([at[0] + l / 2, at[1] + w / 2, at[2] + h / 2])
    return b

def cyl(d, h, at=(0, 0, 0), sections=96):
    c = _cyl(radius=d / 2, height=h, sections=sections)
    c.apply_translation([at[0], at[1], at[2] + h / 2])
    return c

def sphere(d, at=(0, 0, 0), subd=3):
    s = _ico(subdivisions=subd, radius=d / 2)
    s.apply_translation(list(at))
    return s

def rot(m, deg, axis, point=(0, 0, 0)):
    m.apply_transform(trimesh.transformations.rotation_matrix(
        np.radians(deg), axis, point))
    return m

def union(ms):
    return trimesh.boolean.union(ms, engine="manifold")

def diff(base, cuts):
    return trimesh.boolean.difference([base] + cuts, engine="manifold")

def inter(ms):
    return trimesh.boolean.intersection(ms, engine="manifold")

def scaled(mesh, fx, fy, fz, about):
    m = mesh.copy()
    T = np.eye(4)
    T[0, 0], T[1, 1], T[2, 2] = fx, fy, fz
    T[0, 3] = about[0] * (1 - fx)
    T[1, 3] = about[1] * (1 - fy)
    T[2, 3] = about[2] * (1 - fz)
    m.apply_transform(T)
    return m

def save(mesh, name, check=True):
    if check:
        assert mesh.is_watertight, f"{name} not watertight"
    mesh.export(f"{OUT}/{name}.stl")
    vol = f"vol={mesh.volume/1000:.1f}cm3" if check else "assembly"
    print(f"{name}.stl  {vol}  tris={len(mesh.faces)}")

# ================= PEBBLE SHELL =================
# Organic pebble = convex hull of eight spheres. Bottom spheres are large and
# sit tangent to z=0 (flat, stable base); top spheres are inset and lifted so
# the stone domes gently toward the thumb.
def pebble_solid():
    ax, ay = STONE_L / 2 - 12, STONE_W / 2 - 12
    r_lo, r_hi = 12, 9
    anchors = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            anchors.append(sphere(2 * r_lo, (sx * ax, sy * ay, r_lo)))
            anchors.append(sphere(2 * r_hi,
                                  (sx * (ax - 4), sy * (ay - 4),
                                   STONE_H - r_hi)))
    hull = trimesh.util.concatenate(anchors).convex_hull
    # guarantee a dead-flat base
    return inter([hull, box(STONE_L + 20, STONE_W + 20, STONE_H + 20,
                            (-(STONE_L + 20) / 2, -(STONE_W + 20) / 2, 0))])

def hollow_shell():
    outer = pebble_solid()
    e = outer.extents
    c = outer.bounds.mean(axis=0)
    inner = scaled(outer,
                   (e[0] - 2 * WALL) / e[0],
                   (e[1] - 2 * WALL) / e[1],
                   (e[2] - 2 * WALL) / e[2],
                   c)
    # keep a solid floor: trim the inner cavity to start at WALL
    inner = inter([inner, box(STONE_L + 20, STONE_W + 20, STONE_H + 20,
                              (-(STONE_L + 20) / 2, -(STONE_W + 20) / 2, WALL))])
    return outer, diff(outer, [inner])

_OUTER, _SHELL = hollow_shell()

def _cut_lo():
    return box(STONE_L + 20, STONE_W + 20, PART_Z,
               (-(STONE_L + 20) / 2, -(STONE_W + 20) / 2, 0))

def _cut_hi():
    return box(STONE_L + 20, STONE_W + 20, STONE_H + 20 - PART_Z,
               (-(STONE_L + 20) / 2, -(STONE_W + 20) / 2, PART_Z))

# component placement (shared by base features and assembly)
SV_X, SV_Y = -4, 0                      # servo body corner region (centered-ish)
sv_at = (SV_X - SV_L / 2, SV_Y - SV_W / 2, WALL)
BAT_L, BAT_W, BAT_H = 30, 13, 6         # 401230-class LiPo bay
TP_L, TP_W = 24, 17.5                   # TP4056 board
PCB_L, PCB_W = 23.6, 18.2               # ESP32-C3 SuperMini
BOSS = [( STONE_L / 2 - 9, 0),
        (-STONE_L / 2 + 11,  STONE_W / 2 - 10),
        (-STONE_L / 2 + 11, -STONE_W / 2 + 10)]

def tray(l, w, at, wall=1.6, h=6):
    return diff(box(l + 2 * wall, w + 2 * wall, h, at),
                [box(l, w, h, (at[0] + wall, at[1] + wall, at[2] + 1))])

def stone_base():
    solid = inter([_SHELL, _cut_lo()])
    # servo well (four walls up from the floor)
    well = box(SV_L + 2 * 1.6, SV_W + 2 * 1.6, PART_Z - WALL,
               (sv_at[0] - 1.6, sv_at[1] - 1.6, WALL))
    # battery bay + component shelves along the back
    bay = tray(BAT_L, BAT_W, (-BAT_L / 2, STONE_W / 2 - BAT_W - 6, WALL),
               h=PART_Z - WALL - 3)
    shelf_tp = tray(TP_L, TP_W, (STONE_L / 2 - TP_L - 8,
                                 -STONE_W / 2 + 6, WALL), h=5)
    bosses = [cyl(7, PART_Z - WALL, (bx, by, WALL)) for bx, by in BOSS]
    solid = union([solid, well, bay, shelf_tp] + bosses)

    cuts = []
    # servo pocket + horn screw clearance
    cuts.append(box(SV_L, SV_W, SV_H + 2, (sv_at[0], sv_at[1], WALL - 1)))
    # cable notch from the servo well toward the electronics
    cuts.append(box(6, 4, 8, (SV_X - 3, SV_Y + SV_W / 2, WALL + 2)))
    # slide-switch slot in the side wall (cadence select)
    cuts.append(box(13, WALL + 3, 6, (-6.5, -STONE_W / 2 - 1, WALL + 3)))
    # USB-C charge port notch (TP4056)
    cuts.append(box(10, WALL + 3, 5, (STONE_L / 2 - 24, -STONE_W / 2 - 1, WALL + 1)))
    # screw pilot holes in the bosses
    for bx, by in BOSS:
        cuts.append(cyl(2.4, PART_Z, (bx, by, WALL - 0.5)))
    # two ballast-washer pockets in the floor (heft = "worry stone" feel)
    for fx in (-0.24, 0.24):
        cuts.append(cyl(20.2, 2.6, (STONE_L * fx * 0.5, 0, -0.01)))
    return diff(solid, cuts)

def stone_lid():
    solid = inter([_SHELL, _cut_hi()])
    # inner guide tube the piston slides in
    guide = cyl(PISTON_D + 2 * 2.2, 12, (0, 0, PART_Z - 1))
    solid = union([solid, guide])
    cuts = []
    # dome aperture through the top with a capture groove for the dome lip
    top_z = STONE_H
    cuts.append(cyl(DOME_D, STONE_H, (0, 0, PART_Z - 2)))          # opening
    cuts.append(cyl(DOME_D + 3, 1.6, (0, 0, top_z - 1.6)))         # lip groove
    # piston guide bore
    cuts.append(cyl(PISTON_D + 2 * FIT, 30, (0, 0, PART_Z - 3)))
    # boss screw holes (countersunk from the top)
    for bx, by in BOSS:
        cuts.append(cyl(3.4, STONE_H, (bx, by, PART_Z - 1)))
        cuts.append(cyl(6.4, 3, (bx, by, top_z - 3)))
    # small recessed label window on the front skirt
    cuts.append(box(26, 0.8, 9, (-13, -STONE_W / 2 + 0.2, PART_Z + 2)))
    return diff(solid, cuts)

# ================= PISTON =================
# Rides the guide bore; flat shoulder limits travel; bottom socket takes the
# crank pin; a key flat stops rotation so the dome never twists.
def piston():
    body = cyl(PISTON_D, 20)
    shoulder = cyl(PISTON_D + 5, 3, (0, 0, 17))            # travel stop
    key = box(3, PISTON_D + 6, 14, (-1.5, -(PISTON_D + 6) / 2, 0))
    solid = union([body, shoulder, key])
    cuts = [
        cyl(PISTON_D - 2 * 2, 15, (0, 0, 6)),              # lighten from the top
        # crank-pin socket across the bottom (a slot the pin rides in)
        box(PISTON_D + 2, 4.2, 5, (-(PISTON_D + 2) / 2, -2.1, 1.5)),
        cyl(3.2, 6, (0, 0, -0.5)),                         # pin clearance
    ]
    return diff(solid, cuts)

# ================= CRANK =================
# Presses onto the SG90 spline; the arm carries a pin at radius e so half a
# turn lifts the piston by 2*e = TRAVEL. Sine-eased in firmware.
def crank():
    e = TRAVEL / 2
    hub = cyl(9, 6)
    arm = box(16, 6, 4, (0, -3, 1))
    pin = cyl(3.0, 9, (e + 6, 0, 4))                      # up-standing pin
    solid = union([hub, arm, pin])
    cuts = [
        cyl(4.9, 6, (0, 0, -0.5)),                        # spline hole (press fit)
        cyl(1.6, 8, (0, 0, -0.5)),                        # retainer screw pilot
    ]
    return diff(solid, cuts)

# ================= DOME =================
# Thin spherical-cap membrane (print in TPU). Outer cap minus inner cap, with
# a bottom lip that snaps into the lid groove.
def _cap(d, rise, at=(0, 0, 0)):
    # a sphere squashed to (d, d, 2*rise), keep the top half above its equator
    R = d / 2
    s = sphere(2 * R, subd=4)
    s = scaled(s, 1, 1, rise / R, (0, 0, 0))
    s = inter([s, box(d + 6, d + 6, rise + 2,
                      (-(d + 6) / 2, -(d + 6) / 2, 0))])
    s.apply_translation(list(at))
    return s

def dome():
    outer = _cap(DOME_D, DOME_RISE)
    inner = _cap(DOME_D - 2 * 1.4, DOME_RISE - 1.4, (0, 0, 0))
    shell = diff(outer, [inner])
    lip = diff(cyl(DOME_D + 2.6, 1.6), [cyl(DOME_D - 1.5, 2, (0, 0, -0.2))])
    # seat the piston: a small inner boss the piston top bonds to
    boss = diff(cyl(PISTON_D - 1, 3), [cyl(PISTON_D - 6, 3.5, (0, 0, -0.2))])
    return union([shell, lip, boss])

# ================= MOCKS + ASSEMBLY =================
def mock_servo(at):
    body = box(SV_L, SV_W, SV_H, at)
    tab = box(SV_L + 10, SV_W, 2.5, (at[0] - 5, at[1], at[2] + 15.8))
    shaft = cyl(4.8, 4, (at[0] + SV_L / 2 - 6, at[1] + SV_W / 2, at[2] + SV_H))
    return trimesh.util.concatenate([body, tab, shaft])

def assembly():
    parts = [stone_base()]
    parts.append(mock_servo(sv_at))
    shaft_top = WALL + SV_SHAFT_Z
    cr = crank()
    cr.apply_translation([SV_X + SV_L / 2 - 6, SV_Y, shaft_top])
    parts.append(cr)
    pst = piston()
    pst.apply_translation([0, 0, PART_Z - 2])
    parts.append(pst)
    lid = stone_lid()
    parts.append(lid)
    dm = dome()
    dm.apply_translation([0, 0, STONE_H - 1.6])
    parts.append(dm)
    # electronics mocks
    parts.append(box(BAT_L, BAT_W, BAT_H,
                     (-BAT_L / 2, STONE_W / 2 - BAT_W - 6, WALL + 1)))     # LiPo
    parts.append(box(TP_L, TP_W, 3.5,
                     (STONE_L / 2 - TP_L - 8, -STONE_W / 2 + 6, WALL + 1)))  # TP4056
    return parts

# ================= build everything =================
if __name__ == "__main__":
    save(stone_base(), "stone_base")
    save(stone_lid(),  "stone_lid")
    save(piston(),     "piston")
    save(crank(),      "crank")
    save(dome(),       "dome")
    save(trimesh.util.concatenate(assembly()), "ASSEMBLED_stone", check=False)
    print("done")
