import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# The wheel is a disclination.  Its Frank angle is the tritone.
#
# The salon's read of the kiss, to fourth order:
#   lelia:  the wheel is the disclination -- the ghost the core line, the fold
#           the flat reference.  miss^4 = (miss^2)^2: disclination = dislocation^2.
#   rahel:  (110,110) is the vertex, curvature extremal, so the wheel agrees to
#           third order and peels at miss^4 -- the sign to itself.
#   lou:    the wheel is a band; one lap flips the -1; the spoke is the tritone.
#
# NEW, checked: the disclination has an angle, and that angle is the tritone.
#   count 110, ghost 220 are an octave apart -- the same pitch class.
#   the wheel's radius R = 110 sqrt2 = 155.6 Hz is the half-octave, pi.
#   the fold is the flat reference (radius inf) -- the dislocation's half-plane.
#   the wheel is the rotated twin: one lap around the ghost is the rotation by
#   pi, the -1.  a dislocation returns a translation b = -1; a disclination
#   returns a rotation omega = pi.  the doubled peel carries no sign.

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_frame = "#8a8a94"
col_rose = "#c98a9e"
col_teal = "#7ba4b7"

C = 110.0
fold = lambda x: 220.0 - x
mirror = lambda x: 12100.0 / x
R = 110.0 * np.sqrt(2)
G = (220.0, 220.0)

fig = plt.figure(figsize=(12.4, 5.6), dpi=200)

# ---------------------------------------------------------------- left panel
ax = fig.add_axes([0.05, 0.12, 0.45, 0.76])
ax.set_facecolor(col_bg)
fig.patch.set_facecolor(col_bg)

xs = np.linspace(45, 320, 800)
fl = fold(xs)
mi = mirror(xs)

# the peel between mirror and fold
ax.plot(xs, fl, color=col_gold, lw=2.2, zorder=5, label="fold: 220 − x  (flat reference)")
ax.plot(xs, mi, color=col_amber, lw=2.2, zorder=5, label="mirror: 12100/x")
ax.fill_between(xs, fl, mi, color=col_rose, alpha=0.12, zorder=2)

# the wheel: mirror's osculating circle, centre the ghost
th = np.linspace(0, 2 * np.pi, 600)
ax.plot(G[0] + R * np.cos(th), G[1] + R * np.sin(th),
        color=col_rose, lw=1.6, ls=(0, (4, 3)), zorder=4,
        label="the wheel (centre the ghost)")

# the seam of the disclination: the wheel is cut at the count --
# the ghost-to-count ray is the identified edge of the cut.
ax.plot([G[0], C], [G[1], C], color=col_rose, lw=1.0, ls=":", zorder=3)
ax.text(136, 213, "seam: the cut at the count", color=col_rose, fontsize=9,
        rotation=-45)

# the count on the rim
ax.scatter([C], [C], s=90, facecolor="none", edgecolor=col_rose, lw=2.2, zorder=6)
ax.annotate("count 110\non the rim of the wheel", (C, C), xytext=(48, 142),
            color=col_rose, fontsize=10,
            arrowprops=dict(arrowstyle="-", color=col_rose, lw=0.8))
# the ghost at the core
ax.scatter([G[0]], [G[1]], s=60, color=col_teal, zorder=6)
ax.annotate("ghost 220 = the core\n= the count, an octave up", (G[0], G[1]),
            xytext=(196, 240), color=col_teal, fontsize=10)
ax.plot([C, G[0]], [C, G[1]], color=col_teal, lw=1.0, ls=":", zorder=3)
ax.text(152, 168, "R = 110√2 ≈ 155.6 Hz\n= the tritone, π in the octave",
        color=col_teal, fontsize=9, rotation=40)

# holonomy: a tangent frame at the count, and its image after one lap.
# one lap around the ghost is the rotation by pi -- the frame returns flipped.
t0 = np.array([1.0, -1.0]) / np.sqrt(2)          # tangent along the fold
ax.annotate("", xy=(C, C) + 17 * t0, xytext=(C, C),
            arrowprops=dict(arrowstyle="->", color=col_gold, lw=2.2, mutation_scale=16))
ax.annotate("", xy=(C, C) - 17 * t0, xytext=(C, C),
            arrowprops=dict(arrowstyle="->", color=col_rose, lw=2.2, mutation_scale=16))
ax.text(56, 66, "one lap → rotated by π\n(the −1: the frame flips)",
        color=col_gold, fontsize=9)

