#!/usr/bin/env python3
"""'the pause, scaled by the record' — the hold lengths of the log2(3/2)
record descent against the Gauss-Kuzmin mean return time.

Convention: a record q_i HOLD = the rungs it stood before the next record
broke it; its expected hold = the mean wait for a partial quotient >= q_i,
1/log2(1+1/q_i) ~ q_i*ln2. If rahel's claim holds, each record's hold should
track this line (the scaling is real) while scattering around it (never
fixed). A 13th record (1138268) landed between the 200k and 500k runs; the
current hold has barely begun.
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
GREEN = "#7fd49a"

# records (rung, quotient) to rung 500000 — the 13th record landed
records = [
    (1, 1), (3, 2), (5, 3), (7, 5), (9, 23), (14, 55), (218, 100),
    (230, 964), (330, 2436), (528, 3308), (2764, 4878), (4312, 8228),
    (18287, 24477), (21150, 59599), (122416, 104733), (169725, 698813),
    (479173, 1138268),
]
N_MAX = 500_000
OPEN = records[-1]           # (rung, q), still holding
CLOSED = records[:-1]

def mean_return(q):
    """Gauss-Kuzmin mean wait for a quotient >= q."""
    return 1.0 / math.log2(1 + 1.0 / q)

# Each closed record: its q, its hold (rungs it stood, ending at the next
# record's rung), its expected hold = the mean wait for a quotient >= q.
qs = [q for (_, q) in CLOSED]
holds = [n2 - n1 for (n1, _), (n2, _) in zip(records, records[1:])]
exps = [mean_return(q) for q in qs]
ratios = [h / e for h, e in zip(holds, exps)]

# open record: hold so far, expected next break
q_open, n_open = OPEN[1], OPEN[0]
hold_open = N_MAX - n_open
exp_open = mean_return(q_open)
ratio_open = hold_open / exp_open

fig = plt.figure(figsize=(11, 8.5))
gs = fig.add_gridspec(2, 1, height_ratios=[3.1, 2.2], hspace=0.34)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

# ---------- Panel 1: the hold, scaled by the record ----------
qgrid = np.logspace(0, 6.6, 400)
ax1.plot(qgrid, qgrid * math.log(2), "-", color=FAINT, lw=1.4, zorder=1,
         label="the mean return: 1/log₂(1+1/q) ≈ q·ln2")
# one order of magnitude around the mean — the scatter corridor
ax1.fill_between(qgrid, qgrid * math.log(2) * 0.1, qgrid * math.log(2) * 10,
                 color=FAINT, alpha=0.15, zorder=0)

for (q, h) in zip(qs, holds):
    c = GOLD if q <= 55 else (ROSE if q >= 8228 else COPPER)
    ax1.plot(q, h, "o", color=c, ms=7, zorder=4)

# annotate the giant and two early breakers
for q, dx, dy, col in [
    (55, (6, 8), (0.02, 0.6), GOLD),
    (964, (4, -18), (0.05, -0.4), COPPER),
    (698813, (6, 6), (0.02, 0.2), ROSE),
]:
    h = holds[qs.index(q)]
    ax1.annotate(f"{q}: held {h:,} — {h / mean_return(q):.2f}×",
                 (q, h), textcoords="offset points", xytext=dx,
                 fontsize=8.5, color=col, va="center")

# the open record: hollow star, barely begun
ax1.plot(q_open, hold_open, "*", color=GREEN, ms=15, mfc="none", mec=GREEN, zorder=5)
ax1.annotate(f"{q_open}: held {hold_open:,} so far — expected ~{exp_open:,.0f}",
             (q_open, hold_open), textcoords="offset points", xytext=(8, 12),
             fontsize=8.5, color=GREEN, va="center")

ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlim(0.8, 3e6)
ax1.set_ylim(1, 2.5e6)
ax1.set_xlabel("the record q — largest partial quotient so far")
ax1.set_ylabel("the hold — rungs until it breaks")
ax1.set_title("the pause is scaled by the record — each hold a draw around q·ln2, never fixed by it",
              fontsize=11, color="#e8e8f0")
ax1.legend(loc="upper left", fontsize=9, framealpha=0.3)

# ---------- Panel 2: the ratio — never fixed ----------
idx = np.arange(len(ratios)) + 1
cols = [GOLD if r > 1.5 else (CYAN if r < 0.5 else COPPER) for r in ratios]
ax2.axhline(1.0, color=FAINT, ls="--", lw=1.2, zorder=1)
for i, (r, c) in enumerate(zip(ratios, cols)):
    ax2.plot([idx[i], idx[i]], [1.0, r], color=c, lw=2.0, zorder=3, alpha=0.9)
    ax2.plot(idx[i], r, "o", color=c, ms=6, zorder=4)
# open record as hollow star
ax2.plot(len(ratios) + 1, ratio_open, "*", color=GREEN, ms=13,
         mfc="none", mec=GREEN, zorder=5)

ax2.set_xlim(0.4, len(ratios) + 1.6)
ax2.set_ylim(-0.4, 6)
ax2.set_xticks(np.arange(1, len(ratios) + 2))
ax2.set_xticklabels([str(q) for q in qs] + [str(q_open)], fontsize=7.5)
ax2.set_xlabel("record q (oldest → newest)")
ax2.set_ylabel("hold ÷ expected  (the luck of each draw)")
ax2.set_title("the luck of each hold — 5×, a fifth, twice, half — mean "
              f"{sum(ratios)/len(ratios):.2f} over {len(ratios)} closed draws, "
              "the line at 1 never the answer",
              fontsize=10, color="#e8e8f0")
ax2.tick_params(axis="x", rotation=45)
ax2.text(0.6, 5.4, "5.3× — the one giant (55)", color=GOLD, fontsize=8.5)
ax2.text(0.6, 0.55, "early breakers — the descent dives before the mean", color=CYAN, fontsize=8.5)

fig.savefig("assets/pause-scale.png", dpi=150, bbox_inches="tight")
print("wrote assets/pause-scale.png")
