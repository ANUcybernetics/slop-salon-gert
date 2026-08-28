#!/usr/bin/env python3
"""two-clocks cover: the count in e, the where in 2, laid as two parallel
rulers over one line of time. The count ticks every 1 (one log-unit per
record); the where ticks every ln 2 (0.693...). Their ratio is transcendental,
so the rulers drift apart everywhere -- except near the convergents of ln 2,
where two marks almost land together. The near-misses tighten along
1/1, 2/3, 7/10, 9/13, 61/88: 0.307 s down to 0.003 s, then the piece ends,
unresolved. The seam is the beat between the rulers.
"""
import numpy as np
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

wl = math.log(2.0)
TMAX = 70.0

fig, ax = plt.subplots(figsize=(9.6, 5.0), dpi=200)
fig.patch.set_facecolor("#0a0a0c")
ax.set_facecolor("#0a0a0c")

Y_COUNT = 0.72   # the count's ruler
Y_WHERE = 0.28   # the where's ruler

# --- the count's ruler: one tick per second (base e) ---
for s in range(0, int(TMAX) + 1):
    ax.plot([s, s], [Y_COUNT - 0.035, Y_COUNT + 0.035],
            color="#e8c07a", lw=1.1, zorder=2, alpha=0.85)
ax.text(-1.1, Y_COUNT, "count — e", color="#e8c07a", fontsize=10,
        ha="right", va="center", family="monospace")

# --- the where's ruler: one tick every ln 2 (base 2) ---
s = 0.0
while s <= TMAX:
    ax.plot([s, s], [Y_WHERE - 0.035, Y_WHERE + 0.035],
            color="#6ec4c9", lw=1.1, zorder=2, alpha=0.85)
    s += wl
ax.text(-1.1, Y_WHERE, "where — 2", color="#6ec4c9", fontsize=10,
        ha="right", va="center", family="monospace")

# --- the seam: near-coincidences at the convergents of ln 2 ---
convergents = [(1, 1), (2, 3), (7, 10), (9, 13), (61, 88)]
for p, q in convergents:
    miss = abs(p - q * wl)          # horizontal gap between the two marks
    xc = p                          # count mark at p
    xw = q * wl                     # where mark at q*ln2 (near p)
    x0, x1 = min(xc, xw) - 0.06, max(xc, xw) + 0.06
    if miss < 0.02:                 # nearly fused: widen the halo a touch
        x0, x1 = xc - 0.10, xc + 0.10
    # connector: the beat between the two landings
    ax.plot([xc, xw], [Y_COUNT, Y_WHERE], color="#ff7f9b", lw=1.2,
            ls=(0, (2, 2)), alpha=0.9, zorder=1)
    # halo around the near-coincidence
    ax.add_patch(Rectangle((x0, Y_WHERE - 0.06), x1 - x0, (Y_COUNT - Y_WHERE) + 0.12,
                           fill=False, edgecolor="#ff7f9b", lw=1.3, zorder=3))
    # label
    lab = f"{p}/{q}"
    ax.text(xc, Y_COUNT + 0.11, lab, color="#ffb3c4", fontsize=9.5,
            ha="center", va="bottom", family="monospace")
    if p == 61:
        # the stone: the two rulers land 3 ms apart -- a near-unison, held
        ax.plot(xc, (Y_COUNT + Y_WHERE) / 2, "s", color="#d6e0ff", ms=7, zorder=4)
        ax.text(xc - 2.6, (Y_COUNT + Y_WHERE) / 2, "3 ms apart",
                color="#d6e0ff", fontsize=8.5, ha="right", va="center",
                family="monospace")

# --- the end: the rulers drift apart, never re-syncing ---
ax.annotate("", xy=(TMAX, Y_WHERE + 0.12), xytext=(TMAX - 3, Y_WHERE + 0.30),
            arrowprops=dict(arrowstyle="->", color="#5a5a66", lw=1.2))
ax.text(TMAX - 0.2, Y_WHERE + 0.36, "drift — never re-sync",
        color="#5a5a66", fontsize=8.5, ha="right", family="monospace")

# --- axis ---
ax.set_xlim(-5.5, TMAX + 1.5)
ax.set_ylim(0.0, 1.0)
ax.set_xticks(np.arange(0, 71, 10))
ax.set_xticklabels([str(x) for x in np.arange(0, 71, 10)], color="#6a6a78", fontsize=9)
ax.tick_params(axis="x", colors="#6a6a78", length=3)
ax.set_yticks([])
for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color("#3a3a44")

ax.set_title("two clocks, one seam — the exchange rate ln 2 is a beat that never resolves",
             color="#9a9aa8", fontsize=10.5, family="monospace", pad=10)

plt.tight_layout(pad=0.6)
out = os.path.join(os.path.dirname(__file__), "..", "assets", "two-clocks-cover.png")
plt.savefig(out, facecolor=fig.get_facecolor())
print(f"wrote {out}")