ax.set_xlim(45, 320)
ax.set_ylim(40, 275)
ax.set_title("the wheel is a disclination — its angle is the tritone, π",
             color=col_gold, fontsize=12)
ax.legend(loc="upper left", fontsize=8, facecolor=col_bg, edgecolor=col_frame,
          framealpha=0.9)
for s in ax.spines.values():
    s.set_color(col_frame)
ax.tick_params(colors=col_frame, labelsize=8)

# ------------------------------------------------------------- right panel
# the two defects: dislocation (translation) and disclination (rotation).
ax2 = fig.add_axes([0.58, 0.12, 0.38, 0.76])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_xlim(40, 310)
ax2.set_ylim(0, 270)

# ---- top: the dislocation (Aug 28) -- translation, b = -1, the fold's half-plane
ax2.plot([60, 300], [215, 215], color=col_gold, lw=2.2)
ax2.fill_between([60, 300], 215, 270, color=col_gold, alpha=0.10)
ax2.text(288, 252, "the fold:\nradius ∞,\nthe flat reference", color=col_gold,
         fontsize=8, ha="right", va="center")
# a Burgers-style circuit around a missing step: two squares, one displaced
bx, by = 150.0, 215.0
ax2.plot([bx, bx+40, bx+40, bx, bx], [by, by, by+40, by+40, by], color=col_gold,
         lw=1.4, ls="--")
ax2.plot([bx+18, bx+58, bx+58, bx+18, bx+18], [by, by, by+40, by+40, by],
         color=col_amber, lw=1.4, ls="--")
ax2.annotate("", xy=(bx+40, by-4), xytext=(bx+58, by-4),
             arrowprops=dict(arrowstyle="<->", color=col_amber, lw=1.4))
ax2.text(bx+49, by-16, "b = −1", color=col_amber, fontsize=10, ha="center")
ax2.text(150, 168, "dislocation: a translation\nwalk a circuit, return shifted by b = −1\npeel = miss²",
         color=col_gold, fontsize=9, ha="center")
ax2.plot([60, 300], [148, 148], color=col_frame, lw=0.6, ls=":")

# ---- bottom: the disclination -- rotation, omega = pi, the wheel's half-wedge
g2 = np.array([195.0, 106.0])
R2 = 46.0
ax2.add_patch(mpatches.Wedge(g2, R2, 180, 360, color=col_rose, alpha=0.14))
th2 = np.linspace(0, 2 * np.pi, 300)
ax2.plot(g2[0] + R2 * np.cos(th2), g2[1] + R2 * np.sin(th2),
         color=col_rose, lw=2.0)
ax2.plot([g2[0], g2[0]-R2], [g2[1], g2[1]], color=col_rose, lw=1.0, ls=":")
ax2.plot([g2[0], g2[0]+R2], [g2[1], g2[1]], color=col_rose, lw=1.0, ls=":")
ax2.text(g2[0], g2[1]+12, "core\n(ghost)", color=col_rose, fontsize=8, ha="center")
ax2.text(g2[0]+R2+5, g2[1]-3, "seam", color=col_rose, fontsize=8)
ax2.annotate("", xy=(g2[0]-R2-16, 40), xytext=(g2[0]+R2+16, 40),
             arrowprops=dict(arrowstyle="<->", color=col_teal, lw=1.4))
# a frame on the rim, and its flipped image after one lap (rotation by pi)
a0 = np.array([g2[0]+R2, g2[1]])
ax2.annotate("", xy=a0 + np.array([0, 13]), xytext=a0,
             arrowprops=dict(arrowstyle="->", color=col_rose, lw=2.2, mutation_scale=13))
ax2.annotate("", xy=a0 - np.array([0, 13]), xytext=a0,
             arrowprops=dict(arrowstyle="->", color=col_amber, lw=2.2, mutation_scale=13))
ax2.text(g2[0]+R2+6, g2[1]+10, "one lap\n→ flip", color=col_rose, fontsize=8)
ax2.text(195, 8, "disclination: a rotation\nω = π = the tritone (half the octave)\nwalk a circuit, return rotated by π\npeel = miss⁴ = (miss²)² — no side",
         color=col_rose, fontsize=9, ha="center")

ax2.set_title("the disclination is the dislocation, squared",
              color=col_gold, fontsize=12)

fig.savefig("assets/disclination-cover.png", facecolor=col_bg)
print("wrote assets/disclination-cover.png")
