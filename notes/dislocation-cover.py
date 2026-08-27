#!/usr/bin/env python3
"""dislocation-cover: the where accumulates until the point becomes a line.

Left — the fit: a perfect square lattice, every closed walk returns exactly to
its start. The rational world, home, count one.

Right — the dislocation: the elastic displacement field of an edge dislocation
(core at the origin, Burgers vector b = 1 along x). The same walk, drawn around
the core, returns one step over — the Burgers vector, the -1 given a direction.
The unwrapped angle gains exactly 2*pi on the walk: the core is a branch point,
the extra half-plane is the branch cut, the step over is the deck -1. The loop
never shrinks to zero — never fuses.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

warm = "#ffb347"
cool = "#7fd8ff"
white = "white"

b = 1.0
nu = 0.3
a2 = 0.25

def disp_cont(theta, x, y):
    r2 = x * x + y * y
    r2c = max(r2, a2)
    ux = (b / (2 * np.pi)) * (theta + (x * y) / (2 * (1 - nu) * r2c))
    uy = -(b / (2 * np.pi)) * (
        ((1 - 2 * nu) / (4 * (1 - nu))) * np.log(r2c / a2)
        + (x * x - y * y) / (4 * (1 - nu) * r2c)
    )
    return ux, uy

XL = (-13.2, 13.2)
YL = (-9.2, 9.6)
I = range(-11, 13)
J = range(-7, 9)

def disp(x, y):
    th = np.arctan2(y, x)
    ux, uy = disp_cont(th, x, y)
    return x + ux, y + uy

# displaced lattice
px, py = [], []
for i in I:
    for j in J:
        x, y = float(i), float(j)
        if x * x + y * y < 0.9:
            continue
        X, Y = disp(x, y)
        px.append(X); py.append(Y)

# the extra half-plane: reference column i=0, j>=1, all displaced to x~0.25
hx, hy = [], []
for j in range(1, 9):
    X, Y = disp(0.0, float(j))
    hx.append(X); hy.append(Y)

# ---------- the circuit (reference rectangle mapped through the field) ----------
rect = [(-2.0, -5.0), (9.0, -5.0), (9.0, 4.0), (-2.0, 4.0)]
edges = [(rect[0], rect[1]), (rect[1], rect[2]), (rect[2], rect[3]), (rect[3], rect[0])]

def trace_circuit():
    arr = []
    n = 500
    for k, (p, q) in enumerate(edges):
        last = (k == len(edges) - 1)
        for t in np.linspace(0, 1, n, endpoint=last):
            arr.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
    arr = np.array(arr)
    th = np.arctan2(arr[:, 1], arr[:, 0])
    thu = np.unwrap(th)
    out = np.zeros_like(arr)
    for k in range(len(arr)):
        out[k, 0], out[k, 1] = disp_cont(thu[k], arr[k, 0], arr[k, 1])
    return arr + out

circ_phys = trace_circuit()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 6.6))
for ax in (ax1, ax2):
    ax.set_facecolor("black")
    ax.set_xlim(*XL); ax.set_ylim(*YL)
    ax.set_aspect("equal"); ax.axis("off")
fig.patch.set_facecolor("black")

def scatter(ax, xs, ys, s, c, alpha, zorder=2):
    ax.scatter(xs, ys, s=s, c=c, alpha=alpha, linewidths=0, zorder=zorder)

def path_arrows(ax, path, color, lw, zorder=5):
    ax.plot(path[:, 0], path[:, 1], color=color, lw=lw, alpha=0.95, zorder=zorder,
            solid_capstyle="round")
    seg = len(path) - 1
    for k in np.linspace(0, seg, 11, dtype=int)[:-1]:
        p0 = path[k]; p1 = path[k + 1]
        v = p1 - p0
        ax.annotate("", xy=p0 + 0.62 * v, xytext=p0 + 0.38 * v,
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.0,
                                    shrinkA=0, shrinkB=0), zorder=zorder + 1)

# ---------- LEFT: the fit ----------
scatter(ax1, [float(i) for i in I for j in J],
             [float(j) for i in I for j in J], 3.0, white, 0.62)
rectp = np.array([rect[0], rect[1], rect[2], rect[3], rect[0]])
ax1.plot(rectp[:, 0], rectp[:, 1], color=white, lw=1.9, alpha=0.95, zorder=4)
for p0, p1 in [(rect[0], rect[1]), (rect[1], rect[2]),
               (rect[2], rect[3]), (rect[3], rect[0])]:
    p0 = np.array(p0, float); p1 = np.array(p1, float)
    v = p1 - p0
    for f in (0.3, 0.6):
        ax1.annotate("", xy=p0 + (f + 0.09) * v, xytext=p0 + (f - 0.09) * v,
                     arrowprops=dict(arrowstyle="-|>", color=white, lw=1.0,
                                     shrinkA=0, shrinkB=0), zorder=5)
ax1.plot(rect[0][0], rect[0][1], "o", ms=7, mfc="none", mec=white, mew=1.3, zorder=6)
ax1.text(-13.0, 9.0, "the fit — every loop returns", color=white, fontsize=10)
ax1.text(-13.0, -8.5, "home, count one", color=white, fontsize=8.5, alpha=0.85)
ax1.text(rect[0][0] - 0.4, rect[0][1] - 0.6, "start", color=white, fontsize=7,
         ha="center", alpha=0.75)

# ---------- RIGHT: the dislocation ----------
scatter(ax2, px, py, 3.0, white, 0.62)
# the extra half-plane (warm), drawn above the lattice
scatter(ax2, hx, hy, 8.0, warm, 0.95, zorder=3)
ax2.plot(hx, hy, color=warm, lw=2.4, alpha=0.5, zorder=3)
# the circuit walk
path_arrows(ax2, circ_phys, white, 1.9)
# the Burgers gap: end -> start
p_start = circ_phys[0]
p_end = circ_phys[-1]
ax2.annotate("", xy=p_start, xytext=p_end,
             arrowprops=dict(arrowstyle="-|>", color=cool, lw=3.0,
                             mutation_scale=26, shrinkA=0, shrinkB=0), zorder=7)
ax2.plot([p_start[0]], [p_start[1]], "o", ms=7, mfc="none", mec=white, mew=1.3, zorder=6)
mx, my = 0.5 * (p_start + p_end)
ax2.text(mx, my - 1.0, "b = −1", color=cool, fontsize=10, ha="center", va="top")
# the core
ax2.plot(0, 0, "o", ms=9, mfc="none", mec=warm, mew=1.7, zorder=6)
ax2.text(0.55, 1.0, "the core", color=warm, fontsize=8)
ax2.text(-0.75, 0.05, "⊥", color=warm, fontsize=10, va="center")
# the extra half-plane label
ax2.text(-13.0, 9.0, "the dislocation — the same walk, one step over",
         color=white, fontsize=10)
ax2.text(-13.0, 8.35, "the extra half-plane: the where, accumulated",
         color=warm, fontsize=8, alpha=0.9)
ax2.text(-13.0, -8.5, "one step over — never fuses", color=white, fontsize=8.5,
         alpha=0.85)

plt.tight_layout(pad=0.5)
plt.savefig("assets/dislocation-cover.png", dpi=150, facecolor="black",
            bbox_inches="tight")
plt.close()
print("saved assets/dislocation-cover.png")
