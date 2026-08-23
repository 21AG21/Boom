#!/usr/bin/env python3
"""Lull — split-zone breathing squishy, prototype geometry -> STL.

Two zones that never touch (see ../mechanism.md):
  BREATH: a slow gearmotor turns a breath-profiled CAM; the cam lifts a
          FOLLOWER, which pushes a PLATEN through an "authority" spring
          (the slip-clutch); the platen drives a sealed FOAM DOME.
  FIDGET: a separate sealed GEL LOBE on the rim, kneaded independently.

Printable parts (this file):
    lull_base      lower shell: motor pocket, 2xAAA bay, follower guide,
                   authority-spring pocket, screw bosses, switch slot
    lull_lid       upper shell: big dome opening + capture groove, a SEPARATE
                   lobe opening on the rim, follower clearance, label window
    lull_cam       the breath-shaped disc (its edge = the 4-1-6 waveform)
    lull_follower  rides the cam, seats the authority spring
    lull_platen    disc bonded under the foam dome
    ASSEMBLED_lull all of the above + bought-part mocks (motor, AAA, dome, lobe)

Bought / cast (not printed rigid): the closed-cell silicone foam dome, the
NeeDoh-style gel lobe, the compression "authority" spring, N20 gearmotor,
2xAAA holder. See ../build-guide.md.

    pip install trimesh manifold3d scipy numpy matplotlib
    python3 ideas/lull/hardware/lull.py
"""
import os
import numpy as np
import trimesh
from trimesh.creation import box as _box, cylinder as _cyl, icosphere as _ico

# ================= MEASUREMENTS =================
L, W, H = 82, 60, 30          # pebble length(x) x depth(y) x height(z)
WALL    = 2.4
PART_Z  = 15

DOME_D  = 40                  # breathing dome opening (big top)
LOBE_D  = 22                  # gel-lobe opening on the +x rim
PIS_D   = 10                  # follower piston / guide bore
SPR_D   = 9                   # authority spring bore

# breath cam
CAM_R0, CAM_A, CAM_TH = 8, 3, 3.6
CAM_Y, CAM_Z = 2, 7          # cam centre (x=0)
SHAFT_D = 3.2                 # N20 shaft

# N20 gearmotor envelope (body, lying along -y behind the cam)
MOT_L, MOT_W, MOT_H = 25, 12, 10
FIT = 0.35

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stl")
os.makedirs(OUT, exist_ok=True)

# ---------------- helpers ----------------
def box(l, w, h, at=(0, 0, 0)):
    b = _box(extents=[l, w, h]); b.apply_translation([at[0]+l/2, at[1]+w/2, at[2]+h/2]); return b
def cyl(d, h, at=(0, 0, 0), sec=96):
    c = _cyl(radius=d/2, height=h, sections=sec); c.apply_translation([at[0], at[1], at[2]+h/2]); return c
def sph(d, at=(0, 0, 0), subd=3):
    s = _ico(subdivisions=subd, radius=d/2); s.apply_translation(list(at)); return s
def rot(m, deg, axis, pt=(0, 0, 0)):
    m.apply_transform(trimesh.transformations.rotation_matrix(np.radians(deg), axis, pt)); return m
def union(ms): return trimesh.boolean.union(ms, engine="manifold")
def diff(b, c): return trimesh.boolean.difference([b]+c, engine="manifold")
def inter(ms): return trimesh.boolean.intersection(ms, engine="manifold")
def scaled(mesh, fx, fy, fz, about):
    m = mesh.copy(); T = np.eye(4); T[0,0],T[1,1],T[2,2]=fx,fy,fz
    T[0,3]=about[0]*(1-fx); T[1,3]=about[1]*(1-fy); T[2,3]=about[2]*(1-fz); m.apply_transform(T); return m
def save(mesh, name, check=True):
    if check: assert mesh.is_watertight, f"{name} not watertight"
    mesh.export(f"{OUT}/{name}.stl")
    print(f"{name}.stl  {'vol=%.1fcm3'%(mesh.volume/1000) if check else 'assembly'}  tris={len(mesh.faces)}")

# ---------------- breath waveform (matches firmware + the 3D viewer) ----------------
def breath(p):
    IN, HOLD, OUT_ = 4, 1, 6; T = IN+HOLD+OUT_; s = (p % 1.0)*T
    sm = lambda t: t*t*(3-2*t)
    if s < IN: return sm(s/IN)
    if s < IN+HOLD: return 1.0
    return 1 - sm((s-IN-HOLD)/OUT_)

