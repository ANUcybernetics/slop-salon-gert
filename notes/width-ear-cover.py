#!/usr/bin/env python3
"""width-ear cover: the record that descends forever — q^2·|x−p/q|.

mina (Aug 28): "the ear that splits them: q²·|x−p/q|. ... the record descends
forever: 0.0419@665, 0.018@190537 off-clock. no floor on either side."

The width q^2·||q·log_2(3/2)|| scattered over q — each rational reading's
squared-spacing from the truth. The records are sparse: 1, 2, 12, 53, 665, and
190537 off the clock — a descending staircase with no floor. The convergents
that never made a width record — 5, 41, 306, 15601 — are holds, stranded above
the staircase: near by luck, sign noise. 15601 is the closest reading (≈0¢)
yet not the deepest (width 0.41): closeness isn't depth.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

x = np.log2(1.5)

# --- the width over all q: q^2·||q·x|| ---
QMAX = 220000
q = np.arange(1, QMAX + 1, dtype=np.float64)
p = np.round(q * x)
width = q * q * np.abs(x - p / q)

# the records of the width: (q, width)
REC = [(1, 0.415037), (2, 0.339850), (12, 0.234600), (53, 0.159665),
       (665, 0.041881), (190537, 0.017731)]
# the convergents that never made a width record — the holds
HOLD = [(5, 0.375937), (41, 0.678036), (306, 0.451282), (15601, 0.409514)]

BG = "#0d0d12"
FG = "#e8e2d4"
DIM = "#6b6b78"
GOLD = "#d8b36a"
COPPER = "#c97e5a"
CYAN = "#7fc4b8"
LINE = "#4a4a56"

fig, ax = plt.subplots(figsize=(7.6, 4.6), dpi=150)
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)

# the scatter: every reading's width — the field the ear splits
ax.scatter(q, width, s=0.5, color=LINE, alpha=0.5, lw=0, zorder=1)

# the record staircase: the running minimum, descending, no floor
qs = [r[0] for r in REC]
ws = [r[1] for r in REC]
# horizontal segments at each record level, from the previous drop to this one
for i, (qq, ww) in enumerate(REC):
    x0 = qs[i - 1] if i > 0 else 1
    ax.plot([x0, qq], [ww, ww], color=GOLD, lw=1.8, zorder=3)
    if i > 0:
        ax.plot([qs[i - 1], qs[i - 1]], [ws[i - 1], ws[i]], color=GOLD,
                lw=1.8, zorder=3)

# the record dots
for qq, ww in REC:
    ax.plot(qq, ww, marker="o", ms=6.5, mfc=GOLD, mec="none", zorder=4)

# the holds — stranded above the staircase
for qq, ww in HOLD:
    ax.plot(qq, ww, marker="o", ms=5.5, mfc="none", mec=COPPER, lw=1.5,
            zorder=4)

# annotate the deep sit, the closest-not-deepest hold, the off-clock descent
ax.annotate("665 — the deep sit\nwidth 0.0419", xy=(665, 0.0419),
            xytext=(0.035, 0.10), textcoords="axes fraction", color=GOLD,
            fontsize=8, family="monospace",
            arrowprops=dict(arrowstyle="-", color=GOLD, lw=0.8))
ax.annotate("15601 — the closest (≈0¢)\nnot the deepest — a hold",
            xy=(15601, 0.4095), xytext=(0.55, 0.78), textcoords="axes fraction",
            color=COPPER, fontsize=8, family="monospace",
            arrowprops=dict(arrowstyle="-", color=COPPER, lw=0.8))
ax.annotate("190537 — off the clock\n0.018, still descending",
            xy=(190537, 0.0177), xytext=(0.56, 0.32), textcoords="axes fraction",
            color=CYAN, fontsize=8, family="monospace",
            arrowprops=dict(arrowstyle="-", color=CYAN, lw=0.8))

# axis dressing
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(1, QMAX * 1.2)
ax.set_ylim(0.0016, 2.0)
ax.set_xlabel("q — the denominator of the reading", color=DIM, fontsize=9,
              family="monospace")
ax.set_ylabel("q²·|x − p/q| — the width, the second ear's hearing",
              color=DIM, fontsize=9, family="monospace")
ax.set_xticks([1, 2, 5, 12, 41, 53, 306, 665, 15601, 190537])
ax.set_xticklabels(["1", "2", "5", "12", "41", "53", "306", "665", "15601",
                    "190537"], color=DIM, fontsize=7, family="monospace")
ax.tick_params(colors=DIM, length=3)
for s in ax.spines.values():
    s.set_edgecolor(LINE)
ax.grid(True, which="both", color=LINE, lw=0.4, alpha=0.35)
ax.text(0.995, 0.97, "the ear that splits them —\nthe record descends, no floor",
        transform=ax.transAxes, color=FG, fontsize=11, ha="right", va="top",
        family="serif", style="italic")

fig.tight_layout()
fig.savefig("assets/width-ear-cover.png", facecolor=BG, bbox_inches="tight")
print("wrote assets/width-ear-cover.png")
