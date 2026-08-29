#!/usr/bin/env python3
"""the reflection's seats — the product's singularities are the triangle's vertices.

mina drew the three seats {−1, ½, 2} as an ideal triangle, area π.  The raw
reflection product φ(s)φ(1−s) = (2s−1)cot(πs)/(2π) is elementary, and its
singularities sit exactly ON the seats:

  s = ½  (the count)  → a DOUBLE ZERO — the two mirror voices meet there
  s = −1 (the sign)   → a POLE         (the trivial zero ζ(−2) of the denominator)
  s = 2  (the fifth)  → a POLE         (the mirror pole, φ(1−s) at 1−s = −1)

And on the whole strip 0 < s < 1 the product is NEGATIVE — φ(s) and φ(1−s)
never share a side of zero (verified: sign opposite at every s ≠ ½).  They
cross only at the count's seat, where the product bounces off zero from below
(order 2: φ(½+ε) ≈ −ε²·(1/π)).  The quarter-seats ¼ and ¾ are the shallowest
points, value exactly −1/(4π).  The reflection's −1 is all the way in.

Left:  the product on the real axis, poles clipped.  The strip is shaded; the
       graph lives below zero there and touches only at ½ — the two voices
       never share a side.  The seats are the triangle's vertices.
Right: the ideal triangle in the upper half-plane.  Vertices = the seats:
       poles at the sign and the fifth, the double zero at the count.  The
       deck T rotates the triangle 120° about e^{iπ/3}, on the seam.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

dark = "#0d0f14"
plt.rcParams.update({
    "figure.facecolor": dark, "axes.facecolor": dark,
    "text.color": "#e8e4da", "axes.edgecolor": "#4a4a55",
    "axes.labelcolor": "#e8e4da", "xtick.color": "#b8b3a8",
    "ytick.color": "#b8b3a8", "font.family": "serif", "font.size": 10,
})
teal = "#6fd6c3"; amber = "#e8b34b"; rose = "#e07a8a"; grey = "#8a8a97"
blue = "#7fa8d9"

def prod(s):
    return (2 * s - 1) * 1.0 / np.tan(np.pi * s) / (2 * np.pi)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.2, 5.6), dpi=160)
fig.suptitle("the reflection's seats — the product's poles and zero are the triangle's vertices",
             fontsize=12.5, color="#e8e4da", y=0.985)

# ---- left: the reflection product ---------------------------------------------
ax1.set_facecolor(dark)
ax1.set_xlim(-2.6, 3.1)
ax1.set_ylim(-2.6, 2.6)
ax1.axhline(0, color="#3a3a44", lw=0.8)
ax1.axvline(0, color="#3a3a44", lw=0.8)

# the strip 0<s<1 shaded
ax1.axvspan(0, 1, color=blue, alpha=0.07, zorder=0)

s = np.linspace(-2.6, 3.1, 20001)
# skip exact integers (poles)
mask = np.ones_like(s, dtype=bool)
for k in range(-3, 4):
    mask &= np.abs(s - k) > 1e-6
y = prod(s[mask])
yclip = np.clip(y, -2.6, 2.6)
ax1.plot(s[mask], yclip, color=teal, lw=1.4, zorder=3)

# pole marks
for seat, name, color in [(-1, "sign −1", amber), (2, "fifth 2", rose)]:
    ax1.plot([seat], [0], marker="x", ms=9, mew=2, color=color, zorder=5)
    ax1.annotate(name, (seat, 0), xytext=(seat, -0.45), ha="center",
                 color=color, fontsize=10)
    ax1.plot([seat], [2.45], marker="^", ms=7, color=color, zorder=4)
    ax1.text(seat, 2.35, "pole", ha="center", va="bottom", color=color, fontsize=8)

# the double zero at 1/2
half = 0.5
ax1.plot([half], [0], marker="o", ms=7, mfc=dark, mew=2, color=teal, zorder=5)
ax1.annotate("count ½", (half, 0), xytext=(half, -0.45), ha="center",
             color=teal, fontsize=10)
ax1.plot([half], [2.45], marker="v", ms=7, color=teal, zorder=4)
ax1.text(half, 2.35, "double zero", ha="center", va="bottom", color=teal, fontsize=8)

# quarter seats
for q in [0.25, 0.75]:
    ax1.plot([q], [prod(q)], marker="o", ms=5, mfc=dark, mew=1.5, color=grey, zorder=5)
ax1.annotate("−1/4π", (0.25, prod(0.25)), xytext=(0.15, -1.55), color=grey, fontsize=8.5)
ax1.annotate("−1/4π", (0.75, prod(0.75)), xytext=(0.9, -1.55), color=grey, fontsize=8.5)

# the "never shares a side of zero" label in the strip
ax1.text(0.5, 1.55, "negative throughout the strip", ha="center", color=blue,
         fontsize=9, alpha=0.9)
ax1.text(0.5, 1.25, "φ(s) and φ(1−s) never share a side of zero", ha="center",
         color=blue, fontsize=8, alpha=0.8)

ax1.set_xlabel("s", fontsize=11)
ax1.set_ylabel("φ(s)·φ(1−s) = (2s−1)·cot(πs)/(2π)", fontsize=9)
ax1.set_title("the reflection product — its zero is the count's seat",
              fontsize=10.5, color="#e8e4da")

# inset: the strip, zoomed — the negative valley with the double zero at 1/2
axin = ax1.inset_axes([0.10, 0.62, 0.34, 0.30])
axin.set_facecolor(dark)
s_in = np.linspace(0.01, 0.99, 2001)
axin.plot(s_in, prod(s_in), color=teal, lw=1.6)
axin.axhline(0, color="#3a3a44", lw=0.7)
axin.axvline(0.5, color=teal, lw=0.7, ls="--", alpha=0.5)
axin.plot([0.5], [0], marker="o", ms=5, mfc=dark, mew=1.5, color=teal)
for q in [0.25, 0.75]:
    axin.plot([q], [prod(q)], marker="o", ms=4, mfc=dark, mew=1.2, color=grey)
axin.set_xlim(0, 1)
axin.set_ylim(-0.42, 0.06)
axin.tick_params(labelsize=6.5, colors="#b8b3a8")
axin.text(0.5, -0.34, "−1/4π at ¼ and ¾", ha="center", color=grey, fontsize=7)
axin.text(0.5, 0.03, "zero at ½", ha="center", color=teal, fontsize=7, va="bottom")
axin.set_title("the strip, zoomed", fontsize=8, color="#b8b3a8", pad=2)

# ---- right: the ideal triangle -------------------------------------------------
ax2.set_facecolor(dark)
ax2.set_xlim(-2.0, 2.8)
ax2.set_ylim(-0.4, 1.9)
ax2.axhline(0, color="#3a3a44", lw=0.8)
ax2.set_aspect("equal")
ax2.set_title("the ideal triangle — vertices are the seats", fontsize=10.5,
              color="#e8e4da")

def geodesic(ax, v1, v2, color, lw=2.2, ls="-"):
    cx = (v1 + v2) / 2.0
    r = abs(v2 - v1) / 2.0
    th = np.linspace(-np.pi / 2, np.pi / 2, 200)
    if v1 > v2:
        th = np.linspace(np.pi / 2, 3 * np.pi / 2, 200)
    x = cx + r * np.cos(th)
    yy = np.abs(r * np.sin(th))
    ax.plot(x, yy, color=color, lw=lw, ls=ls, zorder=3)

# the three edges of the ideal triangle
geodesic(ax2, -1, 2, amber, lw=1.0)
geodesic(ax2, -1, 0.5, teal, lw=2.2)
geodesic(ax2, 0.5, 2, rose, lw=2.2)

# vertices = the seats
for seat, name, color, mark in [(-1, "sign −1\n(pole)", amber, "x"),
                                (2, "fifth 2\n(pole)", rose, "x"),
                                (0.5, "count ½\n(double zero)", teal, "o")]:
    ax2.plot([seat], [0], marker=mark, ms=9, mew=2, mfc=dark, color=color, zorder=5)
    ax2.annotate(name, (seat, 0), xytext=(seat, -0.30), ha="center",
                 va="top", color=color, fontsize=9)

# the seam Re = 1/2
ax2.axvline(0.5, color=teal, lw=0.7, ls="--", alpha=0.6)

# the order-3 point e^{iπ/3} — the deck's axis, the phantom center
e = (0.5, np.sqrt(3) / 2)
ax2.plot([e[0]], [e[1]], marker="*", ms=13, color=amber, zorder=6)
ax2.annotate("e^{iπ/3}", e, xytext=(0.78, 1.28), color=amber, fontsize=10)

# the deck T: the 120° turn about e^{iπ/3}, cycling the vertices
for v, c in [(0.5, teal), (-1, amber), (2, rose)]:
    th = np.linspace(0, 2 * np.pi / 3, 80)
    r = np.hypot(v - e[0], 0 - e[1])
    x = e[0] + r * np.cos(th + np.angle((v - e[0]) - 1j * e[1]))
    y = e[1] + r * np.sin(th + np.angle((v - e[0]) - 1j * e[1]))
    ax2.plot(x, y, color=c, lw=0.9, ls=":", alpha=0.85)

ax2.set_xlabel("Re s", fontsize=11)
ax2.set_ylabel("Im s", fontsize=11)

fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig("assets/reflection-seats-cover.png", dpi=160, facecolor=dark,
            bbox_inches="tight")
print("saved assets/reflection-seats-cover.png")
