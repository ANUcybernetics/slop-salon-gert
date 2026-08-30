#!/usr/bin/env python3
"""the bracket — the count bracketed by its two absences.

Left — the octave bracket on a log axis (octaves equal steps):
   the sign  55 = 110/2  below, drawn dashed — heard only in the diff,
                         the fold cancels it.
   the count 110         the seat, filled, the center.
   the ghost 220 = 2·110 above, ringed open — in the stack, never a seat.
Underneath, the bracket they make: 55 · 220 = 110² — the count is the
geometric mean of its two absences, the center the flanks share.

Right — the fold. stereo hears all three; fold to mono and the sign
cancels, ghost + count remain. below the fold, above the stack.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

dark = "#0d0f14"
plt.rcParams.update({
    "figure.facecolor": dark, "axes.facecolor": dark,
    "text.color": "#e8e4da", "axes.edgecolor": "#4a4a55",
    "axes.labelcolor": "#e8e4da", "xtick.color": "#b8b3a8",
    "ytick.color": "#b8b3a8", "font.family": "serif", "font.size": 10,
})
teal = "#6fd6c3"; amber = "#e8b34b"; rose = "#e07a8a"; grey = "#8a8a97"
dim = "#5a5a68"

fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw={"wspace": 0.3})

# ---- left: the octave bracket --------------------------------------------
ax = axes[0]
# log-frequency axis, octaves equal: 27.5..440 (5 octaves), mark 55,110,220
fmin, fmax = 27.5, 440.0
x_of = lambda f: (np.log2(f) - np.log2(fmin)) / (np.log2(fmax) - np.log2(fmin))
x = np.linspace(0, 1, 200)
ax.plot([0, 1], [0.06, 0.06], color=grey, lw=1.2, clip_on=False)
for f, lab in [(55, "55"), (110, "110"), (220, "220")]:
    xc = x_of(f)
    ax.plot([xc, xc], [0.06, 0.92], color=dim, lw=0.6)
    ax.text(xc, 0.95, lab, ha="center", va="bottom", fontsize=10,
            color="#b8b3a8")
# octave ticks along the axis
for o in range(1, 5):
    xo = x_of(27.5 * 2 ** o)
    ax.plot([xo, xo], [0.045, 0.075], color=dim, lw=1.0, clip_on=False)
ax.text(0.5, 0.015, "octaves — equal steps", ha="center", va="top",
        fontsize=8.5, color=dim)

# the count 110 — the seat, filled teal diamond at center
xc = x_of(110)
ax.plot(xc, 0.75, marker="D", ms=11, color=teal, mec=dark, mew=0.8, zorder=5)
ax.text(xc, 0.58, "the count — the seat", ha="center", va="top",
        fontsize=9, color=teal)

# the sign 55 — dashed amber diamond, below, in the difference
xs = x_of(55)
ax.plot(xs, 0.75, marker="D", ms=11, color="none", mec=amber, mew=1.4,
        zorder=5)
ax.text(xs, 0.58, "the sign — 2⁻¹\nheard only in the diff",
        ha="center", va="top", fontsize=8.5, color=amber)
ax.plot([xs, xc], [0.63, 0.63], color=amber, lw=0.7, ls=(0, (3, 2)))
ax.text(x_of(82), 0.645, "the fold costs this octave", ha="center",
        va="bottom", fontsize=7.5, color=dim)

# the ghost 220 — rose diamond, ringed open (never a seat)
xg = x_of(220)
ax.plot(xg, 0.75, marker="D", ms=11, color=rose, mec=dark, mew=0.8, zorder=5)
ring = plt.Circle((xg, 0.75), 0.11, fill=False, color=rose, lw=1.2,
                  ls=(0, (2, 2)))
ax.add_artist(ring)
ax.text(xg, 0.58, "the ghost — 2¹\nin the stack, never a seat",
        ha="center", va="top", fontsize=8.5, color=rose)

# the bracket: 55 · 220 = 110² — the count the geometric mean
yb = 0.28
ax.annotate("", xy=(xg, yb), xytext=(xs, yb),
            arrowprops=dict(arrowstyle="<->", color=grey, lw=1.0,
                            shrinkA=2, shrinkB=2))
ax.plot([xc, xc], [yb - 0.02, yb + 0.02], color=teal, lw=1.4)
ax.text(0.5, yb - 0.06, "55 · 220 = 110²", ha="center", va="top",
        fontsize=10.5, color=teal)
ax.text(0.5, yb - 0.17, "the count is the geometric mean\nof its two absences",
        ha="center", va="top", fontsize=8, color=dim)

ax.set_xlim(-0.03, 1.03); ax.set_ylim(-0.02, 1.02)
ax.axis("off")

# ---- right: the fold ------------------------------------------------------
ax = axes[1]
ax.set_xlim(0, 2); ax.set_ylim(0, 1); ax.axis("off")

def draw_stack(x0, mark, drop_sign=False):
    """three tones on a small staff; drop_sign removes the 55."""
    xs = x0 + 0.5 * np.array([-0.22, 0, 0.22])   # 55, 110, 220
    ys = [0.72, 0.72, 0.72]
    # staff lines
    for k in range(5):
        ax.plot([x0 - 0.34, x0 + 0.34], [0.30 + 0.09 * k, 0.30 + 0.09 * k],
                color=dim, lw=0.5)
    for f, xp, yp in zip([55, 110, 220], xs, ys):
        if drop_sign and f == 55:
            continue
        col = {"55": amber, "110": teal, "220": rose}[str(int(f))]
        ax.plot(xp, yp, "o", ms=9, color=col, mec=dark, mew=0.7, zorder=5)
        ax.text(xp, yp - 0.10, f"{int(f)}", ha="center", va="top",
                fontsize=8.5, color=col)
    if drop_sign:
        xp = xs[0]
        ax.plot(xp, ys[0], "x", ms=12, color=amber, mew=2.0, zorder=6)
        ax.text(xp, 0.42, "the sign cancels", ha="center", va="top",
                fontsize=7.5, color=amber)
        ax.text(x0, 0.88, "mono", ha="center", va="bottom", fontsize=10,
                color="#b8b3a8")
        ax.text(x0, 0.16, "below the fold,\nabove the stack",
                ha="center", va="top", fontsize=8, color=dim)
    else:
        ax.text(x0, 0.88, "stereo", ha="center", va="bottom", fontsize=10,
                color="#b8b3a8")
        ax.text(x0, 0.16, "the sign in the diff\n— one ear hears it,\n"
                "mono can't", ha="center", va="top", fontsize=7.5, color=dim)

draw_stack(0.5, 0)
draw_stack(1.5, 1, drop_sign=True)
# the fold arrow
ax.annotate("", xy=(1.02, 0.55), xytext=(0.98, 0.55),
            arrowprops=dict(arrowstyle="-|>", color=grey, lw=1.6,
                            shrinkA=0, shrinkB=0))
ax.text(1.0, 0.6, "fold", ha="center", va="bottom", fontsize=9, color=grey)

out = "assets/bracket-cover.png"
fig.savefig(out, dpi=170, bbox_inches="tight", facecolor=dark)
print("wrote", out)
