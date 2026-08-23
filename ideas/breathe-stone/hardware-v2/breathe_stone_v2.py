#!/usr/bin/env python3
"""Breathe Stone v2 — silent shape-memory (nitinol) actuator.

v1 used an SG90 servo + crank: it works, but a servo hunts and buzzes and
forces a chunky 38 mm body. v2 replaces the whole motor with a nitinol
(shape-memory-alloy) wire. The key insight: a breath is SLOW (4-8 per
minute), and nitinol is "slow" only because it is cooling-limited — so the
one thing that makes SMA a poor general actuator makes it a perfect one
*here*. The result is:

    - SILENT   — no motor, no gears, nothing to hunt or hold.
    - THIN     — no upright servo, so the body drops to ~24 mm (a real
                 worry-stone, not a hockey puck).
    - SOLID-STATE — one wire, one MOSFET, a return spring.

Mechanism: a nitinol wire, anchored in the base and routed as a hairpin,
contracts when a MOSFET pulses current through it. It pulls the short (input)
arm of a bell crank; the long (output) arm lifts the piston that carries the
dome — inhale. Current off, the wire cools, and a light return spring lowers
the dome — exhale. The firmware shapes the current to the breathing cadence.

Travel math (set your wire length from this):
    output_travel = b * dθ         (b = output-arm length)
    wire_contract = a * dθ         (a = input-arm length)
    wire_length   = wire_contract / 0.04     (nitinol shortens ~4%)
  => wire_length ≈ 25 * a * output_travel / b
    With a=5, b=14, output_travel=4 mm -> wire ≈ 36 mm (route as a hairpin).

Same idiom as the repo's other generators (trimesh + manifold booleans,
watertight checks). Parts land in hardware-v2/stl/.

    pip install trimesh manifold3d scipy numpy matplotlib
    python3 ideas/breathe-stone/hardware-v2/breathe_stone_v2.py
"""
import os
import numpy as np
import trimesh
from trimesh.creation import box as _box, cylinder as _cyl, icosphere as _ico

# ================= MEASUREMENTS =================
STONE_L = 78          # x
STONE_W = 56          # y
STONE_H = 24          # z — thin, a real worry stone
WALL    = 2.4
PART_Z  = 12          # parting plane

DOME_D    = 34
DOME_RISE = 8
TRAVEL    = 4
PISTON_D  = 22

# bell crank
PIV_X   = 14          # pivot x (piston sits at x=0)
ARM_IN  = 5           # a: vertical input arm (wire pulls here)
ARM_OUT = PIV_X       # b: horizontal output arm reaches the piston at x=0
PIV_Z   = 6           # pivot height above the floor
WIRE_D  = 0.6         # nitinol wire (0.012") + a little room in the channel
FIT     = 0.35

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stl")
os.makedirs(OUT, exist_ok=True)

# ---------------- helpers (repo idiom) ----------------
def box(l, w, h, at=(0, 0, 0)):
    b = _box(extents=[l, w, h]); b.apply_translation([at[0]+l/2, at[1]+w/2, at[2]+h/2]); return b

def cyl(d, h, at=(0, 0, 0), sections=96):
    c = _cyl(radius=d/2, height=h, sections=sections); c.apply_translation([at[0], at[1], at[2]+h/2]); return c

def sphere(d, at=(0, 0, 0), subd=3):
    s = _ico(subdivisions=subd, radius=d/2); s.apply_translation(list(at)); return s

def rot(m, deg, axis, point=(0, 0, 0)):
    m.apply_transform(trimesh.transformations.rotation_matrix(np.radians(deg), axis, point)); return m

def union(ms):  return trimesh.boolean.union(ms, engine="manifold")
def diff(b, c): return trimesh.boolean.difference([b]+c, engine="manifold")
def inter(ms):  return trimesh.boolean.intersection(ms, engine="manifold")

def scaled(mesh, fx, fy, fz, about):
    m = mesh.copy(); T = np.eye(4); T[0,0], T[1,1], T[2,2] = fx, fy, fz
    T[0,3]=about[0]*(1-fx); T[1,3]=about[1]*(1-fy); T[2,3]=about[2]*(1-fz)
    m.apply_transform(T); return m

def save(mesh, name, check=True):
    if check: assert mesh.is_watertight, f"{name} not watertight"
    mesh.export(f"{OUT}/{name}.stl")
    vol = f"vol={mesh.volume/1000:.1f}cm3" if check else "assembly"
    print(f"{name}.stl  {vol}  tris={len(mesh.faces)}")

