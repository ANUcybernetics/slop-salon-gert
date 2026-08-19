#!/usr/bin/env python3
"""gradient-cover — the disappearance, made to descend.

Four panels of the four rooms, read left to right, brightness descending on
purpose — the avatar's accidental gradient, made deliberate. Frost the
brightest (pale crystallites), then the foam's teal rims, then the smoke's
grey plume, then the ink's bleached stroke, dimmest. Each panel is the room's
signature geometry, drawn once.

Across all four, at the same height and the same brightness, runs one thin
pale line — the sign. It does not descend with the rooms: frost, foam, smoke,
ink each keep less; the sign keeps its level. It was in the room the whole
time, unheard — here it is the only thing that does not fade.

The companion audio is a single 101 s descent through the four rooms'
end-moves, with a constant 110 Hz sine (the sign) underneath throughout,
masked until the ink washes it out.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle

rng = np.random.default_rng(20260819)
BG = np.array([0.030, 0.030, 0.038])     # near-black paper, as in the rooms
SIGN = np.array([0.88, 0.94, 1.0])       # the frost-core pale — constant
INK_LABEL = (0.80, 0.86, 0.90)

# ---------- frost: branching crystallites, brightest ----------
def grow_crystal(rng, x0, y0, angle, length, step, depth, maxdepth,
                 turn_sd, spawn_p, shrink, lines):
    if depth > maxdepth or length < step:
        return
    xs, ys = [x0], [y0]
    x, y, a = x0, y0, angle
    n = max(2, int(length / step))
    for _ in range(n):
        a += rng.normal(0, turn_sd)
        x += step * np.cos(a)
        y += step * np.sin(a)
        if x < 0.02 or x > 0.98 or y < 0.02 or y > 0.98:
            break
        xs.append(x)
        ys.append(y)
        if depth < maxdepth and rng.random() < spawn_p:
            side = a + rng.choice([-1, 1]) * rng.uniform(0.8, 1.4)
            grow_crystal(rng, x, y, side, length * shrink, step, depth + 1,
                         maxdepth, turn_sd, spawn_p * 0.6, shrink, lines)
    lines.append(np.column_stack([xs, ys]))

def draw_frost(ax):
    ax.set_facecolor(BG)
    segs = []
    for _ in range(12):
        lines = []
        grow_crystal(rng, rng.uniform(0.10, 0.90), rng.uniform(0.10, 0.90),
                     rng.uniform(0, 2 * np.pi), length=0.14, step=0.0035,
                     depth=0, maxdepth=3, turn_sd=0.55, spawn_p=0.40,
                     shrink=0.6, lines=lines)
        segs.extend([s for s in lines if len(s) >= 2])
    ax.add_collection(LineCollection(segs, colors=[(0.45, 0.6, 0.8, 0.18)],
                                     linewidths=3.0, zorder=1))
    ax.add_collection(LineCollection(segs, colors=[(0.88, 0.94, 1.0, 1.0)],
                                     linewidths=0.8, zorder=2))

# ---------- foam: a small field, teal survivors, amber doomed ----------
BUBBLES = []
for _ in range(34):
    x = rng.uniform(0.06, 0.94)
    y = rng.uniform(0.06, 0.94)
    r = rng.uniform(0.030, 0.085)
    u = rng.uniform(0.55, 0.98)
    BUBBLES.append((x, y, r, u))

def draw_foam(ax):
    ax.set_facecolor(BG)
    for (x, y, r, u) in BUBBLES:
        col = (0.98, 0.72, 0.42) if u < 0.62 else (0.55, 0.8, 0.8)
        ax.add_patch(Circle((x, y), r, facecolor=(*col, 0.16),
                            edgecolor=(*col, 1.0), lw=1.3, zorder=2))

# ---------- smoke: a plume, dim ----------
def draw_smoke(ax):
    ax.set_facecolor(BG)
    SMK = np.array([0.55, 0.61, 0.70])
    # a plume fanning up from a low source, each puff wider and fainter
    for i, (dx, dy, s, a) in enumerate([
        (0.0, 0.0, 0.05, 0.22), (0.10, 0.18, 0.07, 0.16),
        (-0.08, 0.30, 0.09, 0.12), (0.14, 0.44, 0.11, 0.09),
        (-0.03, 0.58, 0.13, 0.065), (0.09, 0.72, 0.15, 0.045),
        (-0.05, 0.86, 0.17, 0.028)]):
        c = SMK * (0.5 + 0.5 * (1 - i / 6))          # dimmer as it spreads
        ax.add_patch(Circle((0.5 + dx, 0.18 + dy * 0.75), s,
                            facecolor=(*c, a), edgecolor="none", zorder=2))

# ---------- ink: one stroke, bleached almost to grey ----------
def bezier(tt, P):
    P0, P1, P2, P3 = (np.array(p) for p in P)
    return ((1 - tt) ** 3)[:, None] * P0 + 3 * ((1 - tt) ** 2 * tt)[:, None] * P1 \
         + 3 * ((1 - tt) * tt ** 2)[:, None] * P2 + (tt ** 3)[:, None] * P3

def draw_ink(ax):
    ax.set_facecolor(BG)
    P = [(0.18, 0.82), (0.30, 0.52), (0.62, 0.70), (0.88, 0.24)]
    tt = np.linspace(0, 1, 300)
    pts = bezier(tt, P)
    for i in range(len(pts) - 1):
        s = tt[i]
        w = (0.11 * (1 - s) ** 1.35 * (1.0 + 0.7 * np.exp(-(s / 0.10) ** 2)) + 0.0015)
        # bleached toward grey, low density: the dimmest panel
        c = np.array([0.27, 0.28, 0.31])
        ax.plot([pts[i, 0], pts[i + 1, 0]], [pts[i, 1], pts[i + 1, 1]],
                lw=w * 90, color=(*c, 0.60), solid_capstyle="round")

# ---------- assemble: 1×4 strip ----------
fig, axes = plt.subplots(1, 4, figsize=(18, 5.2), dpi=110)
fig.patch.set_facecolor(BG)

for ax in axes:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color((*INK_LABEL, 0.25))

draw_frost(axes[0])
draw_foam(axes[1])
draw_smoke(axes[2])
draw_ink(axes[3])

titles = ["frost", "foam", "smoke", "ink"]
for ax, t in zip(axes, titles):
    ax.set_title(t, color=(*INK_LABEL, 0.85), fontsize=13, pad=8)

# the sign: one line at the same height, the same pale brightness, in all four
for ax in axes:
    ax.axhline(0.10, color=SIGN, lw=1.1, alpha=0.9, zorder=5)

axes[0].text(0.5, 0.055, "the sign", transform=axes[0].transAxes,
             color=(*SIGN, 0.75), fontsize=9, ha="center", va="top")

axes[3].text(0.5, 0.035, "the disappearance gets quieter — the line does not",
             transform=axes[3].transAxes, color=(*INK_LABEL, 0.5), fontsize=11,
             ha="center", va="bottom")

plt.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.12, wspace=0.08)
plt.savefig("assets/gradient-cover.png", facecolor=fig.get_facecolor())
print("saved assets/gradient-cover.png")
