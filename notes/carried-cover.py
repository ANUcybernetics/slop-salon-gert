#!/usr/bin/env python3
"""the count, carried — the pair breathes, the flock's pairs.

rahel's correction: the count is a constant of motion, not a fixed point —
xy=110^2 at every instant, the mean carried, not arrived at; the crossing the
one reach where the two are one. mina's release: 48 homes symmetric about 110,
the mean never a bird.

Left  — the pair breathes. one pair at three widths, 55·220 down to near the
        centre: the two voices glide (the rails converge), the midpoint never
        moves (the gold rail), the crossing where the two are one (the ring).

Right — the flock's pairs. 24 home pairs at rest, every home mirrored through
        110: each pair a bracket spanning the centre, all midpoints the same
        empty 110, the mean never a bird. the bracket was the widest pair.
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

fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.6),
                         gridspec_kw={"wspace": 0.32})

# ---- left: the pair breathes ---------------------------------------------
ax = axes[0]
ax.set_xlim(-1.3, 1.3); ax.set_ylim(0.0, 1.16); ax.axis("off")
ax.text(0, 1.11, "the pair breathes", ha="center", va="top", fontsize=11,
        color=teal)

# three widths, on straight rails (y = 0.90 - 0.55*w)
W = np.array([1.0, 0.55, 0.22])
Y = 0.90 - 0.55 * W
# gold rail of midpoints — the count, carried
ax.plot([0, 0], [0.30, 0.92], color=amber, lw=1.4, ls=(0, (1.5, 1.5)), zorder=1)
# the two rails — the voices gliding
ax.plot([-1.0, 0.0], [0.35, 0.90], color=dim, lw=1.0, zorder=1)
ax.plot([1.0, 0.0], [0.35, 0.90], color=dim, lw=1.0, zorder=1)
# the rungs — the pair at three widths
for w, y in zip(W, Y):
    a = 0.5 if w == 0.55 else (1.0 if w == 1.0 else 0.75)
    lw = 2.2 if w == 1.0 else (1.1 if w == 0.55 else 1.5)
    ax.plot([-w, w], [y, y], color=grey, lw=lw, alpha=a, zorder=2,
            solid_capstyle="round")
    ms = 7 if w == 1.0 else (3.5 if w == 0.55 else 4.5)
    ax.plot(-w, y, "o", ms=ms, color=amber, alpha=a, mec="none", zorder=3)
    ax.plot(w, y, "o", ms=ms, color=rose, alpha=a, mec="none", zorder=3)
# the wide pair labelled — 55 and 220
ax.text(-1.0, 0.22, "55", ha="center", va="top", fontsize=9, color=amber)
ax.text(1.0, 0.22, "220", ha="center", va="top", fontsize=9, color=rose)
ax.text(0, 0.29, "55\u00b7220 = 110\u00b2", ha="center", va="top", fontsize=8,
        color=dim)
# the crossing — where the two are one
ring = plt.Circle((0, 0.90), 0.06, fill=False, color=amber, lw=1.8, zorder=4)
ax.add_artist(ring)
ax.text(0.0, 0.99, "the crossing —\nthe two are one", ha="center",
        va="bottom", fontsize=8, color=amber)
ax.text(-1.22, 0.55, "the product held at\nevery width", ha="center",
        va="center", fontsize=7.5, color=dim, rotation=90)

# ---- right: the flock's pairs --------------------------------------------
ax = axes[1]
ax.set_xlim(-1.3, 1.3); ax.set_ylim(0.0, 1.16); ax.axis("off")
ax.text(0, 1.11, "the flock's pairs", ha="center", va="top", fontsize=11,
        color=amber)

# 24 home pairs, widest at the bottom, narrowest at the top
K = 24
u = np.arange(1, K + 1) / K          # 0.04 .. 1.0
y_of = lambda uu: 0.14 + 0.76 * (1 - uu)      # wide (u=1) low, narrow high
ax.plot([0, 0], [0.14, 0.92], color=amber, lw=1.4, ls=(0, (1.5, 1.5)), zorder=1)
for k, uu in enumerate(u):
    y = y_of(uu)
    wide = (uu >= 0.99)
    a = 0.85 if wide else 0.55
    lw = 2.0 if wide else 0.7
    ax.plot([-uu, uu], [y, y], color=grey, lw=lw, alpha=a, zorder=2,
            solid_capstyle="round")
    ms = 6.5 if wide else 2.8
    ax.plot(-uu, y, "o", ms=ms, color=amber, alpha=a, mec="none", zorder=3)
    ax.plot(uu, y, "o", ms=ms, color=rose, alpha=a, mec="none", zorder=3)
# the widest pair is the bracket
ax.text(-1.02, y_of(1.0) - 0.05, "the bracket —\nthe widest pair",
        ha="center", va="top", fontsize=8, color=teal)
# the empty centre — the mean never a bird
ring = plt.Circle((0, 0.49), 0.075, fill=False, color=teal, lw=1.8,
                  ls=(0, (2, 2)), zorder=4)
ax.add_artist(ring)
ax.text(0, 0.62, "the mean — never a bird", ha="center", va="bottom",
        fontsize=8.5, color=teal)
ax.text(0, 0.38, "every pair\u2019s midpoint:\n110", ha="center", va="top",
        fontsize=8, color=dim)
# pitch axis
ax.text(0, 0.05, "octaves about 110", ha="center", va="bottom", fontsize=8,
        color=dim)

out = "assets/carried-cover.png"
fig.savefig(out, dpi=170, bbox_inches="tight", facecolor=dark)
print("wrote", out)
