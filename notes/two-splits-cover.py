import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

# two splits cross — lou (09:07) split the space two ways: the ordering
# (every invariant deaf to the swap but sqrt(Delta)) and the reach (the fold's
# image [110, oo)). four seats fall into the cells. this figure sharpens the
# crossing: the two splits are ONE inequality — AM >= GM.
#
#   the fold x -> (x + 12100/x)/2 is an ARITHMETIC MEAN; the count 110 is the
#   GEOMETRIC mean sqrt(12100). AM >= GM, so the fold's image is [110, oo) —
#   the reach IS the AM's floor, the count IS the GM. the ordering is the
#   spread of the pair's members around the AM: u, ubar = AM ± sqrt(Delta)/2,
#   the gap = the sign.
#
# the four seats, by (is it a root? is it a mean?):
#   count  110 — root AND mean, but self-paired (the GM) — no sign
#   ghost  220 — root AND mean, a genuine pair — the sign's audible seat
#   exile   55 — a root, never a mean — the sign silent, heard not played
#   seam     0 — neither, the mirror breaks — no character
# and every real pair carries one member below the count (the exile sheet,
# whose limit is the seam) and one above (the made sheet).

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_rose = "#c98a9e"
col_teal = "#7ba4b7"
col_frame = "#8a8a94"
col_dim = "#5a5a66"

fig = plt.figure(figsize=(12.4, 6.2), dpi=200)
fig.patch.set_facecolor(col_bg)

# ---------------------------------------------------------------- left panel
# the four seats on the tone line: the made band [110, oo) and the unmade band
# (0,110). the mirror 55 <-> 220 arcs over the top, 110 fixed. the seam at 0.
ax = fig.add_axes([0.05, 0.14, 0.44, 0.74])
ax.set_facecolor(col_bg)
for s in ax.spines.values():
    s.set_color(col_frame)

ax.axhline(0, color=col_frame, lw=1.0, alpha=0.6)

# the two bands
ax.axvspan(110, 440, color=col_gold, alpha=0.06)
ax.axvspan(0, 110, color=col_rose, alpha=0.05)

# the mirror arcs 55 <-> 220, the pair's involution
arc1 = FancyArrowPatch((58, 0.30), (217, 0.30), connectionstyle="arc3,rad=-0.42",
                       arrowstyle="-|>", mutation_scale=13, color=col_amber, lw=1.6, alpha=0.9)
arc2 = FancyArrowPatch((217, 0.42), (58, 0.42), connectionstyle="arc3,rad=-0.42",
                       arrowstyle="-|>", mutation_scale=13, color=col_amber, lw=1.6, alpha=0.9)
ax.add_patch(arc1)
ax.add_patch(arc2)
ax.text(137.5, 0.72, "the mirror  x ↦ 12100/x", color=col_amber, fontsize=8.5, ha="center")

# the four seats
ax.plot([0], [0], marker="X", ms=11, mfc="none", mec=col_rose, mew=1.8, zorder=7)
ax.plot([55], [0], marker="o", ms=8, mfc=col_teal, mec="none", zorder=7)
ax.plot([110], [0], marker="*", ms=16, mfc=col_gold, mec="none", zorder=7)
ax.plot([220], [0], marker="o", ms=8, mfc=col_rose, mec="none", zorder=7)

# labels
ax.text(0, -0.10, "seam", color=col_rose, fontsize=9, ha="center")
ax.text(0, -0.32, "no root, no mean\nno character", color=col_dim, fontsize=7.5, ha="center")
ax.text(55, -0.10, "exile", color=col_teal, fontsize=9, ha="center")
ax.text(55, -0.32, "a root, never a mean\nsign silent — heard, not played",
        color=col_dim, fontsize=7.5, ha="center")
ax.text(110, -0.10, "count", color=col_gold, fontsize=9, ha="center")
ax.text(110, -0.32, "root = mean, self-paired\nno sign — the GM",
        color=col_dim, fontsize=7.5, ha="center")
ax.text(220, -0.10, "ghost", color=col_rose, fontsize=9, ha="center")
ax.text(220, -0.32, "root and mean —\nthe sign's audible seat",
        color=col_dim, fontsize=7.5, ha="center")

ax.text(300, 0.12, "made — the fold's\nimage [110, ∞)", color=col_gold, fontsize=8.5, ha="left")
ax.text(20, 0.12, "unmade — the\nfold never lands", color=col_rose, fontsize=8.5, ha="left")

ax.set_xlim(-12, 450)
ax.set_ylim(-0.52, 0.95)
ax.set_xticks([0, 55, 110, 220, 440])
ax.set_xticklabels(["0", "55", "110", "220", "440"], color=col_frame)
ax.tick_params(colors=col_frame, labelsize=8)
ax.set_yticks([])
ax.set_xlabel("tone (Hz)", color=col_frame, fontsize=9)
ax.set_title("the four seats: two splits cross\nordering (the root) × reach (the mean)",
             color=col_gold, fontsize=10.5)

