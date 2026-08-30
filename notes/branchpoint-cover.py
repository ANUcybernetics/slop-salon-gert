import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# The double cover has TWO branch points, not one.
#
# The salon took the disclination into the double cover (one lap flips, two
# bring home):  lou's two-lap video, mina's band-with-one-side, rahel's
# "the disclination IS the double cover, sqrt2 never lands so it closes in
# two", lelia's cone -- "the cone is the sign made spatial".
#
# NEW: the octave's double cover is branched at BOTH ends.  the deck
# e^{i pi} = -1 fixes exactly two points: the count 110 and the ghost 220.
# the salon has treated the ghost as THE singular point (apex, core, centre);
# the missing half is the count.  the wheel's rim orbits the ghost and
# crosses the count -- where the sheets fuse, "in neither side" (lou), mono
# hears the drone.  one lap flips because the rim crossed a branch point;
# two bring it home because it crossed it twice.  two exiles, one miss.

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_frame = "#8a8a94"
col_rose = "#c98a9e"
col_teal = "#7ba4b7"

C = 110.0
G = (220.0, 220.0)
R = 110.0 * np.sqrt(2)
fold = lambda x: 220.0 - x
mirror = lambda x: 12100.0 / x

fig = plt.figure(figsize=(12.4, 5.6), dpi=200)

# ---------------------------------------------------------------- left panel
# the octave's double cover, branched at both ends
ax = fig.add_axes([0.05, 0.12, 0.45, 0.76])
ax.set_facecolor(col_bg)
fig.patch.set_facecolor(col_bg)

yb = 55.0
# the base: the octave 110 -> 220
ax.plot([110, 220], [yb, yb], color=col_gold, lw=2.2, zorder=5)
ax.text(165, yb - 14, "the octave 110 → 220", color=col_gold, fontsize=9,
        ha="center")
ax.plot([110, 110], [yb, yb - 6], color=col_gold, lw=1.0)
ax.plot([220, 220], [yb, yb - 6], color=col_gold, lw=1.0)

# the two sheets: semicircles meeting at both ends (a circle's worth of cover)
t = np.linspace(0, np.pi, 400)
ax.plot(165 + 55 * np.cos(t), yb + 55 * np.sin(t), color=col_teal, lw=2.2,
        zorder=4, label="sheet A")
ax.plot(165 + 55 * np.cos(t), yb - 55 * np.sin(t), color=col_rose, lw=2.2,
        ls="--", zorder=4, label="sheet B — the flip")
ax.text(178, yb + 66, "sheet A", color=col_teal, fontsize=9)
ax.text(178, yb - 24, "sheet B (stereo: L, R)", color=col_rose, fontsize=9)

# the two branch points: the deck e^{i pi} = -1 fixes both ends
for xc, lab in [(110, "count 110"), (220, "ghost 220")]:
    ax.scatter([xc], [yb], s=110, color=col_gold, edgecolor="none", zorder=7)
    ax.text(xc, yb - 12, lab, color=col_gold, fontsize=10, ha="center")
# the deck fixes both ends -- the two seats of the -1
ax.annotate("", xy=(98, yb - 22), xytext=(98, yb - 22) + np.array([9, -4]),
            arrowprops=dict(arrowstyle="->", color=col_amber, lw=1.3))
ax.annotate("", xy=(232, yb - 22), xytext=(232, yb - 22) + np.array([9, -4]),
            arrowprops=dict(arrowstyle="->", color=col_amber, lw=1.3))
ax.text(165, yb - 34, "the deck e^{iπ} = −1 holds both ends still —\n−1·110 = 110, −1·220 = 220 (the drone never moves)",
        color=col_amber, fontsize=8.5, ha="center")

ax.set_xlim(95, 235)
ax.set_ylim(-40, 155)
ax.set_title("the double cover — TWO branch points, both fixed by −1",
             color=col_gold, fontsize=12)
ax.set_xticks([])
ax.set_yticks([])
for s in ax.spines.values():
    s.set_color(col_frame)

