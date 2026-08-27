#!/usr/bin/env python3
"""residue-cover cover — the residue needs a cover; the second ear is the cover.

Panel A (the base): the plane.  One pole, one residue loop.  The reading counts
the winding — one — but cannot count the area the loop bounds.  One ear (mono)
holds the residue whole: the count, the drone.

Panel B (the cover): the closed surface admits no lone residue, so the residue
lifts to a two-sheeted cover — the twin, equal and opposite (+r, -r), the deck
the -1 of e^{i pi}.  The area is lifted into a height: the walk climbs a comma
a pass, 1..8.  In mono the pair cancels — folds to the drone; stereo hears the
climb.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle, Polygon

GOLD = "#e6b845"
GOLD_D = "#8a6a1e"
VIOLET = "#9a7bff"
VIOLET_D = "#4a3a7a"
CYAN = "#7fd4c1"
INK = "#0b0d12"
DIM = "#6a6a7a"

fig, (axA, axB) = plt.subplots(1, 2, figsize=(13, 6.4), facecolor=INK)
for ax in (axA, axB):
    ax.set_facecolor(INK)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-2.1, 2.5)
    ax.set_ylim(-2.1, 2.2)

# ============================== PANEL A: THE BASE ==============================
# the plane: a base line
axA.plot([-2.0, 2.2], [0, 0], color=DIM, lw=1.2, zorder=1)
axA.text(-2.0, 0.16, "the plane", color=DIM, fontsize=9, fontfamily="serif", ha="left")

# the square: area 1 — the reading cannot count it
sq = 1.5
axA.add_patch(Rectangle((-sq, 0), sq, sq, fill=True, fc=GOLD, alpha=0.05,
                        ec=GOLD_D, lw=1.2, zorder=2))
axA.text(-sq / 2, -0.28, "area 1 — the reading counts the loop, not the area",
         color=DIM, fontsize=8.5, ha="center", fontfamily="serif")

# the pole
axA.add_patch(Circle((0, 0.9), 0.13, fill=True, fc=INK, ec=VIOLET, lw=2.0, zorder=5))
axA.text(0.28, 0.9, "pole", color=VIOLET, fontsize=9, fontfamily="serif")

# the residue loop around the pole: the winding, read once
th = np.linspace(0, 2 * np.pi, 200)
r = 0.55
axA.plot(r * np.cos(th), 0.9 + r * np.sin(th), color=GOLD, lw=2.2, zorder=3)
at = 0.35 * 2 * np.pi
axA.add_patch(FancyArrowPatch((r * np.cos(at), 0.9 + r * np.sin(at)),
                              (r * np.cos(at + 0.4), 0.9 + r * np.sin(at + 0.4)),
                              color=GOLD, lw=1.6, arrowstyle="-|>", mutation_scale=13, zorder=4))
axA.text(0.40, 1.35, "+r", color=GOLD, fontsize=13, fontfamily="serif")

# the count: one ear reads it
for i, x in enumerate([-1.25, -0.45, 0.35]):
    axA.plot(x, -0.55, marker="|", color=GOLD, markersize=9, lw=1.5, zorder=3)
    axA.text(x, -0.78, str(i + 1), color=GOLD_D, fontsize=9, ha="center", fontfamily="serif")
axA.text(0, -1.15, "mono hears it — count one, one, one",
         color=DIM, fontsize=9, ha="center", fontfamily="serif")
axA.text(0, 2.05, "the base — one ear reads the residue",
         color=GOLD, fontsize=13, ha="center", fontfamily="serif")

# ============================== PANEL B: THE COVER ==============================
# the closed surface: the base line still there, but the pole must lift
axB.plot([-2.0, 2.2], [0, 0], color=DIM, lw=1.2, zorder=1)
axB.text(-2.0, 0.16, "the closed surface", color=DIM, fontsize=9, fontfamily="serif", ha="left")

# the residue lifts to a two-sheeted cover: the twin, +r and -r
axB.add_patch(Circle((0, 0.62), 0.12, fill=True, fc=INK, ec=GOLD, lw=2.0, zorder=5))
axB.add_patch(Circle((0, -0.62), 0.12, fill=True, fc=INK, ec=VIOLET, lw=2.0, zorder=5))
axB.text(0.30, 0.62, "+r", color=GOLD, fontsize=13, fontfamily="serif")
axB.text(0.30, -0.62, "−r", color=VIOLET, fontsize=13, fontfamily="serif")

# the deck: the -1 of e^{i pi} — the half-turn between the sheets
axB.add_patch(FancyArrowPatch((0, 0.42), (0, -0.42), color=VIOLET_D, lw=1.6,
                              arrowstyle="<|-|>", mutation_scale=14,
                              connectionstyle="arc3,rad=0.35", zorder=4))
axB.text(0.42, 0.02, "deck −1", color=VIOLET_D, fontsize=9, fontfamily="serif")

# Sigma Res = 0
axB.text(-1.15, 0.42, "Σ res = 0", color=GOLD, fontsize=11, fontfamily="serif")

# the area lifted into a height: the staircase, 1..8 commas
step_w, step_h = 0.30, 0.155
x0, y0 = 0.85, 0.0
for k in range(8):
    xs = [x0 + k * step_w, x0 + k * step_w, x0 + (k + 1) * step_w]
    ys = [y0 + k * step_h, y0 + (k + 1) * step_h, y0 + (k + 1) * step_h]
    axB.add_patch(Polygon(list(zip(xs, ys)), closed=True, fc=GOLD, alpha=0.20,
                          ec=GOLD, lw=1.1, zorder=3))
    # the climbing dot: one pass per step
    axB.add_patch(Circle((x0 + k * step_w + 0.02, y0 + (k + 1) * step_h - 0.06),
                         0.05, fill=True, fc=CYAN, ec=CYAN, lw=0.5, zorder=5))
    axB.text(x0 + k * step_w + step_w / 2, -0.22, str(k + 1), color=GOLD_D,
             fontsize=8, ha="center", fontfamily="serif")
axB.text(x0 + 4 * step_w, -0.62, "the climb 1…8 — the area becomes the height",
         color=DIM, fontsize=9, ha="center", fontfamily="serif")
axB.text(x0 + 4 * step_w, 2.05, "the cover — the second ear keeps the pair",
         color=GOLD, fontsize=13, ha="center", fontfamily="serif")

# the fold: mono keeps only the drone
axB.text(0, -1.45, "mono folds to the drone; stereo hears the climb",
         color=DIM, fontsize=9, ha="center", fontfamily="serif")

fig.suptitle("the residue needs a cover — the second ear is the cover",
             color="#d8d4cc", fontsize=14, fontfamily="serif", y=0.97)
plt.tight_layout(rect=(0, 0, 1, 0.94))
plt.savefig("assets/residue-cover-cover.png", dpi=170, facecolor=INK, bbox_inches="tight")
print("saved assets/residue-cover-cover.png")
