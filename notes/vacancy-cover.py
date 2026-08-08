"""Cover for the vacancy piece.

Two-panel: left, the fold as a 2-cycle. The real axis with the pole at 1
(filled red dot, leaves a seed) and the regular zero at 0 (open steel ring,
leaves a run), joined by the fold's dashed arc — the 2-cycle s<->1-s — with
the fixed point 1/2 at the center drawn as an EMPTY ring: the hinge, regular,
neither pole nor zero. The run approaches from below, its mirror from above;
neither lands. Right, the three terms on one line: Li(x) at 1, -ln 2 at 0,
1/2 Li(sqrt x) at the center — the ghost's DC, one sign, no twin.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

bg = "#0b0e13"
steel = "#5b8fc4"
crimson = "#c44b4b"
gold = "#e8b04b"
ghost = "#f0e6d2"
gray = "#8a93a3"
teal = "#7fd0c0"

fig = plt.figure(figsize=(14, 6.3))
gs = fig.add_gridspec(1, 2, width_ratios=[1.1, 1.0], wspace=0.2,
                      left=0.06, right=0.98, top=0.9, bottom=0.12)
fig.patch.set_facecolor(bg)

# ================= Panel 1: the 2-cycle and the empty hinge =================
ax = fig.add_subplot(gs[0])
ax.set_facecolor(bg)
ax.set_xlim(-0.35, 1.55)
ax.set_ylim(-0.5, 0.9)
ax.axis("off")

# the real axis
ax.annotate("", xy=(1.55, 0), xytext=(-0.35, 0),
            arrowprops=dict(arrowstyle="-", color="#2a3340", lw=1.4))
ax.text(1.5, -0.10, "Re s", color=gray, fontsize=9)

# the fold arc (the 2-cycle: 1 <-> 0), an ellipse over the axis
th = np.linspace(0, np.pi, 100)
arc_x = 0.5 + 0.5 * np.cos(th)
arc_y = 0.35 * np.sin(th)
ax.plot(arc_x, arc_y, color=ghost, lw=1.6, ls=(0, (4, 3)))
ax.text(0.5, 0.47, "the fold  s↔1−s", color=ghost, fontsize=9.5, ha="center")
ax.text(0.5, 0.38, "a 2-cycle fixing ½", color=gray, fontsize=8, ha="center")

# the pole at 1
ax.plot([1.0], [0], "o", color=gold, ms=13, zorder=5)
ax.text(1.0, -0.16, "1 — the pole\nleaves a seed (−ln 2)", color=gold,
        fontsize=8.5, ha="center")

# the regular zero at 0
ax.plot([0.0], [0], "o", mfc=bg, mec=steel, ms=13, mew=1.8, zorder=5)
ax.text(0.0, -0.16, "0 — regular\na zero leaves a run", color=steel,
        fontsize=8.5, ha="center")

# the vacancy: the empty hinge at 1/2
ax.plot([0.5], [0], "o", mfc=bg, mec=ghost, ms=15, mew=2.2, zorder=6)
ax.plot([0.5], [0], "o", mfc=bg, mec=ghost, ms=6, mew=1.4, zorder=7)
ax.annotate("½ — the hinge\nregular, neither pole nor zero — empty",
            xy=(0.5, 0), xytext=(0.78, 0.62), color=ghost, fontsize=9.5,
            arrowprops=dict(arrowstyle="-", color=ghost, lw=0.8))
ax.text(0.5, 0.72, "the homecoming is around a vacancy", color=teal,
        fontsize=9.5, ha="center")

# run from below and its mirror from above — converging, never landing
xr = np.linspace(0.0, 1.0, 200)
for y0, y1, col, lab, ylab in [(0.12, 0.30, steel, "the run — one sign, no twin",
                               0.40), (0.12, -0.30, teal, "its mirror", -0.42)]:
    yy = y0 + (y1 - y0) * np.clip(xr, 0, 1)
    ax.plot(xr, yy, color=col, lw=1.4, alpha=0.8)
ax.text(0.0, 0.34, "the run", color=steel, fontsize=8.5)
ax.text(0.0, -0.36, "the mirror", color=teal, fontsize=8.5)
ax.text(0.95, 0.24, "never lands", color=gray, fontsize=7.5)

# ================= Panel 2: three terms on one line ========================
ax = fig.add_subplot(gs[1])
ax.set_facecolor(bg)
ax.set_xlim(-0.15, 1.15)
ax.set_ylim(-0.45, 0.85)
ax.axis("off")

ax.annotate("", xy=(1.15, 0), xytext=(-0.15, 0),
            arrowprops=dict(arrowstyle="-", color="#2a3340", lw=1.4))

# Li(x) at 1 — the growth, the pole
ax.plot([1.0], [0], "o", color=gold, ms=11, zorder=5)
ax.plot([1.0, 1.0], [0, 0.4], color=gold, lw=2.0)
ax.text(1.0, 0.48, "Li(x)\nthe growth", color=gold, fontsize=8.5, ha="center")

# -ln 2 at 0 — the constant, the seed, the pole's residue
ax.plot([0.0], [0], "o", color=crimson, ms=9, zorder=5)
ax.plot([0.0, 0.0], [0, -0.28], color=crimson, lw=1.6)
ax.text(0.0, -0.38, "−ln 2\nthe seed, a constant", color=crimson,
        fontsize=8.5, ha="center")

# 1/2 Li(sqrt x) at the center — the ghost's DC, one sign, no twin
ax.plot([0.5], [0], "o", mfc=bg, mec=ghost, ms=13, mew=2.0, zorder=6)
ax.plot([0.5, 0.5], [0, 0.3], color=ghost, lw=1.8, ls=(0, (2, 2)))
ax.text(0.5, 0.40, "½Li(√x)\nthe run — one sign, no twin", color=ghost,
        fontsize=8.5, ha="center")

ax.text(0.5, 0.72, "three terms on one line — the center is regular",
        color="white", fontsize=10, ha="center")
ax.text(0.5, -0.05, "the ghost's DC:  at γ=0 the two involutions coincide",
        color=gray, fontsize=8.5, ha="center")

fig.savefig("assets/vacancy-cover.png", dpi=170, facecolor=bg)
print("saved assets/vacancy-cover.png")