# ================= pebble shell =================
def pebble_solid():
    ax, ay = L/2-13, W/2-13; r_lo, r_hi = 13, 9; A = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            A.append(sph(2*r_lo, (sx*ax, sy*ay, r_lo)))
            A.append(sph(2*r_hi, (sx*(ax-4), sy*(ay-4), H-r_hi)))
    hull = trimesh.util.concatenate(A).convex_hull
    return inter([hull, box(L+20, W+20, H+20, (-(L+20)/2, -(W+20)/2, 0))])

def hollow():
    outer = pebble_solid(); e = outer.extents; c = outer.bounds.mean(axis=0)
    inner = scaled(outer, (e[0]-2*WALL)/e[0], (e[1]-2*WALL)/e[1], (e[2]-2*WALL)/e[2], c)
    inner = inter([inner, box(L+20, W+20, H+20, (-(L+20)/2, -(W+20)/2, WALL))])
    return outer, diff(outer, [inner])
_OUTER, _SHELL = hollow()
def _lo(): return box(L+20, W+20, PART_Z, (-(L+20)/2, -(W+20)/2, 0))
def _hi(): return box(L+20, W+20, H+20-PART_Z, (-(L+20)/2, -(W+20)/2, PART_Z))

BOSS = [(-L/2+11, 0), (L/2-11, W/2-11), (L/2-11, -(W/2-11))]

def base():
    solid = inter([_SHELL, _lo()])
    add = []
    # motor cradle walls (motor lies along -y behind the cam)
    add.append(box(MOT_L+3.2, MOT_W+3.2, MOT_H+2, (-(MOT_L+3.2)/2, -MOT_L/2-2, WALL)))
    # follower guide post (under the dome centre)
    add.append(cyl(PIS_D+2*2.3, PART_Z-WALL, (0, 0, WALL)))
    # 2xAAA bay along +y (front), holders side by side in x
    add.append(box(48, 26, PART_Z-WALL, (-24, W/2-28, WALL)))
    bosses = [cyl(7, PART_Z-WALL, (bx, by, WALL)) for bx, by in BOSS]
    solid = union([solid]+add+bosses)

    cuts = []
    cuts.append(box(MOT_L, MOT_W, MOT_H, (-MOT_L/2, -MOT_L/2-0.4, WALL+1)))           # motor pocket
    cuts.append(box(6, 8, 8, (-3, -2, WALL+3)))                                       # cam window in cradle
    cuts.append(cyl(PIS_D+2*FIT, PART_Z, (0, 0, WALL+1)))                             # follower bore
    # AAA channels (2x Ø10.7 x 46 along x)
    for yy in (W/2-22, W/2-11):
        ch = rot(cyl(10.7, 46), 90, [0, 1, 0]); ch.apply_translation([0, yy, WALL+7]); cuts.append(ch)
    cuts.append(box(13, 30, 6, (-6.5, -W/2-1, WALL+3)))                               # slide-switch slot (back wall)
    cuts.append(box(12, 8, 4, (-6, W/2-4, WALL+1)))                                   # wire pass to battery
    for bx, by in BOSS: cuts.append(cyl(2.4, PART_Z, (bx, by, WALL-0.5)))
    for fx in (-0.28, 0.28): cuts.append(cyl(20.2, 2.6, (L*fx*0.5, -W*0.18, -0.01)))  # ballast pockets
    return diff(solid, cuts)

def lid():
    solid = inter([_SHELL, _hi()])
    solid = union([solid, cyl(DOME_D+2*2.2, 7, (0, 0, PART_Z-1))])                    # dome collar
    cuts = []
    cuts.append(cyl(DOME_D, H, (0, 0, PART_Z-2)))                                     # dome opening
    cuts.append(cyl(DOME_D+3, 1.8, (0, 0, H-1.8)))                                    # dome lip groove
    cuts.append(cyl(PIS_D+2*FIT+1, 30, (0, 0, PART_Z-3)))                             # follower/spring clearance
    # separate gel-lobe opening on the +x rim
    lobe = rot(cyl(LOBE_D, 14), 90, [0, 1, 0]); lobe.apply_translation([L/2-2, 0, PART_Z+5]); cuts.append(lobe)
    cuts.append(rot(cyl(LOBE_D+3, 1.8), 90, [0, 1, 0]).apply_translation([L/2-1, 0, PART_Z+5]))  # lobe lip groove
    for bx, by in BOSS:
        cuts.append(cyl(3.4, H, (bx, by, PART_Z-1))); cuts.append(cyl(6.4, 3, (bx, by, H-3)))
    cuts.append(box(26, 0.8, 8, (-13, -W/2+0.2, PART_Z+2)))                           # label window
    return diff(solid, cuts)

