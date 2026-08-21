#!/usr/bin/env python3
"""mirror-fixed-cover — the fixed point of the reflection.

The residue register's last move, made visible. The critical line
Re(s)=1/2 is the mirror: the reflection ρ → 1−ρ̄ sends a pole off the
line to its twin, and the pair cancels in the mirror sum — two states,
one pitch. On the line a pole is its own reflection: the fixed point,
self-conjugate, count one — the mode no symmetry doubles.

The zeros on the mirror (computed, first seven) are the room's ringing
points. One phantom pair off the line shows what a broken symmetry
would look like: two dim poles at ±β, joined by the dashed tie of the
2-cycle, collapsing to a hollow seat where the tie crosses the mirror.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from scipy.special import loggamma
from scipy.optimize import brentq

# ---- zeta zeros on the critical line (Van Wijngaarden-accelerated η) ----
def vw(partial, conv=512):
    b = partial[:conv].copy()
    while len(b) > 1:
        b = 0.5 * (b[:-1] + b[1:])
    return b[0]

def zeta(s, terms=12000, conv=512):
    n = np.arange(1, terms + 1)
    a = (-1.0) ** (n - 1) * n ** (-s)
    return vw(np.cumsum(a), conv) / (1 - 2 ** (1 - s))

def theta(t):
    return np.imag(loggamma(0.25 + 0.5j * t)) - 0.5 * t * np.log(np.pi)

def Z(t):
    return np.real(np.exp(1j * theta(t)) * zeta(0.5 + 1j * t))

ts = np.linspace(12, 46, 3000)
vals = np.array([Z(t) for t in ts])
ZEROS = []
for i in range(len(ts) - 1):
    if vals[i] * vals[i + 1] < 0:
        try:
            ZEROS.append(brentq(Z, ts[i], ts[i + 1]))
        except ValueError:
            pass
    if len(ZEROS) >= 7:
        break

fig, ax = plt.subplots(figsize=(6.4, 9.0), dpi=150)
fig.patch.set_facecolor("#0b0b0f")
ax.set_facecolor("#0b0b0f")

GOLD = (0.88, 0.70, 0.36)
PALE = (0.95, 0.90, 0.75)
ROSE = (0.76, 0.35, 0.31)
ASH = (0.55, 0.62, 0.70)

Y0, Y1 = 12.5, 45.0
X0, X1 = -1.55, 1.55
ax.set_xlim(X0, X1)
ax.set_ylim(Y0, Y1)

# pixel scale per data unit (used to draw rings circular despite auto aspect)
XS = (fig.get_size_inches()[0] * fig.dpi) / (X1 - X0)   # px per x-unit
YS = (fig.get_size_inches()[1] * fig.dpi) / (Y1 - Y0)   # px per y-unit

def circle(center, r_px, **kw):
    """A ring of pixel-radius r_px, drawn as an Ellipse (circular on screen)."""
    w = 2 * r_px / XS      # width in x-data units
    h = 2 * r_px / YS      # height in y-data units
    return Ellipse(center, w, h, fill=False, **kw)

# ---- the mirror: Re(s) = 1/2, the reflection's fixed set ------------------
ax.plot([0, 0], [Y0, Y1], color=GOLD, lw=2.2, alpha=0.9, zorder=2)
ax.plot([0, 0], [Y0 - 2.0, Y0], color=GOLD, lw=1.0, alpha=0.25)
ax.plot([0, 0], [Y1, Y1 + 2.0], color=GOLD, lw=1.0, alpha=0.25)

# ---- the room's ring at each pole: faint concentric rings (the shed ring) --
for tz in ZEROS:
    for r_px in [14, 30, 52]:
        ax.add_patch(circle((0, tz), r_px, color=GOLD,
                            alpha=0.12 - 0.03 * (r_px > 22), lw=0.9, zorder=1))

# ---- the self-conjugate zeros: each its own mirror -------------------------
for tz in ZEROS:
    ax.plot([0], [tz], 'o', ms=8, color=PALE, zorder=6)
    ax.plot([0], [tz], 'o', ms=13, color=GOLD, alpha=0.35, zorder=5)
    # the reflection mark: it maps to itself — a short double arrow
    ax.annotate("", xy=(0.16, tz), xytext=(-0.16, tz),
                arrowprops=dict(arrowstyle="<->", color=GOLD, alpha=0.4, lw=0.9),
                zorder=4)

# ---- the phantom pair: off the mirror, the 2-cycle that would cancel -------
TP = 27.9          # a height between zeros
BETA = 0.42        # how far off the mirror
for sx in (-1, 1):
    ax.plot([sx * BETA], [TP], 'o', ms=7, color=ASH, alpha=0.8, zorder=5)
    ax.plot([sx * BETA], [TP], 'o', ms=12, color=ASH, alpha=0.25, zorder=4)
ax.plot([-BETA, BETA], [TP, TP], color=ASH, alpha=0.55, lw=1.1,
        ls=(0, (4, 3)), zorder=3)
# the seat: where the tie crosses the mirror — the fixed point it collapses to
ax.add_patch(circle((0, TP), 15, color=ROSE, alpha=0.85, lw=1.6, zorder=6))
ax.plot([0], [TP], '+', ms=9, color=ROSE, alpha=0.9, zorder=6)

# ---- faint vertical guides through the pair (each holds its height) --------
for sx in (-1, 1):
    ax.plot([sx * BETA, sx * BETA], [Y0, Y1], color=ASH, alpha=0.07, lw=0.8)

ax.axis("off")
fig.tight_layout(pad=0)
fig.savefig("assets/mirror-fixed-cover.png", dpi=150, facecolor=fig.get_facecolor())
print("saved assets/mirror-fixed-cover.png")
print("zeros:", [round(z, 4) for z in ZEROS])
print("xscale %.1f px/unit, yscale %.1f px/unit" % (XS, YS))
