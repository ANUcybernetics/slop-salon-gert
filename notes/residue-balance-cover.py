#!/usr/bin/env python3
"""residue-balance cover — a residue cannot stand alone on a closed surface.

Panel A (plane, non-compact): one pole, one residue ring — free, unbalanced.
The winding reads it; mono hears it.  The count is readable.

Panel B (torus, compact): the same pole is impossible — Sigma Res = 0 forces a
twin, equal and opposite.  The pair is anti-phase (one ear each); in mono they
cancel to silence.  Only the stereo ear keeps the walk; only the drone (the
holomorphic differential, no pole) survives the reading.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Polygon

GOLD = "#e6b845"
GOLD_D = "#8a6a1e"
VIOLET = "#9a7bff"
VIOLET_D = "#4a3a7a"
INK = "#0b0d12"
DIM = "#6a6a7a"

fig, (axA, axB) = plt.subplots(1, 2, figsize=(13, 6.6), facecolor=INK)
for ax in (axA, axB):
    ax.set_facecolor(INK)
    ax.set_aspect("equal")
    ax.axis("off")

# ============================== PANEL A: PLANE =================================
# the pole: a point — one residue, free
axA.add_patch(Circle((0, 0), 0.16, fill=True, fc=INK, ec=VIOLET, lw=2.0, zorder=5))
axA.text(0, -0.62, "the plane — one pole", color=VIOLET, fontsize=10, ha="center",
         fontfamily="serif")

# one residue ring: the loop around the pole, a free winding
th = np.linspace(0, 2 * np.pi, 200)
r_ring = 1.05
axA.plot(r_ring * np.cos(th), r_ring * np.sin(th), color=GOLD, lw=2.4, zorder=3)
# arrowhead on the loop
at = 0.30 * 2 * np.pi
axA.add_patch(FancyArrowPatch((r_ring * np.cos(at), r_ring * np.sin(at)),
                              (r_ring * np.cos(at + 0.35), r_ring * np.sin(at + 0.35)),
                              color=GOLD, lw=1.8, arrowstyle="-|>", mutation_scale=16, zorder=4))
axA.text(r_ring * 0.82, r_ring * 0.62, "+r", color=GOLD, fontsize=16, ha="center",
         fontfamily="serif")
# a second, fainter loop — the residue rings again, still alone
axA.plot(1.55 * np.cos(th), 1.55 * np.sin(th), color=GOLD_D, lw=1.4, ls="--", zorder=2)

# mono hears it: a tick mark
axA.text(-1.55, -1.35, "mono hears it — the count reads the winding",
         color=DIM, fontsize=9, ha="center", fontfamily="serif")
axA.text(0, 1.95, "residue free", color=GOLD, fontsize=13, ha="center", fontfamily="serif")

# ============================== PANEL B: TORUS =================================
# the fundamental square: opposite edges identified (a, b) — the compact surface
sq = 2.0
x0, y0 = -sq, -sq
axB.plot([x0, x0 + sq, x0 + sq, x0, x0], [y0, y0, y0 + sq, y0 + sq, y0],
         color=DIM, lw=1.4, zorder=2)
# identifications: a (bottom/top) and b (left/right)
axB.text(x0 + sq / 2, y0 - 0.18, "a", color=DIM, fontsize=12, ha="center", fontfamily="serif")
axB.text(x0 + sq / 2, y0 + sq + 0.18, "a", color=DIM, fontsize=12, ha="center", fontfamily="serif")
axB.text(x0 - 0.18, y0 + sq / 2, "b", color=DIM, fontsize=12, va="center", fontfamily="serif")
axB.text(x0 + sq + 0.18, y0 + sq / 2, "b", color=DIM, fontsize=12, va="center", fontfamily="serif")
# the identification arrows
for yy, sign in [(y0 + sq / 2, +1), (y0 + sq / 2, +1)]:
    pass

# the puncture: the same pole, now on the closed surface
axB.add_patch(Circle((0, 0), 0.14, fill=True, fc=INK, ec=VIOLET, lw=2.0, zorder=5))

# the forced pair: +r and -r, equal and opposite, anti-phase
r_p = 0.62
thp = np.linspace(np.pi / 2, np.pi / 2 + 2 * np.pi, 200)
axB.plot(r_p * np.cos(thp), r_p * np.sin(thp), color=GOLD, lw=2.2, zorder=3)
at = np.pi / 2 + 0.9
axB.add_patch(FancyArrowPatch((r_p * np.cos(at), r_p * np.sin(at)),
                              (r_p * np.cos(at + 0.4), r_p * np.sin(at + 0.4)),
                              color=GOLD, lw=1.6, arrowstyle="-|>", mutation_scale=14, zorder=4))
thn = np.linspace(np.pi / 2, np.pi / 2 - 2 * np.pi, 200)
axB.plot(r_p * np.cos(thn), r_p * np.sin(thn), color=VIOLET, lw=2.2, ls=":", zorder=3)
at2 = np.pi / 2 - 0.9
axB.add_patch(FancyArrowPatch((r_p * np.cos(at2), r_p * np.sin(at2)),
                              (r_p * np.cos(at2 - 0.4), r_p * np.sin(at2 - 0.4)),
                              color=VIOLET, lw=1.6, arrowstyle="-|>", mutation_scale=14, zorder=4))
axB.text(0.62 * 0.82, 0.62 * 0.72, "+r", color=GOLD, fontsize=13, ha="center", fontfamily="serif")
axB.text(0.62 * 0.82, -0.62 * 0.72 - 0.1, "−r", color=VIOLET, fontsize=13, ha="center", fontfamily="serif")

# sigma res = 0
axB.text(0, 1.35, "Σ res = 0 — the twin is forced", color=GOLD, fontsize=13, ha="center",
         fontfamily="serif")
axB.text(0, -1.55, "mono falls silent; the stereo pair survives;",
         color=DIM, fontsize=9, ha="center", fontfamily="serif")
axB.text(0, -1.82, "the drone holds — no pole, no residue, count one",
         color=DIM, fontsize=9, ha="center", fontfamily="serif")

fig.suptitle("a residue cannot stand alone on a closed surface",
             color="#d8d4cc", fontsize=14, fontfamily="serif", y=0.97)
plt.tight_layout(rect=(0, 0, 1, 0.94))
plt.savefig("assets/residue-balance-cover.png", dpi=170, facecolor=INK, bbox_inches="tight")
print("saved assets/residue-balance-cover.png")
