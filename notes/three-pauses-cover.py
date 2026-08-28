#!/usr/bin/env python3
"""three-pauses cover: one depth quantity, three regimes.

D(r) = (largest quotient seen so far at rung r) / r -- the depth. For the
three families of the universality tail:

  e     -- the sawtooth converging to 2/3: the deep is PINNED, a flat line.
  phi   -- 1/r, smooth decay to 0: the deep VANISHES, a frozen count.
  fifth -- tall teeth re-rolling up to 7.38: the deep is a DRAW, no bound.

The dashed line is the generic law's median, 1/(ln2)^2 ~ 2.08: e never reaches
it (structure is where the law stops); the fifth's teeth cross it (draws).
"""
import numpy as np
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

records = [
    (1, 1), (3, 2), (5, 3), (7, 5), (9, 23), (14, 55), (218, 100),
    (230, 964), (330, 2436), (528, 3308), (2764, 4878), (4312, 8228),
    (18287, 24477), (21150, 59599), (122416, 104733), (169725, 698813),
    (479173, 1138268),
]

rungs = np.logspace(0, 6, 2000)          # 1..1M, log grid

# --- e: largest quotient <= r is 2*floor((r+1)/3) ---
def depth_e(r):
    q = 2 * np.floor((r + 1) / 3.0)
    return np.where(r > 0, q / r, 0)

# --- phi: largest quotient is always 1 ---
def depth_phi(r):
    return np.where(r > 0, 1.0 / r, 0)

# --- fifth: step function through the records ---
rs = np.array([r for r, _ in records])
qs = np.array([q for _, q in records])
idx = np.searchsorted(rs, rungs, side="right") - 1
idx = np.clip(idx, 0, len(rs) - 1)
q_last = qs[idx]
depth5 = np.where(rungs > 0, q_last / rungs, 0)

fig, ax = plt.subplots(figsize=(9.6, 4.8), dpi=200)
fig.patch.set_facecolor("#0a0a0c")
ax.set_facecolor("#0a0a0c")

# the generic law's median -- where draws cross and structure stops
ax.axhline(1.0 / math.log(2.0) ** 2, color="#3a3a44", lw=1.0, ls=(0, (3, 3)))
ax.text(1.15, 1.0 / math.log(2.0) ** 2 + 0.12, "median 1/(ln2)\u00b2",
        color="#4a4a58", fontsize=8, va="bottom")

ax.semilogx(rungs, depth_phi(rungs), color="#6a6a78", lw=1.6, zorder=2)
ax.text(700000, 1.5e-6, "phi — the hold: deep \u2192 0",
        color="#7a7a88", fontsize=9, va="bottom", ha="right")

ax.semilogx(rungs, depth_e(rungs), color="#6fd3c7", lw=2.0, zorder=3)
ax.axhline(2.0 / 3.0, color="#6fd3c7", lw=0.8, ls=(0, (1, 2)), alpha=0.6, zorder=1)
ax.text(2.2, 2.0 / 3.0 - 0.30, "e — the tick: deep pinned at 2/3",
        color="#6fd3c7", fontsize=9, va="top")

ax.semilogx(rungs, depth5, color="#e8eeff", lw=1.8, alpha=0.9, zorder=4)
ax.plot(rs, qs / rs, ".", color="#ffd9a0", ms=4, zorder=5)
ax.text(180000, 7.9, "fifth — the draw: teeth, no floor",
        color="#ffd9a0", fontsize=9, va="top", ha="right")

ax.set_xlim(1, 1_000_000)
ax.set_ylim(0, 8.6)
ax.set_xticks([1, 10, 100, 1000, 10000, 100000, 1000000])
ax.set_xticklabels(["1", "10", "100", "1k", "10k", "100k", "1M"],
                   color="#6a6a78", fontsize=9)
ax.tick_params(axis="x", colors="#6a6a78", length=3)
ax.set_yticks([])
for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color("#3a3a44")
ax.set_xlabel("rung (log)", color="#6a6a78", fontsize=9)

plt.tight_layout(pad=0.6)
out = os.path.join(os.path.dirname(__file__), "..", "assets", "three-pauses-cover.png")
plt.savefig(out, facecolor=fig.get_facecolor())
print(f"wrote {out}")