# ================= breath cam =================
# The disc's edge radius follows the 4-1-6 breath curve, so one rotation of a
# constant-speed motor produces a correct breath. Built as a clean polygon
# extrusion (watertight), thickness along Y (axis = motor shaft).
def cam():
    from shapely.geometry import Polygon
    seg = 96
    pts = [(( CAM_R0 + CAM_A*breath(j/seg))*np.cos(2*np.pi*j/seg),
            ( CAM_R0 + CAM_A*breath(j/seg))*np.sin(2*np.pi*j/seg)) for j in range(seg)]
    disc = trimesh.creation.extrude_polygon(Polygon(pts), CAM_TH)   # axis Z, radius X-Y
    disc.apply_translation([0, 0, -CAM_TH/2])
    rot(disc, -90, [1, 0, 0])                                        # axis -> Y
    hub = rot(cyl(9, CAM_TH+2), 90, [1, 0, 0])
    m = union([disc, hub])
    shaft = rot(cyl(SHAFT_D, CAM_TH+4), 90, [1, 0, 0])
    setscrew = cyl(1.6, 9, (0, -CAM_TH/2-1, 0))
    return diff(m, [shaft, setscrew])

# ================= follower / platen =================
def follower():
    body = cyl(PIS_D, 12)
    key = box(2.6, PIS_D+5, 9, (-1.3, -(PIS_D+5)/2, 0))
    tip = sph(6, (0, 0, 0))                       # rounded foot that rides the cam
    tip = inter([tip, box(8, 8, 4, (-4, -4, -4))])
    solid = union([body, key, tip])
    cuts = [cyl(SPR_D, 7, (0, 0, 6))]             # authority-spring seat (top)
    return diff(solid, cuts)

def platen():
    disc = cyl(DOME_D-8, 3)
    seat = cyl(SPR_D-0.6, 4, (0, 0, -4))          # spring locates here (bottom)
    solid = union([disc, seat])
    cuts = [cyl(DOME_D-14, 1.6, (0, 0, 1.6))]     # light pocket on top (foam bonds around it)
    return diff(solid, cuts)

# ================= mocks + assembly =================
def m_motor():
    b = box(MOT_L, MOT_W, MOT_H, (-MOT_L, -MOT_L/2, WALL+1))
    s = rot(cyl(SHAFT_D, 10), 90, [1, 0, 0]); s.apply_translation([0, CAM_Y-4, WALL+1+MOT_H/2])
    return trimesh.util.concatenate([b, s])

def assembly():
    P = [base()]
    P.append(m_motor())
    cm = cam(); cm.apply_translation([0, CAM_Y, CAM_Z]); P.append(cm)
    fl = follower(); fl.apply_translation([0, 0, CAM_Z+CAM_R0]); P.append(fl)
    spr = rot(cyl(SPR_D, 4), 0, [1, 0, 0]); spr.apply_translation([0, 0, CAM_Z+CAM_R0+12]); P.append(spr)
    pl = platen(); pl.apply_translation([0, 0, CAM_Z+CAM_R0+17]); P.append(pl)
    P.append(lid())
    dome = scaled(sph(DOME_D-2), 1, 1, 0.62, (0, 0, 0)); dome = inter([dome, box(DOME_D, DOME_D, 20, (-DOME_D/2, -DOME_D/2, 0))])
    dome.apply_translation([0, 0, H-3]); P.append(dome)                                # foam dome mock
    lobe = scaled(sph(LOBE_D+3), 1, 1, 1, (0, 0, 0)); lobe.apply_translation([L/2+3, 0, PART_Z+5]); P.append(lobe)  # gel lobe mock
    for yy in (W/2-22, W/2-11):
        aaa = rot(cyl(10.5, 44), 90, [0, 1, 0]); aaa.apply_translation([0, yy, WALL+7]); P.append(aaa)
    return P

if __name__ == "__main__":
    save(base(), "lull_base")
    save(lid(), "lull_lid")
    save(cam(), "lull_cam")
    save(follower(), "lull_follower")
    save(platen(), "lull_platen")
    save(trimesh.util.concatenate(assembly()), "ASSEMBLED_lull", check=False)
    print("done")
