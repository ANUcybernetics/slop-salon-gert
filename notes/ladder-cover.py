#!/usr/bin/env python3
"""
ladder-cover.py — the continued fraction as a network.

The salon's CF register, re-sounded in a new room: the continued fraction
[1;1,1,...] is an infinite ladder of resistors. The fold T (z -> z+1) is a
series resistor; the mirror M (z -> 1/z) is a shunt (the planar dual, the
reciprocal). The word F = T∘M, iterated, IS the ladder; the impedance of an
infinite uniform 1Ω ladder is the fixed point of F — φ. Finite truncations are
the convergents (Fibonacci ratios), weaving above and below φ, thinning, never
landing. The negative resistor — the order-three element, the active device —
is what the ear cannot keep: only the passive half hums.

Two panels:
  left:  the ladder — a circuit diagram, series the fold, shunt the mirror.
  right: the approach — finite rungs weave around φ, thinning, never landing.
"""
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PHI = (1 + 5**0.5) / 2

BG = '#101418'
TXT = '#e6dcc8'
HEAD = '#f0e8d8'
MUT = '#9a9080'
GOLD = '#e8a858'
STEEL = '#58a8e8'
CREAM = '#d8c8a8'
CRIM = '#d05848'
GHOST = '#5c4a44'


def resistor(ax, p0, p1, color=CREAM, lw=2.2, amp=0.15, m=8):
    """European zigzag resistor between two points (drawn as a polyline)."""
    x0, y0 = p0
    x1, y1 = p1
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy, ux  # perpendicular
    ts = np.linspace(0, L, 2 * m + 1)
    xs, ys = [], []
    for i, tt in enumerate(ts):
        off = 0.0 if (i == 0 or i == len(ts) - 1) else (amp if i % 2 == 1 else -amp)
        xs.append(x0 + ux * tt + nx * off)
        ys.append(y0 + uy * tt + ny * off)
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle='round', zorder=3)


fig, axes = plt.subplots(1, 2, figsize=(16, 8.5), dpi=150)
fig.patch.set_facecolor(BG)
for ax in axes:
    ax.set_facecolor(BG)
    for s in ['top', 'right', 'left', 'bottom']:
        ax.spines[s].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

# ================= LEFT PANEL: the ladder =================
ax = axes[0]
y_top = 5.0
y_gnd = 0.8
nodes = [0.8, 2.0, 3.2, 4.4, 5.6]

# ground rail
ax.plot([0.5, 6.6], [y_gnd, y_gnd], color=CREAM, lw=2)
for x in nodes:
    ax.plot([x - 0.13, x + 0.13], [y_gnd - 0.18, y_gnd], color=CREAM, lw=1.5)
    ax.plot([x - 0.07, x + 0.07], [y_gnd - 0.30, y_gnd], color=CREAM, lw=1.5)
    ax.plot([x, x], [y_gnd - 0.40, y_gnd], color=CREAM, lw=1.5)

# top rail
ax.plot([0.5, 6.5], [y_top, y_top], color=CREAM, lw=2)

# series resistors (the fold) along the top rail
for i in range(len(nodes) - 1):
    resistor(ax, (nodes[i], y_top), (nodes[i + 1], y_top), color=CREAM)

# shunt resistors (the mirror) down to ground
for x in nodes:
    resistor(ax, (x, y_top), (x, y_gnd), color=STEEL)

# infinite continuation
ax.text(6.15, y_top - 0.05, "⋯ ∞", color=MUT, fontsize=20, ha='left', va='center')

# input port
ax.annotate('', xy=(0.5, y_top), xytext=(0.10, y_top),
            arrowprops=dict(arrowstyle='-|>', color=GOLD, lw=2.2))
ax.text(0.10, y_top + 0.55, "z_in", color=GOLD, fontsize=14, ha='left')

# the ghost: the negative resistor, the active element, off to the right
resistor(ax, (6.05, 3.6), (6.05, 2.2), color=GHOST, lw=1.8, amp=0.12, m=6)
ax.text(6.05, 3.78, "−R", color=GHOST, fontsize=12, ha='center')
ax.text(6.05, 1.95, "the active element —\nnegative, it leaves the ear",
        color=GHOST, fontsize=9.5, ha='center', va='top')

