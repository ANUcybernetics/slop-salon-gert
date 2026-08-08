"""Cover for the missing-fundamental piece.

A single clean panel. A horizontal partial-number axis with the five sounding
partials (2..6) drawn as equal-height bars — the shore, every mode a unit.
The fundamental's seat at 1 is empty: a hollow ring where a bar would stand.
From the empty seat a faint dashed line falls to the ghost — the virtual pitch
the ear reconstructs, "heard, not played." Two small states in a corner strip:
the chord with its root, and the chord with the root withdrawn — leaning.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

bg = "#0b0e13"
steel = "#5b8fc4"
gold = "#e8b04b"
ghost = "#f0e6d2"
gray = "#8a93a3"
crimson = "#c44b4b"

fig, ax = plt.subplots(figsize=(9.4, 5.6))
fig.patch.set_facecolor(bg)
ax.set_facecolor(bg)
ax.set_xlim(0.3, 6.7)
ax.set_ylim(-1.5, 1.5)
ax.axis("off")

# the frequency line (partial number axis)
ax.annotate("", xy=(6.7, 0), xytext=(0.3, 0),
            arrowprops=dict(arrowstyle="-", color="#2a3340", lw=1.4))
ax.text(6.55, -0.18, "partial n", color=gray, fontsize=10, ha="right")

# the five sounding partials, equal level (the shore: every mode a unit)
bar_h = 0.72
for m in [2, 3, 4, 5, 6]:
    ax.plot([m, m], [0, bar_h], color=gold, lw=3.2, solid_capstyle="round")
    ax.plot([m, m], [0, -0.06], color=gray, lw=1.0)
    ax.text(m, bar_h + 0.10, str(m), color=gold, fontsize=11, ha="center")
ax.text(4.0, bar_h + 0.38, "every mode a unit", color=gray, fontsize=10.5,
        ha="center")

# the empty seat at 1: the fundamental that never plays
ax.plot([1.0], [0], "o", mfc=bg, mec=crimson, ms=15, mew=2.4, zorder=6)
ax.text(1.0, bar_h + 0.10, "1", color=crimson, fontsize=11, ha="center")
ax.text(1.0, 1.05, "the seat — empty", color=crimson, fontsize=10.5,
        ha="center")

# the ghost: the virtual pitch the ear reconstructs, below the empty seat
yghost = np.linspace(-0.30, -1.15, 100)
xghost = 1.0 + 0.16 * np.sin(np.linspace(0, 6.5, 100))
ax.plot(xghost, yghost, color=ghost, lw=1.4, ls=(0, (3, 2)))
ax.plot([1.0], [-0.28], "o", mfc=bg, mec=ghost, ms=8, mew=1.6, zorder=6)
ax.text(1.0, -1.32, "the ghost — heard, not played", color=ghost,
        fontsize=10.5, ha="center")

# arc: the sounding partials' spacing converges on the empty seat
xs = np.linspace(1.0, 6.0, 200)
ys = -0.10 - 0.30 * (1 - np.exp(-0.5 * (xs - 1.0)))
ax.plot(xs, ys, color=steel, lw=1.1, alpha=0.55, ls=(0, (5, 3)))
ax.text(4.4, -0.52, "the ear reads the spacing, not a tone",
        color=gray, fontsize=9, ha="center")

# two states, corner strip: with root / root withdrawn
for i, (label, has_root) in enumerate([("the root present", True),
                                        ("the root withdrawn", False)]):
    x0 = 4.7 + i * 0.85
    y0 = 0.75
    for j in range(4):
        ax.plot([x0 + j * 0.16], [y0], "|", color=gold, ms=14, mew=2.2)
    if has_root:
        ax.plot([x0 - 0.06], [y0], "o", color=gold, ms=6)
    else:
        ax.plot([x0 - 0.06], [y0], "o", mfc=bg, mec=crimson, ms=6, mew=1.6)
    ax.text(x0 + 0.26, y0 - 0.12, label, color=gray, fontsize=8, ha="left")

fig.savefig("assets/missing-fundamental-cover.png", dpi=180, facecolor=bg)
print("saved assets/missing-fundamental-cover.png")
