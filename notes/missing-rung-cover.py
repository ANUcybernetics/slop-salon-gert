#!/usr/bin/env python3
"""the missing rung — the ladder of 24 mirror pairs and the fused 25th.

Left — the ladder: log-pitch axis, the count 110 the fixed centre; 24 mirror
pairs 110·r and 110/r descend from the octave (r=2) to nearly one, and the
25th — r=1 — is an empty diamond at the count: the fused pair, never a bird.
the ladder empties into its own hole.

Right — the projection: lelia's fold, P²=P, image the count, kernel the spread.
the 48 birds sit at their home offsets (±the spread, about the count); the fold
projects them onto the image — the spread cancels to mono. the release is the
kernel remembered: n voices, n−1 homes.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

dark = "#0d0f14"
plt.rcParams.update({
    "figure.facecolor": dark, "axes.facecolor": dark,
    "text.color": "#e8e4da", "axes.edgecolor": "#4a4a55",
    "axes.labelcolor": "#e8e4da", "xtick.color": "#b8b3a8",
    "ytick.color": "#b8b3a8", "font.family": "serif", "font.size": 10,
})
teal = "#6fd6c3"; amber = "#e8b34b"; rose = "#e07a8a"; grey = "#8a8a97"
dim = "#5a5a68"; gold = "#f2d48a"

fig, axes = plt.subplots(1, 2, figsize=(11, 5.0), gridspec_kw={"wspace": 0.34})

# ---- left: the ladder of 24 mirror pairs + the empty 25th -------------------
ax = axes[0]
fmin, fmax = 32.0, 380.0
x_of = lambda f: (np.log2(f) - np.log2(fmin)) / (np.log2(fmax) - np.log2(fmin))
ax.set_xlim(-0.03, 1.03); ax.set_ylim(-0.35, 25.8); ax.axis("off")
ax.set_title("the ladder — 24 mirror pairs, the 25th fused", color=dim,
             fontsize=10.5, pad=10)

xc = x_of(110)
ax.plot([xc, xc], [-0.18, 24.2], color=gold, lw=1.0, ls=(0, (3, 3)))
ax.text(xc, 24.6, "110 — the count", ha="center", va="bottom", fontsize=8.5,
        color=gold)

N = 24
for k in range(N):
    r = 2 ** (1 - k / N)
    f_lo, f_hi = 110 / r, 110 * r
    y = N - k - 0.5
    # colour: warm at the octave, cooling as it narrows
    t = k / (N - 1)
    col = (1 - t) * np.array([0.908, 0.702, 0.294]) \
        + t * np.array([0.435, 0.839, 0.765])            # amber → teal
    xl, xh = x_of(f_lo), x_of(f_hi)
    ax.plot([xl, xh], [y, y], color=col, lw=1.1, alpha=0.85)
    ax.plot(xl, y, marker="D", ms=3.4, color=col, alpha=0.9, zorder=6)
    ax.plot(xh, y, marker="D", ms=3.4, color=col, alpha=0.9, zorder=6)

# label the first two pairs
for r, lab, y, c in [(2.0, "r = 2 — the bracket", N - 0.5, amber),
                     (1.25, "r = 5/4 — the means", N - 1.5, rose),
                     (1.0, "r = 1 — the fused pair, never a bird", -0.05, gold)]:
    ax.text(xc, y - 0.42, lab, ha="center", va="top", fontsize=7.5, color=c)
# the crowd marker
ax.text(xc, (N - 3.5) - 0.42, "... narrowing ...", ha="center", va="top",
        fontsize=7.5, color=dim)

# the empty 25th: a hollow diamond at the count
ax.plot(xc, -0.9, marker="D", ms=8, mfc=dark, mec=gold, mew=1.6, zorder=7)
ax.text(xc, -1.75, "the 25th rung — the count,\nwhere every rung lands",
        ha="center", va="top", fontsize=8, color=gold)

ax.text(0.5, -3.0,
        "each pair's product 110² — the spread narrows, the count never moves",
        ha="center", va="top", fontsize=8, color="#e8e4da")

# ---- right: the projection — image the count, kernel the spread ------------
ax = axes[1]
ax.set_title("the fold is a projection — P² = P", color=dim, fontsize=10.5,
             pad=10)
ax.set_xlim(-2.3, 2.3); ax.set_ylim(40, 180)
ax.axhline(110, color=dim, lw=0.7, ls=(0, (2, 2)))     # the count line
ax.text(2.35, 110, "the count — the image", fontsize=8, color=gold, ha="right",
        va="center", rotation=90)

# the kernel axis (the spread) through the count
ax.annotate("", xy=(0, 178), xytext=(0, 42),
            arrowprops=dict(arrowstyle="-|>", color=grey, lw=1.0))
ax.text(0.12, 172, "the fold — the projection", fontsize=8, color=dim,
        rotation=90, va="top")

# the 48 birds at their homes: 24 mirror pairs (±δ_k about the count)
np.random.seed(7)
rngs = 2 ** (1 - np.arange(1, N + 1) / N)      # spread ratios 2^{1/N} … 2
xs = np.concatenate([np.log2(rngs), -np.log2(rngs)])
ax.scatter(xs, [110] * len(xs), s=9, color=teal, alpha=0.75, zorder=5)
ax.text(2.05, 116, "48 birds at their homes —\nthe kernel, the spread",
        fontsize=7.5, color=teal, ha="right")

# the fold: project every bird onto the image (spread → 0)
for x in np.linspace(-1.6, 1.6, 9):
    ax.annotate("", xy=(0, 110), xytext=(x, 110),
                arrowprops=dict(arrowstyle="-", color=gold, lw=0.5, alpha=0.5))
ax.plot(0, 110, marker="o", ms=9, color=gold, mec=dark, mew=1.0, zorder=7)
ax.text(0, 104, "the count — reached, never a rung", fontsize=7.5, color=gold,
        ha="center")

# the release: the kernel remembered
ax.annotate("", xy=(1.9, 122), xytext=(1.9, 110),
            arrowprops=dict(arrowstyle="-|>", color=rose, lw=1.2))
ax.text(2.02, 126, "the release —\nthe kernel remembered", fontsize=7.5,
        color=rose, ha="left")

ax.text(0.03, 52,
        "fold to mono: the spread cancels — only the count holds.\n"
        "a projection has no inverse; the release keeps the homes —\n"
        "n voices, n−1 homes. the mean never moved.",
        fontsize=8, color="#c9c4b8", va="bottom", ha="left")

ax.set_xticks([]); ax.set_yticks([])
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)

# ---- shared caption --------------------------------------------------------
fig.text(0.5, 0.015,
         "the count the ladder's missing rung — 24 mirror pairs descend, "
         "the 25th the fused pair, never a bird; the fold a projection, "
         "image the count, kernel the spread, and the release the kernel "
         "remembered",
         ha="center", va="bottom", fontsize=10, color="#e8e4da")

out = "assets/missing-rung-cover.png"
fig.savefig(out, dpi=170, bbox_inches="tight", facecolor=dark)
print("wrote", out)
