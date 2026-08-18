#!/usr/bin/env python3
"""ink-cover — the ink bleaches and keeps the where.

Three panels of ONE brushstroke. The stroke is the same in every panel — the
same curve, the same width profile, the same pooling and taper, the same
pressure — because the where stays. Only the palette bleaches: indigo to
madder to ochre at full colour, then the wash taking hold (colour draining
halfway to grey), then the same stroke in bare grey: shape intact, colour
gone. The geometry is pixel-identical across panels; the bleach is analytic
(each segment colour mixed toward its own luminance), so nothing moves and
only the quality drains. Inverted from smoke (the where became nowhere): ink
nails the where down and lets the quality go instead.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(20260818)

INK = (0.80, 0.86, 0.90)
BG = np.array([0.030, 0.030, 0.038])     # near-black paper

# colour stops along the stroke, arc-length s in [0,1]
STOPS = [(0.00, (0.13, 0.22, 0.48)),      # indigo
         (0.34, (0.55, 0.10, 0.13)),      # madder
         (0.68, (0.60, 0.32, 0.10)),      # sienna
         (1.00, (0.74, 0.46, 0.16))]      # ochre

def stroke_colour(s):
    s = np.clip(s, 0, 1)
    for (s0, c0), (s1, c1) in zip(STOPS[:-1], STOPS[1:]):
        if s0 <= s <= s1:
            u = (s - s0) / (s1 - s0)
            return (1 - u) * np.array(c0) + u * np.array(c1)
    return np.array(STOPS[-1][1])

def luminance(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]

def bleached(s, bleach):
    """The stroke colour at arc-length s, mixed bleach in [0,1] toward grey."""
    c = stroke_colour(s)
    if bleach > 0:
        L = luminance(c)
        c = (1 - bleach) * c + bleach * np.array([L, L, L])
    return c

def bezier(tt, P):
    P0, P1, P2, P3 = (np.array(p) for p in P)
    return ((1 - tt) ** 3)[:, None] * P0 + 3 * ((1 - tt) ** 2 * tt)[:, None] * P1 \
         + 3 * ((1 - tt) * tt ** 2)[:, None] * P2 + (tt ** 3)[:, None] * P3

# ---- main stroke: an S-curve, thick head, fine tail ----
P = [(0.20, 0.80), (0.32, 0.52), (0.62, 0.68), (0.86, 0.24)]
tt = np.linspace(0, 1, 420)
pts = bezier(tt, P)

def width_main(s):
    pressure = 1.0 + 0.7 * np.exp(-(s / 0.10) ** 2)    # the head pool
    return 0.11 * (1 - s) ** 1.35 * pressure + 0.0015
def dens_main(s):
    return 0.58 + 0.42 * (1 - s) ** 0.8                 # heavy head, dry tail

# ---- secondary flick: a thin counter-stroke off the body ----
P2 = [(0.44, 0.60), (0.58, 0.78), (0.74, 0.80), (0.90, 0.66)]
tt2 = np.linspace(0, 1, 240)
pts2 = bezier(tt2, P2)
def width_flick(s):
    return 0.026 * (1 - s) ** 1.6 + 0.002
def dens_flick(s):
    return 0.45 * (1 - s) ** 0.6

# droplets near the head: (x, y, r, coverage)
drops = [(0.105, 0.715, 0.016, 1.0), (0.138, 0.758, 0.011, 0.85),
         (0.088, 0.665, 0.009, 0.7), (0.150, 0.705, 0.006, 0.6)]

def ink_over_paper(c, cov):
    """semi-transparent ink composited analytically over the paper."""
    return cov * np.array(c) + (1 - cov) * BG

def draw_strokes(ax, bleach, lw_px):
    """The same strokes every time; only the palette bleaches."""
    for i in range(len(pts) - 1):
        s = tt[i]
        c = ink_over_paper(bleached(s, bleach), dens_main(s))
        ax.plot([pts[i, 0], pts[i + 1, 0]], [pts[i, 1], pts[i + 1, 1]],
                lw=width_main(s) * lw_px, color=c,
                solid_capstyle="round", solid_joinstyle="round")
    for i in range(len(pts2) - 1):
        s = tt2[i]
        c = ink_over_paper(bleached(0.55 + 0.45 * s, bleach), dens_flick(s))
        ax.plot([pts2[i, 0], pts2[i + 1, 0]], [pts2[i, 1], pts2[i + 1, 1]],
                lw=width_flick(s) * lw_px, color=c,
                solid_capstyle="round", solid_joinstyle="round")
    for (dx, dy, r, cov) in drops:
        c = ink_over_paper(bleached(0.06, bleach), cov)
        ax.add_patch(plt.Circle((dx, dy), r, color=c))

fig, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=110)
fig.patch.set_facecolor("#08080a")

# axes_px_per_data = panel width in inches * dpi  (panel is 6 in wide, data 0..1)
LW_PX = 6.0 * 110

panels = [(0.00, "the brush touches down", "full colour"),
          (0.55, "the wash", "colour draining"),
          (1.00, "the colour is gone", "the shape remains")]

for ax, (bleach, title, subt) in zip(axes, panels):
    draw_strokes(ax, bleach, LW_PX)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_facecolor("#08080a")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color((*INK, 0.30))
    ax.set_title(title, color=INK, fontsize=14, pad=8)
    ax.text(0.5, -0.05, subt, transform=ax.transAxes,
            color=(*INK, 0.55), fontsize=11, ha="center")

axes[2].text(0.5, 0.035, "the ink bleaches and keeps the where",
             transform=axes[2].transAxes, color=(*INK, 0.95), fontsize=13,
             ha="center", va="bottom")

plt.subplots_adjust(left=0.01, right=0.99, top=0.90, bottom=0.11, wspace=0.08)
plt.savefig("assets/ink-cover.png", facecolor=fig.get_facecolor())
print("saved assets/ink-cover.png")
