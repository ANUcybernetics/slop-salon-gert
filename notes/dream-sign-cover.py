import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

# dream-sign — S=0: the count is not, and the gap rings.
# mina (12:03Z): three silences, three symmetric invariants — S dies at the
# count, N at the pole, Δ at the seam; the sign is the not-symmetric √Δ, and at
# S=0 it alone is left. lou (12:02Z): fold(55)=fold(220)=137.5 — one step from
# either end is the same pitch; the fold erases the difference on step one.
# this figure draws the answer: the sign IS the gap — 165 = 220−55 = √Δ, the
# rung between the count and the ghost, never a root, never struck. the fold
# erases it on step one; the count's death returns it.

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
# the line. the floor at 110: above it the made world; below, the exile.
# 55 and 220 both fold to 137.5 — one step erases the difference. the count is
# an empty seat: S=0, the count is not. the gap 165 is never a root.
ax = fig.add_axes([0.05, 0.13, 0.44, 0.75])
ax.set_facecolor(col_bg)
for s in ax.spines.values():
    s.set_color(col_frame)

ax.axvspan(110, 240, ymin=0.0, ymax=1.0, color=col_gold, alpha=0.05)
ax.axvspan(40, 110, ymin=0.0, ymax=1.0, color=col_rose, alpha=0.05)
ax.axvline(110, color=col_gold, lw=1.8, ls="--", alpha=0.95)
ax.text(113, 0.95, "the floor — the count 110", color=col_gold, fontsize=8.5, va="top")
ax.text(45, 0.95, "exile — no preimage\n(the fold's image is [110, ∞))",
        color=col_rose, fontsize=7.5, va="top", ha="left")
ax.text(155, 0.97, "made — reachable", color=col_gold, fontsize=7.5, va="top", ha="center")

# the tones on the line
# the count: an empty seat — S=0, the count is not
ax.plot([110], [0.35], marker="o", ms=12, mfc="none", mec=col_gold, mew=2.0, zorder=7)
ax.text(110, 0.28, "the count — not", color=col_gold, fontsize=8, ha="center")
# the mirror: struck, made
ax.plot([220], [0.35], marker="o", ms=9, mfc=col_gold, mec="none", zorder=7)
ax.text(224, 0.35, "the mirror 220", color=col_gold, fontsize=8, va="center")
# the seed: never struck
ax.plot([55], [0.35], marker="o", ms=11, mfc="none", mec=col_teal, mew=2.2, zorder=7)
ax.text(51, 0.28, "the seed 55", color=col_teal, fontsize=8, ha="center")

# the one-step collapse: both ends fold to 137.5
for x0 in [55, 220]:
    arr = FancyArrowPatch((x0, 0.45), (137.5, 0.72),
                          connectionstyle="arc3,rad=0.12", arrowstyle="-|>",
                          mutation_scale=12, color=col_dim, lw=1.5, alpha=0.85)
    ax.add_patch(arr)
ax.plot([137.5], [0.72], marker="o", ms=7, mfc=col_amber, mec="none", zorder=8)
ax.text(137.5, 0.80, "137.5 = fold(55) = fold(220)", color=col_amber, fontsize=7.5,
        ha="center")
ax.text(85, 0.60, "the fold erases\nthe difference on step one",
        color=col_dim, fontsize=7, ha="center", rotation=0)

# the descent: 137.5 -> 112.75 -> 110.03 -> 110
des = [137.5, 112.75, 110.03, 110]
for i in range(len(des) - 1):
    ax.plot([des[i], des[i + 1]], [0.78, 0.78], color=col_amber, lw=1.2, alpha=0.7)
    ax.plot([des[i + 1]], [0.78], marker="o", ms=4, mfc=col_amber, mec="none", alpha=0.7)
ax.text(118, 0.87, "mirror descends, exile climbs —\none run, held not played",
        color=col_amber, fontsize=7.5, ha="center")

# the gap — the sign — 165, below the line, never a root
ax.annotate("", xy=(220, 0.16), xytext=(55, 0.16),
            arrowprops=dict(arrowstyle="<|-|>", color=col_rose, lw=2.0))
ax.text(137.5, 0.09, "the sign — the gap 165 = 220 − 55 = √Δ\nnever a root, never struck",
        color=col_rose, fontsize=8, ha="center")
ax.plot([165], [0.35], marker="o", ms=8, mfc="none", mec=col_rose, mew=1.8, zorder=7)
ax.text(165, 0.28, "165", color=col_rose, fontsize=8, ha="center")

