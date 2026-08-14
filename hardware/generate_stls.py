#!/usr/bin/env python3
"""Render Boom turret parts to STL using trimesh + manifold3d.
Mirrors the geometry in hardware/*.scad with default measurements."""
import numpy as np
import trimesh
from trimesh.creation import box as _box, cylinder as _cyl

import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stl")
os.makedirs(OUT, exist_ok=True)

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

def save(mesh, name):
    assert mesh.is_watertight, f"{name} not watertight"
    mesh.export(f"{OUT}/{name}.stl")
    print(f"{name}.stl  vol={mesh.volume/1000:.1f}cm3  tris={len(mesh.faces)}")

# ================= POUCH CHASSIS =================
pouch_l, pouch_w = 190, 70          # default pouch interior
base_l, base_w = pouch_l - 12, pouch_w - 12
base_t, rim_h, rim_t = 3, 12, 2
laser_d = 6.4
sv_l, sv_w, sv_well_h = 23.2, 12.6, 17
sv_flange = 32.5

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
    nose = rot(cyl(laser_d + 5, 6), 90, [0, 1, 0])
    nose.apply_translation([base_l - 1 + 3, base_w / 2, base_t + 16])
    well_at = (base_l - sv_flange - 14, (base_w - sv_w - 5) / 2, base_t)
    well = box(sv_flange + 4, sv_w + 5, sv_well_h, well_at)
    trays = [tray(52, 35, (6, (base_w - 35) / 2 - 1.6, base_t)),
             tray(28, 18, (68, 6, base_t)),
             tray(23.5, 19, (68, base_w - 19 - 10, base_t))]
    clips = [pen_clip((x, base_w - 8, rim_h)) for x in (30, 75, 120)]
    solid = union([plate, rim, nose, well] + trays + clips)

    cuts = []
    # washer weight pockets
    for fx in (0.25, 0.6):
        cuts.append(cyl(25.8, 3.6, (base_l * fx, base_w / 2, base_t - 2.6)))
    # nose beam bore
    bore = rot(cyl(laser_d + 2, 14), 90, [0, 1, 0])
    bore.apply_translation([base_l - 3 + 7, base_w / 2, base_t + 16])
    cuts.append(bore)
    # servo pocket + flange screw holes
    cuts.append(box(sv_l, sv_w, sv_well_h + 2,
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

save(chassis(), "pouch_chassis")
save(tilt_bracket(), "pouch_tilt_bracket")
save(laser_clip(), "laser_clip")

# ================= BOTTLE TOP =================
od, wall = 73, 2.4
band_h, dome_h = 30, 18
slot_h, slot_z, spine = 6, 12, 60
tilt_down, plug_h, fit_tol = 5, 12, 0.4
mouth_id = 55
top_d = od * 0.66

def shell():
    outer = union([cyl(od, band_h, sections=128),
                   frustum(od, top_d, dome_h, (0, 0, band_h), sections=128),
                   cyl(top_d, 3, (0, 0, band_h + dome_h - 0.5), sections=128)])
    inner = union([cyl(od - 2 * wall, band_h + 1, (0, 0, -1), sections=128),
                   frustum(od - 2 * wall, top_d - 2 * wall, dome_h,
                           (0, 0, band_h), sections=128)])
    # window slot ring, minus the blind spine (spine faces +X)
    half_w = (od / 2 + 2) * np.sin(np.radians(spine / 2))
    slot = diff(cyl(od + 4, slot_h, (0, 0, slot_z), sections=128),
                [box(od / 2 + 3, half_w * 2, slot_h + 2,
                     (0, -half_w, slot_z - 1))])
    usb = box(wall + 2, 10, 4, (od / 2 - wall - 1, -5, 3))
    groove = diff(cyl(od - 2 * wall + 1.6, 2.4, (0, 0, band_h - 4), sections=128),
                  [cyl(od - 2 * wall - 2, 2.8, (0, 0, band_h - 4.2), sections=128)])
    return diff(outer, [inner, slot, usb, groove])

def bulkhead():
    d = od - 2 * wall - 0.6
    lip = diff(cyl(d + 2, 2, (0, 0, 0.3), sections=128),
               [cyl(d - 2, 2.4, (0, 0, 0.1), sections=128)])
    solid = union([cyl(d, 3, sections=128), lip])
    cuts = [box(sv_l, sv_w, 5, (-sv_l + 17.4, -sv_w / 2, -1)),
            cyl(8, 5, (d / 2 - 8, 0, -1))]
    for y in (-sv_w / 2 - 4, sv_w / 2 + 4):
        cuts.append(box(6, 3, 5, (-3, y - 1.5, -1)))
    return diff(solid, cuts)

def carriage():
    ring = rot(cyl(laser_d + 4, 12, (0, 0, -6)), 90 + tilt_down, [1, 0, 0])
    ring.apply_translation([0, -6.5, 14])
    solid = union([cyl(16, 3), box(4, 3, 18, (-2, -8, 0)), ring])
    bore = rot(cyl(laser_d, 14, (0, 0, -7)), 90 + tilt_down, [1, 0, 0])
    bore.apply_translation([0, -6.5, 14])
    cuts = [bore, cyl(2.4, 5, (0, 0, -1))]
    for a in (0, 90, 180, 270):
        r = np.radians(a)
        cuts.append(cyl(1.8, 5, (5 * np.cos(r), 5 * np.sin(r), -1)))
    return diff(solid, cuts)

def plug():
    stem_d = mouth_id - fit_tol
    solid = union([cyl(od, 3, sections=128),
                   cyl(stem_d, plug_h, (0, 0, -plug_h), sections=128),
                   frustum(stem_d - 2, stem_d, 2, (0, 0, -plug_h), sections=128)])
    return diff(solid, [cyl(stem_d - 2 * wall, plug_h + 5,
                            (0, 0, -plug_h - 1), sections=128)])

save(shell(), "bottle_shell")
save(bulkhead(), "bottle_bulkhead")
save(carriage(), "bottle_carriage")
save(plug(), "bottle_plug_ring")
print("done")
