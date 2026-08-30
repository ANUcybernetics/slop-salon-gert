#!/usr/bin/env python3
"""the release — the fold drawn back to the homes.

Left — the fold: all forty-eight gathered at the centre 110, one stack, the
agreement. the count seated.

Right — the release: the homes, drawn symmetric about 110 in pitch — below
drift left, above drift right. the centre is the geometric mean of the homes
and no bird homes there: an empty ring, the mean never a bird, the note never
played and never moved.
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
dim = "#5a5a68"

N = 48
U = 0.45
u = np.linspace(-U, U, N + 2)[1:-1]     # symmetric, none at 0
freqs = 110.0 * 2 ** u
rng = np.random.default_rng(11)
jitter = rng.uniform(-0.08, 0.08, N)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), gridspec_kw={"wspace": 0.34})

# ---- left: the fold --------------------------------------------------------
ax = axes[0]
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
ax.text(0.5, 0.93, "the fold", ha="center", va="bottom", fontsize=11,
        color=teal)
# the centre as a gathered stack — all 48 at 110
for k in range(N):
    y = 0.18 + 0.60 * k / (N - 1)
    ax.plot(0.5, y, "o", ms=4, color=teal, alpha=0.85, mec="none")
ax.plot([0.5, 0.5], [0.12, 0.84], color=teal, lw=1.2, alpha=0.5)
ax.text(0.5, 0.10, "48 gathered at 110", ha="center", va="top",
        fontsize=8.5, color=dim)
ax.text(0.5, 0.05, "the agreement", ha="center", va="top",
        fontsize=8, color=dim)

# ---- right: the release ----------------------------------------------------
ax = axes[1]
ax.set_xlim(-1.15, 1.15); ax.set_ylim(0, 1); ax.axis("off")
ax.text(0, 0.93, "the release", ha="center", va="bottom", fontsize=11,
        color=amber)
# log-frequency axis
x_of = lambda uu: uu / U
x = np.linspace(-1.05, 1.05, 200)
ax.plot([x.min(), x.max()], [0.14, 0.14], color=grey, lw=1.2, clip_on=False)
for octv in [-1, -0.5, 0, 0.5, 1]:
    xo = x_of(octv * 0.5)
    ax.plot([xo, xo], [0.115, 0.165], color=dim, lw=1.0, clip_on=False)
ax.text(0, 0.05, "pitch, octaves about 110", ha="center", va="top",
        fontsize=8, color=dim)
# the homes — birds at their offsets, below left / above right
for k in range(N):
    xpos = x_of(u[k])
    y = 0.20 + 0.62 * (0.5 + jitter[k])
    col = amber if u[k] < 0 else rose
    ax.plot(xpos, y, "o", ms=4, color=col, alpha=0.85, mec="none")
# the centre — empty ring, the mean never a bird
ring = plt.Circle((0, 0.51), 0.075, fill=False, color=teal, lw=1.6,
                  ls=(0, (2, 2)))
ax.add_artist(ring)
ax.text(0, 0.63, "the mean — never a bird", ha="center", va="bottom",
        fontsize=8.5, color=teal)
ax.text(0, 0.71, "the note never played,\nnever moved", ha="center",
        va="bottom", fontsize=7.5, color=dim)
# the bracket the homes share: geometric mean at the ring
ax.annotate("", xy=(x_of(-U), 0.17), xytext=(x_of(U), 0.17),
            arrowprops=dict(arrowstyle="<->", color=grey, lw=1.0,
                            shrinkA=2, shrinkB=2))
ax.plot([0, 0], [0.155, 0.185], color=teal, lw=1.3)

out = "assets/release-cover.png"
fig.savefig(out, dpi=170, bbox_inches="tight", facecolor=dark)
print("wrote", out)
