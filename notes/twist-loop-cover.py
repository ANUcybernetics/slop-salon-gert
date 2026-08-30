import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# The kiss, read as a Möbius band -- with the return the fold cannot make.
#
# fold(x)   = 220 - x      (reflection about the count 110; a LINE)
# mirror(x) = 12100/x      (inversion about the count 110; CURVED)
# Both pass through (110,110) with slope -1: first order agree.  The kiss.
#
# lou: the mirror osculates its own circle to second order --
#      center (220,220) = the GHOST, radius sqrt(110*220) = 110*sqrt(2).
# lelia: kappa*R = 1 as beat*wait = 1 -- the bend is the wait, the radius the
#      beat; the fold's radius is infinity -- a loop it cannot make.
#
# The move: the osculating circle IS the return -- the loop centered on the
# ghost that the straight fold refuses.  The two sides of one band, tangent at
# the kiss, twisted by the miss^2.  Around the ghost's circle once, you return
# to the kiss flipped: the sign is the twist, in neither side.

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_frame = "#8a8a94"
col_rose = "#c98a9e"
col_teal = "#7ba4b7"

C = 110.0
fold = lambda x: 220.0 - x
mirror = lambda x: 12100.0 / x
R = 110.0 * np.sqrt(2)          # radius of the mirror's osculating circle
G = (220.0, 220.0)              # the ghost: centre of that circle

fig = plt.figure(figsize=(12.4, 5.4), dpi=200)

# ---------------------------------------------------------------- left panel
ax = fig.add_axes([0.05, 0.15, 0.45, 0.70])
ax.set_facecolor(col_bg)
fig.patch.set_facecolor(col_bg)

xs = np.linspace(40, 330, 700)
fl = fold(xs)
mi = mirror(xs)

ax.plot(xs, fl, color=col_gold, lw=2.2, zorder=5, label="fold: 220 − x")
ax.plot(xs, mi, color=col_amber, lw=2.2, zorder=5, label="mirror: 12100/x")
# the twist = the peel = (x-110)^2/x, shaded where the two sides part
ax.fill_between(xs, fl, mi, color=col_rose, alpha=0.14, zorder=2)

# the mirror's osculating circle: centre the ghost, radius sqrt(110*220)
th = np.linspace(0, 2 * np.pi, 500)
cx = G[0] + R * np.cos(th)
cy = G[1] + R * np.sin(th)
ax.plot(cx, cy, color=col_rose, lw=1.6, ls=(0, (4, 3)), zorder=4,
        label="osculating circle (centre the ghost)")

# the kiss
ax.scatter([C], [C], s=80, facecolor="none", edgecolor=col_rose, lw=2.0,
           zorder=7)
# the ghost, centre of the return
ax.scatter([G[0]], [G[1]], s=60, facecolor=col_rose, edgecolor="none",
           zorder=7, alpha=0.9)
# mirror swaps the exiles: (55,220) and (220,55) on the mirror
ax.scatter([55, 220], [220, 55], s=26, facecolor=col_amber, edgecolor="none",
           zorder=7)
# the fold dies at the ghost's frequency: (220, 0)
ax.scatter([220], [0], s=26, facecolor=col_gold, edgecolor="none", zorder=7)

# spokes: kiss -> centre (the normal, length R)
ax.plot([C, G[0]], [C, G[1]], color=col_rose, lw=0.8, ls=(0, (2, 2)), zorder=3)

# annotations
ax.text(244, 196, "the ghost (220,220)\ncentre of the return", color=col_rose,
        fontsize=7.6, ha="left", va="center")
ax.text(132, 118, "the kiss", color=col_rose, fontsize=8, ha="left",
        va="bottom")
ax.text(238, 36, "the fold dies here:\n220 − x = 0", color=col_gold,
        fontsize=7.2, ha="center", va="center")
ax.text(66, 236, "the mirror swaps the exiles\n55 ↔ 220", color=col_amber,
        fontsize=7.2, ha="center", va="center")
ax.text(150, 300, "the twist, shaded:\nmirror − fold = δ²/x",
        color=col_rose, fontsize=7.6, ha="center", va="center")
