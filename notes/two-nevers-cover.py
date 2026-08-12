#!/usr/bin/env python3
"""
two-nevers-cover.py — cover for "two never's, one price" (2026-08-12)

Left, the hollow: phi's convergents zigzag alternately above and below a dashed
centre, the side set by the index's parity — the two voices close on a seat the
pair can never land on. Right, the drone: twelve fifths almost return to the
octave; the residue (odd vs even, 23.46 cents) is kept, and the near-return
beats forever — the ring that never closes.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyArrowPatch
import matplotlib.font_manager as fm

plt.rcParams["font.family"] = "serif"
plt.rcParams["text.color"] = "#e8dcc0"

GOLD = "#d9a441"
CRIMSON = "#c0523a"
CREAM = "#e8dcc0"
DIM = "#8a7f6a"
BG = "#141210"

fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.8, 7.2), dpi=180)
fig.patch.set_facecolor(BG)
for ax in (axL, axR):
    ax.set_facecolor(BG)
    ax.axis("off")

# ---------------- Left: the hollow ----------------
phi = (1 + 5 ** 0.5) / 2
a, b = 1, 1
xs, ys_up, ys_dn, sides = [], [], [], []
for n in range(13):
    r = a / b
    above = r > phi
    sides.append(above)
    a, b = a + b, a
    xs.append(n)
    if above:
        ys_up.append(1.0 / (1.5 + n * 0.28))
        ys_dn.append(np.nan)
    else:
        ys_dn.append(1.0 / (1.5 + n * 0.28))
        ys_up.append(np.nan)

axL.axhline(0, color=DIM, ls=(0, (4, 4)), lw=1.0, alpha=0.6)
for i, x in enumerate(xs):
    up = sides[i]
    col = GOLD if up else CRIMSON
    yy = ys_up[i] if up else ys_dn[i]
    if i > 0:
        prev = ys_up[i - 1] if sides[i - 1] else ys_dn[i - 1]
        axL.plot([i - 1, i], [prev, yy], color=col, lw=1.8, alpha=0.85, solid_capstyle="round")
    axL.plot(i, yy, "o", color=col, ms=4.5, zorder=5)
# annotate the empty seat
axL.annotate("the seat", xy=(12.4, 0), xytext=(10.6, 0.33),
             fontsize=13, color=CREAM, ha="center",
             arrowprops=dict(arrowstyle="-", color=DIM, lw=0.9))
axL.text(6.3, 0.55, "the pair never forms", fontsize=16, color=GOLD, ha="center",
         weight="bold")
axL.text(6.3, 0.47, "side = parity of the index —", fontsize=11, color=DIM, ha="center")
axL.text(6.3, 0.40, "even below, odd above, never together", fontsize=11, color=DIM, ha="center")
axL.text(6.3, -0.33, "the gate would need an index that is both", fontsize=11,
         color=CREAM, ha="center")
axL.text(6.3, -0.41, "the center is never struck", fontsize=12, color=CREAM, ha="center")
axL.set_xlim(-1, 14.5)
axL.set_ylim(-0.75, 0.85)
axL.set_title("the hollow", fontsize=19, color=CREAM, pad=14)

# ---------------- Right: the drone ----------------
# circle of fifths: 12 fifths, 7 octaves, gap 23.46 cents.
axR.add_patch(plt.Circle((0, 0), 1.0, fill=False, color=CREAM, lw=1.4, alpha=0.9))
# the near-closed ring: 12 fifths walk up by a fifth each; the return is short.
xs_p, ys_p = [], []
r = 1.0
for k in range(12):
    th = np.pi / 2 - 2 * np.pi * k * (1 / 12)          # fifths around the clock
    xs_p.append(r * np.cos(th))
    ys_p.append(r * np.sin(th))
# the attempted closing arc
th0 = np.pi / 2
th1 = th0 - 2 * np.pi * (12 / 12) + 0.06               # almost, leaves a gap
axR.add_patch(Arc((0, 0), 2, 2, theta1=np.degrees(th1), theta2=np.degrees(th0) + 0.5,
                  color=GOLD, lw=2.2, alpha=0.95, ls=(0, (5, 3))))
for (x, y) in zip(xs_p, ys_p):
    axR.plot(x, y, "o", color=CRIMSON, ms=4.0)
# the gap / comma marker
gx = r * np.cos(th1 - 0.02)
gy = r * np.sin(th1 - 0.02)
axR.annotate("23.46¢", xy=(r * np.cos(th1), r * np.sin(th1)),
             xytext=(0.15, -0.15), fontsize=13, color=GOLD, ha="center",
             arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.1))
axR.text(0, -1.35, "twelve fifths, seven octaves", fontsize=13, color=CREAM, ha="center")
axR.text(0, -1.48, "odd never becomes even — the return never lands", fontsize=11,
         color=DIM, ha="center")
# a small beat under it
tb = np.linspace(0, 2.6, 400)
beat = 0.6 * np.sin(2 * np.pi * 1.5 * tb) * (1 + 0.6 * np.cos(2 * np.pi * 0.5 * tb))
axR.plot(tb * 0.9 - 1.17, -0.95 + 0.11 * beat, color=GOLD, lw=1.1, alpha=0.85)
axR.set_title("the drone", fontsize=19, color=CREAM, pad=14)
axR.set_xlim(-1.5, 1.5)
axR.set_ylim(-1.7, 1.25)
axR.set_aspect("equal")

fig.text(0.5, 0.02, "two never's, one price", fontsize=17, color=GOLD,
         ha="center", weight="bold")
fig.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.06)
plt.savefig("assets/two-nevers-cover.png", facecolor=BG, bbox_inches="tight")
print("wrote assets/two-nevers-cover.png")
