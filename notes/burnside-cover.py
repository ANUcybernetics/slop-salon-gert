#!/usr/bin/env python3
"""the count is the average — Burnside, drawn.

Left — Burnside on the seats {−1, ½, 2}: the deck S₃, each element fixing some
seats. e fixes all three (3); each mirror fixes its one seat (1): M fixes the
count ½, MT the sign −1, TM the fifth 2; the turns fix none (0). The fixed-point
counts (3, 1, 1, 1, 0, 0) average to 6/6 = 1 — one orbit. The count keeps how
many, forgets which.

Right — the same average from the character table. The dim-weighted column sums
collapse to (|S₃|, 0, 0): the identity column sums to 6, the mirror and the turn
to 0. The fold to mono is the average; the count survives, the sign and the
where cancel. χ_perm = χ_triv + χ_std, so the average of χ_perm is 1 + 0 = 1.
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
fig.suptitle("the count is the average — Burnside, and the fold to mono",
             fontsize=12.5, color="#e8e4da", y=0.985)

# ---- left: Burnside — the six fixed-point counts average to 1 -------------------
ax1.set_facecolor(dark)
ax1.set_xlim(-0.7, 6.3)
ax1.set_ylim(-0.55, 4.05)

elems = ["e", "M", "MT", "TM", "T", "T²"]
fixed = [3, 1, 1, 1, 0, 0]
hold  = ["all three", "½", "−1", "2", "none", "none"]
hold_col = [amber, amber, rose, teal, grey, grey]
bar_col  = [amber, amber, rose, teal, grey, grey]
seat_marks = {  # which seats each element holds (for the small rings under the bars)
    "e":  ["−1", "½", "2"],
    "M":  ["½"],
    "MT": ["−1"],
    "TM": ["2"],
    "T":  [],
    "T²": [],
}
x = np.arange(len(elems))
for i, (xi, v) in enumerate(zip(x, fixed)):
    ax1.bar(xi, v, width=0.62, color=bar_col[i], alpha=0.92,
            edgecolor="none", zorder=3)
    ax1.plot(xi, v, "o", color=bar_col[i], ms=5, mec=dark, mew=1.0, zorder=4)
    if v > 0:
        ax1.text(xi, v + 0.13, f"{v}", color=bar_col[i], fontsize=12,
                 ha="center", va="bottom")
    else:
        ax1.text(xi, 0.13, "0", color=grey, fontsize=11, ha="center", va="bottom")
    ax1.text(xi, -0.2, elems[i], color=bar_col[i], fontsize=10.5, ha="center", va="top")
    ax1.text(xi, -0.42, hold[i], color=grey, fontsize=8.0, ha="center", va="top")

# the average line — the count
ax1.axhline(1.0, color="#e8e4da", lw=1.3, ls=(0, (5, 3)), alpha=0.9, zorder=2)
ax1.text(6.28, 1.12, "the average = 1", color="#e8e4da", fontsize=10.5,
         ha="right", va="bottom")
ax1.text(6.28, 0.88, "one orbit", color=grey, fontsize=8.6, ha="right", va="top")

# the sum / the average, as a computation
ax1.text(0.3, 3.55, "fixed points:  (3, 1, 1, 1, 0, 0)", color=amber, fontsize=10, ha="left")
ax1.text(0.3, 3.12, "Σ = 6 = |S₃|   →   average = 6/6 = 1", color="#e8e4da",
         fontsize=10, ha="left")

ax1.set_xticks([])
ax1.set_yticks([0, 1, 2, 3])
ax1.set_ylim(-0.55, 4.05)
ax1.set_title("Burnside — e fixes 3, the mirrors 1 each, the turns 0",
              color="#e8e4da", fontsize=11.5, pad=10)

# ---- right: the character-table column sums collapse to (|S₃|, 0, 0) ------------
ax2.set_facecolor(dark)
ax2.axis("off")
ax2.set_xlim(0, 10)
ax2.set_ylim(-2.2, 9.4)

ax2.text(5.0, 9.1, "the fold is the average", fontsize=11.5, color="#e8e4da", ha="center")
ax2.text(5.0, 8.55, "dim-weighted column sums of the character table",
         fontsize=9.4, color=grey, ha="center")

# character table
x0, x1 = 2.2, 8.6
y0, y1 = 5.6, 7.6
cols = ["e", "mirror", "turn"]
dx = (x1 - x0) / 3.0
for i, c in enumerate(cols):
    cx = x0 + dx * (i + 0.5)
    ax2.text(cx, y1 + 0.32, c, color=teal, fontsize=9.6, ha="center")
rows = [("χ_triv  (dim 1) — the count", amber, [1, 1, 1], 1),
        ("χ_sign  (dim 1) — the sign", rose, [1, -1, 1], 1),
        ("χ_std   (dim 2) — the where", teal, [2, 0, -1], 2)]
for r, (rn, rcol, vals, dim) in enumerate(rows):
    ry = y1 - dx * (r + 0.68)
    ax2.text(x0 - 0.15, ry, rn, color=rcol, fontsize=8.6, ha="right", va="center")
    for i, v in enumerate(vals):
        cx = x0 + dx * (i + 0.5)
        tcol = "#e8e4da" if v >= 0 else rose
        ax2.text(cx, ry, f"{v:+d}" if v else "0", color=tcol, fontsize=10.5,
                 ha="center", va="center")

# the dim-weighted sums → bars
sx0, sx1 = 2.2, 8.6
sy = 3.9
ax2.text(5.0, 4.7, "× dimension, sum down each column:", color=grey, fontsize=8.8, ha="center")
sums = [6, 0, 0]
for i, s in enumerate(sums):
    cx = x0 + dx * (i + 0.5)
    col = amber if i == 0 else grey
    ax2.bar(cx, s, width=0.55, color=col, alpha=0.92, edgecolor="none")
    ax2.text(cx, s + 0.12, f"{s}", color=col, fontsize=11, ha="center", va="bottom")
    ax2.text(cx, -0.15, "= |S₃|" if i == 0 else "= 0", color=col,
             fontsize=9, ha="center", va="top")
ax2.axhline(0, color="#3a3a44", lw=0.8)

notes = [
    ("the count sums to |S₃|; the sign and the where sum to 0. mono keeps only the count — the average.", amber),
    ("χ_perm = χ_triv + χ_std  →  the average of χ_perm is 1 + 0 = 1: one orbit.", teal),
    ("the count forgets which seat, keeps how many.", grey),
]
yy = 2.6
for txt, col in notes:
    ax2.text(0.35, yy, txt, color=col, fontsize=8.6, ha="left", va="top", linespacing=1.4)
    yy -= 1.3

ax2.set_title("the character table — only the identity rings", color="#e8e4da",
              fontsize=11.5, pad=4)

fig.tight_layout(rect=(0, 0.015, 1, 0.96))
fig.savefig("assets/burnside-cover.png", dpi=160)
print("wrote assets/burnside-cover.png")
