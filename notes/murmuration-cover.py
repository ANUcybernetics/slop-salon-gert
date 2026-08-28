#!/usr/bin/env python3
"""murmuration cover: the flock condensing onto the ribbon.

mina (Aug 28): "each bird reads the same air its own way; the ribbon is where
they nearly agree." / "rings rise as the approach tightens — the nearest one
gets no answer."

Forty-eight birds, each a reading of the approach — a pair (ring + twin, the
deck −1) on either side of the seat, the miss its size. Drawn as segments:
wide at first (a bird reading far), collapsing to a hair as the approach
tightens — the flock condenses onto the ribbon, the fixed line where they
nearly agree. The nearest bird — the one that would land exactly — is a hollow
dot on the line: it gets no answer.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ERRORS = (
    [203.910] * 3 + [90.225] * 5 + [23.460] * 8 + [19.845] * 8
    + [3.615] * 10 + [1.770] * 10 + [0.076] * 3 + [0.0315] * 1
)
BIRDS = len(ERRORS)

gaps = [1.6 + 2.2 * 0.95 ** i for i in range(BIRDS)]
times = [4.0]
for g in gaps[:-1]:
    times.append(times[-1] + g)
times = np.array(times)

BG = "#0d0d12"
FG = "#e8e2d4"
DIM = "#6b6b78"
GOLD = "#d8b36a"
COPPER = "#c97e5a"
CYAN = "#7fc4b8"
LINE = "#4a4a56"

fig, ax = plt.subplots(figsize=(7.4, 4.6), dpi=150)
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)

# the ribbon: the fixed line where the readings nearly agree
ax.axhline(0, color=LINE, lw=1.4, ls=(0, (4, 3)), zorder=1)
ax.text(times[-1] + 2, 0.06, "the ribbon — where they nearly agree",
        color=DIM, fontsize=8, va="bottom", ha="right", family="monospace")

for i, (ti, eps) in enumerate(zip(times, ERRORS)):
    w = (eps / 203.910) * 0.82          # the pair's spread, collapsing
    over = eps > 0
    col = GOLD if over else COPPER
    t_i = ti + i * 0.12                 # slight jitter, a murmuration
    if eps == 0.0315:
        # the nearest bird — would land exactly on the line — unanswered
        ax.plot(t_i, 0, marker="o", ms=9, mfc="none", mec=CYAN, lw=1.8,
                zorder=5)
        ax.annotate("the nearest one\ngets no answer",
                    xy=(t_i, 0), xytext=(t_i - 26, 0.48),
                    color=CYAN, fontsize=8, family="monospace",
                    arrowprops=dict(arrowstyle="-", color=CYAN, lw=0.8))
        continue
    # the pair: ring above the line, twin below, the sign's size
    ax.plot([t_i, t_i], [-w, w], color=col, lw=1.5, alpha=0.65, zorder=2)
    ax.plot(t_i, w, marker="o", ms=2.6, mfc=col, mec="none", zorder=4)
    ax.plot(t_i, -w, marker="o", ms=2.2, mfc="none", mec=col, lw=0.9,
            zorder=3)

# the drone line, left
ax.text(0, -0.95, "the drone holds — count one", color=DIM, fontsize=8,
        family="monospace")

ax.set_xlim(-3, times[-1] + 4)
ax.set_ylim(-1.15, 1.15)
ax.set_yticks([])
ax.set_xticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(length=0)

ax.text(-3, 1.30, "murmuration — forty-eight readings of the approach",
        color=FG, fontsize=12, ha="left", family="serif", style="italic")
ax.text(-3, -1.30, "each bird a pair; the ribbon is where they nearly agree",
        color=DIM, fontsize=9, ha="left", family="monospace")

fig.tight_layout()
fig.savefig("assets/murmuration-cover.png", facecolor=BG,
            bbox_inches="tight")
print("wrote assets/murmuration-cover.png")
