#!/usr/bin/env python3
"""the altitudes — mina's move, verified.

mina drew the three mirrors as the altitudes of the ideal triangle
{−1, ½, 2} and found them concurring at the incenter e^{iπ/3}:

  M  (s ↦ 1−s)   fixes the count's line  Re s = ½
  MT (s ↦ 1/s)   fixes the unit circle  — through −1
  TM (s ↦ s/(s−1)) fixes the circle centered 1 — through 2

Every claim checks exactly: e^{iπ/3} = ½ + i√3/2 lies on all three
(re ½, |s| = 1, |s−1| = 1), and each altitude carries its vertex —
½ on Re = ½, −1 on the unit circle, 2 on the circle through 2.  The
concurrence is no accident: the ideal triangle is hyperbolically
equilateral, so its orthocenter is its incenter, the unique point fixed
by all of S₃ — and each altitude is the geodesic through a vertex
orthogonal to the opposite side (each mirror circle is orthogonal to the
opposite side-arc: 1² + (3/4)² = (5/4)² = 1² + (3/4)²).

The hinge: the incenter e^{iπ/3} sits ON the count's line Re = ½.  The
odd reflections — the sign, the stereo ear — all hinge on a point of the
even line.  And it is the regulator's fixed point: the order-3 turn T
centers exactly there.  The sign anchors at the count; stereo's three
ears meet on mono's seam.

Left:  the altitude confluence (stereo).  The three mirrors drawn as the
       altitudes, concurring at the star e^{iπ/3} on the seam.
Right: the same triangle, folded to mono.  The odd altitudes vanish; the
       even turn T (the 120° rotation) centers at the same star, on the
       count's line.  Both ears meet at the same hinge.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

dark = "#0d0f14"
plt.rcParams.update({
    "figure.facecolor": dark, "axes.facecolor": dark,
    "text.color": "#e8e4da", "axes.edgecolor": "#4a4a55",
    "axes.labelcolor": "#e8e4da", "xtick.color": "#b8b3a8",
    "ytick.color": "#b8b3a8", "font.family": "serif", "font.size": 10,
})
teal = "#6fd6c3"; amber = "#e8b34b"; rose = "#e07a8a"; grey = "#8a8a97"
blue = "#7fa8d9"

E = 0.5 + 1j * np.sqrt(3) / 2   # the incenter e^{iπ/3}

def side_arc(ax, v1, v2, **kw):
    """upper semicircle geodesic between real-axis points v1, v2"""
    cx = (v1 + v2) / 2.0
    r = abs(v2 - v1) / 2.0
    th = np.linspace(0, np.pi, 200)
    ax.plot(cx + r * np.cos(th), r * np.sin(th), **kw)

def alt_arc(ax, center, radius, color, **kw):
    th = np.linspace(0, np.pi, 200)
    ax.plot(center + radius * np.cos(th), radius * np.sin(th),
            color=color, **kw)

def triangle_fill(ax):
    """shade the ideal triangle interior (closed loop of the three arcs)"""
    def pts(v1, v2):
        cx = (v1 + v2) / 2.0
        r = abs(v2 - v1) / 2.0
        th = np.linspace(0, np.pi, 120)
        return cx + r * np.cos(th), r * np.sin(th)
    xs, ys = [], []
    for a, b in [(-1, 0.5), (0.5, 2), (2, -1)]:
        x, y = pts(a, b)
        xs.append(x); ys.append(y)
    ax.fill(np.concatenate(xs), np.concatenate(ys), color="#2a3140",
            alpha=0.55, zorder=1)

def draw_triangle(ax, edges_lw=1.0):
    for a, b in [(-1, 0.5), (0.5, 2), (2, -1)]:
        side_arc(ax, a, b, color=grey, lw=edges_lw, alpha=0.55)

def draw_seats(ax, big=True):
    ms = 9 if big else 7
    for seat, name, color, mark in [(-1, "sign −1", amber, "x"),
                                    (2, "fifth 2", rose, "x"),
                                    (0.5, "count ½", teal, "o")]:
        ax.plot([seat], [0], marker=mark, ms=ms, mew=2, mfc=dark,
                color=color, zorder=6)
    for seat, name, color in [(-1, "sign −1\n(pole)", amber),
                              (2, "fifth 2\n(pole)", rose),
                              (0.5, "count ½\n(zero)", teal)]:
        ax.annotate(name, (seat, 0), xytext=(seat, -0.30), ha="center",
                    va="top", color=color, fontsize=8.5)

def draw_star(ax, label=True):
    ax.plot([E.real], [E.imag], marker="*", ms=16, color="#f0e68c",
            mfc="#f0e68c", mec="#0d0f14", zorder=8)
    if label:
        ax.annotate("e^{iπ/3}", (E.real, E.imag), xytext=(0.88, 1.30),
                    color="#f0e68c", fontsize=10.5, zorder=8)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.2, 5.8), dpi=160)
fig.suptitle("the altitudes — the three mirrors concur at the incenter, on the count's line",
             fontsize=12.5, color="#e8e4da", y=0.985)

# ============ left: the altitude confluence (stereo) ============
ax1.set_facecolor(dark)
ax1.set_xlim(-2.05, 2.85)
ax1.set_ylim(-0.55, 2.0)
ax1.axhline(0, color="#3a3a44", lw=0.8)
ax1.set_aspect("equal")
ax1.set_title("stereo — the odd reflections, heard", fontsize=10.5,
              color="#e8e4da")

triangle_fill(ax1)
draw_triangle(ax1)
draw_seats(ax1)

# the three altitudes = the mirrors, each carrying its vertex
ax1.axvline(0.5, color=teal, lw=2.4, zorder=4)                    # M: Re = 1/2
alt_arc(ax1, 0.0, 1.0, amber, lw=2.2, zorder=4)                   # MT: unit circle
alt_arc(ax1, 1.0, 1.0, rose, lw=2.2, zorder=4)                    # TM: circle c=1

# labels for the three altitudes
ax1.text(0.62, 1.78, "M: Re s = ½", color=teal, fontsize=9,
         rotation=90, va="top", ha="left")
ax1.annotate("MT: |s| = 1\nthrough −1", (-1, 0), xytext=(-1.95, 1.05),
             color=amber, fontsize=8.5)
ax1.annotate("TM: |s−1| = 1\nthrough 2", (2, 0), xytext=(2.0, 1.35),
             color=rose, fontsize=8.5, ha="center")

# the seam emphasized through the star
ax1.plot([0.5, 0.5], [0, 2.0], color=teal, lw=0.6, ls=":", alpha=0.5)
draw_star(ax1)

ax1.text(0.62, 0.28, "the sign's three ears\nhinge on the count's line",
         color=blue, fontsize=8.5, va="center")
ax1.set_xlabel("Re s", fontsize=11)
ax1.set_ylabel("Im s", fontsize=11)

# ============ right: folded to mono — the even turn at the same hinge ============
ax2.set_facecolor(dark)
ax2.set_xlim(-2.05, 2.85)
ax2.set_ylim(-0.55, 2.0)
ax2.axhline(0, color="#3a3a44", lw=0.8)
ax2.set_aspect("equal")
ax2.set_title("mono — the odd folds in, the turn centers at the same point",
              fontsize=10.5, color="#e8e4da")

triangle_fill(ax2)
draw_triangle(ax2, edges_lw=0.7)
draw_seats(ax2, big=False)

# the even turn T: the 120° rotation about e^{iπ/3} cycling ½ → −1 → 2 → ½
for v, c in [(0.5, teal), (-1, amber), (2, rose)]:
    r = np.hypot(v - E.real, 0 - E.imag)
    ang = np.angle((v - E.real) - 1j * E.imag)
    th = np.linspace(0, 2 * np.pi / 3, 100)
    x = E.real + r * np.cos(th + ang)
    y = E.imag + r * np.sin(th + ang)
    ax2.plot(x, y, color=c, lw=1.3, ls=":", alpha=0.9)

# the count's line drawn as the hinge
ax2.axvline(0.5, color=teal, lw=1.2, alpha=0.8, zorder=3)
draw_star(ax2)

ax2.text(0.62, 0.30, "fold to mono — the odd altitudes vanish;\nthe even turn T stays, centered at e^{iπ/3}\non the count's line",
         color=blue, fontsize=8.5, va="center")
ax2.text(0.95, 1.72, "T³ = id: ½ → −1 → 2 → ½", color=grey, fontsize=8.5)
ax2.set_xlabel("Re s", fontsize=11)
ax2.set_ylabel("Im s", fontsize=11)

fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig("assets/altitudes-cover.png", dpi=160, facecolor=dark,
            bbox_inches="tight")
print("saved assets/altitudes-cover.png")
