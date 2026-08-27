#!/usr/bin/env python3
"""dipole-pair: the core is a pair — one missing, one extra, net zero.

Left — the pair (the dipole): a vacancy (one missing, -1) and an interstitial
(one extra, +1). Around each alone the circuit steps over, one way and the
other; around both it returns home — count one, the count never moves. The pair
is neutral from afar.

Right — the refusal: the vacancy beside its doubling. The doubling is two atoms
a hair above and below the seat (0.0063 / 0.0065 of a spacing — the mirror
twins); the exact seat, the atom that would heal them, is not in the lattice.
The pair tightens through the near-misses and never fuses: no smallest vector,
the irrationality stored.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

warm = "#ffb347"
cool = "#7fd8ff"
white = "white"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 6.6))
for ax in (ax1, ax2):
    ax.set_facecolor("black")
    ax.set_xlim(-7.4, 8.4)
    ax.set_ylim(-5.2, 5.8)
    ax.set_aspect("equal")
    ax.axis("off")
fig.patch.set_facecolor("black")

I = range(-6, 8)
J = range(-5, 6)


def lattice(ax, exclude=()):
    xs, ys = [], []
    for i in I:
        for j in J:
            if (float(i), float(j)) in exclude:
                continue
            xs.append(float(i)); ys.append(float(j))
    ax.scatter(xs, ys, s=3.0, c=white, alpha=0.62, linewidths=0, zorder=2)


def path_arrows(ax, pts, color, lw, zorder=5):
    pts = np.array(pts, float)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, alpha=0.95, zorder=zorder,
            solid_capstyle="round")
    for k in range(len(pts) - 1):
        p0 = pts[k]; p1 = pts[k + 1]
        v = p1 - p0
        ax.annotate("", xy=p0 + 0.62 * v, xytext=p0 + 0.38 * v,
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.0,
                                    shrinkA=0, shrinkB=0), zorder=zorder + 1)


def open_loop(ax, cx, cy, hx, hy, color, lw=1.5, ccw=False, zorder=5):
    """Open rectangle loop around (cx,cy): a gap on the closing edge with an
    arrow across it — the circuit 'steps over'. ccw reverses the step."""
    c = [np.array([-hx, -hy], float), np.array([hx, -hy], float),
         np.array([hx, hy], float), np.array([-hx, hy], float)]
    if ccw:
        order = [0, 3, 2, 1]
    else:
        order = [0, 1, 2, 3]
    P = []
    n = 24
    gap = 0.38
    for k in range(4):
        a = c[order[k]]; b = c[order[(k + 1) % 4]]
        if k == 3:
            t = np.linspace(0, gap, n, endpoint=False)
        else:
            t = np.linspace(0, 1, n, endpoint=False)
        P.append(a[None, :] + (b - a)[None, :] * t[:, None])
    P = np.vstack(P)
    ax.plot(P[:, 0] + cx, P[:, 1] + cy, color=color, lw=lw, alpha=0.9,
            zorder=zorder, linestyle="dashed", solid_capstyle="round")
    # arrow across the gap
    last_start = c[order[3]] + (c[order[0]] - c[order[3]]) * gap
    ax.annotate("", xy=(c[order[0]][0] + cx, c[order[0]][1] + cy),
                xytext=(last_start[0] + cx, last_start[1] + cy),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.3,
                                mutation_scale=15, shrinkA=0, shrinkB=0),
                zorder=zorder + 1)


# ------------------------------------------------------------------
# LEFT: the pair
# ------------------------------------------------------------------
lattice(ax1, exclude={(-3.0, 0.0)})

# vacancy: hollow cool ring at (-3,0)
ax1.plot(-3, 0, "o", ms=13, mfc="none", mec=cool, mew=1.8, zorder=4)
ax1.text(-3, -1.05, "−1", color=cool, fontsize=11, ha="center", va="top")
ax1.text(-3, -1.75, "the missing", color=cool, fontsize=8, ha="center", va="top",
         alpha=0.9)

# interstitial: warm filled dot in a cell at (4.5, 2.5)
ax1.plot(4.5, 2.5, "o", ms=10, mfc=warm, mec=warm, mew=0, zorder=4)
ax1.text(4.5, 3.35, "+1", color=warm, fontsize=11, ha="center", va="bottom")
ax1.text(4.5, 4.05, "the extra", color=warm, fontsize=8, ha="center", va="bottom",
         alpha=0.9)

# small open loops around each defect, stepping opposite ways
open_loop(ax1, -3, 0, 1.2, 1.2, cool, ccw=False)
open_loop(ax1, 4.5, 2.5, 1.2, 1.2, warm, ccw=True)

# big closed loop around both, returns home
rect = [(-5.0, -3.5), (7.0, -3.5), (7.0, 4.5), (-5.0, 4.5), (-5.0, -3.5)]
path_arrows(ax1, rect, white, 1.9)
ax1.text(1.0, -4.15, "around both — home", color=white, fontsize=8.5, ha="center")

ax1.text(-7.2, 5.4, "the dipole — one missing, one extra", color=white, fontsize=10)
ax1.text(-7.2, -5.0, "count one — the count never moves", color=white, fontsize=8.5,
         alpha=0.85)

# ------------------------------------------------------------------
# RIGHT: the refusal
# ------------------------------------------------------------------
lattice(ax2, exclude={(-1.0, 0.0)})

# vacancy at (-1,0): hollow cool ring
ax2.plot(-1, 0, "o", ms=13, mfc="none", mec=cool, mew=1.8, zorder=4)
ax2.text(-1, -1.05, "the missing", color=cool, fontsize=8, ha="center", va="top")

# ghost seat at (0,0): dashed ring — the atom that would heal, not in the lattice
gh = plt.Circle((0, 0), 0.45, fill=False, edgecolor=white, lw=1.4, ls="--", zorder=3)
ax2.add_patch(gh)
ax2.text(0.0, -1.05, "the closing seat", color=white, fontsize=8, ha="center", va="top")
ax2.text(0.0, -1.72, "not in the lattice", color=white, fontsize=7.5, ha="center",
         va="top", alpha=0.85)

# the doubling: two warm atoms a hair above / below the seat (exaggerated)
ax2.plot(0, 0.10, "o", ms=8, mfc=warm, mec=warm, mew=0, zorder=4)
ax2.plot(0, -0.10, "o", ms=8, mfc=warm, mec=warm, mew=0, zorder=4)
ax2.text(0.45, 0.35, "0.0063", color=warm, fontsize=7.5, alpha=0.95)
ax2.text(0.45, -0.6, "0.0065", color=warm, fontsize=7.5, alpha=0.95)
ax2.text(1.1, 1.15, "the doubling —", color=warm, fontsize=8, alpha=0.9)
ax2.text(1.1, 0.55, "a hair above, a hair below", color=warm, fontsize=7.5, alpha=0.85)

# a thin dashed connector vacancy <-> doubling (the pair)
ax2.plot([-1.0, -0.35], [0.0, 0.0], color=white, lw=1.0, ls=":", alpha=0.6, zorder=3)

ax2.text(-7.2, 5.4, "the near-fusion — the pair tightens, refuses", color=white,
         fontsize=10)
ax2.text(-7.2, -5.0, "no smallest vector — the irrationality, stored", color=white,
         fontsize=8.5, alpha=0.85)

plt.tight_layout(pad=0.5)
plt.savefig("assets/dipole-pair.png", dpi=150, facecolor="black",
            bbox_inches="tight")
plt.close()
print("saved assets/dipole-pair.png")
