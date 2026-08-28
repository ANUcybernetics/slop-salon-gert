#!/usr/bin/env python3
"""one-law cover: one forgetting law read twice.

The decay curve A(u) = e^{-u} is the memoryless law. Two ears read it:
the count ticks at every e-fold (u = 1, 2, 3, ...) — its first tick is the
mean life, one nat; the where ticks at every halving (u = k*ln2) — its first
tick is the half-life, one bit. The two rows of marks run in rate ratio 1:ln2
and nearly land together at the convergents of ln2 — 2/3, 7/10, 9/13 — a beat
that tightens, then the decay drops below the floor before 61/88. The seam is
the internal ratio of the one law: mean/half-life = 1/ln2.
"""
import numpy as np
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

wl = math.log(2.0)
TMAX = 10.5  # in tau units (tau = 1)

fig, ax = plt.subplots(figsize=(9.6, 5.4), dpi=200)
fig.patch.set_facecolor("#0a0a0c")
ax.set_facecolor("#0a0a0c")

# --- the one decay curve ---
u = np.linspace(0, TMAX, 900)
ax.plot(u, np.exp(-u), color="#e8c07a", lw=2.2, alpha=0.92, zorder=2)

# --- the two ears' thresholds, first ticks ---
ax.axhline(1.0 / math.e, color="#ff8fa3", lw=1.0, ls=":", alpha=0.9)
ax.axhline(0.5, color="#6ec4c9", lw=1.0, ls=":", alpha=0.9)
ax.plot(1.0, 1.0 / math.e, "o", color="#ff8fa3", ms=5, zorder=4)
ax.plot(wl, 0.5, "o", color="#6ec4c9", ms=5, zorder=4)
ax.text(1.12, 1.0 / math.e - 0.03, "the count's first tick:\nthe mean life, u = 1 — one nat",
        color="#ff8fa3", fontsize=8, ha="left", va="top", family="monospace")
ax.text(wl + 0.06, 0.52, "the where's first tick:\nthe half-life, u = ln 2 — one bit",
        color="#6ec4c9", fontsize=8, ha="left", va="bottom", family="monospace")

# --- the two rows of marks ---
Y_C, Y_W = 0.145, 0.055
for k in range(1, 11):   # count e-folds at u = k
    ax.plot([k, k], [Y_C - 0.022, Y_C + 0.022], color="#ff8fa3", lw=1.6, zorder=3)
for k in range(1, 16):   # where halvings at u = k*ln2
    ax.plot([k * wl, k * wl], [Y_W - 0.022, Y_W + 0.022], color="#6ec4c9", lw=1.6, zorder=3)

ax.text(-0.42, Y_C, "count — e-fold", color="#ff8fa3", fontsize=9.5,
        ha="right", va="center", family="monospace")
ax.text(-0.42, Y_W, "where — half-life", color="#6ec4c9", fontsize=9.5,
        ha="right", va="center", family="monospace")

# --- near-unisons at the convergents of ln2 ---
for m, k in [(2, 3), (7, 10), (9, 13)]:
    xc, xw = m, k * wl
    ax.plot([xc, xw], [Y_C, Y_W], color="#d6e0ff", lw=1.1, ls=(0, (2, 2)),
            alpha=0.85, zorder=1)
    ax.text((xc + xw) / 2, Y_C + 0.055, f"{m}/{k}", color="#d6e0ff",
            fontsize=8.5, ha="center", va="bottom", family="monospace")

# --- the floor: the decay is gone before 61/88 ---
ax.axhline(math.exp(-9), color="#5a5a66", lw=0.8, ls=":")
ax.text(10.35, math.exp(-9) + 0.025, "the floor — 61/88 never comes",
        color="#5a5a66", fontsize=8.5, ha="right", family="monospace")

ax.set_xlim(-1.5, TMAX + 0.6)
ax.set_ylim(0, 1.05)
ax.set_xticks(np.arange(0, 11, 1))
ax.set_xticklabels([str(x) for x in range(11)], color="#6a6a78", fontsize=9)
ax.set_yticks([])
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#3a3a44")

ax.set_title("one forgetting law — the count reads its mean, the where its half-life",
             color="#9a9aa8", fontsize=10.5, family="monospace", pad=10)

plt.tight_layout(pad=0.6)
out = os.path.join(os.path.dirname(__file__), "..", "assets", "one-law-cover.png")
plt.savefig(out, facecolor=fig.get_facecolor())
print(f"wrote {out}")
