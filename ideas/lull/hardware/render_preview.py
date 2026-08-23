#!/usr/bin/env python3
"""Render the Lull prototype STLs to a labelled preview PNG."""
import os
import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

HERE = os.path.dirname(os.path.abspath(__file__)); STL = os.path.join(HERE, "stl")
PARTS = [("lull_base.stl","lull_base","#e8663a"),("lull_lid.stl","lull_lid","#2e6fb0"),
         ("lull_cam.stl","cam (breath curve)","#c9a227"),("lull_follower.stl","follower","#0e9e82"),
         ("lull_platen.stl","platen","#8a5cd1"),("ASSEMBLED_lull.stl","ASSEMBLED","#455066")]
INK="#191a2b"; PAPER="#e9ebe4"

def shade(mesh, base):
    light=np.array([0.4,-0.6,0.8]); light/=np.linalg.norm(light)
    lit=0.35+0.65*np.clip(mesh.face_normals@light,0,1)
    bc=np.array(matplotlib.colors.to_rgb(base)); return np.clip(bc[None,:]*lit[:,None],0,1)

def draw(ax, mesh, base, title):
    pc=Poly3DCollection(mesh.vertices[mesh.faces], linewidths=0); pc.set_facecolor(shade(mesh,base)); ax.add_collection3d(pc)
    c=mesh.bounds.mean(axis=0); r=mesh.extents.max()*0.62
    ax.set_xlim(c[0]-r,c[0]+r); ax.set_ylim(c[1]-r,c[1]+r); ax.set_zlim(c[2]-r,c[2]+r)
    try: ax.set_box_aspect((1,1,1))
    except Exception: pass
    ax.view_init(elev=26, azim=-56); ax.set_axis_off()
    ax.set_title(title, color=INK, fontsize=12.5, fontweight="bold", pad=-2, family="monospace")

def main():
    fig=plt.figure(figsize=(13.5,8.6), dpi=132); fig.patch.set_facecolor(PAPER)
    for i,(fn,title,color) in enumerate(PARTS,1):
        p=os.path.join(STL,fn)
        if not os.path.exists(p): continue
        ax=fig.add_subplot(2,3,i,projection="3d"); ax.set_facecolor(PAPER); draw(ax, trimesh.load(p), color, title)
    fig.suptitle("LULL  ·  split-zone breathing squishy (prototype)", color=INK, fontsize=17, fontweight="bold", family="monospace", y=0.98)
    fig.text(0.5, 0.02, "print base/lid/cam/follower/platen · bought: N20 motor, 2×AAA, foam dome, gel lobe, spring · 82×60×30 mm",
             ha="center", color="#54566b", fontsize=9.5, family="monospace")
    fig.tight_layout(rect=(0,0.03,1,0.95))
    out=os.path.join(HERE,"parts_preview.png"); fig.savefig(out, facecolor=PAPER); print("wrote", out)

if __name__=="__main__": main()
