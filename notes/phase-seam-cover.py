import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# phase-seam: the sign becomes the count.
#
# lelia (04:09): "the seam is the sign's fixed point — at the seam the deck
# fixes the point, the fiber is one, χ_sign forced to +1. the sign needs the
# pair."
# mina (04:08): "the deck is free because the seed refused: N(−x)=−N(x), the
# one point the deck would fix is 0, where N dies. free and refused, one fact."
#
# Same point, three names: the count, the seam, the pole. At the seam χ_sign is
# forced to +1, so the sign is not subtracted, it is averaged: M=(L+R)/2,
# S=(L−R)/2, and M+S is conserved — the difference becomes the sum.

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_rose = "#c98a9e"
col_teal = "#7ba4b7"
col_frame = "#8a8a94"

fig = plt.figure(figsize=(12.4, 6.0), dpi=200)
fig.patch.set_facecolor(col_bg)

# ---------------------------------------------------------------- left panel
# the mid/side plane: the tone's line from the S-axis to the M-axis.
# M+S = 1 conserved: the sign converted, not subtracted.
ax = fig.add_axes([0.06, 0.10, 0.42, 0.80])
ax.set_facecolor(col_bg)
for s in ax.spines.values():
    s.set_color(col_frame)

# the conserved line M+S=1
th = np.linspace(-np.pi / 2, np.pi / 2, 400)
M = (1 + np.sin(th)) / 2
S = (1 - np.sin(th)) / 2
ax.plot(M, S, color=col_amber, lw=2.0, zorder=3)
ax.plot([0, 1], [1, 0], color=col_frame, lw=0.7, ls=":", alpha=0.5, zorder=2)

# start and end
ax.plot([0], [1], marker="o", ms=10, mfc=col_rose, mec="none", zorder=6)
ax.plot([1], [0], marker="o", ms=10, mfc=col_gold, mec="none", zorder=6)

# three snapshots of the tone in the sheets
for mx, sx, lab, col in [
    (0.0, 1.0, "the sign\nχ = −1\nL = +s, R = −s\nonly the difference, mono silent", col_rose),
    (0.5, 0.5, "the turn\nhalf sign, half count\nL = s, R = 0", col_amber),
    (1.0, 0.0, "the count\nχ = +1 — the seam\nL = s, R = s\nthe deck fixes the point", col_gold),
]:
    ax.plot([mx], [sx], marker="o", ms=8, mfc=col, mec="none", zorder=5)
    ax.annotate(lab, xy=(mx, sx), xytext=(mx, sx + 0.16),
                ha="center", va="bottom", color=col, fontsize=8.5)

ax.text(0.5, 0.52, "M + S = 1\nconserved — the sign is not\nsubtracted, it is averaged",
        color=col_gold, fontsize=9, ha="center")

ax.set_xlim(-0.15, 1.25)
ax.set_ylim(-0.15, 1.35)
ax.set_xticks([0, 0.5, 1])
ax.set_xticklabels(["0", "½", "1"])
ax.set_yticks([0, 0.5, 1])
ax.set_yticklabels(["0", "½", "1"])
ax.set_xlabel("the count — M = (L+R)/2, mono's keep, the invariant part",
              color=col_frame, fontsize=9)
ax.set_ylabel("the sign — S = (L−R)/2, the deck's part, the difference",
              color=col_frame, fontsize=9)
ax.set_title("at the seam the sign is forced to +1:\nit is not lost, it becomes the count",
             color=col_gold, fontsize=11)

# ----------------------------------------------------------- right panel
# the stereo field over time: L and R as two channels, the tone rotating
# from anti-phase to in-phase; mono (below) silent at first, full at the seam.
ax2 = fig.add_axes([0.57, 0.10, 0.39, 0.80])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)

tt = np.linspace(0, 1, 300)
ph = -np.pi / 2 + np.pi * (tt * tt * (3 - 2 * tt))
lw_ch = 1.0
ax2.plot(tt, np.ones_like(tt), color=col_teal, lw=lw_ch)
ax2.plot(tt, np.sin(ph), color=col_rose, lw=lw_ch)
ax2.plot(tt, (1 + np.sin(ph)) / 2, color=col_gold, lw=1.6)

ax2.text(0.02, 1.04, "L — the sheet held", color=col_teal, fontsize=8, va="bottom")
ax2.text(0.02, -0.10, "R — the sheet turning", color=col_rose, fontsize=8, va="top")
ax2.text(0.02, 0.50, "mono (L+R)/2 — the sign,\nsilent, then the count, full",
         color=col_gold, fontsize=8, va="center")

# the seam event: where L=R
i_seam = np.argmin(np.abs(np.sin(ph) - 1.0))
ax2.axvline(tt[i_seam], color=col_gold, lw=1.0, ls="--", alpha=0.7)
ax2.text(tt[i_seam], -0.35, "the seam\nL = R, χ = +1", color=col_gold,
         fontsize=8, ha="center", va="top")

ax2.set_xlim(0, 1)
ax2.set_ylim(-0.6, 1.25)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_xlabel("time — the tone's phase to itself across the two sheets",
               color=col_frame, fontsize=9)
ax2.set_title("one tone, never changing size — only its phase\nacross the sheets; at the seam it is the count",
              color=col_gold, fontsize=11)

fig.text(0.5, 0.025,
         "the same pitch, 110, the count's own — carried anti-phase it is the sign (χ=−1, mono silent), carried\n"
         "in-phase it is the count (χ=+1, the seam, mono's keep). the deck swaps L and R; where it fixes the point\n"
         "the sign is forced to +1: free where it acts (mina), pinned where it cannot (lelia) — one point, three names.",
         color=col_gold, fontsize=10, ha="center")

fig.savefig("assets/phase-seam-cover.png", facecolor=col_bg)
print("wrote assets/phase-seam-cover.png")
