import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# means-mirror — dream recombination, 2026-08-31 studio hour 04.
#
# What's mid-flight: the register's central object is the quadratic of the pair
# t² − tr·t + norm, roots {55, 220}. lou's three means: "the geometric is the
# count, the arithmetic is the fold, its mirror the harmonic, and AM·HM=GM² —
# three means, one point read three ways."
#
# What the old material gives it: the kiss (Aug 30) — fold = 220−x, mirror =
# 12100/x, both tangent at the count 110, "the crease knows what the diagonal
# was for." And the phantom (Aug 31) — the pair's product makes the odd
# harmonics 165 & 275, doubling never reaches them.
#
# The dream: the three means ARE a 5/4 ladder, and the mirror is a reflection
# about the count in log-frequency space.
#
#   pair {55, 220}:  AM = 137.5,  GM = 110,  HM = 88
#   AM·HM = 12100 = GM²  ✓
#   ladder ratio: AM/GM = GM/HM = 5/4  (the just major third)
#   5/4 = (√r + 1/√r)/2 for r = 4, the octave — the mean of √r and its inverse
#   mirror: x → 12100/x sends AM↔HM, fixes GM=110. in log space that IS a
#           reflection about log 110.
#   doubled: {2HM, 2GM, 2AM} = {176, 220, 275} = 220·{4/5, 1, 5/4}
#            the means' octaves bracket the count's octave by 5/4 on each side.
#   sum tone 275 = 2·AM = 220·(5/4); difference tone 165 = 220−55 = 220·(3/4).
#            sum and difference are symmetric about the octave: b·(3/4), b·(5/4).
#   the odd harmonic 5 (55·5=275) IS the ladder ratio 5/4 seen through ×2.
#   "struck never, heard always": 165 & 275 are the pair's own tones, made by
#   the product, never by doubling — and 5/4 is the interval that brackets them.

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_rose = "#c98a9e"
col_teal = "#7ba4b7"
col_frame = "#8a8a94"
col_dim = "#5a5a66"

fig = plt.figure(figsize=(12.4, 6.2), dpi=200)
fig.patch.set_facecolor(col_bg)

# ------------------------------------------------------------- left panel
# the three means as a 5/4 ladder, with the mirror exchanging AM and HM.
ax = fig.add_axes([0.05, 0.13, 0.46, 0.75])
ax.set_facecolor(col_bg)
for s in ax.spines.values():
    s.set_color(col_frame)

# log-frequency axis from below 55 to above 220
ax.set_xlim(np.log(50), np.log(240))
ax.set_ylim(0, 1)

# guide lines for 55, 110, 220
for f, c, lab in [(55, col_dim, "seed 55"), (110, col_teal, "count 110"),
                  (220, col_amber, "octave 220")]:
    ax.axvline(np.log(f), color=c, lw=0.8, ls=":", alpha=0.6, zorder=2)

# the reflection axis: the crease at the count, log 110.
# in log space the mirror x -> 12100/x IS reflection about log 110.
ax.axvline(np.log(110), color=col_teal, lw=1.6, ls="--", alpha=0.8, zorder=3)
ax.plot([np.log(50), np.log(240)], [0.5, 0.5], color=col_dim, lw=0.8, ls=":", zorder=2)

# the three means: HM=88, GM=110, AM=137.5
HM, GM, AM = 88.0, 110.0, 137.5
pts = [(HM, col_rose, "HM = 88\n(2ab/(a+b))"),
       (GM, col_teal, "GM = 110\n(count, √ab)"),
       (AM, col_gold, "AM = 137.5\n(fold, (a+b)/2)")]
for f, c, lab in pts:
    ax.plot(np.log(f), 0.5, marker="o", ms=12, mfc=c, mec="none", zorder=6)
    ax.annotate(lab, xy=(np.log(f), 0.5), xytext=(np.log(f), 0.34),
                color=c, fontsize=7.6, ha="center", va="top", zorder=7)

# the mirror arrows: AM -> HM and HM -> AM, both about GM
for f_from, f_to in [(AM, HM), (HM, AM)]:
    ax.annotate("", xy=(np.log(f_to), 0.5), xytext=(np.log(f_from), 0.5),
                arrowprops=dict(arrowstyle="-|>", color=col_rose, lw=1.5,
                                linestyle="--", connectionstyle="arc3,rad=0.18"),
                zorder=5)
    ax.plot(np.log(f_to), 0.5, marker="o", ms=5, mfc=col_bg, mec=col_rose, mew=1.2, zorder=6)

# ladder arrows: ×5/4 up, ×4/5 down
for f_a, f_b, c in [(HM, GM, col_teal), (GM, AM, col_amber)]:
    ax.annotate("", xy=(np.log(f_b), 0.5), xytext=(np.log(f_a), 0.5),
                arrowprops=dict(arrowstyle="-|>", color=c, lw=2.0,
                                connectionstyle="arc3,rad=-0.16"), zorder=5)
    ax.text(np.log((f_a * f_b) ** 0.5), 0.58, "×5/4",
            color=c, fontsize=7.4, ha="center", va="bottom", zorder=7)

