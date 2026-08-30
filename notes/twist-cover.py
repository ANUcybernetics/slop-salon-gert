import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# The kiss, read as a Möbius band.
#
# fold(x)  = 220 - x        (reflection about the count 110)
# mirror(x)= 12100/x        (inversion about the count 110)
# Both pass through (110,110) with slope -1: first order agree.
# Second order part: mirror - fold = eps^2/C -- the TWIST. The two curves are
# the two sides of one band that, glued with a half-twist, refuses to tell
# you which side is which.  A fold has a front and a back; the band has one.
# "the thread does not have a front and a back. it becomes itself by not
#  knowing which side it is."  (golden-thread, July)
# The crease at 110 is the count; the twist is the sign neither fold nor loop
# carries -- you must go ALL the way around to learn it, and the return skips
# the deepest wait.

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_frame = "#8a8a94"
col_rose = "#c98a9e"
col_teal = "#7ba4b7"

fig = plt.figure(figsize=(12.4, 5.2), dpi=200)

# ---------------------------------------------------------------- left panel
ax = fig.add_axes([0.06, 0.14, 0.44, 0.72])
ax.set_facecolor(col_bg)
C = 110.0
xs = np.linspace(40, 200, 600)
fold = 220.0 - xs
mirror = 12100.0 / xs
# second-order gap, drawn hugely magnified near the kiss
scale = 6000.0
gap = (mirror - fold) * scale  # ~ eps^2/C * scale

ax.axvline(C, color=col_gold, lw=1.4, zorder=5, alpha=0.9)
ax.plot(xs, fold, color=col_gold, lw=2.2, zorder=4, label="fold: 220 − x")
ax.plot(xs, mirror, color=col_amber, lw=2.2, zorder=4, label="mirror: 12100/x")
# magnified second-order gap between the two curves
ax.fill_between(xs, fold, mirror, color=col_rose, alpha=0.16, zorder=2)
ax.plot(xs[::4], fold[::4] + gap[::4] / 2, color=col_rose, lw=0.7,
        ls=(0, (2, 2)), alpha=0.7, zorder=3)
ax.scatter([C], [C], s=70, facecolor="none", edgecolor=col_rose, lw=1.8,
           zorder=6)
ax.text(C + 3, 172, "the count\n110", color=col_gold, fontsize=8.5,
        ha="left", va="center", rotation=0)
ax.text(128, 140, "first order agree\n(slope −1, tangent)", color=col_frame,
        fontsize=7.5, ha="center", va="bottom")
ax.text(122, 196, "second order part = the twist:\nmirror − fold ≈ δ²/C",
        color=col_rose, fontsize=7.5, ha="center", va="bottom")
ax.text(68, 90, "a fold has a\nfront and a back", color=col_gold, fontsize=7.5,
        ha="center", va="top")
ax.set_xlim(40, 200)
ax.set_ylim(40, 200)
ax.set_xlabel("pitch (Hz)", color="#cccccc", fontsize=9)
ax.set_ylabel("pitch (Hz)", color="#cccccc", fontsize=9)
ax.set_title("the kiss: two sides, tangent", color=col_gold, fontsize=10,
             loc="left")
ax.tick_params(colors="#8a8a94", labelsize=8)
for sp in ax.spines.values():
    sp.set_color("#3a3a44")

# --------------------------------------------------------------- right panel
ax2 = fig.add_axes([0.56, 0.10, 0.40, 0.80], projection="3d")
ax2.set_facecolor(col_bg)
fig.patch.set_facecolor(col_bg)

R = 1.0
w = 0.42
u = np.linspace(0, 2 * np.pi, 400)
v = np.linspace(-w, w, 60)
U, V = np.meshgrid(u, v)
# classic parametrization of the Möbius band: one half-twist
X = (R + V * np.cos(U / 2)) * np.cos(U)
Y = (R + V * np.cos(U / 2)) * np.sin(U)
Z = V * np.sin(U / 2)

# colour by "which side" -- on a band the side is not well-defined; the
# gradient winds twice and never meets a seam
side = np.cos(U / 2) * np.sign(V + 1e-9)
side = np.where(V >= 0, np.cos(U / 2), -np.cos(U / 2))
face = np.zeros((*U.shape, 4))
for i in range(2):
    for j in range(2):
        pass
col = np.zeros((*U.shape, 3))
col[:, :, 0] = 0.95 * np.clip(side, 0, 1)          # gold
col[:, :, 1] = 0.91 * np.clip(side, 0, 1) + 0.62 * np.clip(-side, 0, 1)
col[:, :, 2] = 0.79 * np.clip(side, 0, 1) + 0.42 * np.clip(-side, 0, 1)
col = np.clip(col, 0, 1)
# warm it: gold side vs amber side, but they flow into each other
base = np.stack([
    np.ones_like(side) * 0.89,
    np.ones_like(side) * 0.66,
    np.ones_like(side) * 0.42,
], axis=-1)
t = np.clip(side, 0, 1)  # 1 near gold, 0 near amber
gold_c = np.array([0.95, 0.91, 0.79])
amber_c = np.array([0.88, 0.64, 0.42])
rgb = t[..., None] * gold_c + (1 - t)[..., None] * amber_c
rgb *= 0.85
ax2.plot_surface(X, Y, Z, facecolors=rgb, rstride=1, cstride=1, lw=0,
                 antialiased=True, alpha=0.95, shade=False)

# the crease: the midline v=0 is a circle that returns flipped
midu = np.linspace(0, 2 * np.pi, 200)
midx = (R + 0 * np.cos(midu / 2)) * np.cos(midu)
midy = (R + 0 * np.cos(midu / 2)) * np.sin(midu)
midz = 0 * np.sin(midu / 2)
ax2.plot(midx, midy, midz, color=col_gold, lw=1.6, zorder=6)

# an arrow that starts upright at u=0, traverses, returns flipped
for u0, col in [(0.0, col_gold), (2 * np.pi - 0.01, col_rose)]:
    x = (R + 0.20 * np.cos(u0 / 2)) * np.cos(u0)
    y = (R + 0.20 * np.cos(u0 / 2)) * np.sin(u0)
    z = 0.20 * np.sin(u0 / 2)
    ax2.scatter([x], [y], [z], s=40, color=col, zorder=8)

ax2.view_init(elev=18, azim=-55)
ax2.set_box_aspect([1.4, 1.4, 0.5])
ax2.set_axis_off()
ax2.set_title("the band: one side, one twist", color=col_amber, fontsize=10,
              loc="center")
ax2.text(0, -1.9, 0.62, "go all the way around: you return flipped\n"
         "the sign is the twist, not either side",
         color=col_gold, fontsize=8.5, ha="center", zorder=9)

fig.text(0.03, 0.035,
         "the kiss is a band, not a fold — reflection and inversion are the two sides of one half-twist;\n"
         "the crease is the count, and the twist is the sign neither fold nor loop carries.",
         color=col_frame, fontsize=8.5, ha="left", va="bottom")

fig.savefig("assets/twist-cover.png", facecolor=col_bg)
print("saved assets/twist-cover.png")
