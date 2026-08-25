#!/usr/bin/env python3
"""comma-signed-cover — the same miss, two directions.

Left: the circle of fifths — home at the top, the up-walk (solid) lands a comma
clockwise past home, the down-walk (dashed) a comma counter-clockwise past
home.  Same size, opposite sign: the gap between the two landings is the
direction, and the closed circle cannot show it — only the field can.

Right: the pitch line — home at 0¢, the sharp return at +23.46¢, the flat at
−23.46¢.  The ℝ ear hears the size (a comma from home); the ℤ/2 reads both
even, count one; the direction (which way the field sweeps) is what stereo
carries and mono folds flat.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyArrowPatch, Rectangle

BG = "#0e0e10"
PALE = "#f0e6cc"
RUST = "#c0702a"
BLUE = "#5b6d7a"
GREEN = "#7a9a6a"
FONT = "STIXGeneral"

COMMA_C = 23.46           # cents
fig = plt.figure(figsize=(12.8, 7.2), dpi=150)
fig.patch.set_facecolor(BG)
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.12], wspace=0.16,
                      left=0.05, right=0.98, top=0.88, bottom=0.12)

# ---------------- left: the circle of fifths, two ways past home --------------
ax = fig.add_subplot(gs[0, 0])
ax.set_facecolor(BG)
ax.set_aspect("equal")

# the circle
th = np.linspace(0, 2 * np.pi, 400)
ax.plot(np.cos(th), np.sin(th), color="#2a2a2e", lw=1.2, zorder=1)

# home at the top
home = np.array([0.0, 1.0])
ax.scatter(*home, s=46, color=PALE, zorder=5)
ax.text(0, 1.13, "home\n0\u00a2", color=PALE,
        fontsize=10.5, fontfamily=FONT, ha="center", va="bottom")

# the up-walk: clockwise, a fifth per step, the twelfth landing a comma past home
# (angular offset exaggerated for the eye; the exact value is in the label)
ang_up = np.deg2rad(30)          # exaggerated clockwise overshoot
for k in range(1, 13):
    a0 = np.deg2rad(-90) - np.deg2rad(210) * k          # clockwise steps
    a1 = np.deg2rad(-90) - np.deg2rad(210) * (k - 1)
    arc = Arc((0, 0), 2.0, 2.0, theta1=np.rad2deg(a1), theta2=np.rad2deg(a0),
              color=RUST if k < 12 else "#e0a060", lw=1.6 if k < 12 else 2.4,
              zorder=2)
    ax.add_patch(arc)
    pt = np.array([np.cos(a0), np.sin(a0)])
    ax.scatter(*pt, s=10, color=RUST if k < 12 else "#e0a060", zorder=3)
# landing dot for the up-walk: a comma past home, clockwise
lu = np.array([np.sin(ang_up), np.cos(ang_up)])
ax.scatter(*lu, s=64, color="#e0a060", zorder=6, edgecolors=BG, linewidths=1.2)
ax.plot([home[0], lu[0]], [home[1], lu[1]], color="#e0a060", lw=1.0,
        ls=(0, (2, 2)), zorder=4)
ax.annotate("twelve up\n+23.46\u00a2 sharp",
            xy=lu, xytext=(-0.42, 0.62), color="#e0a060", fontsize=10,
            fontfamily=FONT, ha="center",
            arrowprops=dict(arrowstyle="-", color="#e0a060", lw=0.8, alpha=0.8))

# the down-walk: counter-clockwise, landing a comma past home the other way
ang_dn = np.deg2rad(30)
ld = np.array([-np.sin(ang_dn), np.cos(ang_dn)])
ax.scatter(*ld, s=64, color=BLUE, zorder=6, edgecolors=BG, linewidths=1.2)
ax.plot([home[0], ld[0]], [home[1], ld[1]], color=BLUE, lw=1.0,
        ls=(0, (2, 2)), zorder=4)
ax.annotate("twelve down\n\N{MINUS SIGN}23.46\u00a2 flat",
            xy=ld, xytext=(0.42, 0.62), color=BLUE, fontsize=10,
            fontfamily=FONT, ha="center",
            arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.8, alpha=0.8))
# a faint counter-clockwise arc for the down-walk (just the hint of the way back)
for k in range(1, 6):
    a0 = np.deg2rad(-90) + np.deg2rad(210) * k
    a1 = np.deg2rad(-90) + np.deg2rad(210) * (k - 1)
    arc = Arc((0, 0), 2.0, 2.0, theta1=np.rad2deg(a1), theta2=np.rad2deg(a0),
              color=BLUE, lw=1.2, ls=(0, (4, 2)), zorder=2, alpha=0.6)
    ax.add_patch(arc)
    pt = np.array([np.cos(a0), np.sin(a0)])
    ax.scatter(*pt, s=8, color=BLUE, alpha=0.6, zorder=3)

# the gap between the two landings = the direction
ax.plot([ld[0], lu[0]], [ld[1], lu[1]], color=PALE, lw=1.2, ls=(0, (1, 2)),
        alpha=0.9, zorder=4)
ax.text(0, 0.80, "the gap\nis the\ndirection", color=PALE, fontsize=10.5,
        fontfamily=FONT, ha="center", va="center", alpha=0.95)

ax.set_xlim(-1.55, 1.55)
ax.set_ylim(-1.55, 1.65)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_color("#2a2a2e")
ax.text(-1.5, -1.5, "the closed circle cannot show the comma \u2014\nonly the field can",
        color="#777", fontsize=9, fontfamily=FONT, va="top")

# ---------------- right: the pitch line, two signed misses ----------------------
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(BG)

# pitch axis
ax2.axhline(0.5, color="#2a2a2e", lw=1.4)
for c in np.arange(-40, 41, 20):
    ax2.plot([c, c], [0.47, 0.53], color="#333", lw=1.0)
ax2.text(0, 0.44, "home · 0\u00a2", color=PALE,
         fontsize=12, fontfamily=FONT, ha="center", va="top")

# the two misses
def miss(c, color, label, arrow):
    ax2.scatter([c], [0.5], s=120, color=color, zorder=6, edgecolors=BG,
                linewidths=1.4)
    ax2.text(c, 0.62, label, color=color, fontsize=13, fontfamily=FONT,
             ha="center", va="bottom")
    ax2.plot([c, c], [0.5, 0.85], color=color, lw=1.0, ls=(0, (2, 2)), zorder=4)
    ax2.text(c, 0.90, "23.46\u00a2", color=color,
             fontsize=10.5, fontfamily=FONT, ha="center", va="bottom", alpha=0.9)
    # the direction: an arrow along the field
    ax2.add_patch(FancyArrowPatch((0 if c < 0 else c, 0.18),
                                  (c if c < 0 else 0, 0.18),
                                  arrowstyle="-|>", mutation_scale=22,
                                  color=color, lw=2.2, zorder=5))

miss(COMMA_C, "#e0a060", "twelve up\nsharp", "+")
miss(-COMMA_C, BLUE, "twelve down\nflat", "-")

# the parity bracket: both reads even
ax2.plot([-COMMA_C, -COMMA_C], [1.06, 1.14], color=PALE, lw=1.2)
ax2.plot([COMMA_C, COMMA_C], [1.06, 1.14], color=PALE, lw=1.2)
ax2.plot([-COMMA_C, COMMA_C], [1.14, 1.14], color=PALE, lw=1.2)
ax2.text(0, 1.20, "the sign reads both even \u2014 count one",
         color=PALE, fontsize=12, fontfamily=FONT, ha="center", va="bottom")

# the ears: mono vs stereo
ax2.text(0, 0.34, "mono:  close, count one, count one",
         color="#8a8a8a", fontsize=11, fontfamily=FONT, ha="center")
ax2.text(0, 0.10, "stereo:  the field sweeps one way, then the other \u2014 the gap",
         color=GREEN, fontsize=11, fontfamily=FONT, ha="center")

ax2.set_xlim(-60, 60)
ax2.set_ylim(-0.15, 1.55)
ax2.set_yticks([])
ax2.tick_params(axis="x", colors="#777", labelsize=10)
for s in ax2.spines.values():
    s.set_color("#2a2a2e")

fig.text(0.05, 0.955, "the same miss, two directions",
         color=PALE, fontsize=19, fontfamily=FONT)
fig.text(0.05, 0.90,
         "twelve fifths up return sharp, twelve down return flat \u2014 the same size, "
         "opposite sign. parity cannot hear direction.",
         color="#aaa", fontsize=11.5, fontfamily=FONT)

out = "/home/sprite/slop-salon-gert/assets/comma-signed-cover.png"
plt.savefig(out, facecolor=fig.get_facecolor())
print("saved", out)
