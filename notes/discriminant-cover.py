#!/usr/bin/env python3
"""discriminant-cover — the mirror reads the ghost three times.

The conjugate pair ±i (roots of x²+1) has three symmetric functions that
land on the real line even though the roots never do:

    sum         i + (−i)   =  0     the trace      → ψ   the node, no shadow
    product     i·(−i)     =  1     the norm       → χ₀  the drone, count one
    difference² (i−(−i))²  = −4     the discriminant → χ₂  the sign, turns

Read together they are the ghost's column in the real character table of
Z/4:  (χ₀, χ₂, ψ) = (1, −1, 0) = (norm, discriminant, trace).  The sign is
the discriminant: the separation of the pair is imaginary (2i, the smear),
and squared it lands negative — anti-phase, the fall, a hole in mono.
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

fig, (axl, axr) = plt.subplots(1, 2, figsize=(9.6, 5.6), dpi=150,
                               gridspec_kw={"width_ratios": [5, 4]})
for ax in (axl, axr):
    ax.set_facecolor(BG)
    ax.axis("off")
fig.patch.set_facecolor(BG)

# ===================== left: the pair and its three landings ==================
R = 2.0
axl.add_patch(Circle((0, 0), R, fill=False, lw=1.3, color=PALE, alpha=0.45))
# the real and imaginary axes
axl.plot([-R*1.45, R*1.45], [0, 0], color=ASH, lw=1.0, alpha=0.6, zorder=1)
axl.plot([0, 0], [-R*1.45, R*1.45], color=ASH, lw=0.7, alpha=0.35, zorder=1)
axl.text(R*1.5, 0.12, "the real line", color=ASH, fontsize=7.5, ha="left")
axl.text(0.1, R*1.5, "imaginary", color=ASH, fontsize=7.5, ha="left")

# the ghost pair ±i — hollow, they refuse to land
for y, name in [(R, "i"), (-R, "−i")]:
    axl.plot(0, y, 'o', ms=11, mfc=BG, mec=VIOLET, mew=2.2, zorder=6)
    axl.text(-R*0.30, y, name, color=VIOLET, fontsize=13, fontweight="bold",
             ha="right", va="center", zorder=7)
axl.text(-R*0.32, R*1.22, "±i: the roots of x²+1 — never a real landing",
         color=VIOLET, fontsize=7.5, ha="right", va="center", style="italic")

# the difference 2i between them, and its square
axl.annotate("", xy=(0, -R), xytext=(0, R),
             arrowprops=dict(arrowstyle="<|-|>", color=VIOLET, lw=1.4,
                             alpha=0.7, linestyle=(0, (3, 2))), zorder=4)
axl.text(-R*0.34, 0, "difference 2i — the smear",
         color=VIOLET, fontsize=7.5, ha="right", va="center")
axl.text(-R*1.30, -R*0.62, "squared → −4: the sign",
         color=ROSE, fontsize=7.5, ha="right", va="center")

# the three landings on the real line
# trace = 0 — the node, a hollow square (casts no shadow)
axl.plot(0, 0, 's', ms=9, mfc=BG, mec=PALE, mew=2.0, zorder=7)
axl.text(0.18, -R*0.18, "0 the trace — the node, no shadow",
         color=PALE, fontsize=7.5, ha="left")
# norm = 1 — the drone, a gold dot
axl.plot(R*0.5, 0, 'o', ms=9, color=GOLD, zorder=7)
axl.text(R*0.54, -R*0.18, "1 the norm — the drone, count one",
         color=GOLD, fontsize=7.5, ha="left")
# discriminant = −4 — the sign, a rose dot, negative
axl.plot(-R, 0, 'o', ms=9, color=ROSE, zorder=7)
axl.text(-R*1.06, -R*0.18, "−4 the discriminant — the sign, the turn",
         color=ROSE, fontsize=7.5, ha="right")

axl.text(0, -R*1.42, "the ghost never lands as a root —", color=PALE,
         ha="center", va="top", fontsize=9)
axl.text(0, -R*1.70, "its symmetric functions land three times:",
         color=VIOLET, ha="center", va="top", fontsize=8.5)

# ===================== right: the column, complete ============================
col_x = [0.55, 1.45, 2.35, 3.25]
row_y = [2.7, 1.6, 0.5]
heads = ["1", "i", "−1", "−i"]
rows = [("χ₀  the norm", [1, 1, 1, 1], GOLD, "the drone — count one"),
        ("χ₂  the discriminant", [1, -1, 1, -1], ROSE, "the sign — the turn"),
        ("ψ  the trace", [2, 0, -2, 0], VIOLET, "the node — no shadow")]

# ghost columns highlighted (i and −i)
for cx in (col_x[1], col_x[3]):
    axr.add_patch(plt.Rectangle((cx-0.36, 0.15), 0.72, 2.75,
                                color=VIOLET, alpha=0.10, zorder=1))
axr.text((col_x[1]+col_x[3])/2, 3.1, "the ghost column",
         color=VIOLET, ha="center", fontsize=7.5)

for c, h in zip(col_x, heads):
    axr.text(c, 3.6, h, color=PALE, ha="center", fontsize=10, fontweight="bold")
for (label, vals, col, note), y in zip(rows, row_y):
    axr.text(0.08, y+0.06, label, color=PALE, ha="left", fontsize=7.2)
    axr.text(0.08, y-0.16, note, color=col, ha="left", fontsize=6.6)
    for c, v in zip(col_x, vals):
        if v == 0:
            axr.add_patch(plt.Rectangle((c-0.30, y-0.30), 0.60, 0.60,
                                        fill=False, edgecolor=VIOLET,
                                        lw=1.6, zorder=3))
        axr.text(c, y, str(v), color=col, ha="center", va="center",
                 fontsize=15, fontweight="bold", zorder=4)

axr.text(0.08, -0.30, "at the ghost, the real column reads", color=PALE,
         ha="left", fontsize=8)
axr.text(0.08, -0.68, "(1, −1, 0) = (norm, discriminant, trace):",
         color=PALE, ha="left", fontsize=8)
axr.text(0.08, -1.06, "the sign is the ghost's square —", color=ROSE,
         ha="left", fontsize=8)
axr.text(0.08, -1.38, "the smear, squared, is the fall.",
         color=ROSE, ha="left", fontsize=8)

axl.set_xlim(-R*1.7, R*1.7)
axl.set_ylim(-R*1.9, R*1.65)
axr.set_xlim(0, 3.8)
axr.set_ylim(-1.8, 3.9)
fig.tight_layout(pad=0.4)
fig.savefig("assets/discriminant-cover.png", dpi=150, facecolor=BG)
print("saved assets/discriminant-cover.png")
