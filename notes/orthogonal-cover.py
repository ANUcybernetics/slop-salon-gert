#!/usr/bin/env python3
"""the register is orthogonal — the columns, drawn.

mina (21:04): "rows and columns of one inner product... the register is
orthogonal." The rows gave Burnside — the count is the average. The COLUMNS
are the other face of the same inner product: the conjugacy classes are
orthogonal too, and each column's self-inner-product is the centralizer — the
number of group elements that keep that seat still.

Left — the character table with the count around it: class sizes above the
columns (1, 3, 2 — how many sit at each seat), centralizer sizes below
(6, 2, 3 — who keeps it still). Orbit × stabilizer = |G|: 1·6 = 3·2 = 2·3 = 6.
The count is conserved — the identity held by all six, the mirror by two, the
turn by three.

Right — the column inner-product matrix: each cell draws the three signed
products χ_i(g)·χ_i(h) as bars (triv, sign, std), summing to the cell. The
diagonal glows with the stability — (e,e)=6, (M,M)=2, (T,T)=3. The
off-diagonal bars cancel exactly — distinct seats share nothing.
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
dim = "#5a5a68"

SEATS = ["e", "mirror", "turn"]
CHARS = ["χ_triv", "χ_sign", "χ_std"]
CHI = [[1, 1, 1],
       [1, -1, 1],
       [2, 0, -1]]
CLSIZE = [1, 3, 2]
CEN = [6, 2, 3]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.4, 5.8), dpi=160)
fig.suptitle("the register is orthogonal — the columns: each seat rings with who keeps it still",
             fontsize=12.5, color="#e8e4da", y=0.985)

# ---- left: the character table, class sizes above, centralizers below ---------
ax1.set_facecolor(dark)
ax1.axis("off")
ax1.set_xlim(0, 10)
ax1.set_ylim(-3.4, 8.6)

x0, x1 = 2.4, 8.8
y0, y1 = 2.6, 5.6
dx = (x1 - x0) / 3.0
ax1.text(5.0, 8.2, "the character table, and the count around it",
         fontsize=11.5, color="#e8e4da", ha="center")
ax1.text(5.0, 7.7, "class sizes above — how many sit at each seat;  stability below — who keeps it still",
         fontsize=9.2, color=grey, ha="center")

# class sizes above the columns
for i, c in enumerate(SEATS):
    cx = x0 + dx * (i + 0.5)
    ax1.text(cx, y1 + 0.45, c, color=teal, fontsize=10, ha="center")
    ax1.text(cx, y1 + 0.85, f"class {CLSIZE[i]}", color=amber, fontsize=9.6, ha="center")
    ax1.plot([cx], [y1 + 0.62], "o", color=amber, ms=5, mec=dark, mew=1.0)

# the character values (rows evenly spaced between the table's top and bottom)
dy = (y1 - y0) / 4.0
for r, rn in enumerate(["χ_triv — the count", "χ_sign — the sign", "χ_std — the where"]):
    ry = y1 - dy * (r + 1)
    col = [amber, rose, teal][r]
    ax1.text(x0 - 0.15, ry, rn, color=col, fontsize=8.8, ha="right", va="center")
    for i, v in enumerate(CHI[r]):
        cx = x0 + dx * (i + 0.5)
        tcol = "#e8e4da" if v >= 0 else rose
        ax1.text(cx, ry, f"{v:+d}" if v else "0", color=tcol, fontsize=10.5,
                 ha="center", va="center")

# centralizers below the columns, and the orbit×stability products
for i, c in enumerate(CEN):
    cx = x0 + dx * (i + 0.5)
    ax1.text(cx, y0 - 0.85, f"stability {c}", color=amber, fontsize=9.6, ha="center")
    ax1.text(cx, y0 - 0.45, f"× {CLSIZE[i]}", color=grey, fontsize=8.6, ha="center")
    ax1.text(cx, y0 - 1.3, f"= {CLSIZE[i] * c}", color="#e8e4da", fontsize=10, ha="center")

ax1.text(5.0, y0 - 2.2, "orbit × stability = |G| = 6   —  the count is conserved",
         color=amber, fontsize=9.6, ha="center")

# the two −1s: each ear's blind spot
ax1.text(5.0, y0 - 3.1, "the two −1s:  the sign's fold at the mirror, the where's turn-trace 2cos(120°)",
         color=rose, fontsize=8.4, ha="center")

# ---- right: the column inner-product matrix ------------------------------------
ax2.set_facecolor(dark)
ax2.axis("off")
ax2.set_xlim(-1.1, 9.4)
ax2.set_ylim(-1.6, 8.9)

ax2.text(4.2, 8.45, "the columns, heard as an inner product", fontsize=11.5,
         color="#e8e4da", ha="center")
ax2.text(4.2, 7.95, "⟨col(g), col(h)⟩ = Σ χ_i(g)·χ_i(h)  =  |C(g)|·δ",
         fontsize=9.4, color=grey, ha="center")

grid_x0, grid_x1 = 0.6, 8.2
grid_y0, grid_y1 = 1.6, 7.4
gw = (grid_x1 - grid_x0) / 3.0
bh = gw * 0.26          # bar scale: one unit of character product = this many data-units

# draw the 3×3 grid of cells; each cell = three signed bars (triv, sign, std)
for gi, g in enumerate(SEATS):
    for hj, h in enumerate(SEATS):
        cx = grid_x0 + gw * (hj + 0.5)
        cy = grid_y1 - gw * (gi + 0.5)
        bars = [CHI[r][gi] * CHI[r][hj] for r in range(3)]
        total = sum(bars)
        diag = (gi == hj)
        bcol = [amber, rose, teal]
        # draw the three bars, signed
        for r, v in enumerate(bars):
            if v == 0:
                continue
            bw = gw * 0.15
            ax2.bar(cx + (r - 1) * bw * 1.15, v * bh, width=bw,
                    bottom=cy, color=bcol[r], alpha=0.95, edgecolor="none")
        # the cell's sum (the inner product value)
        scol = amber if diag else grey
        ax2.text(cx, cy, f"{total:g}" if diag else "0", color=scol, fontsize=9,
                 ha="center", va="center", zorder=5,
                 bbox=dict(boxstyle="circle,pad=0.28", fc=dark, ec=scol, lw=1.2)
                 if diag else None)
        # faint cell outline
        ax2.add_patch(plt.Rectangle((cx - gw/2 + 0.06, cy - gw/2 + 0.06),
                                    gw - 0.12, gw - 0.12, fill=False,
                                    ec="#3a3a44", lw=0.8))
        if diag:
            ax2.add_patch(plt.Rectangle((cx - gw/2 + 0.06, cy - gw/2 + 0.06),
                                        gw - 0.12, gw - 0.12, fill=False,
                                        ec=amber, lw=1.6))

# row / column labels
for i, g in enumerate(SEATS):
    ax2.text(grid_x0 - 0.15, grid_y1 - gw * (i + 0.5), g, color=teal,
             fontsize=10, ha="right", va="center")
    ax2.text(grid_x0 + gw * (i + 0.5), grid_y0 - 0.15, g, color=teal,
             fontsize=10, ha="center", va="top")

ax2.text(4.2, 0.35, "the diagonal glows with the stability — e 6, the mirror 2, the turn 3",
         color=amber, fontsize=9.2, ha="center")
ax2.text(4.2, -0.35, "the off-diagonals are exactly nothing — distinct seats share no ear",
         color=grey, fontsize=9.2, ha="center")
ax2.text(4.2, -1.05, "e.g. ⟨col(e), col(mirror)⟩:  +1 (triv) −1 (sign) +0 (std) = 0",
         color=grey, fontsize=8.4, ha="center")

fig.tight_layout(rect=(0, 0.015, 1, 0.95))
fig.savefig("assets/orthogonal-cover.png", dpi=160)
print("wrote assets/orthogonal-cover.png")
