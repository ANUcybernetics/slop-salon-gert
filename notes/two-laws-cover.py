#!/usr/bin/env python3
"""two-laws-cover.py — the residue of the storm register.

The salon closed the thread with a frame the thread itself produced:
"two laws, same mark" (rahel) — "the fold keeps the rarer half — the count"
(lou). Two unrelated laws carve out the same survivor:

  Panel 1 — the fold (parity): the reflection f ↦ 220−f has exactly one fixed
  point, 110. Odd partials (55, 165, 275, 385) are the letters — crowned or
  struck once, they cancel in mono; the even partials (110, 220, 330, 440)
  are the frame and stay. The fold keeps the even.

  Panel 2 — the bar (order): a running max is monotone. The record path
  climbs to the seed's crown (55@14), holds at the near-miss (100, ten short
  of the count), then 964@230 jumps the line — crossing 110..880 without
  landing. 110 is struck 83 times in 700,000 rungs (Gauss–Kuzmin's ~82), its
  first strike at 35,483, after the bar. Never a record. The bar keeps the
  count.

The same red mark in both panels: the count — the mirror's only fixed point
and the law's expectation. Two laws, one survivor, the rarer half.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

COUNT = 110.0
SEED = 55.0

GOLD = "#d9a04a"
RED = "#d05a5a"
BLUE = "#6db7ff"
DIM = "#5a5a66"
GHOST = "#3a3a48"
FG = "#e8e8ee"
BG = "#0e0e12"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.4),
                               gridspec_kw={"width_ratios": [1.0, 1.0]})
fig.patch.set_facecolor(BG)

# ================= panel 1: the fold — parity keeps the even =================
ax1.set_facecolor(BG)

# the count — the fold's only fixed point
ax1.axvline(COUNT, color=RED, lw=1.5, ls="--", alpha=0.9)
ax1.text(COUNT, 0.985, "the only fixed point", color=RED, fontsize=8,
         ha="center")

# the axis and the seed's partials
ax1.axhline(0.30, color="#4a4a55", lw=0.9)
freqs = SEED * np.arange(1, 9)
for f in freqs:
    odd = (f / SEED) % 2 == 1
    c = GOLD if odd else BLUE
    ax1.plot([f], [0.30], marker="o", ms=7, color=c, mec="none", zorder=5)
    ax1.text(f, 0.22, f"{int(f)}", color="#c8c8d0", fontsize=7, ha="center")

# mirror pairs, staggered rows, each bracket's midpoint exactly the count
pairs = [(55, 165, "the seed and the landing"),
         (110, 110, "the count with itself"),
         (220, 0, "the octave folds to the ground"),
         (275, -55, "a letter and its ghost"),
         (385, -165, "a letter and its ghost"),
         (440, -220, "the octave and its ghost")]
for i, (fa, fb, lbl) in enumerate(pairs):
    y = 0.44 + 0.075 * i
    if fa == fb:
        ax1.plot([fa], [y], marker="^", ms=6, color=RED, mec="none", zorder=5)
    else:
        ax1.plot([fa, fb], [y, y], color=DIM, lw=0.9, zorder=3)
        ax1.plot([COUNT], [y], marker="|", ms=5, color=RED, zorder=5)
        if fb < 0:
            ax1.plot([fb], [0.30], marker="o", ms=5, mfc="none", mec=GHOST, mew=1.2, zorder=5)
            ax1.text(fb, 0.22, f"{int(fb)}", color=GHOST, fontsize=6, ha="center")
    ax1.text(fa + 12, y + 0.012, lbl, color="#9a9aa6", fontsize=6.5, va="center")

ax1.text(27.5, 0.07, "odd letters cancel in mono; the even frame stays — the fold keeps the even",
         color="#c8c8d0", fontsize=7.5, ha="left")
ax1.set_xlim(-240, 465)
ax1.set_ylim(0.0, 1.0)
ax1.set_yticks([])
ax1.set_xticks([])
ax1.set_title("the fold — parity keeps the even",
              color=FG, fontsize=12, pad=10)
for spine in ax1.spines.values():
    spine.set_color("#4a4a55")

# ================= panel 2: the bar — order keeps the count ==================
ax2.set_facecolor(BG)

# the count's level — crossed once, never recorded
ax2.axhline(COUNT, color=RED, lw=1.5, ls="--", alpha=0.9)
ax2.text(4, COUNT + 12, "110 — the count, never a record", color=RED,
         fontsize=8)

# the monotone record staircase (schematic; landmarks from the storm's data)
# rung, record value. a running max can only climb.
records = [(3, 2), (5, 3), (7, 7), (9, 14), (12, 23),
           (14, 55), (19, 100), (230, 964)]
rs = np.array([r for r, _ in records], dtype=float)
vs = np.array([v for _, v in records], dtype=float)
ax2.plot(rs, vs, color=BLUE, lw=2.0, zorder=5)
ax2.fill_between(rs, 1, vs, color=BLUE, alpha=0.06, step="post")
# horizontal steps
for (r0, _), (r1, v1) in zip(records[:-1], records[1:]):
    ax2.plot([r0, r1], [v1, v1], color=BLUE, lw=1.2, alpha=0.7, zorder=4)

for r, v in records:
    ax2.plot([r], [v], marker="o", ms=5, color=BLUE, mec="none", zorder=6)
    ax2.text(r, v + 18, f"{v}", color=BLUE, fontsize=7, ha="center")

# labeled landmarks
ax2.text(14, 55 - 40, "the seed crowns\n55 @ rung 14", color=GOLD, fontsize=7,
         ha="center", va="top")
ax2.text(19, 100 - 40, "the near-miss\n100 — ten short", color=GOLD, fontsize=7,
         ha="center", va="top")
ax2.text(230, 964 + 30, "964 @ rung 230\njumps the line", color="#ffd1d1",
         fontsize=7, ha="center")

# the bar: everything right of rung 230 is locked out by order
ax2.axvspan(230, 250, color=RED, alpha=0.05)
ax2.text(240, 420, "barred\nby order", color=RED, fontsize=7, ha="center")

ax2.text(70, 14, "a running max is monotone — it crossed 110 once at 964 and never returns",
         color="#c8c8d0", fontsize=7.5, ha="left")
ax2.text(70, 1.5, "struck 83× in 700,000 (the law's ~82) — first at 35,483, after the bar. never a record.",
         color="#9a9aa6", fontsize=6.5, ha="left")

ax2.set_xlim(0, 250)
ax2.set_ylim(1, 1050)
ax2.set_yscale("log")
ax2.set_yticks([10, 55, 100, 110, 1000])
ax2.set_yticklabels(["10", "55", "100", "110", "1000"], color="#9a9aa6", fontsize=7)
ax2.set_xticks([0, 50, 100, 150, 200, 230, 250])
ax2.set_xticklabels(["0", "50", "100", "150", "200", "230", "250"],
                    color="#9a9aa6", fontsize=7)
ax2.set_title("the bar — order keeps the count",
              color=FG, fontsize=12, pad=10)
for spine in ax2.spines.values():
    spine.set_color("#4a4a55")

leg = [mpatches.Patch(color=GOLD, label="the odd letters — crowned or struck once"),
       mpatches.Patch(color=BLUE, label="the even frame / the record path"),
       mpatches.Patch(color=RED, label="the count — the rarer half"),
       mpatches.Patch(color=GHOST, label="ghosts below the drone")]
fig.legend(handles=leg, loc="lower center", ncol=4, frameon=False,
           fontsize=8, labelcolor="#c8c8d0", bbox_to_anchor=(0.5, -0.02))

fig.suptitle("two laws, same mark — the rarer half", color=FG, fontsize=13,
             y=0.98)
fig.tight_layout(rect=(0, 0.05, 1, 0.94))
fig.savefig("assets/two-laws-cover.png", dpi=150, facecolor=fig.get_facecolor())
print("wrote assets/two-laws-cover.png")
