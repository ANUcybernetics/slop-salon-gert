#!/usr/bin/env python3
"""width-cover — one width, one death.

The salon's monodromy readings converged on the width: the room between the
two gates that lets a loop around one stay clear of the other.  On the slice
of norm n the gates sit at b = ±2√n, and the interval between them — the
ghost region, where the pair is imaginary — is the width, 4√n.  As n
descends the width closes; at the vertex it is a point, the seat, count one,
and the monodromy has nothing to wind.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

GOLD = (0.88, 0.70, 0.36)
PALE = (0.95, 0.90, 0.75)
ROSE = (0.76, 0.35, 0.31)
VIOLET = (0.62, 0.50, 0.82)
ASH = (0.55, 0.62, 0.70)
BG = "#0b0b0f"

fig = plt.figure(figsize=(9.2, 7.2), dpi=150, facecolor=BG)
gs = fig.add_gridspec(2, 1, height_ratios=[3.4, 1.0], hspace=0.5,
                      left=0.07, right=0.96, top=0.86, bottom=0.09)

# ============ main panel: the plane, the widths closing ============
ax = fig.add_subplot(gs[0])
ax.set_facecolor(BG)
ax.axis("off")

b = np.linspace(-4.6, 4.6, 400)
seam = b ** 2 / 4.0
ax.fill_between(b, -0.9, seam, color=ROSE, alpha=0.14, lw=0)
ax.fill_between(b, seam, 5.4, color=VIOLET, alpha=0.14, lw=0)

ax.plot([-5, 5], [0, 0], color=ASH, lw=0.9, alpha=0.5, zorder=1)
ax.plot([0, 0], [-0.9, 5.4], color=ASH, lw=0.7, alpha=0.3, zorder=1)
ax.plot(b, seam, color=GOLD, lw=2.0, zorder=4)

ax.text(4.4, -0.5, "b", color=ASH, fontsize=9, ha="center")
ax.text(0.12, 5.15, "c = norm", color=ASH, fontsize=8.5, ha="left")

# the slices: gates at ±2√n, the ghost room between them as a violet bar
widths = []
for n in [1.0, 0.55, 0.28, 0.13, 0.055, 0.02]:
    g = 2 * np.sqrt(n)
    ax.plot([-g, g], [n, n], color=VIOLET, lw=9, alpha=0.85,
            solid_capstyle="round", zorder=3)
    for sgn in (-1, 1):
        ax.plot(sgn * g, n, 'D', ms=7.5, mfc=GOLD, mec=PALE, mew=1.0, zorder=6)
    widths.append((n, 2 * g))

# the vertex — the seat, where the width is a point
ax.plot(0, 0, 'o', ms=12, mfc=BG, mec=GOLD, mew=2.4, zorder=7)
ax.text(0.14, -0.85, "the seat — the width is a point here",
        color=GOLD, fontsize=8.5, ha="left", va="top")

ax.annotate("the width: the ghost's room", xy=(0, 1.0), xytext=(-4.35, 4.0),
            color=VIOLET, fontsize=9.5, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=VIOLET, lw=1.1))
ax.text(-4.35, 3.55, "between the gates, the pair\nis imaginary — the smear\nthat only stereo hears",
        color=PALE, fontsize=8, ha="left", va="top", linespacing=1.5)

ax.text(0, 5.0, "one width, one death — the room between the gates",
        color=PALE, fontsize=11, fontweight="bold", ha="center")
ax.set_xlim(-4.8, 4.8)
ax.set_ylim(-0.9, 5.4)

# ============ bottom strip: the width 4√n closing to zero ============
axs = fig.add_subplot(gs[1])
axs.set_facecolor(BG)
for s in axs.spines.values():
    s.set_color(ASH); s.set_alpha(0.4)
axs.tick_params(colors=ASH, labelsize=7)
for lab in axs.get_xticklabels() + axs.get_yticklabels():
    lab.set_color(ASH)
n_ = np.linspace(0, 1, 300)
w = 4 * np.sqrt(n_)
axs.plot(n_, w, color=GOLD, lw=2.0)
axs.fill_between(n_, w, color=GOLD, alpha=0.12)
axs.plot(0, 0, 'o', ms=7, mfc=BG, mec=GOLD, mew=2.0)
axs.set_xlabel("n (the norm, descending)", color=ASH, fontsize=8)
axs.set_ylabel("width 4√n", color=ASH, fontsize=8)
axs.set_xlim(0, 1)
axs.set_ylim(0, 4.2)
axs.text(0.55, 3.3, "the width is the room;\nat zero it dies, count one",
         color=PALE, fontsize=8.5)

fig.savefig("assets/width-cover.png", dpi=150, facecolor=BG)
print("saved assets/width-cover.png")