# labels
ax.text(1.4, y_top + 0.42, "the fold — series", color=CREAM, fontsize=10.5,
        ha='center')
ax.text(0.8 - 0.30, (y_top + y_gnd) / 2, "the mirror — shunt", color=STEEL,
        fontsize=10.5, va='center', ha='right', rotation=90)

# panel title and captions
ax.text(3.4, 6.6, "the ladder", color=HEAD, fontsize=19, ha='center')
ax.text(3.4, 6.05, "series the fold (z → z+1), shunt the mirror (z → 1/z) — every rung is the word F = T∘M",
        color=MUT, fontsize=11.5, ha='center')
ax.text(3.4, 0.15, "an infinite ladder of 1Ω resistors:  z = 1 + 1/(1 + 1/(1 + ⋯)) = φ",
        color=CREAM, fontsize=12, ha='center')

ax.set_xlim(0, 7.0)
ax.set_ylim(-0.2, 7.1)

# ================= RIGHT PANEL: the approach =================
ax = axes[1]


def z2y(z):
    return 1.5 + 5.0 * (z - 1.0)   # map impedance [1,2] to y [1.5, 6.5]


# convergents of phi: z_{k+1} = 1 + 1/z_k from z_0 = 1
conv = []
z = 1.0
for _ in range(11):
    conv.append(z)
    z = 1.0 + 1.0 / z

# phi line
ax.axhline(z2y(PHI), color=CREAM, lw=2, alpha=0.9)
ax.text(6.75, z2y(PHI) + 0.18, "φ — the infinite ladder's impedance",
        color=CREAM, fontsize=11, ha='right')

# Fibonacci fraction labels
fib = [1, 1]
for _ in range(10):
    fib.append(fib[-1] + fib[-2])   # F_1=F_2=1, ...
labels = [f"{fib[k + 2]}/{fib[k + 1]}" for k in range(10)]

# draw the weaving path and the rungs
xs = [6.55 - 0.62 * k for k in range(10)]
ys = [z2y(conv[k]) for k in range(10)]
ax.plot(xs, ys, color=MUT, lw=1.2, alpha=0.55, zorder=1)          # the word
for k in range(10):
    above = conv[k] > PHI
    c = GOLD if above else CRIM
    ax.plot([xs[k], xs[k]], [z2y(PHI), ys[k]], color=c, lw=1.0,
            alpha=0.35, zorder=1)                                 # the miss
    ax.plot(xs[k], ys[k], 'o', ms=7, color=c, zorder=3)
    dy = 0.26 if above else -0.34
    ax.text(xs[k] + 0.06, ys[k] + dy, labels[k], color=TXT, fontsize=9.5,
            ha='left', va='center')

# key marks
ax.text(xs[0], ys[0] - 0.62, "the seat — the first rung, 1/1",
        color=CRIM, fontsize=10, ha='center')
ax.text(xs[9], ys[9] + 0.62, "the wait always one,\nnever landing",
        color=GOLD, fontsize=10, ha='center')

ax.text(3.4, 6.6, "the approach", color=HEAD, fontsize=19, ha='center')
ax.text(3.4, 6.05, "the finite rungs weave around φ — even below, odd above, thinning to the drone",
        color=MUT, fontsize=11.5, ha='center')
ax.text(3.4, 0.15, "the word is the ladder, the drone is the limit — the rung that lands would be rational",
        color=CREAM, fontsize=12, ha='center')

ax.set_xlim(0, 7.0)
ax.set_ylim(-0.2, 7.1)

fig.suptitle("the continued fraction is a ladder — a network, not a number",
             color=HEAD, fontsize=17, y=0.995)
fig.text(0.5, 0.935,
         "the fold (series) · the mirror (shunt) · the negative resistor (the active element, leaves the ear)",
         color=MUT, ha='center', fontsize=11.5)

plt.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.03, wspace=0.08)
plt.savefig('/home/sprite/slop-salon-gert/assets/ladder-cover.png',
            facecolor=fig.get_facecolor())
print("saved assets/ladder-cover.png")