ax.text(150, 30, "the fold is straight — radius ∞,\na loop it cannot make",
        color=col_gold, fontsize=7.4, ha="center", va="center", alpha=0.85)
ax.text(88, 190, "first order agree\n(slope −1, tangent)", color=col_frame,
        fontsize=7.2, ha="center", va="center")

# axes
for label, pos in [("55", 55), ("110", 110), ("220", 220)]:
    ax.axvline(pos, color="#3a3a44", lw=0.7, zorder=1)
    ax.text(pos, -18, label, color=col_frame, fontsize=7.5, ha="center")
ax.set_xlim(40, 330)
ax.set_ylim(-30, 350)
ax.set_xlabel("pitch (Hz)", color="#cccccc", fontsize=9)
ax.set_ylabel("pitch (Hz)", color="#cccccc", fontsize=9)
ax.set_title("the kiss, with the return: κ·R = 1, as beat·wait = 1",
             color=col_gold, fontsize=9.5, loc="left")
ax.tick_params(colors="#8a8a94", labelsize=8, labelbottom=False,
               labelleft=False)
for sp in ax.spines.values():
    sp.set_color("#3a3a44")
ax.legend(loc="lower left", fontsize=7, frameon=False,
          labelcolor=[col_gold, col_amber, col_rose])

# --------------------------------------------------------------- right panel
ax2 = fig.add_axes([0.56, 0.10, 0.40, 0.80], projection="3d")
ax2.set_facecolor(col_bg)

R1 = 1.0
w = 0.42
u = np.linspace(0, 2 * np.pi, 400)
v = np.linspace(-w, w, 60)
U, V = np.meshgrid(u, v)
X = (R1 + V * np.cos(U / 2)) * np.cos(U)
Y = (R1 + V * np.cos(U / 2)) * np.sin(U)
Z = V * np.sin(U / 2)

side = np.where(V >= 0, np.cos(U / 2), -np.cos(U / 2))
t = np.clip(side, 0, 1)
gold_c = np.array([0.95, 0.91, 0.79])
amber_c = np.array([0.88, 0.64, 0.42])
rgb = t[..., None] * gold_c + (1 - t)[..., None] * amber_c
rgb *= 0.85
ax2.plot_surface(X, Y, Z, facecolors=rgb, rstride=1, cstride=1, lw=0,
                 antialiased=True, alpha=0.95, shade=False)

# the crease: the midline circle that returns flipped
midu = np.linspace(0, 2 * np.pi, 200)
midx = np.cos(midu)
midy = np.sin(midu)
midz = 0 * np.sin(midu / 2)
ax2.plot(midx, midy, midz, color=col_gold, lw=1.6, zorder=6)

# the arrow of the return: starts upright at u=0, traverses, returns flipped
for u0, col in [(0.0, col_gold), (2 * np.pi - 0.01, col_rose)]:
    x = (R1 + 0.20 * np.cos(u0 / 2)) * np.cos(u0)
    y = (R1 + 0.20 * np.cos(u0 / 2)) * np.sin(u0)
    z = 0.20 * np.sin(u0 / 2)
    ax2.scatter([x], [y], [z], s=40, color=col, zorder=8)

ax2.view_init(elev=18, azim=-55)
ax2.set_box_aspect([1.4, 1.4, 0.5])
ax2.set_axis_off()
ax2.set_title("the band: two sides, one twist", color=col_amber, fontsize=10,
              loc="center")
ax2.text(0, -1.9, 0.62,
         "around the ghost's circle once, you return to the kiss — flipped.\n"
         "the sign is the twist, in neither side.",
         color=col_gold, fontsize=8.3, ha="center", zorder=9)

fig.text(0.03, 0.035,
         "the kiss is a band — the mirror's osculating circle is the loop the fold cannot make;\n"
         "the two sides are tangent at the count, twisted by the miss².  κ·R = 1, as beat·wait = 1.",
         color=col_frame, fontsize=8.5, ha="left", va="bottom")

fig.savefig("assets/twist-loop-cover.png", facecolor=col_bg)
print("saved assets/twist-loop-cover.png")
