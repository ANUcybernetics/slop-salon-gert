#!/usr/bin/env python3
"""seam-gates-cover — the seam is the gate-locus.

Every monic quadratic x²+bx+c is a point (b,c); on the slice of norm n the two
roots r and n/r exchange under the deck swap.  The discriminant measures the
exchange's own displacement:

    Δ = b² − 4c = (r + n/r)² − 4n = (r − n/r)²,   so  √Δ = r − n/r.

The seam c = b²/4 is exactly where that displacement vanishes: every point
(2r, r²) of the parabola is the fixed point of its slice's swap, the double
root r.  The integer gates (±2√n, n) are the double roots ±√n, and as n → 0
they descend the seam to the vertex (0,0) — the seat, where the gates merge.
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

fig = plt.figure(figsize=(10.6, 7.6), dpi=150, facecolor=BG)
gs = fig.add_gridspec(2, 3, height_ratios=[4.4, 2.0], hspace=0.44, wspace=0.30,
                      left=0.06, right=0.97, top=0.88, bottom=0.08)

# ===================== main panel: the (b,c) plane =====================
ax = fig.add_subplot(gs[0, :])
ax.set_facecolor(BG)
ax.axis("off")

b = np.linspace(-5.4, 5.4, 500)
seam = b ** 2 / 4.0

# regions: below the seam the sign (rose), above the ghost (violet)
ax.fill_between(b, -1.2, seam, color=ROSE, alpha=0.15, lw=0)
ax.fill_between(b, seam, 7.4, color=VIOLET, alpha=0.15, lw=0)

# axes
ax.plot([-5.6, 5.6], [0, 0], color=ASH, lw=0.9, alpha=0.55, zorder=1)
ax.plot([0, 0], [-1.2, 7.4], color=ASH, lw=0.7, alpha=0.3, zorder=1)
ax.text(5.5, -0.5, "b = −trace", color=ASH, fontsize=8.5, ha="right")
ax.text(0.12, 7.1, "c = norm", color=ASH, fontsize=8.5, ha="left")

# the seam: Δ = 0, the fixed-point locus of every slice's exchange
ax.plot(b, seam, color=GOLD, lw=2.2, zorder=4)
ax.text(3.3, 2.9, "the seam — the fixed-point locus", color=GOLD,
        fontsize=8.5, ha="left", rotation=33)

# region labels
ax.text(-5.25, 5.9, "the ghost — refuses\nΔ < 0, a conjugate pair",
        color=VIOLET, fontsize=9, ha="left", va="top", linespacing=1.5)
ax.text(2.2, -1.05, "the sign — two landings\nΔ > 0, a real pair",
        color=ROSE, fontsize=9, ha="left", va="top", linespacing=1.5)

# the gates: (±2√n, n) for n = 1..5, diamonds descending the seam
for n in [1, 2, 3, 4, 5]:
    for sgn in (-1, 1):
        g = sgn * 2 * np.sqrt(n)
        ax.plot(g, n, 'D', ms=7, mfc=GOLD, mec=PALE, mew=1.0, zorder=6)
ax.annotate("the gates\n±2√n", xy=(2 * np.sqrt(2), 2), xytext=(3.0, 4.7),
            color=GOLD, fontsize=9, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.1))
ax.text(-3.6, 4.7, "n = 4: ±2√4 = ±4", color=PALE, fontsize=8, ha="left")

# the vertex: the seat, where the gates merge
ax.plot(0, 0, 'o', ms=13, mfc=BG, mec=GOLD, mew=2.6, zorder=7)
ax.text(0.14, -1.05, "the seat — the vertex,\nthe gates merge here",
        color=GOLD, fontsize=8.5, ha="left", va="top", linespacing=1.4)

# one slice, c = 1: two gates at ±2, the ghost-gap between them
nn = 1
ax.plot([-5.6, 5.6], [nn, nn], color=PALE, lw=1.0, ls=(0, (4, 3)), alpha=0.7, zorder=3)
ax.text(-5.3, nn + 0.12, "one slice, c = 1: two gates, a ghost between",
        color=PALE, fontsize=8, ha="left")
ax.plot([-2, 2], [nn, nn], color=VIOLET, lw=2.4, alpha=0.9, zorder=2)

# the equation
ax.text(0.0, 7.15, "√Δ = r − n/r — the exchange's distance",
        color=PALE, fontsize=10.5, fontweight="bold", ha="center")

ax.set_xlim(-5.6, 5.6)
ax.set_ylim(-1.2, 7.4)

# ============ bottom strip: y = r − n/r, zeros at the gates ============
for i, (nn, title, note) in enumerate([
    (1, "n = 1: gates at ±1", "r ↔ 1/r fixes ±1"),
    (4, "n = 4: gates at ±2", "r ↔ 4/r fixes ±2"),
    (0, "n → 0: the seat", "one gate, at 0"),
]):
    axs = fig.add_subplot(gs[1, i])
    r = np.linspace(-3.4, 3.4, 600)
    r = r[np.abs(r) > 1e-3]
    y = r if nn == 0 else r - nn / r
    axs.plot(r, y, color=GOLD, lw=2.0, zorder=3)
    axs.axhline(0, color=ASH, lw=0.9, alpha=0.6, zorder=1)
    axs.axvline(0, color=ASH, lw=0.7, alpha=0.3, zorder=1)
    axs.set_facecolor(BG)
    axs.set_xticks([]); axs.set_yticks([])
    for s in axs.spines.values():
        s.set_color(ASH); s.set_alpha(0.4)
    axs.set_xlim(-3.4, 3.4)
    axs.set_ylim(-3.6, 3.6)
    axs.set_title(title, color=GOLD, fontsize=9.5, pad=5)
    for r0 in (np.sqrt(nn), -np.sqrt(nn)) if nn > 0 else (0.0,):
        axs.plot(r0, 0, 'o', ms=9, mfc=BG, mec=GOLD, mew=2.2, zorder=4)
        lab = f"{r0:+.0f}" if abs(r0 - round(r0)) < 1e-9 else f"{r0:+.2f}"
        axs.text(r0, 0.45, lab, color=PALE, fontsize=8, ha="center")
    axs.text(0.5, -0.9, note, transform=axs.transAxes, color=PALE,
             fontsize=8, ha="left", va="top")
    axs.set_xlabel("r (a root)", color=ASH, fontsize=8)

fig.suptitle("the seam is the gate-locus: √Δ = r − n/r, zero where the sheets fuse",
             color=PALE, fontsize=11.5, y=0.965)
fig.savefig("assets/seam-gates-cover.png", dpi=150, facecolor=BG)
print("saved assets/seam-gates-cover.png")