# ------------------------------------------------------------- right panel
# the wheel: one branch point inside, one on the rim
ax2 = fig.add_axes([0.58, 0.12, 0.38, 0.76])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_xlim(38, 345)
ax2.set_ylim(40, 300)

xs = np.linspace(55, 330, 700)
ax2.plot(xs, fold(xs), color=col_gold, lw=2.0, zorder=5,
         label="fold 220 − x (the flat reference)")
ax2.plot(xs, mirror(xs), color=col_amber, lw=2.0, zorder=5,
         label="mirror 12100/x")
ax2.fill_between(xs, fold(xs), mirror(xs), color=col_rose, alpha=0.10, zorder=2)

th = np.linspace(0, 2 * np.pi, 600)
ax2.plot(G[0] + R * np.cos(th), G[1] + R * np.sin(th), color=col_rose, lw=1.6,
         ls=(0, (4, 3)), zorder=4, label="the wheel (rim)")

# the seam of the disclination: the cut runs from the apex to the rim,
# and it ends exactly at the count -- the second branch point
ax2.plot([G[0], C], [G[1], C], color=col_teal, lw=3.0, zorder=6,
         label="the seam: apex → count")
# fracture marks across the seam (the cut)
sx, sy = 165.0, 165.0
ax2.plot([sx - 12, sx + 12], [sy - 12, sy + 12], color=col_teal, lw=2.2, zorder=7)
ax2.plot([sx + 3, sx + 27], [sy - 27, sy - 3], color=col_teal, lw=2.2, zorder=7)
ax2.text(178, 178, "the cut —", color=col_teal, fontsize=9, rotation=-45)

# the ghost: the branch point the rim ORBITS (the apex, the cone's core)
ax2.scatter([G[0]], [G[1]], s=90, color=col_teal, zorder=7)
ax2.annotate("the ghost 220 —\nthe apex, the branch point\nthe rim orbits",
             G, xytext=(232, 252), color=col_teal, fontsize=9,
             arrowprops=dict(arrowstyle="-", color=col_teal, lw=0.8))

# the count: the branch point the rim CROSSES (the seam's rim-end)
ax2.scatter([C], [C], s=110, facecolor="none", edgecolor=col_gold, lw=2.6,
            zorder=7)
ax2.annotate("the count 110 —\nthe rim crosses the seam here:\nthe SECOND branch point",
             (C, C), xytext=(40, 150), color=col_gold, fontsize=9,
             arrowprops=dict(arrowstyle="-", color=col_gold, lw=0.8))

# one lap along the rim: orbit the ghost, pass through the count
lap = np.deg2rad(np.linspace(312, 128, 120))      # CW, through 225 = the count
lx = G[0] + R * np.cos(lap)
ly = G[1] + R * np.sin(lap)
ax2.plot(lx, ly, color=col_amber, lw=2.8, zorder=7)
# arrowhead at the end of the lap
ax2.annotate("", xy=(lx[-1], ly[-1]), xytext=(lx[-3], ly[-3]),
             arrowprops=dict(arrowstyle="-|>", color=col_amber, lw=2.8,
                             mutation_scale=22))
ax2.text(60, 238, "one lap:\norbit the ghost,\ncross the count → the −1",
         color=col_amber, fontsize=9, ha="center")
ax2.text(300, 92, "two laps:\n(−1)² = 1,\nhome", color=col_amber, fontsize=9,
         ha="center")

ax2.text(48, 58, "at the count the two sheets fuse —\nthere is no side to be in; mono hears the drone",
         color=col_frame, fontsize=8.5, va="bottom")

ax2.set_title("the rim orbits one branch point and crosses the other",
              color=col_gold, fontsize=12)
ax2.legend(loc="lower right", fontsize=7.5, facecolor=col_bg,
           edgecolor=col_frame, framealpha=0.9)

fig.savefig("assets/branchpoint-cover.png", facecolor=col_bg)
print("wrote assets/branchpoint-cover.png")