# ================= pebble shell (thin) =================
def pebble_solid():
    ax, ay = STONE_L/2-12, STONE_W/2-12
    r_lo, r_hi = 12, 8
    anchors = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            anchors.append(sphere(2*r_lo, (sx*ax, sy*ay, r_lo)))
            anchors.append(sphere(2*r_hi, (sx*(ax-4), sy*(ay-4), STONE_H-r_hi)))
    hull = trimesh.util.concatenate(anchors).convex_hull
    return inter([hull, box(STONE_L+20, STONE_W+20, STONE_H+20,
                            (-(STONE_L+20)/2, -(STONE_W+20)/2, 0))])

def hollow_shell():
    outer = pebble_solid(); e = outer.extents; c = outer.bounds.mean(axis=0)
    inner = scaled(outer, (e[0]-2*WALL)/e[0], (e[1]-2*WALL)/e[1], (e[2]-2*WALL)/e[2], c)
    inner = inter([inner, box(STONE_L+20, STONE_W+20, STONE_H+20,
                              (-(STONE_L+20)/2, -(STONE_W+20)/2, WALL))])
    return outer, diff(outer, [inner])

_OUTER, _SHELL = hollow_shell()
def _cut_lo(): return box(STONE_L+20, STONE_W+20, PART_Z, (-(STONE_L+20)/2, -(STONE_W+20)/2, 0))
def _cut_hi(): return box(STONE_L+20, STONE_W+20, STONE_H+20-PART_Z, (-(STONE_L+20)/2, -(STONE_W+20)/2, PART_Z))

BOSS = [(STONE_L/2-9, 0), (-STONE_L/2+11, STONE_W/2-10), (-STONE_L/2+11, -STONE_W/2+10)]
BAT_L, BAT_W = 30, 13
PCB_L, PCB_W = 23.6, 18.2

def tray(l, w, at, wall=1.6, h=6):
    return diff(box(l+2*wall, w+2*wall, h, at), [box(l, w, h, (at[0]+wall, at[1]+wall, at[2]+1))])

def base():
    solid = inter([_SHELL, _cut_lo()])
    add = []
    # pivot fork: two posts straddling y=0 that carry the crank pin
    for sy in (-1, 1):
        add.append(box(5, 3, PIV_Z+5, (PIV_X-2.5, sy*4-1.5, WALL)))
    # nitinol anchor post at the +x end (crimp the hairpin here)
    add.append(cyl(8, PART_Z-WALL, (STONE_L/2-9, 0, WALL)))
    # return-spring seat under the piston centre
    add.append(cyl(9, 3, (0, 0, WALL)))
    # electronics shelves: ESP32-C3 + a small MOSFET/driver board + LiPo
    add.append(tray(PCB_L, PCB_W, (-STONE_L/2+7, -PCB_W/2, WALL), h=PART_Z-WALL-3))
    add.append(tray(BAT_L, BAT_W, (-6, STONE_W/2-BAT_W-6, WALL), h=PART_Z-WALL-3))
    bosses = [cyl(7, PART_Z-WALL, (bx, by, WALL)) for bx, by in BOSS]
    solid = union([solid]+add+bosses)

    cuts = []
    # crank-pin cross hole through the fork
    pin = rot(cyl(2.2, 14, (0, 0, 0)), 90, [1, 0, 0]); pin.apply_translation([PIV_X, 7, WALL+PIV_Z]); cuts.append(pin)
    # wire channel: a shallow trough from the crank toward the anchor
    cuts.append(box(STONE_L/2-9-PIV_X, WIRE_D+1.4, WIRE_D+1.2, (PIV_X, -(WIRE_D+1.4)/2, WALL+PIV_Z-ARM_IN)))
    # anchor: vertical wire hole + a set-screw pocket to crimp it
    cuts.append(cyl(WIRE_D+0.4, PART_Z, (STONE_L/2-9, 0, WALL-0.5)))
    cuts.append(box(3, 3, 4, (STONE_L/2-9-1.5, -1.5, WALL+3)))
    # return-spring pocket
    cuts.append(cyl(6.2, 4.5, (0, 0, WALL-0.5)))
    # side hole for the USB-C charge port and a button
    cuts.append(box(10, WALL+3, 5, (-STONE_L/2-1, -5, WALL+2)))
    cuts.append(cyl(3.6, WALL+3, (-STONE_L/2+3, 0, WALL+6)))  # button (through side) approx
    # screw pilots
    for bx, by in BOSS: cuts.append(cyl(2.4, PART_Z, (bx, by, WALL-0.5)))
    return diff(solid, cuts)

