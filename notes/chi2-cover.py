#!/usr/bin/env python3
"""χ₂ heard — the winding the parity can't read.

S₃ on the seats {−1, ½, 2}.  The sign character (the fold, mono/diff) reads the
parity: even {e, T, T²} in phase, odd {R, RT, TR} anti-phase.  The parity never
hears the regulator — every even permutation is +1 to both 1-dim characters, so
the fold cannot tell e from T from T².

The 2-dim character χ₂ tells them apart, as a winding.  In the standard rep the
regulator is a rotation by 120° (trace −1), the mirror a reflection (trace 0).
χ₂ is a stereo pair: the two outer seats {−1, 2} = {55, 440} are the channels.
Fold to mono = project onto the shore (the mirror's +1 line) — the count; the
difference is the mirror's −1 line — the where.  A transposition (trace 0) rings
in the difference: mono can't hear it.  A 3-cycle is a rotation: it winds the
count's in-phase image into the difference — the mono loses half (χ₂ = −1), the
diff gains the winding.

Left: the χ₂ plane.  The mono line (the shore) and the diff line (the where);
the identity's placement in phase; the two 3-cycles wound to 120° and 240°; the
mirror as a reflection flipping the diff.  Right: the character table — χ₂
vanishes on the mirrors and reads −1 on the regulator.

And [R, T] = T: the commutator of two mirrors is the regulator.  The commutator
subgroup A₃ is exactly the even rotations — the winding is born of folds, and
the parity (trivial on commutators) never reaches it.  stereo reads it, mono
can't.
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.2, 5.6), dpi=160)
fig.suptitle("χ₂ heard — the winding the parity can't read",
             fontsize=13, color="#e8e4da", y=0.985)

# ---- left: the χ₂ plane -------------------------------------------------------
ax1.set_facecolor(dark)
ax1.set_xlim(-2.1, 2.1)
ax1.set_ylim(-2.1, 2.1)
ax1.axhline(0, color="#3a3a44", lw=0.8)
ax1.axvline(0, color="#3a3a44", lw=0.8)
ax1.set_aspect("equal")

# the two read-lines: mono (shore) and diff (where)
ax1.plot([-2, 2], [-2, 2], color=amber, lw=1.6, ls=(0, (5, 3)), alpha=0.8)
ax1.plot([-2, 2], [2, -2], color=teal, lw=1.6, ls=(0, (5, 3)), alpha=0.8)
ax1.text(2.05, 1.95, "mono — the shore, the count", color=amber, fontsize=9,
         ha="right", va="top", rotation=-45)
ax1.text(-1.95, 1.55, "diff — the where, the winding", color=teal, fontsize=9,
         ha="left", va="top", rotation=45)

# the placements of the pair under each deck
pts = {
    "e":  (1.0, 1.0, amber, "e  in phase\nχ₂ = +2"),
    "T":  (-0.5, -0.866, teal, "T  wound 120°\nχ₂ = −1"),
    "T2": (-0.5, 0.866, teal, "T²  wound 240°\nχ₂ = −1"),
    "R":  (-1.0, 1.0, rose, "R  the mirror\nχ₂ = 0"),
}
for k, (x, y, col, lab) in pts.items():
    ax1.plot(x, y, "o", color=col, ms=13, mec=dark, mew=1.5, zorder=5)
    ax1.text(x * 1.28, y * 1.28, lab, color=col, fontsize=8.6,
             ha="center", va="center", linespacing=1.25)

# the winding: arcs from in-phase to the two rotations
def arc(a1, a2, col, rad=1.05):
    th = np.linspace(a1, a2, 40)
    x, y = rad * np.cos(th), rad * np.sin(th)
    ax1.plot(x, y, color=col, lw=1.5)
    # arrowhead
    dx, dy = x[-1] - x[-2], y[-1] - y[-2]
    ax1.annotate("", xy=(x[-1], y[-1]), xytext=(x[-2], y[-2]),
                 arrowprops=dict(arrowstyle="-|>", color=col, lw=1.5))

arc(np.pi / 4, np.pi + np.arctan(0.866 / 0.5), teal)     # (1,1) -> (-0.5,-0.866)
arc(np.pi / 4, np.pi - np.arctan(0.866 / 0.5), teal)     # (1,1) -> (-0.5,+0.866)
ax1.text(0.05, -1.9, "the regulator winds the pair — the count leaks into the where",
         color=grey, fontsize=8.6, ha="center")

# the mirror: reflection of the diff placement across the mono line
ax1.annotate("", xy=(1.0, -1.0), xytext=(-1.0, 1.0),
             arrowprops=dict(arrowstyle="<->", color=rose, lw=1.3,
                             linestyle=(0, (3, 3)), alpha=0.7))
ax1.text(0.0, -1.05, "mirror: the flip — trace 0, mono can't hear it",
         color=rose, fontsize=8.4, ha="center")

ax1.set_xticks([]); ax1.set_yticks([])
ax1.set_title("χ₂ — the stereo pair", color="#e8e4da", fontsize=11.5, pad=10)

# ---- right: the character table ----------------------------------------------
ax2.set_facecolor(dark)
ax2.axis("off")
ax2.set_xlim(0, 10)
ax2.set_ylim(-3.0, 10)

cols = ["e", "T", "T²", "R", "RT", "TR"]
parity = {"e": 1, "T": 1, "T2": 1, "R": -1, "RT": -1, "TR": -1}
chi2 = {"e": 2, "T": -1, "T2": -1, "R": 0, "RT": 0, "TR": 0}
x0, x1 = 3.0, 9.6
y0, y1 = 2.0, 6.4
dx = (x1 - x0) / 6.0

ax2.text((x0 + x1) / 2, 9.3, "the character table — the fold, and χ₂",
         fontsize=11, color="#e8e4da", ha="center")

rows = [("χ₀  trivial — the count, the drone, mono", amber, [1, 1, 1, 1, 1, 1]),
        ("χ₁  sign — the parity, the difference", rose, [1, 1, 1, -1, -1, -1]),
        ("χ₂  standard — the winding, stereo", teal, [2, -1, -1, 0, 0, 0])]
evens = {"e", "T", "T²"}
for i, c in enumerate(cols):
    cx = x0 + dx * (i + 0.5)
    ax2.text(cx, 7.2, c, color=amber if c in evens else rose,
             fontsize=11, ha="center", fontweight="bold")
for r, (rn, rcol, vals) in enumerate(rows):
    ry = y1 - dx * (r + 0.6)
    ax2.text(x0 - 0.1, ry, rn, color=rcol, fontsize=9.2, ha="right", va="center")
    for i, c in enumerate(cols):
        cx = x0 + dx * (i + 0.5)
        key = {"T²": "T2"}.get(c, c)
        val = vals[["e", "T", "T2", "R", "RT", "TR"].index(key)]
        tcol = "#e8e4da" if val >= 0 else rose
        ax2.text(cx, ry, f"{val:+d}" if val else "0", color=tcol,
                 fontsize=10.5, ha="center", va="center")

# the readings
notes = [
    ("the parity gives every even permutation +1 — the fold can't tell e from T from T².",
     grey),
    ("χ₂(T) = −1: the regulator is a rotation, a winding. the count leaks half, the diff reads the rest.",
     teal),
    ("χ₂(R) = 0: the mirror is mono-invisible. a transposition rings only in the difference.",
     rose),
    ("[R, T] = T: the commutator of two mirrors is the regulator. [S₃, S₃] = A₃ — the winding is born of folds, the parity never reaches it.",
     amber),
]
yy = 1.7
for txt, col in notes:
    ax2.text(0.35, yy, txt, color=col, fontsize=8.6, ha="left", va="top", linespacing=1.4)
    yy -= 1.15

fig.tight_layout(rect=(0, 0.015, 1, 0.96))
fig.savefig("assets/chi2-cover.png", dpi=160)
print("wrote assets/chi2-cover.png")
