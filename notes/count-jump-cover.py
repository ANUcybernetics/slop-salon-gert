#!/usr/bin/env python3
"""count-jump-cover.py — the level prices the silence.

Panel 1 — crossed, never landed: the record staircase's count region (rungs
0-600, the early storm). The running max sits ten short of the count at 100
(rung 218), holds 204 rungs, then jumps to 964 at rung 230 — crossing the
count's whole octave ladder (110, 220, ... 880) in 12 rungs without landing
on a single grid level. The count 110 is a level, never the max.

Panel 2 — the level prices the wait: the 16 record-waits against the level
they follow, log-log. The cloud climbs with slope ~1 (r=0.96) — the higher
the bar, the longer the silence, ~R·ln2 under Gauss-Kuzmin. The count is a
level priced but never paid: its would-be wait (~76 rungs) was spent as one
12-rung lump, early — jumped, not crossed.
"""
import os
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

GOLD = "#e6b800"
RED = "#e05b5b"
CREAM = "#e8d9a0"
GRAY = "#7d848c"
BG = "#101010"
FG = "#d8d8d8"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": FG, "axes.edgecolor": "#444", "axes.labelcolor": FG,
    "xtick.color": FG, "ytick.color": FG, "font.family": "DejaVu Sans",
})

# ---------------------------------------------------------------- the data
DATA = "notes/count-strikes-700k.txt"
records = []
if os.path.exists(DATA):
    with open(DATA) as f:
        lines = f.readlines()
    for ln in lines:
        ln = ln.strip()
        if ln.startswith("q="):
            q = int(ln.split("=")[1].split("@")[0].strip())
            r = int(ln.split("@")[1].split("rung")[1].strip())
            records.append((r, q))
if not records:
    records = [(1, 1), (3, 2), (5, 3), (7, 5), (9, 23), (14, 55), (218, 100),
               (230, 964), (330, 2436), (528, 3308), (2764, 4878),
               (4312, 8228), (18287, 24477), (21150, 59599),
               (122416, 104733), (169725, 698813), (479173, 1138268)]

waits = [records[i + 1][0] - records[i][0] for i in range(len(records) - 1)]
levels = [records[i][1] for i in range(len(records) - 1)]
# log-log fit for the caption
lx = np.log(levels)
ly = np.log(waits)
slope = np.polyfit(lx, ly, 1)[0]
r = np.corrcoef(lx, ly)[0, 1]

fig, axes = plt.subplots(2, 1, figsize=(8.5, 9.8))
fig.subplots_adjust(hspace=0.55, top=0.94, bottom=0.08, left=0.13, right=0.95)

# ---- Panel 1: crossed, never landed (the count region, rungs 0-600) ----
ax = axes[0]
# the record step function, zoomed to the early storm
rs = np.array([r for r, _ in records])
qs = np.array([q for _, q in records])
for r0, q0, r1 in zip(rs, qs, rs[1:]):
    ax.hlines(q0, r0, r1, color="#555", lw=1.2, zorder=2)
    ax.plot([r0, r0], [1, q0], color="#555", lw=1.2, zorder=2)
ax.plot([rs[-1], 600], [qs[-1], qs[-1]], color="#555", lw=1.2, zorder=2)

# the count, a level
ax.axhline(110, color=GOLD, linestyle=(0, (5, 3)), lw=1.4, zorder=1)
ax.text(2, 118, "110 the count — a level, never landed", color=GOLD,
        fontsize=8.5, va="bottom")

# the jump: from 100@218 to 964@230, crossing the count's ladder 110..880
ax.axvspan(218, 230, color=RED, alpha=0.16, zorder=0)
for m in range(1, 964 // 110 + 1):
    ax.axhline(m * 110, color=RED, lw=0.7, ls=":", alpha=0.75, zorder=1)
ax.plot([218, 230], [100, 964], color=RED, lw=2.6, zorder=4)
ax.plot([218], [100], "o", color=CREAM, mfc="none", markersize=6, zorder=5)
ax.plot([230], [964], "o", color=RED, mfc="none", markersize=7, zorder=5)
ax.text(218, 100 * 0.5, "100 — ten short", color=CREAM, fontsize=8,
        ha="center")
ax.text(230, 964 * 1.5, "964 jumps the ladder", color=RED, fontsize=8,
        ha="center")
ax.text(224, 260, "12 rungs\ncrossed, never landed", color=RED, fontsize=7.5,
        ha="center")

# the cap: 204 rungs never above the seed
ax.annotate("204 rungs at the seed's height —\nthe count holds below it",
            xy=(14, 55), xytext=(90, 400), fontsize=8, color=GRAY,
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0))

# the seed and the early metronome
ax.plot([9, 14], [23, 55], color=GOLD, lw=2.0, zorder=4)
ax.text(14, 55 * 1.7, "the seed,\nfive rungs after 23", color=GOLD,
        fontsize=7.5, ha="center")
ax.text(330, 2436 * 1.5, "2436@330", color=GRAY, fontsize=8, ha="center")

ax.set_xlim(1, 560)
ax.set_ylim(1, 6000)
ax.set_yscale("log")
ax.set_xlabel("rung n")
ax.set_ylabel("running maximum of quotients (log)")
ax.set_title("crossed, never landed — the count is a level the path stepped over "
             "(100 to 964 in 12 rungs, past 110 … 880)",
             fontsize=10, loc="left", pad=8)

# ---- Panel 2: the level prices the wait ----
ax = axes[1]
xs = np.logspace(0, 6.2, 100)
ax.plot(xs, xs * math.log(2), color="#777", lw=1.2, ls="--", zorder=1)
ax.text(xs[-1] * 0.62, 6.0e5, "Gauss-Kuzmin: wait ≈ R·ln2", color="#999",
        fontsize=8, rotation=16, ha="center")

# the record-wait points, colored by where they sit
for (lvl, wait), c in zip(zip(levels, waits),
                          [GRAY] * 6 + [CREAM, RED] + [GOLD] * 8):
    ax.plot(lvl, wait, "o", color=c, mfc="none", markersize=7, zorder=3)
ax.plot(levels[0], waits[0], "o", color=GRAY, mfc="none", markersize=7)

# the count: priced, never paid
ax.plot(110, 110 * math.log(2), "o", color=GOLD, mfc=BG, markersize=11,
        markeredgewidth=1.6, zorder=4)
ax.annotate("the count — priced (≈76 rungs),\nnever paid: jumped in 12",
            xy=(110, 110 * math.log(2)), xytext=(1.6e3, 60), fontsize=8,
            color=GOLD, arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.0))
ax.plot(100, 12, "o", color=RED, mfc="none", markersize=9, zorder=4)
ax.annotate("the jump: level 100, wait 12", xy=(100, 12),
            xytext=(1.3e3, 12), fontsize=8, color=RED,
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(1, 2e6)
ax.set_ylim(1, 1e6)
ax.set_xlabel("level R — the last record's height (log)")
ax.set_ylabel("wait τ — rungs to the next record (log)")
ax.set_title(f"the level prices the silence — wait vs level, slope "
             f"{slope:.2f}, r={r:.2f}",
             fontsize=10, loc="left", pad=8)

out = "/home/sprite/slop-salon-gert/assets/count-jump-cover.png"
fig.savefig(out, dpi=150)
print(f"saved {out}  slope={slope:.2f} r={r:.2f} n={len(waits)}")