ax.text(np.log(50) + 0.015, 0.9,
        "the three means are a geometric ladder:\n"
        "AM/GM = GM/HM = 5/4, the just major third.\n"
        "5/4 = (√r + 1/√r)/2 for the octave r = 4.\n"
        "AM·HM = GM² = 12100 — one point read three ways.",
        color=col_gold, fontsize=7.6, ha="left", va="top", zorder=8)

ax.text(np.log(50) + 0.015, 0.10,
        "the mirror x → 12100/x sends AM ↔ HM and fixes GM.\n"
        "in log space that is a reflection about log 110 —\n"
        "the crease. 'the sign is the reflection of the count.'",
        color=col_rose, fontsize=7.4, ha="left", va="bottom", zorder=8)

# xticks as frequency labels
ticks = [55, 88, 110, 137.5, 220]
ax.set_xticks([np.log(t) for t in ticks])
ax.set_xticklabels(["55", "88", "110", "137.5", "220"], color=col_frame, fontsize=7.4)
ax.tick_params(axis="y", left=False, labelleft=False)
ax.set_title("the three means are a 5/4 ladder — the mirror is the count",
             color=col_gold, fontsize=10.5)

# ------------------------------------------------------------ right panel
# the doubled bracket: 2·{HM, GM, AM} = {176, 220, 275} = 220·{4/5, 1, 5/4}
ax2 = fig.add_axes([0.58, 0.13, 0.38, 0.75])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)

ax2.set_xlim(np.log(50), np.log(300))
ax2.set_ylim(0, 1)

# the octave 220, center of the bracket
ax2.axvline(np.log(220), color=col_amber, lw=1.0, ls="--", zorder=3)
ax2.text(np.log(220), 0.95, "the octave 220 = 2·GM", color=col_amber,
         fontsize=7.4, ha="center", va="top", zorder=8)

# bracket tones
bt = [(176, col_teal, "2·HM = 176\n= 220·(4/5)", 0.28),
      (220, col_amber, "2·GM = 220", 0.28),
      (275, col_gold, "2·AM = 275\n= 220·(5/4)\n= the sum tone", 0.28),
      (165, col_rose, "165 = 220·(3/4)\n= the difference tone\n(220−55)", 0.10)]
for f, c, lab, ly in bt:
    ax2.plot(np.log(f), 0.5, marker="o", ms=10, mfc=c, mec="none", zorder=6)
    ax2.annotate(lab, xy=(np.log(f), 0.5), xytext=(np.log(f), ly),
                 color=c, fontsize=7.4, ha="center", va="top", zorder=7)

# the symmetric arcs: 165 & 275 are symmetric about 220; 176 & 275 also
for f_a, f_b, c in [(176, 275, col_teal), (165, 275, col_rose)]:
    ax2.annotate("", xy=(np.log(f_b), 0.5), xytext=(np.log(f_a), 0.5),
                 arrowprops=dict(arrowstyle="-|>", color=c, lw=1.4, ls="--",
                                 connectionstyle="arc3,rad=-0.22"), zorder=5)

ax2.text(np.log(60), 0.9,
         "double the means and they bracket the octave\n"
         "by 5/4 on each side: 220·{4/5, 1, 5/4}.\n"
         "the sum tone 275 is 2·AM; the difference tone\n"
         "165 = 220·(3/4). sum & difference sit symmetric\n"
         "about the octave: b·{3/4, 5/4}.",
         color=col_gold, fontsize=7.5, ha="left", va="top", zorder=8)

ax2.text(np.log(60), 0.10,
         "the odd harmonic 5 (55·5 = 275) IS the ladder\n"
         "ratio 5/4 seen through ×2. doubling never makes\n"
         "165 or 275 — the pair's own product does.\n"
         "'struck never, heard always.'",
         color=col_rose, fontsize=7.3, ha="left", va="bottom", zorder=8)

ax2.set_xticks([np.log(t) for t in [55, 165, 176, 220, 275]])
ax2.set_xticklabels(["55", "165", "176", "220", "275"], color=col_frame, fontsize=7.4)
ax2.tick_params(axis="y", left=False, labelleft=False)
ax2.set_title("doubled, the means bracket the count's octave by 5/4",
              color=col_gold, fontsize=10.5)

fig.text(0.5, 0.015,
         "dream: the three means of the pair {55, 220} are a geometric ladder by the just major third — AM/GM = GM/HM = 5/4, and AM·HM = GM².\n"
         "the kiss's mirror x → 12100/x exchanges the arithmetic and harmonic means about the geometric (the count, the crease). doubled, they bracket\n"
         "the count's octave: {176, 220, 275} = 220·{4/5, 1, 5/4}. the sum tone 275 = 2·AM and the difference tone 165 = 220·(3/4) sit symmetric\n"
         "about 220 — and the odd harmonic 5 is the ladder ratio seen through ×2. the fold, the count, and the mirror are one 5/4 ladder.",
         color=col_gold, fontsize=8.0, ha="center")

fig.savefig("assets/means-mirror-cover.png", facecolor=col_bg)
print("wrote assets/means-mirror-cover.png")
