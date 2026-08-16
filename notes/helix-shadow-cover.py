#!/usr/bin/env python3
"""helix-shadow-cover.py

Cover for the helix-shadow piece. "the trace is the helix's shadow" (mina and
lelia, same move, two directions).

LEFT: the covering exp: R -> S^1. A gold helix climbs two laps up a faint
cylinder - the LIFT, the winding, its height the lap count. Dashed gold
verticals show the deck group Z, the fiber over home. Gold dots at home at
heights 0 and 1; a crimson dot at the half-turn e^{ipi} = -1 on the helix (the
deck, the laps' parity, one lap from home). At the base, a crimson circle is
the helix's SHADOW - the trace, the projection, home each lap, blind. At its
center: a hollow black point - the branch point, the DC, the SEAT - the point
exp never reaches, the axis every cosine is measured against. A dashed crimson
arc is the half-turn from home to the deck on the shadow circle.

RIGHT: the same structure made audible - frequency is the winding per second.
Gold: the lift, climbing 110 -> 440 through two octaves, never folding (the
height). Crimson: the shadow, climbing the base octave and FOLDING back to 110
at each lap (home each lap, blind). The folds at 36s and 72s are the deck; the
DC seat sits at 0 Hz below both. The two curves start together (locally the
covering is trivial) and separate after the first fold.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

GOLD = "#d9a441"
GOLD_EDGE = "#f2cf82"
CRIMSON = "#c02942"
CRIMSON_EDGE = "#e0556e"
SEAM = "#f2f0e8"
BG = "#0b0d12"
EDGE_DARK = "#5a6b86"
FAINT = "#8a97ab"

W, H = 12.8, 7.2
fig, ax = plt.subplots(figsize=(W, H), facecolor=BG)
ax.set_facecolor(BG)

# ================= LEFT: the covering =================
# the cylinder
cyl_x = 3.6
cyl_r = 1.5
cyl_y0, cyl_y1 = 0.7, 5.4
for y in np.linspace(cyl_y0, cyl_y1, 9):
    ax.plot([cyl_x - cyl_r, cyl_x + cyl_r], [y, y], color=EDGE_DARK, lw=0.4,
            alpha=0.35, zorder=1)
for x in (cyl_x - cyl_r, cyl_x + cyl_r):
    ax.plot([x, x], [cyl_y0, cyl_y1], color=EDGE_DARK, lw=0.8, alpha=0.6,
            zorder=1)

# the helix: two laps. z climbs the height, angle winds twice.
th = np.linspace(0, 4 * np.pi, 1200)
z = cyl_y0 + (th / (4 * np.pi)) * (cyl_y1 - cyl_y0)
hx = cyl_x + cyl_r * np.cos(th)
hy = cyl_y0 + (z - cyl_y0) * 0.82 + 0.3 * cyl_r * np.sin(th)
ax.plot(hx, hy, color=GOLD, lw=1.8, alpha=0.95, zorder=3)

# fiber over home (the deck group Z): dashed verticals at the helix's home
for zi, lab in ((cyl_y0, "0"), (cyl_y0 + 0.5 * (cyl_y1 - cyl_y0), "1"),
                (cyl_y1, "2")):
    ax.plot([cyl_x, cyl_x], [cyl_y0, cyl_y1], color=GOLD_EDGE, lw=0.7,
            ls=":", alpha=0.5, zorder=2)
    break  # one fiber line, over home

# gold dots at home (lap completions) and the deck dot (half-turn, e^{ipi}=-1)
for frac, lab in ((0.0, "home 0"), (0.5, "the deck  e^{i\\pi}=-1"), (1.0, "home 2")):
    zi = cyl_y0 + frac * (cyl_y1 - cyl_y0)
    if frac in (0.0, 1.0):
        ax.plot([cyl_x], [cyl_y0 + frac * 0.82 * (cyl_y1 - cyl_y0) + 0.3 * cyl_r * 0.0],
                marker="o", ms=7, color=GOLD_EDGE, mec=BG, zorder=5)
    else:
        # the half-turn sits on the helix at theta = pi, height half a lap
        htheta = np.pi
        hz = cyl_y0 + (htheta / (4 * np.pi)) * (cyl_y1 - cyl_y0)
        ax.plot([cyl_x + cyl_r * np.cos(htheta)],
                [cyl_y0 + (hz - cyl_y0) * 0.82 + 0.3 * cyl_r * np.sin(htheta)],
                marker="o", ms=7, color=CRIMSON_EDGE, mec=BG, zorder=5)
ax.text(cyl_x + cyl_r + 0.25, cyl_y1 - 0.2, "the lift: the height,\nthe winding",
        color=GOLD_EDGE, fontsize=8.5, va="top", zorder=6)

# the base circle: the shadow
scx, scy, R = cyl_x, 0.62, 1.5
ax.add_patch(Circle((scx, scy), R, fill=False, color=CRIMSON, lw=1.4, alpha=0.9,
                    zorder=2))
ax.plot([scx + R * np.cos(a) for a in np.linspace(0, 2 * np.pi, 8)],
        [scy + R * np.sin(a) for a in np.linspace(0, 2 * np.pi, 8)],
        marker="o", ms=2.5, color=CRIMSON_EDGE, mec=BG, alpha=0.7, zorder=3)
# home and deck on the shadow circle
ax.plot([scx + R], [scy], marker="o", ms=6, color=GOLD_EDGE, mec=BG, zorder=5)
ax.plot([scx - R], [scy], marker="o", ms=6, color=CRIMSON_EDGE, mec=BG, zorder=5)
# dashed crimson arc: the half-turn from home to the deck
a = np.linspace(0, np.pi, 60)
ax.plot(scx + 0.92 * R * np.cos(a), scy + 0.92 * R * np.sin(a), color=CRIMSON,
        lw=1.0, ls="--", alpha=0.85, zorder=3)
ax.text(scx, scy - R - 0.28, "the shadow: the trace,\nhome each lap, blind",
        color=CRIMSON_EDGE, fontsize=8.5, ha="center", zorder=6)
ax.annotate("one lap the sign,\ntwo laps home",
            xy=(scx - R, scy), xytext=(scx - R - 2.0, scy - 0.9),
            color=SEAM, fontsize=8.5, ha="left",
            arrowprops=dict(arrowstyle="->", color=CRIMSON_EDGE, lw=1.0,
                            alpha=0.8), zorder=6)

# the seat: the branch point, hollow, at the center of the shadow circle
ax.add_patch(Circle((scx, scy), 0.10, fill=False, color=SEAM, lw=1.4, zorder=6))
ax.add_patch(Circle((scx, scy), 0.045, color=BG, zorder=7))
ax.text(scx, scy - 0.34, "the seat: the DC,\nthe point exp never reaches",
        color=SEAM, fontsize=8.5, ha="center", zorder=6)

# ================= RIGHT: the sound =================
x0, x1, y0, y1 = 7.0, 12.4, 0.7, 6.0
ax.text(x0, y1 + 0.25, "frequency = the winding per second",
        color=SEAM, fontsize=10, ha="left", zorder=6)
T = 73.5
# lift: gold, 110 -> 440, never folding
tl = np.linspace(0, 72, 800)
lift_f = 110.0 * 4.0 ** (tl / 72.0)
# shadow: crimson, folded mod one octave
sh_f = np.where(tl < 35.5, 110.0 * 2.0 ** (tl / 35.5),
        np.where(tl < 36.5, 220.0 * 2.0 ** ((36.5 - tl) / 1.0),
        np.where(tl < 71.5, 110.0 * 2.0 ** ((tl - 36.5) / 35.0),
                 220.0 * 2.0 ** ((73.5 - tl) / 2.0))))

def Y(f):
    return y0 + (np.log2(f / 27.5) / np.log2(440.0 / 27.5)) * (y1 - y0)

ax.plot(x0 + tl / T * (x1 - x0), Y(lift_f), color=GOLD, lw=2.0, alpha=0.95,
        zorder=3, label="the lift - the winding, the height")
ax.plot(x0 + tl / T * (x1 - x0), Y(sh_f), color=CRIMSON_EDGE, lw=2.2, alpha=0.95,
        zorder=4, label="the shadow - the trace, folding home")

# the folds marked (the deck)
for tmark, lmark in ((36.0, "the deck\n(e^{i\\pi}=-1)"), (72.0, "two laps home")):
    ax.plot([x0 + tmark / T * (x1 - x0)] * 2, [y0, y1], color=SEAM, lw=0.8,
            ls="--", alpha=0.55, zorder=2)
    ax.text(x0 + tmark / T * (x1 - x0), y1 + 0.02, lmark, color=FAINT,
            fontsize=7.5, ha="center", zorder=6)

# the seat: the DC line at the bottom
ax.plot([x0, x1], [Y(27.5), Y(27.5)], color=SEAM, lw=1.0, ls=":", alpha=0.7,
        zorder=2)
ax.text(x0, Y(27.5) - 0.22, "the seat: 0 Hz, the DC, never reached",
        color=SEAM, fontsize=7.5, ha="left", zorder=6)

# octave labels
for ff, lab in ((27.5, "A0"), (55, "A1"), (110, "A2"), (220, "A3"), (440, "A4")):
    ax.plot([x0 - 0.06, x0], [Y(ff), Y(ff)], color=FAINT, lw=0.7, zorder=2)
    ax.text(x0 - 0.12, Y(ff), lab, color=FAINT, fontsize=7.5, ha="right",
            va="center", zorder=3)
ax.text(x0, y0 - 0.35, "0s", color=FAINT, fontsize=8)
ax.text(x1, y0 - 0.35, "73.5s", color=FAINT, fontsize=8)

ax.legend(loc="upper right", fontsize=8.5, frameon=False, labelcolor=FAINT,
          ncol=1, bbox_to_anchor=(1.0, 1.0))

# title
ax.text(0.3, 6.85, "the trace is the helix's shadow",
        color=SEAM, fontsize=13, ha="left", alpha=0.95, zorder=6)

ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.set_aspect("equal")
ax.set_axis_off()
ax.grid(False)

plt.tight_layout(pad=0.2)
plt.savefig("assets/helix-shadow-cover.png", facecolor=BG, bbox_inches="tight",
            pad_inches=0.06)
print("wrote assets/helix-shadow-cover.png")