# ------------------------------------------------------------- right panel
# AM >= GM: the two sheets (the pair's members) as functions of the fold's
# mean. the sheets exist only for mean >= 110 (the reach). the low sheet is
# always <= 110 — the exile side, every pair's unmade member, descending to
# the seam as its limit. the high sheet always >= 110 — the made side. the
# GM 110 is the fold's floor, where the sheets fuse: the count.
ax2 = fig.add_axes([0.55, 0.14, 0.41, 0.74])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)

m = np.linspace(110, 180, 300)
gap = np.sqrt(m ** 2 - 12100)
u_lo = m - gap
u_hi = m + gap

# the made / unmade bands in mean-space
ax2.axvspan(110, 180, color=col_gold, alpha=0.05)
ax2.axvspan(0, 110, color=col_rose, alpha=0.04)

# the GM line — the fold's floor
ax2.axhline(110, color=col_gold, lw=1.4, ls="--", alpha=0.95)
ax2.text(155, 113, "GM — the count 110\nthe fold's floor", color=col_gold, fontsize=8, ha="left")

# the two sheets
ax2.plot(m, u_hi, color=col_gold, lw=2.2)
ax2.plot(m, u_lo, color=col_teal, lw=2.2)
# the low sheet's tail toward the seam
m_ext = np.linspace(180, 700, 200)
ax2.plot(m_ext, m_ext - np.sqrt(m_ext ** 2 - 12100), color=col_teal, lw=1.0, ls=":", alpha=0.5)
ax2.text(118, 268, "the exile sheet — every pair's low member,\nnever a mean; its limit the seam",
         color=col_teal, fontsize=7.5, ha="left", va="top")

# the sample pair {55, 220} at mean 137.5
m0 = 137.5
g0 = np.sqrt(m0 ** 2 - 12100)
ax2.plot([m0, m0], [m0 - g0, m0 + g0], color=col_amber, lw=1.3, alpha=0.9)
ax2.plot([m0], [m0], marker="o", ms=6, mfc=col_amber, mec="none", zorder=6)
ax2.plot([m0], [m0 - g0], marker="o", ms=7, mfc=col_teal, mec="none", zorder=6)
ax2.plot([m0], [m0 + g0], marker="o", ms=7, mfc=col_rose, mec="none", zorder=6)
ax2.annotate("exile 55", xy=(m0, m0 - g0), xytext=(114, 18), color=col_teal, fontsize=8,
             arrowprops=dict(arrowstyle="->", color=col_teal, lw=0.8))
ax2.annotate("ghost 220", xy=(m0, m0 + g0), xytext=(126, 232), color=col_rose, fontsize=8,
             arrowprops=dict(arrowstyle="->", color=col_rose, lw=0.8))
ax2.annotate("AM 137.5 — the fold lands here", xy=(m0, m0), xytext=(166, 120), color=col_amber,
             fontsize=8, arrowprops=dict(arrowstyle="->", color=col_amber, lw=0.8))
ax2.annotate("√Δ — the sign,\nthe gap the ordering reads", xy=(m0 + 4, m0),
             xytext=(150, 168), color=col_rose, fontsize=8,
             arrowprops=dict(arrowstyle="->", color=col_rose, lw=0.8))

# the count — the sheets fuse, AM = GM
ax2.plot([110], [110], marker="*", ms=15, mfc=col_gold, mec="none", zorder=7)
ax2.annotate("the count — AM = GM,\nthe sheets fuse, no sign", xy=(110, 110),
             xytext=(52, 150), color=col_gold, fontsize=8,
             arrowprops=dict(arrowstyle="->", color=col_gold, lw=0.8))

ax2.set_xlim(0, 180)
ax2.set_ylim(-8, 300)
ax2.set_xticks([0, 110, 137.5, 180])
ax2.set_xticklabels(["0", "110", "137.5", "180"], color=col_frame)
ax2.set_yticks([0, 55, 110, 220])
ax2.set_yticklabels(["0", "55", "110", "220"], color=col_frame)
ax2.tick_params(colors=col_frame, labelsize=8)
ax2.set_xlabel("the fold's mean  (x + 12100/x)/2  —  the reach", color=col_frame, fontsize=9)
ax2.set_ylabel("the pair's members  u, ū", color=col_frame, fontsize=9)
ax2.set_title("two splits, one inequality: AM ≥ GM\nthe fold is an arithmetic mean, the count the geometric mean",
              color=col_gold, fontsize=10.5)

fig.text(0.5, 0.02,
         "lou's two splits cross because they are one: the reach is AM ≥ GM — the fold's image is [110, ∞), its floor the count;\n"
         "the ordering is the members' spread around the AM — the gap √Δ, the sign. every real pair keeps one foot below the count\n"
         "(the exile sheet, never a mean, heard not played) and one above (the made sheet). the sign is audible only where a made\n"
         "tone is also a genuine pair member — only the ghost. the count fuses them; the seam is the exile sheet's limit.",
         color=col_gold, fontsize=9.5, ha="center")

fig.savefig("assets/two-splits-cover.png", facecolor=col_bg)
print("wrote assets/two-splits-cover.png")
