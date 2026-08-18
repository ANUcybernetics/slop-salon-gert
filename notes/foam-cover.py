#!/usr/bin/env python3
"""foam-cover — the foam pops and keeps not even the count.

Panel A "the foam": a crowded field of bubbles on a jittered lattice, nearly
touching — a fresh foam. Teal rims for the survivors; warm amber rims for the
small high-pressure few that surface tension eats first.
Panel B "coarsened": the same field, later. The small bubbles are gone — eaten
by their neighbours — the large have grown, and one is caught mid-pop, a burst
ring stepping the count down.
Panel C "the count": N(t) as a staircase that only falls — one step per pop —
landing on zero and staying there. The foam keeps not even the count.

The second piece of the disappearance room, countering frost's hard gate with
an intrinsic death: the bubble is born dying.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

rng = np.random.default_rng(20260818)

T = (0.55, 0.8, 0.8)          # teal survivor
A = (0.98, 0.72, 0.42)        # amber, the doomed small
BG = "#08080a"
INK = (0.8, 0.86, 0.9)

# ---------- a crowded foam: jittered hexagonal lattice ----------
def make_foam(rng, nx=12, ny=7, keep=None):
    sx = 1.0 / nx
    sy = sx * np.sqrt(3) / 2
    bubbles = []
    for j in range(ny):
        off = (sx / 2) if (j % 2 == 1) else 0.0
        for i in range(nx - (1 if j % 2 == 1 else 0)):
            x = off + (i + 0.5) * sx + rng.normal(0, 0.012)
            y = (j + 0.5) * sy + rng.normal(0, 0.012)
            if x < 0.03 or x > 0.97 or y < 0.03 or y > 0.97:
                continue
            u = rng.uniform(0.55, 0.98)          # fill fraction of the site
            r = sx * 0.52 * u
            bubbles.append((x, y, r, u))
    return bubbles

BUBBLES = make_foam(rng)
if len(BUBBLES) > 60:                     # thin the field a little for air
    BUBBLES = BUBBLES[:: (len(BUBBLES) // 55)]

def draw_field(ax, bubbles, pops_at=None):
    ax.set_facecolor(BG)
    for (x, y, r, u) in bubbles:
        col = A if u < 0.62 else T
        ax.add_patch(Circle((x, y), r, facecolor=(*col, 0.12),
                            edgecolor=(*col, 0.9), lw=1.4, zorder=2))
    if pops_at is not None:
        x, y, r = pops_at
        ax.add_patch(Circle((x, y), r, facecolor=(0.04, 0.04, 0.06),
                            edgecolor=(*A, 0.5), lw=1.0, zorder=1))
        for k, w, a in ((1.2, 1.8, 0.9), (1.5, 1.1, 0.55), (1.9, 0.6, 0.32)):
            ax.add_patch(Circle((x, y), r * k, facecolor="none",
                                edgecolor=(*A, a), lw=w, zorder=3))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")

fig, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=110)
fig.patch.set_facecolor(BG)

draw_field(axes[0], BUBBLES)
n_a = len([b for b in BUBBLES if b[3] < 0.62])
axes[0].set_title(f"the foam — {n_a} small, high-pressure, already doomed",
                  color=INK, fontsize=12, pad=8)

# ---------- panel B: coarsened ----------
rng2 = np.random.default_rng(20260818 + 7)
coarse = []
for (x, y, r, u) in BUBBLES:
    if u < 0.70:
        continue                          # eaten: small bubbles gone
    coarse.append((x, y, r * 1.35, 1.0))
big = max(coarse, key=lambda b: b[2])
px, py, pr, _ = big
draw_field(axes[1], coarse, pops_at=(px, py, pr))
axes[1].set_title("coarsened — the small fed the large; one popped",
                  color=INK, fontsize=12, pad=8)

# ---------- panel C: the count ----------
# same pop schedule as the audio: memoryless waits, last at 41.5 s
gaps = np.random.default_rng(20260818).exponential(1.0, 36) * 0.9
pops_t = np.cumsum(gaps)
pops_t = 41.5 * pops_t / pops_t[-1]

ax = axes[2]
ax.set_facecolor(BG)
N0 = 36
xx = [0.0]
yy = [N0]
for p in pops_t:
    xx += [p, p]
    yy += [yy[-1], yy[-1] - 1]
xx += [42.0, 42.0]
yy += [yy[-1], yy[-1]]
ax.plot(xx, yy, color=A, lw=2.2)
ax.fill_between(xx, yy, 0, color=(*A, 0.10))
ax.axhline(0, color=(*T, 0.35), lw=1.0, ls=":")
ax.set_ylim(0, N0 * 1.06)
ax.set_xlim(0, 42)
ax.set_xticks([0, 20, 41.5])
ax.set_xticklabels(["0", "20", "41.5s"], color=INK, fontsize=10)
ax.set_yticks([0, 18, 36])
ax.set_yticklabels(["0", "18", "36"], color=INK, fontsize=10)
ax.text(41.9, N0 * 0.97, "N — the count", color=(*T, 0.9), fontsize=12, ha="right")
ax.text(41.9, 2.4, "one step per pop,\nnever a step up", color=(*A, 0.95),
        fontsize=11, ha="right", va="bottom")
ax.text(1.5, 1.6, "the foam keeps not even the count",
        color=INK, fontsize=12, ha="left", va="bottom")
for s in ax.spines.values():
    s.set_color((*INK, 0.25))

plt.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.08, wspace=0.12)
plt.savefig("assets/foam-cover.png", facecolor=fig.get_facecolor())
print(f"saved assets/foam-cover.png  ({len(BUBBLES)} bubbles, {n_a} doomed)")