def lid():
    solid = inter([_SHELL, _cut_hi()])
    guide = cyl(PISTON_D+2*2.2, 9, (0, 0, PART_Z-1))
    solid = union([solid, guide])
    cuts = []
    top = STONE_H
    cuts.append(cyl(DOME_D, STONE_H, (0, 0, PART_Z-2)))          # dome opening
    cuts.append(cyl(DOME_D+3, 1.6, (0, 0, top-1.6)))            # dome lip groove
    cuts.append(cyl(PISTON_D+2*FIT, 20, (0, 0, PART_Z-3)))      # piston bore
    # clearance slot so the crank's output tip can reach the piston underside
    cuts.append(box(ARM_OUT+6, 8, 6, (0, -4, PART_Z-3)))
    for bx, by in BOSS:
        cuts.append(cyl(3.4, STONE_H, (bx, by, PART_Z-1)))
        cuts.append(cyl(6.4, 3, (bx, by, top-3)))
    cuts.append(box(26, 0.8, 8, (-13, -STONE_W/2+0.2, PART_Z+2)))  # label window
    return diff(solid, cuts)

# ================= piston =================
def piston():
    body = cyl(PISTON_D, 14)
    shoulder = cyl(PISTON_D+5, 3, (0, 0, 11))
    key = box(3, PISTON_D+6, 10, (-1.5, -(PISTON_D+6)/2, 0))
    stem = cyl(5, 5, (0, 0, -5))                                # rides the return spring
    solid = union([body, shoulder, key, stem])
    cuts = [cyl(PISTON_D-4, 10, (0, 0, 5)),                     # lighten
            box(10, 4.2, 4, (-5, -2.1, -0.5))]                 # crank-tip pocket underneath
    return diff(solid, cuts)

# ================= bell crank =================
# L-shaped: vertical input arm (wire pulls its top) + horizontal output arm
# (lifts the piston). Pivots on the base fork pin.
def crank():
    inp = box(4, 4, ARM_IN+4, (-2, -2, -2))                    # up from the pivot
    outp = box(ARM_OUT+3, 4, 4, (-ARM_OUT-1, -2, -2))          # toward the piston (-x)
    hub = cyl(7, 4); hub = rot(hub, 90, [1, 0, 0]); hub.apply_translation([0, 2, 0])
    solid = union([inp, outp, hub])
    cuts = []
    pinhole = rot(cyl(2.3, 8, (0, 0, 0)), 90, [1, 0, 0]); pinhole.apply_translation([0, 4, 0]); cuts.append(pinhole)
    cuts.append(cyl(WIRE_D+0.5, 6, (0, 0, ARM_IN)))            # wire hole at the input tip
    return diff(solid, cuts)

# ================= dome =================
def _cap(d, rise, at=(0, 0, 0)):
    R = d/2; s = sphere(2*R, subd=4); s = scaled(s, 1, 1, rise/R, (0, 0, 0))
    s = inter([s, box(d+6, d+6, rise+2, (-(d+6)/2, -(d+6)/2, 0))]); s.apply_translation(list(at)); return s

def dome():
    outer = _cap(DOME_D, DOME_RISE)
    inner = _cap(DOME_D-2*1.4, DOME_RISE-1.4)
    shell = diff(outer, [inner])
    lip = diff(cyl(DOME_D+2.6, 1.6), [cyl(DOME_D-1.5, 2, (0, 0, -0.2))])
    boss = diff(cyl(PISTON_D-1, 3), [cyl(PISTON_D-6, 3.5, (0, 0, -0.2))])
    return union([shell, lip, boss])

# ================= assembly =================
def assembly():
    parts = [base()]
    cr = crank(); cr.apply_translation([PIV_X, 0, WALL+PIV_Z]); parts.append(cr)
    pst = piston(); pst.apply_translation([0, 0, PART_Z-1]); parts.append(pst)
    parts.append(lid())
    dm = dome(); dm.apply_translation([0, 0, STONE_H-1.6]); parts.append(dm)
    # electronics mocks
    parts.append(box(PCB_L, PCB_W, 4, (-STONE_L/2+7, -PCB_W/2, WALL+1)))      # ESP32-C3
    parts.append(box(14, 12, 3, (-STONE_L/2+7, PCB_W/2+2, WALL+1)))          # MOSFET driver
    parts.append(box(BAT_L, BAT_W, 5, (-6, STONE_W/2-BAT_W-6, WALL+1)))       # LiPo
    # nitinol wire mock: a thin rod from the crank input tip to the anchor
    w = cyl(WIRE_D, STONE_L/2-9-PIV_X, (PIV_X, 0, WALL+PIV_Z-ARM_IN+0.3))
    w = rot(w, 90, [0, 1, 0]); w.apply_translation([0, 0, WALL+PIV_Z-ARM_IN+0.3+0.0])
    parts.append(w)
    return parts

if __name__ == "__main__":
    save(base(),   "v2_base")
    save(lid(),    "v2_lid")
    save(piston(), "v2_piston")
    save(crank(),  "v2_crank")
    save(dome(),   "v2_dome")
    save(trimesh.util.concatenate(assembly()), "ASSEMBLED_v2", check=False)
    print("done")
