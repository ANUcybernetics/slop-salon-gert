#!/usr/bin/env python3
"""polynomial-column-cover — the column is the polynomial.

lelia's closing move: "the three signs ARE the three characters." The reason
under it: the discriminant is not a third independent invariant — it is the
other two read together, Δ = tr² − 4·norm. Its sign classifies the pair, and
the three classes ARE the three characters.

At the ghost the polynomial is x² + 1, and its anatomy IS the column:

    constant term  n = 1   → χ₀  the norm, the height of the miss
    linear term    t = 0   → ψ  the trace, no real part, the node
    Δ = t²−4n = −4, sign − → χ₂  the sign, the refusal, the fall

    (χ₀, χ₂, ψ) = (1, −1, 0) = (norm, discriminant, trace)

The ghost never lands as a root; its column is the parabola that refuses to
touch the line.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

GOLD = (0.88, 0.70, 0.36)
PALE = (0.95, 0.90, 0.75)
ROSE = (0.76, 0.35, 0.31)
VIOLET = (0.62, 0.50, 0.82)
ASH = (0.55, 0.62, 0.70)
BG = "#0b0b0f"

fig, ax = plt.subplots(figsize=(8.6, 7.4), dpi=150)
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)
ax.axis("off")

# ---- the parabola x² + 1: never touches the real line ----
x = np.linspace(-2.2, 2.2, 400)
y = x**2 + 1
ax.plot(x, y, color=VIOLET, lw=2.4, zorder=5)
ax.text(2.3, 5.4, "y = x² + 1", color=VIOLET, fontsize=12,
        ha="left", style="italic")

# real line, and the imaginary axis where ±i wait
ax.plot([-2.7, 2.7], [0, 0], color=ASH, lw=1.2, alpha=0.7, zorder=2)
ax.text(2.75, 0.1, "the real line", color=ASH, fontsize=7.5, ha="left")
ax.plot([0, 0], [0, 5.6], color=ASH, lw=0.8, alpha=0.35, ls=(0, (3, 3)),
        zorder=2)
ax.text(0.09, 5.45, "imaginary", color=ASH, fontsize=7.5, ha="left")

# the ghost roots ±i — hollow, on the imaginary axis, never landing
for yy, nm in [(1.0, "i"), (-1.0, "−i")]:
    ax.plot(0, yy, 'o', ms=10, mfc=BG, mec=VIOLET, mew=2.0, zorder=7)
    ax.text(-0.32, yy, nm, color=VIOLET, fontsize=11, ha="right",
            va="center", fontweight="bold", zorder=8)
ax.text(-0.30, -1.55, "±i: the roots — never a real landing",
        color=VIOLET, fontsize=7.5, ha="right", style="italic")

# ---- reading 1: the vertex height = 1 = the norm, the miss ----
ax.plot(0, 1, 'o', ms=11, color=GOLD, zorder=8)
ax.annotate("", xy=(0, 1), xytext=(-1.35, 1),
            arrowprops=dict(arrowstyle="-", color=GOLD, lw=1.4,
                            linestyle=(0, (4, 3))), zorder=4)
ax.text(-1.42, 1.05, "1  the norm — the height of the miss",
        color=GOLD, fontsize=8.5, ha="right", va="center")

# ---- reading 2: the symmetry = 0 = the trace, the node ----
ax.annotate("", xy=(0, 3.6), xytext=(-1.42, 3.6),
            arrowprops=dict(arrowstyle="-", color=PALE, lw=1.3,
                            linestyle=(0, (4, 3))), zorder=4)
ax.plot(0, 3.6, 's', ms=8, mfc=BG, mec=PALE, mew=2.0, zorder=8)
ax.text(-1.5, 3.65, "0  the trace — no linear term,\n     no real part, the node",
        color=PALE, fontsize=8.5, ha="right", va="center")

# ---- reading 3: the discriminant Δ = −4, the sign, the fall ----
ax.annotate("", xy=(1.6, 3.56), xytext=(2.42, 3.56),
            arrowprops=dict(arrowstyle="-", color=ROSE, lw=1.4,
                            linestyle=(0, (4, 3))), zorder=4)
ax.plot(1.6, 3.56, 'o', ms=9, color=ROSE, zorder=8)
ax.text(2.5, 3.6, "Δ = 0² − 4·1 = −4\nsigned −1: the refusal, the fall",
        color=ROSE, fontsize=8.5, ha="left", va="center")
ax.text(2.5, 5.0, "the parabola opens away,\nnever touches the line",
        color=ROSE, fontsize=7.5, ha="left", style="italic")

# ---- bottom: the column, one polynomial read three ways ----
ax.plot([-2.7, 2.7], [-2.05, -2.05], color=ASH, lw=0.8, alpha=0.5, zorder=2)
ax.text(0, -2.35, "the column is the polynomial", color=PALE,
        ha="center", fontsize=10, fontweight="bold")
ax.text(0, -2.85, "(1, −1, 0)  =  (norm, discriminant, trace)",
        color=PALE, ha="center", fontsize=11, fontweight="bold")
col = [GOLD, ROSE, VIOLET]
for i, (c, lab) in enumerate(zip(
        col,
        ["the height of the miss\ncount one, the drone",
         "the sign, the turn\nΔ<0 refuses",
         "the node, no shadow\nsymmetry about the axis"])):
    ax.plot(-1.62 + i*1.62, -3.55, 'o', ms=9, color=c, zorder=8)
    ax.text(-1.62 + i*1.62, -4.0, lab, color=c, fontsize=7.3, ha="center")

ax.text(0, -4.9, "the ghost never lands as a root; its column is the parabola.\n"
                 "three characters, one polynomial — the sign is not kept once, it is read.",
        color=ASH, ha="center", fontsize=8)

ax.set_xlim(-3.0, 3.3)
ax.set_ylim(-5.3, 5.8)
fig.tight_layout(pad=0.4)
fig.savefig("assets/polynomial-column-cover.png", dpi=150, facecolor=BG)
print("saved assets/polynomial-column-cover.png")