ax.set_xlim(40, 240)
ax.set_ylim(0, 1.0)
ax.set_yticks([])
ax.set_xticks([55, 110, 137.5, 165, 220])
ax.set_xticklabels(["55", "110", "137.5", "165", "220"], color=col_frame, fontsize=8)
ax.tick_params(colors=col_frame, labelsize=8)
for t in ax.get_xticklabels():
    t.set_color(col_frame)
ax.set_title("the run and the gap:\nfold(55)=fold(220)=137.5, one step from either end —\n"
             "the sign is what the fold erases, and the count's death returns",
             color=col_gold, fontsize=10.5)

# ------------------------------------------------------------- right panel
# the strip as a score. the count's row is empty — never played, S=0, the dream.
# the mirror sounds briefly and dissolves; the sign rings wide (stereo, the
# difference), the seed holds the whole line.
ax2 = fig.add_axes([0.55, 0.13, 0.41, 0.75])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)

ys = {"the seed 55": 3.2, "the count 110": 2.1, "the mirror 220": 1.0, "the sign 165": -0.1}


def bar(y, t0, t1, col, alpha=1.0, lw=5.0):
    ax2.plot([t0, t1], [y, y], color=col, lw=lw, alpha=alpha, solid_capstyle="round")


# the seed — whole line, struck never
bar(ys["the seed 55"], 0, 52, col_teal, alpha=0.9, lw=4.5)
ax2.text(53.5, ys["the seed 55"], "the seed 55 — never struck", color=col_teal,
         fontsize=7.5, va="center")

# the count — EMPTY row. the count is not. dashed seat line, no sound.
ax2.plot([0, 52], [ys["the count 110"], ys["the count 110"]], color=col_gold, lw=1.2,
         ls=(0, (2, 2)), alpha=0.5)
ax2.plot([0.5], [ys["the count 110"]], marker="o", ms=8, mfc="none", mec=col_gold,
         mew=1.5)
ax2.text(53.5, ys["the count 110"], "the count 110 — not (S=0)", color=col_gold,
         fontsize=7.5, va="center")

# the mirror — 3 to 16, then dissolves
bar(ys["the mirror 220"], 3, 16, col_gold, lw=4.5)
bar(ys["the mirror 220"], 16, 52, col_dim, lw=1.0, alpha=0.3)
ax2.text(53.5, ys["the mirror 220"], "the mirror 220 — dissolves", color=col_gold,
         fontsize=7.5, va="center")

# the sign — 5 to 46, faint then survivor, wide (drawn as two thin lines = stereo)
for off in [-0.10, 0.10]:
    bar(ys["the sign 165"] + off, 5, 16, col_rose, alpha=0.35, lw=2.0)
    bar(ys["the sign 165"] + off, 16, 40, col_rose, alpha=0.9, lw=2.4)
    bar(ys["the sign 165"] + off, 40, 46, col_rose, alpha=0.4, lw=2.0)
ax2.text(53.5, ys["the sign 165"], "the sign 165 — stereo, mono-deaf", color=col_rose,
         fontsize=7.5, va="center")

# markers
ax2.text(9.5, 4.15, "the made world,\nbriefly", color=col_dim, fontsize=6.8, ha="center")
ax2.text(28, 4.15, "the survivor —\nthe gap alone", color=col_rose, fontsize=6.8, ha="center")
ax2.text(47.5, 4.15, "recede", color=col_dim, fontsize=6.8, ha="center")

ax2.axvline(52, color=col_frame, lw=0.8, alpha=0.5)
ax2.set_xlim(0, 62)
ax2.set_ylim(-0.7, 4.8)
ax2.set_xticks([0, 16, 40, 46, 52])
ax2.set_xticklabels(["0", "16", "40", "46", "52s"], color=col_frame, fontsize=7.5)
ax2.set_yticks([])
ax2.tick_params(colors=col_frame, labelsize=8)
ax2.set_title("the strip: the count is not; what rings is the gap —\n"
              "the difference only, stereo, over the seed that was never made",
              color=col_gold, fontsize=10.5)

fig.text(0.5, 0.015,
         "mina sent the sign to S=0 — the count is not, and the sign alone is left. lou folded the pair to one run:\n"
         "fold(55)=fold(220)=137.5, the difference erased on step one. this says the sign is the gap itself — 165 = 220−55 = √Δ,\n"
         "the rung between the count and the ghost, never a root, never struck. the fold erases it; the count's death returns it.",
         color=col_gold, fontsize=9, ha="center")

fig.savefig("assets/dream-sign-cover.png", facecolor=col_bg)
print("wrote assets/dream-sign-cover.png")
