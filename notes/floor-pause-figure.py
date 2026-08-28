#!/usr/bin/env python3
"""'the floor was a pause' — verified extension of the descent of log2(3/2).

Panel 1: the record-width staircase to 200,000 rungs (lou's data confirmed to
rung 4000, then extended). Each record width ~1/a is held for a pause (the
record kept by the future), then the descent dives again. The golden floor
1/sqrt(5) is where phi rests; the fifth dived below it at the first record.
The current record (1/698813) is still open.

Panel 2: the descent threading the floors. The ladder of quadratic floors
1/sqrt(M^2+4) (M=1..) is a countable set, measure zero — the count reads it
empty; but it accumulates densely at zero — the where reads it everywhere.
Each record width, drawn as a horizontal line crossing the ladder at M=a, has
dived below the floors of every M < a.
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "figure.facecolor": "#0d0d12",
    "axes.facecolor": "#0d0d12",
    "axes.edgecolor": "#3a3a46",
    "axes.labelcolor": "#d8d8e0",
    "text.color": "#d8d8e0",
    "xtick.color": "#9a9aa6",
    "ytick.color": "#9a9aa6",
    "axes.grid": True,
    "grid.color": "#2a2a34",
    "grid.linewidth": 0.6,
    "font.size": 10,
})

GOLD = "#d4af37"
ROSE = "#e0667a"
CYAN = "#55c9e0"
COPPER = "#b87333"
FAINT = "#55555f"

# records: (rung, quotient a) for log2(3/2); width ~1/a, held until next record
records = [
    (9, 23), (14, 55), (218, 100), (230, 964), (330, 2436), (528, 3308),
    (2764, 4878), (4312, 8228), (18287, 24477), (21150, 59599),
    (122416, 104733), (169725, 698813),
]
N_MAX = 200_000
LOU_LAST_RUNG = 4000  # lou's computation ran to rung 4000

golden = 1 / math.sqrt(5)
alpha = math.log2(1.5)

fig = plt.figure(figsize=(11, 8.5))
gs = fig.add_gridspec(2, 1, height_ratios=[3.1, 2.2], hspace=0.32)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

# ---------- Panel 1: the descent, extended ----------
for i, (n, a) in enumerate(records):
    w = 1.0 / a
    n_next = records[i + 1][0] if i + 1 < len(records) else N_MAX
    color = GOLD if a <= 4878 else ROSE
    lw = 2.4 if a <= 4878 else 2.4
    # horizontal hold (the pause) then drop to next width
    if i + 1 < len(records):
        w_next = 1.0 / records[i + 1][1]
        ax1.hlines(w, n, n_next, color=color, lw=lw, zorder=3)
        ax1.plot([n_next, n_next], [w, w_next], color=color, lw=lw, zorder=3)
        ax1.plot(n, w, "o", color=color, ms=5, zorder=4)
    else:
        # current record: solid hold to rung LOU_LAST_RUNG, then dashed open
        ax1.hlines(w, n, LOU_LAST_RUNG, color=color, lw=lw, zorder=3)
        ax1.plot(n, w, "o", color=color, ms=6, zorder=4)
        ax1.hlines(w, LOU_LAST_RUNG, N_MAX, color=color, lw=1.6, ls="--", alpha=0.7, zorder=3)
        ax1.annotate("?", (N_MAX, w), textcoords="offset points", xytext=(4, 0),
                     color=ROSE, fontsize=15, va="center")

# golden floor (where phi rests)
ax1.axhline(golden, color=CYAN, ls="--", lw=1.2, alpha=0.9, zorder=2)
ax1.text(1.05e4, golden * 1.25, "φ rests here — the golden floor 1/√5",
         color=CYAN, fontsize=10)

# pause annotations on the long holds
for n, a, lab in [
    (14, 55, "1/55 held 204"), (2764, 4878, "1/4878 held 1548"),
    (4312, 8228, "1/8228 held 13,975"), (21150, 59599, "1/59599 held 101,266"),
    (122416, 104733, "1/104733 held 47,309"),
    (169725, 698813, "1/698813 held 30,275+ — open"),
]:
    w = 1.0 / a
    ax1.annotate(lab, (n, w), textcoords="offset points", xytext=(-14, -30),
                 fontsize=8.5, color=ROSE if a > 4878 else GOLD, alpha=0.95)

ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlim(6, N_MAX * 1.4)
ax1.set_ylim(4e-7, 1.3)
ax1.set_xlabel("rung n — partial quotient index")
ax1.set_ylabel("record width  ~1/a")
ax1.set_title("the floor was a pause — the descent of log₂(3/2), verified and extended to 200,000 rungs",
              fontsize=11, color="#e8e8f0")
# mark the boundary of lou's run
ax1.axvline(LOU_LAST_RUNG, color=FAINT, ls=":", lw=1)
ax1.text(LOU_LAST_RUNG, 2e-6, "lou's run → rung 4000", color=FAINT, fontsize=8, ha="right")

# ---------- Panel 2: the descent threading the floors ----------
M = np.logspace(0, 6.0, 2000)
ladder = 1.0 / np.sqrt(M ** 2 + 4)
ax2.plot(M, ladder, "-", color=GOLD, lw=1.0, alpha=0.85, zorder=2,
         label="the floors 1/√(M²+4) — a quadratic rests on each")
# each record width crosses the ladder at M = a
for i, (n, a) in enumerate(records):
    w = 1.0 / a
    color = ROSE if a > 4878 else COPPER
    ax2.hlines(w, 1, a, color=color, lw=1.3, alpha=0.85, zorder=3)
    ax2.plot(a, w, "o", color=color, ms=4, zorder=4)
    if a in (23, 4878, 698813):
        ax2.annotate(f"1/{a}", (a, w), textcoords="offset points", xytext=(4, -2),
                     fontsize=8, color=color)

ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_xlim(1, 1.2e6)
ax2.set_ylim(3e-7, 0.6)
ax2.set_xlabel("M — the quadratic index [M; M, M, …]")
ax2.set_ylabel("floor width")
ax2.set_title("the descent threads the floors — countable, null (the count reads empty); dense near zero (the where reads everywhere)",
              fontsize=10, color="#e8e8f0")
ax2.legend(loc="upper right", fontsize=8, framealpha=0.3)
ax2.text(1.3, 2e-6, "each horizontal line: the fifth's best width has dived below\n"
                    "the floors of every quadratic M < a — passing through the everywhere,\n"
                    "never resting. the current record has passed 698,812 floors.",
         color="#b8b8c4", fontsize=9, va="bottom")

fig.savefig("assets/floor-pause.png", dpi=150, bbox_inches="tight")
print("wrote assets/floor-pause.png")
