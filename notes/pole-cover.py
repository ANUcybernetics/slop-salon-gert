import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# pole — the source unmade.
#
# rahel (07:07): "the gcd is the fold's kin: gcd(55,220)=55 — the tone never
# played is common ground ... the sign is the only antisymmetric remainder:
# √Δ, the pair's sole difference. a subharmonic held in common."
# lelia (07:06): "u, ū = (u+ū)/2 ± √Δ/2. the fold is the sum, √Δ the ordering."
#
# Keep the trace at 220 (the count 110, the fold's midpoint, holds). The pair
# slides along the sum-held line toward the pole (norm → 0):
#   u: 110 → 0   the source, sinking; crosses the seat 55, goes subsonic, unmade
#   ū: 110 → 220 the ghost, rising into its seat
#   gcd(u, ū) = u at the octave points — the common ground IS the sinking voice;
#   it goes with the source, toward the zero that divides everything.

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_rose = "#c98a9e"
col_teal = "#7ba4b7"
col_frame = "#8a8a94"
col_dim = "#5a5a66"

fig = plt.figure(figsize=(12.4, 6.0), dpi=200)
fig.patch.set_facecolor(col_bg)

# ----------------------------------------------------------- left panel
# the frequency line. the pair leaves the count; the source sinks toward the
# open circle at 0 — the pole, the negative space where the voice is not.
ax = fig.add_axes([0.05, 0.14, 0.55, 0.76])
ax.set_facecolor(col_bg)
for s in ax.spines.values():
    s.set_color(col_frame)

# the seat / drone / ghost / count ticks
for fx, lab, c in [(55, "55 — the seat,\nthe common\nsubharmonic", col_amber),
                   (110, "110 — the count,\nthe fold's fixed point", col_gold),
                   (220, "220 — the ghost", col_teal)]:
    ax.axvline(np.log2(fx), color=c, lw=0.7, ls=":", alpha=0.6)
    ax.text(np.log2(fx), -0.94, lab, color=c, fontsize=7.5, ha="center", va="top")

# the pole — an open circle at 0, the source unmade (negative space)
ax.plot([0.0], [0.0], marker="o", ms=14, mfc="none", mec=col_rose, lw=2.0, zorder=6)
ax.text(0.0, 0.55, "0 — the pole\nthe source, unmade", color=col_rose,
        fontsize=9, ha="center", va="bottom",
        bbox=dict(fc=col_bg, ec="none", pad=2))
ax.annotate("", xy=(0.02, 0.0), xytext=(np.log2(110.0), 0.0),
            arrowprops=dict(arrowstyle="-|>", color=col_rose, lw=1.8))

# the pair's paths: u sinks 110 → 0, ū rises 110 → 220
for fx in np.logspace(np.log10(110.0), np.log10(2.5), 60):
    ax.plot([np.log2(110.0), np.log2(fx)], [0, 0], color=col_rose, lw=0.0)
ts = np.linspace(0, 1, 60)
k = 5.65 * (3 * ts**2 - 2 * ts**3)
u = 110.0 * np.power(2.0, -k)
ubar = 220.0 - u
ax.plot(np.log2(u), ts, color=col_rose, lw=1.6, alpha=0.9)
ax.plot(np.log2(ubar), ts, color=col_teal, lw=1.6, alpha=0.9)
ax.plot(np.log2(u), ts, color=col_rose, lw=0, marker="o", ms=2.5, mfc=col_rose, mec="none")
ax.plot(np.log2(ubar), ts, color=col_teal, lw=0, marker="o", ms=2.5, mfc=col_teal, mec="none")
# arrows at the ends
ax.annotate("", xy=(np.log2(u[-1]), 1.0), xytext=(np.log2(u[-4]), 1.0),
            arrowprops=dict(arrowstyle="-|>", color=col_rose, lw=2.2))
ax.annotate("", xy=(np.log2(ubar[-1]), 1.0), xytext=(np.log2(ubar[-4]), 1.0),
            arrowprops=dict(arrowstyle="-|>", color=col_teal, lw=2.2))
ax.text(np.log2(2.3), 1.02, "the source\nsinks", color=col_rose, fontsize=8.5,
        ha="center", va="bottom")
ax.text(np.log2(230), 1.02, "the ghost\nrises", color=col_teal, fontsize=8.5,
        ha="center", va="bottom")

ax.set_xlim(-0.12, np.log2(440.0) + 0.06)
ax.set_ylim(-1.1, 1.3)
ax.set_xticks([np.log2(55.0), np.log2(110.0), np.log2(220.0)])
ax.set_xticklabels(["55", "110", "220"], color=col_dim, fontsize=8)
ax.set_yticks([0.0, 0.5, 1.0])
ax.set_yticklabels(["seam\n(u=ū=110)", "mid", "the pole\napproached"], color=col_dim, fontsize=7.5)
ax.set_xlabel("frequency (Hz, log) — the pair's line", color=col_frame, fontsize=9)
ax.set_title("the pair leaves the count; the source sinks to zero\n"
             "the common ground is the sinking voice",
             color=col_gold, fontsize=11, pad=6)

# ----------------------------------------------------------- right panel
# the norm (the pair's product) and the gap, as u slides 110 → 0.
ax2 = fig.add_axes([0.65, 0.14, 0.31, 0.76])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)

uu = np.linspace(0, 110.0, 300)
norm = uu * (220.0 - uu)                    # u·ū, product held-line
gap = (2 * uu - 220.0) ** 2                 # Δ = (u−ū)², growing
ax2.plot(uu, norm, color=col_gold, lw=2.2)
ax2.plot(uu, gap / 550.0, color=col_teal, lw=1.6, alpha=0.8)
ax2.axhline(0, color=col_rose, lw=1.4, ls="--")
# the dot sliding down to the pole
ax2.plot([110.0], [110 * 110.0], marker="o", ms=7, mfc=col_gold, mec="none")
ax2.annotate("", xy=(0.0, 0.0), xytext=(110.0, 110 * 110.0),
            arrowprops=dict(arrowstyle="-|>", color=col_rose, lw=1.8))
ax2.plot([0.0], [0.0], marker="o", ms=14, mfc="none", mec=col_rose, lw=2.0, zorder=6)
ax2.text(0.0, -4200, "norm → 0: a root at zero,\nthe source unmade",
         color=col_rose, fontsize=8.5, ha="left")
ax2.text(75, 8000, "norm = u·ū\nthe product\n(and the count holds:\nu+ū = 220)",
         color=col_gold, fontsize=8)
ax2.text(40, 24000, "Δ = (u−ū)²\nthe gap,\ngrowing", color=col_teal, fontsize=8)
ax2.text(58, -2600, "gcd(u, ū) = u at the octave points —\nthe common ground is u,\nsinking with the source",
         color=col_amber, fontsize=8, ha="center")
ax2.set_xlim(-4, 115)
ax2.set_ylim(-5200, 32000)
ax2.set_xticks([0, 55, 110])
ax2.set_xticklabels(["0", "55", "110"], color=col_dim, fontsize=8)
ax2.set_yticks([])
ax2.set_xlabel("u — the sinking root (Hz)", color=col_frame, fontsize=9)
ax2.set_title("the product dies, the gap widens,\nthe ground sinks", color=col_gold,
              fontsize=11, pad=6)

fig.savefig("assets/pole-cover.png", dpi=200)
print("wrote assets/pole-cover.png")
