#!/usr/bin/env python3
"""the triangle, heard — the deck's six moves and the count never blinks.

Left: the ideal triangle {−1, ½, 2} in the upper half-plane — three geodesic
semicircles, area exactly π.  The count ½ is the seat the mirror fixes; the sign
−1 and the fifth 2 are the pair the mirror swaps.  The seam (Re = ½, dashed) is
a geodesic after all; the order-3 point e^{iπ/3} sits on it, the axis of the
regulator's 120° turn.  T cycles ½ → −1 → 2 → ½.

Right: the deck as sound.  The three seats become three tones, one geometric
series: ½ → 155.6 Hz (the count), −1 → 55 Hz, 2 → 440 Hz.  The deck's six
permutations move the tones around the stereo field, but every position keeps
L+R = 1 — so the mono sum is one fixed chord under every move (χ_perm = χ₀ + χ₂:
the sum is the trivial rep, the count).  The winding lives in the stereo: read
L−R and the deck moves.  mono is the count; the count never blinks.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Arc
from matplotlib.path import Path

dark = "#0d0f14"
plt.rcParams.update({
    "figure.facecolor": dark, "axes.facecolor": dark,
    "text.color": "#e8e4da", "axes.edgecolor": "#4a4a55",
    "axes.labelcolor": "#e8e4da", "xtick.color": "#b8b3a8",
    "ytick.color": "#b8b3a8", "font.family": "serif", "font.size": 10,
})
teal = "#6fd6c3"; amber = "#e8b34b"; rose = "#e07a8a"; grey = "#8a8a97"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.2, 5.6), dpi=160)
fig.suptitle("the triangle, heard — the deck's six moves, and the count never blinks",
             fontsize=12.5, color="#e8e4da", y=0.985)

# ---- left: the ideal triangle --------------------------------------------------
ax1.set_facecolor(dark)
ax1.set_xlim(-2.4, 3.0)
ax1.set_ylim(-0.35, 2.0)
ax1.axhline(0, color="#3a3a44", lw=0.8)
ax1.set_aspect("equal")

def semi(cx, r, a, b):
    th = np.linspace(a, b, 120)
    return cx + r * np.cos(th), r * np.sin(th)

def arc_pts(v1, v2):
    cx = (v1 + v2) / 2.0; r = (v2 - v1) / 2.0
    return cx, r

# boundary path: arc(−1→½), arc(½→2), arc(2→−1)
def arc_path(cx, r, a0, a1):
    th = np.linspace(a0, a1, 120)
    return np.column_stack([cx + r * np.cos(th), r * np.sin(th)])

seg1 = arc_path(*arc_pts(-1.0, 0.5), np.pi, 0.0)
seg2 = arc_path(*arc_pts(0.5, 2.0), np.pi, 0.0)
seg3 = arc_path(*arc_pts(-1.0, 2.0), 0.0, np.pi)     # the top arc, back to −1
pts = np.vstack([seg1, seg2, seg3])
path = Path(pts, closed=True)
ax1.add_patch(PathPatch(path, facecolor="#1a2233", edgecolor="none", zorder=1))
ax1.add_patch(PathPatch(Path(pts, closed=True), facecolor="none",
                        edgecolor=teal, lw=1.8, zorder=3))

# the three vertices
verts = {"−1": (-1.0, rose, "sign"), "½": (0.5, amber, "count"), "2": (2.0, rose, "fifth")}
for lab, (x, col, name) in verts.items():
    ax1.plot(x, 0, "o", color=col, ms=12, mec=dark, mew=1.5, zorder=5)
    ax1.text(x, -0.16, f"{lab}\n{name}", color=col, fontsize=9.5,
             ha="center", va="top", linespacing=1.2, zorder=6)

# the seam and the order-3 point
ax1.plot([0.5, 0.5], [0.0, 1.62], color=amber, lw=1.4, ls=(0, (4, 3)), alpha=0.85)
ax1.text(0.5, 1.70, "the seam — Re = ½, a geodesic", color=amber, fontsize=8.4,
         ha="center", va="bottom")
cx0, cy0 = 0.5, np.sqrt(3) / 2
ax1.plot(cx0, cy0, "o", color=amber, ms=8, mec=dark, mew=1.2, zorder=6)
ax1.text(cx0 + 0.16, cy0 + 0.06, "e^{iπ/3}", color=amber, fontsize=9, ha="left")

# the 120° turn about e^{iπ/3}
arc = Arc((cx0, cy0), 0.55, 0.55, angle=0, theta1=10, theta2=130,
          color=teal, lw=1.6, zorder=4)
ax1.add_patch(arc)
ax1.annotate("", xy=(cx0 + 0.275 * np.cos(np.radians(130)),
                     cy0 + 0.275 * np.sin(np.radians(130))),
             xytext=(cx0 + 0.275 * np.cos(np.radians(120)),
                     cy0 + 0.275 * np.sin(np.radians(120))),
             arrowprops=dict(arrowstyle="-|>", color=teal, lw=1.4), zorder=4)
ax1.text(cx0 - 0.34, cy0 + 0.32, "the turn\n120°, T(s) = (s−1)/s", color=teal,
         fontsize=8.2, ha="center", linespacing=1.25)

# the orbit of the three seats
ax1.text(0.55, 0.35, "½ → −1 → 2 → ½", color=grey, fontsize=8.6, ha="center")
ax1.text(-2.35, 1.75, "area = π", color=grey, fontsize=9.5, ha="left")

ax1.set_xticks([]); ax1.set_yticks([])
ax1.set_title("the ideal triangle {−1, ½, 2}", color="#e8e4da", fontsize=11.5, pad=8)

# ---- right: the deck as sound, χ_perm = χ₀ + χ₂ -------------------------------
ax2.set_facecolor(dark)
ax2.axis("off")
ax2.set_xlim(0, 10)
ax2.set_ylim(-1.4, 10)

ax2.text(5.0, 9.6, "the three seats, as three tones — one geometric series",
         fontsize=10.5, color="#e8e4da", ha="center")

# tone map on a log-frequency axis
tone_y = {"−1 sign": (55.0, rose), "½ count": (155.6, amber), "2 fifth": (440.0, rose)}
fmin, fmax = 40.0, 1000.0
def fy(f): return 3.0 + 4.5 * (np.log(f / fmin) / np.log(fmax / fmin))
for lab, (f, col) in tone_y.items():
    y = fy(f)
    ax2.plot([1.2, 8.8], [y, y], color="#2a2a34", lw=0.7)
    ax2.plot(2.4, y, "o", color=col, ms=11, mec=dark, mew=1.4, zorder=5)
    ax2.text(3.0, y + 0.12, f"{f:.0f} Hz  —  {lab}", color=col, fontsize=9, va="bottom")
    ax2.text(2.4, y - 0.22, "110·2^s", color=grey, fontsize=7.6, ha="center", va="top")
ax2.text(1.2, 1.55, "count = the geometric mean √(55·440)", color=grey, fontsize=8.2)

# the character table: χ_perm = χ₀ + χ₂
x0, x1 = 3.0, 9.6
y0, y1 = 6.4, 8.1
cols = ["e", "T", "T²", "M", "fix−1", "fix2"]
dx = (x1 - x0) / 6.0
ax2.text(5.0, 8.75, "the six moves — the sum is invariant", color=amber,
         fontsize=10.2, ha="center")
for i, c in enumerate(cols):
    cx = x0 + dx * (i + 0.5)
    ax2.text(cx, y1 + 0.28, c, color=teal, fontsize=9.2, ha="center")
rows = [("χ_perm  sum the three", grey, [3, 0, 0, 1, 1, 1]),
        ("χ₀  trivial — the count", amber, [1, 1, 1, 1, 1, 1]),
        ("χ₂  standard — the winding", teal, [2, -1, -1, 0, 0, 0])]
for r, (rn, rcol, vals) in enumerate(rows):
    ry = y1 - dx * (r + 0.62)
    ax2.text(x0 - 0.1, ry, rn, color=rcol, fontsize=8.6, ha="right", va="center")
    for i, v in enumerate(vals):
        cx = x0 + dx * (i + 0.5)
        tcol = "#e8e4da" if v >= 0 else rose
        ax2.text(cx, ry, f"{v:+d}" if v else "0", color=tcol, fontsize=9.6,
                 ha="center", va="center")
ax2.text(5.0, 5.55, "χ_perm = χ₀ + χ₂  —  sum to the count, leftover the winding",
         color=grey, fontsize=8.8, ha="center")

notes = [
    ("every position keeps L+R = 1 — so the mono sum is ONE fixed chord under all six moves. the count never hears the deck.",
     amber),
    ("the winding lives in the stereo: read L−R and the deck moves — the turn cycles the three, the mirror swaps sign and fifth.",
     teal),
    ("intro: the three tones centred — the count, pure. the deck runs. fold back to centre: it is the same chord.",
     rose),
    ("the seam is a geodesic after all.", grey),
]
yy = 4.7
for txt, col in notes:
    ax2.text(0.35, yy, txt, color=col, fontsize=8.6, ha="left", va="top", linespacing=1.4)
    yy -= 1.25

fig.tight_layout(rect=(0, 0.015, 1, 0.96))
fig.savefig("assets/triangle-cover.png", dpi=160)
print("wrote assets/triangle-cover.png")
