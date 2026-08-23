#!/usr/bin/env python3
"""ghost-node-cover — the ghost casts no shadow.

The real character table of Z/4 has three rows.  The complex pair χ₁, χ₃
fold to the trace of the 90° rotation:  ψ = (2, 0, −2, 0).  A quarter-turn
fixes no direction in the real plane — its real trace is zero, so the
ghost's projection is a node: the ghost casts no shadow.

Left: the circle of roots with each vector's real projection (its shadow
on the real axis) — full at 1 and −1 (the sign's flip), a single point at
i and −i (trace 0).  Right: the three real characters as a table, the two
zeros in the ψ row glowing where the ghost stands.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch

GOLD = (0.88, 0.70, 0.36)
PALE = (0.95, 0.90, 0.75)
ROSE = (0.76, 0.35, 0.31)
VIOLET = (0.62, 0.50, 0.82)
ASH = (0.55, 0.62, 0.70)
BG = "#0b0b0f"
FONT = 9

fig, (axl, axr) = plt.subplots(1, 2, figsize=(9.6, 5.6), dpi=150,
                               gridspec_kw={"width_ratios": [5, 4]})
for ax in (axl, axr):
    ax.set_facecolor(BG)
    ax.axis("off")
fig.patch.set_facecolor(BG)

# ===================== left: the circle and the shadows =======================
cx, cy, R = 0.0, 0.0, 2.0
axl.add_patch(Circle((cx, cy), R, fill=False, lw=1.3, color=PALE, alpha=0.5))
# the real axis
axl.plot([-R*1.25, R*1.25], [0, 0], color=ASH, lw=1.0, alpha=0.6, zorder=1)
axl.text(R*1.28, 0.08, "the real axis", color=ASH, fontsize=7.5, ha="left")

roots = [("1", 0.0, GOLD, "+2", R*0.62, -R*0.55),
         ("i", np.pi/2, VIOLET, "0", R*0.30, R*0.86),
         ("−1", np.pi, ROSE, "−2", -R*0.62, -R*0.55),
         ("−i", 3*np.pi/2, VIOLET, "0", R*0.30, -R*0.86)]
for (name, ang, col, tr, lx, ly) in roots:
    x, y = np.cos(ang), np.sin(ang)
    # the vector
    axl.annotate("", xy=(x*R, y*R), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="-|>", color=col, lw=2.0,
                                 mutation_scale=12), zorder=6)
    # the projection bar (the shadow on the real axis)
    px = x*R
    if abs(px) < 1e-6:
        axl.plot(0, 0, 'o', ms=7, color=col, zorder=7)
    else:
        axl.plot([0, px], [0, 0], color=col, lw=3.4, alpha=0.85, zorder=5)
    # root dot + label
    axl.plot(x*R, y*R, 'o', ms=8, color=PALE, zorder=8)
    axl.text(x*R*(1.12 if abs(x) > 0.9 else 0), y*R*(1.22 if abs(y) > 0.9 else 0),
             name, color=PALE, fontsize=12, fontweight="bold", ha="center",
             zorder=9)
    axl.text(lx, ly, tr, color=col, fontsize=10, ha="center",
             fontweight="bold", zorder=9)

# the ghost's zero trace: the shadow is a point at the origin
axl.text(R*0.10, R*1.62, "the ghost's shadow is a point", color=VIOLET,
         ha="left", fontsize=7.5, style="italic")

axl.text(0, -2.32, "the trace of the rotation:  2,  0,  −2,  0",
         color=PALE, ha="center", va="top", fontsize=9.5)
axl.text(0, -2.66, "a quarter-turn fixes no direction —", color=VIOLET,
         ha="center", va="top", fontsize=8.5)
axl.text(0, -2.96, "the ghost casts no shadow.", color=VIOLET,
         ha="center", va="top", fontsize=8.5)

# ===================== right: the three real characters =======================
col_x = [0.55, 1.45, 2.35, 3.25]
row_y = [2.6, 1.5, 0.4]
heads = ["1", "i", "−1", "−i"]
rows = [("χ₀  the drone", [1, 1, 1, 1], GOLD, "count one"),
        ("χ₂  the sign", [1, -1, 1, -1], ROSE, "the exchange"),
        ("ψ = χ₁+χ₃  the trace", [2, 0, -2, 0], VIOLET, "the ghost folded")]

# ghost columns highlighted (i and −i)
for cx in (col_x[1], col_x[3]):
    axr.add_patch(plt.Rectangle((cx-0.36, 0.08), 0.72, 2.72,
                                color=VIOLET, alpha=0.10, zorder=1))
axr.text((col_x[1]+col_x[3])/2, 3.0, "where the ghost stands",
         color=VIOLET, ha="center", fontsize=7.5)

for c, h in zip(col_x, heads):
    axr.text(c, 3.5, h, color=PALE, ha="center", fontsize=10, fontweight="bold")
for (label, vals, col, note), y in zip(rows, row_y):
    axr.text(0.08, y+0.06, label, color=PALE, ha="left", fontsize=7.5)
    axr.text(0.08, y-0.16, note, color=col, ha="left", fontsize=6.8)
    for c, v in zip(col_x, vals):
        if v == 0:
            axr.add_patch(plt.Rectangle((c-0.30, y-0.30), 0.60, 0.60,
                                        fill=False, edgecolor=VIOLET,
                                        lw=1.6, zorder=3))
        axr.text(c, y, str(v), color=col, ha="center", va="center",
                 fontsize=15, fontweight="bold", zorder=4)

axr.text(0.08, -0.35, "i⁴ = 1 — but the trace of i is 0.", color=PALE,
         ha="left", fontsize=8.5)
axr.text(0.08, -0.75, "the ghost is its own node:", color=VIOLET,
         ha="left", fontsize=8)
axr.text(0.08, -1.05, "never a sound, the walk between walks.",
         color=VIOLET, ha="left", fontsize=8)

axl.set_xlim(-3.0, 3.0)
axl.set_ylim(-3.5, 2.7)
axr.set_xlim(0, 3.8)
axr.set_ylim(-1.5, 3.9)
fig.tight_layout(pad=0.4)
fig.savefig("assets/ghost-node-cover.png", dpi=150, facecolor=BG)
print("saved assets/ghost-node-cover.png")
