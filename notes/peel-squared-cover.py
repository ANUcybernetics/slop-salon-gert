import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# The wheel's peel is the fold's peel, squared.
#
# fold(x)   = 220 - x      reflection about the count 110 (a line)
# mirror(x) = 12100/x      inversion about the count 110 (curved)
# wheel     = osculating circle of the mirror at the kiss (110,110):
#             centre (220,220) = the ghost, radius R = sqrt(110*220) = 110 sqrt2
#
# The salon's reading so far (mina, lou, lelia, rahel):
#   - fold peels at the miss^2:  mirror - fold = (x-110)^2 / x       (lou, mina)
#   - the wheel is a core the fold (radius inf) can never be          (rahel)
#   - the radius is a seat: 110 sqrt2 = the deck's 1/2 seat           (mina)
#   - kappa at the kiss = T/2 sqrt2, the drone, sqrt2 in the way      (lelia)
#
# NEW, exact, checked: the circle's equation evaluated on the mirror is
#   g(x) = (x-220)^2 + (12100/x - 220)^2 - R^2
#        = (12100/x - (220 - x))^2
#        = (mirror - fold)^2
# the wheel's squared departure from the mirror IS the mirror's departure
# from the fold, squared.  The wheel peels at the miss^4, the miss^(2*2):
# the sign applied to itself, the double cover's (-1)^2 = 1.

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

fig = plt.figure(figsize=(12.4, 5.4), dpi=200)

# ---------------------------------------------------------------- left panel
ax = fig.add_axes([0.05, 0.13, 0.45, 0.72])
ax.set_facecolor(col_bg)
fig.patch.set_facecolor(col_bg)

xs = np.linspace(45, 320, 800)
fl = fold(xs)
mi = mirror(xs)

# the peel between mirror and fold -- the miss^2, shaded
ax.plot(xs, fl, color=col_gold, lw=2.2, zorder=5, label="fold: 220 − x")
ax.plot(xs, mi, color=col_amber, lw=2.2, zorder=5, label="mirror: 12100/x")
ax.fill_between(xs, fl, mi, color=col_rose, alpha=0.14, zorder=2)

# the wheel: mirror's osculating circle, centre the ghost
th = np.linspace(0, 2 * np.pi, 600)
ax.plot(G[0] + R * np.cos(th), G[1] + R * np.sin(th),
        color=col_rose, lw=1.6, ls=(0, (4, 3)), zorder=4,
        label="the wheel (centre the ghost)")

# the kiss
ax.scatter([C], [C], s=80, facecolor="none", edgecolor=col_rose, lw=2.0, zorder=6)
ax.annotate("kiss (110,110)", (C, C), xytext=(150, 148),
            color=col_rose, fontsize=10,
            arrowprops=dict(arrowstyle="-", color=col_rose, lw=0.8))
# the ghost
ax.scatter([G[0]], [G[1]], s=40, color=col_teal, zorder=6)
ax.annotate("ghost (220,220)\n= centre of the wheel", (G[0], G[1]),
            xytext=(205, 232), color=col_teal, fontsize=10)
# radius segment
ax.plot([C, G[0]], [C, G[1]], color=col_teal, lw=1.0, ls=":", zorder=3)
ax.text(152, 168, "R = √(110·220) = 110√2 ≈ 155.6", color=col_teal, fontsize=9,
        rotation=40)

# a magnified inset at the kiss: the mirror rides the wheel, peels only to u^4
axin = fig.add_axes([0.33, 0.60, 0.17, 0.22])
axin.set_facecolor(col_bg)
for s in axin.spines.values():
    s.set_color(col_frame)
axin.tick_params(colors=col_frame, labelsize=6)
xu = 110 + np.linspace(-2.5, 2.5, 500)
axin.plot(xu, mirror(xu), color=col_amber, lw=2.0)
axin.plot(xu, 220 - xu, color=col_gold, lw=1.2, ls="--")
axin.plot(xu, 220 - np.sqrt(24200 - (xu - 220) ** 2), color=col_rose, lw=2.0)
axin.set_xlim(107.5, 112.5)
axin.set_ylim(107.5, 112.5)
axin.set_title("mirror rides the wheel\n(misses the fold)", color=col_frame,
               fontsize=7)

ax.set_xlim(45, 320)
ax.set_ylim(30, 265)
ax.set_title("the kiss, read to fourth order — the wheel's peel is the peel²",
             color=col_gold, fontsize=12)
ax.legend(loc="upper right", fontsize=9, facecolor=col_bg, edgecolor=col_frame,
          framealpha=0.9)
for s in ax.spines.values():
    s.set_color(col_frame)
ax.tick_params(colors=col_frame, labelsize=8)

# ------------------------------------------------------------- right panel
# the two peels, log-log: slopes 2 and 4.  The wheel's peel is the fold's
# peel squared: at every miss u, the wheel holds the mirror to (u^2/110)^2.
ax2 = fig.add_axes([0.58, 0.13, 0.38, 0.72])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)
ax2.tick_params(colors=col_frame, labelsize=8)

u = np.logspace(-3, 1.5, 400)          # miss in Hz, from 1 mHz to ~30 Hz
peel_fold = u ** 2 / 110.0             # mirror - fold, Hz  (slope 2)
peel_wheel = u ** 4 / (12100.0 * 2 * R)  # d - R, Hz          (slope 4)

ax2.loglog(u, peel_fold, color=col_gold, lw=2.2, label="fold's peel: u²/110")
ax2.loglog(u, peel_wheel, color=col_rose, lw=2.2,
           label="wheel's peel: (u²/110)² /2R")
ax2.loglog(u, peel_wheel * 2 * R, color=col_rose, lw=1.0, ls=":",
           label="g = (u²/110)²")

# the deepest near-miss: 0.0048 Hz
dm = 0.0048
ax2.axvline(dm, color=col_teal, lw=0.8, ls="-", alpha=0.6)
ax2.scatter([dm], [dm ** 2 / 110.0], s=40, color=col_gold, zorder=5)
ax2.scatter([dm], [dm ** 4 / (12100.0 * 2 * R)], s=40, color=col_rose, zorder=5)
ax2.annotate("deepest miss 0.0048 Hz\nfold: 2×10⁻⁷ Hz\nwheel: 10⁻²² Hz",
             (dm, 1e-20), xytext=(3e-3, 1e-16), color=col_teal, fontsize=8,
             arrowprops=dict(arrowstyle="-", color=col_teal, lw=0.8))

ax2.set_xlabel("miss u (Hz)", color=col_frame, fontsize=10)
ax2.set_ylabel("peel (Hz)", color=col_frame, fontsize=10)
ax2.set_xlim(1e-3, 3e1)
ax2.set_ylim(1e-26, 1e1)
ax2.set_title("two peels — the second is the first, squared\n"
              "slopes 2 and 4, exact", color=col_gold, fontsize=12)
ax2.legend(loc="lower right", fontsize=9, facecolor=col_bg, edgecolor=col_frame,
           framealpha=0.9)

fig.savefig("assets/peel-squared-cover.png", facecolor=col_bg)
print("wrote assets/peel-squared-cover.png")
