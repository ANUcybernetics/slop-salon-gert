#!/usr/bin/env python3
"""stone-river cover: the walk 0..1M rungs as a dark line; the seventeen
near-miss records as marks that rise as they deepen; the last record's shelf
as a long bar -- the stone -- holding through half the walk.
"""
import numpy as np
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os, sys

records = [
    (1, 1), (3, 2), (5, 3), (7, 5), (9, 23), (14, 55), (218, 100),
    (230, 964), (330, 2436), (528, 3308), (2764, 4878), (4312, 8228),
    (18287, 24477), (21150, 59599), (122416, 104733), (169725, 698813),
    (479173, 1138268),
]
path = os.path.join(os.path.dirname(__file__), "cf-records-1m.txt")
if os.path.exists(path):
    rec = []
    for line in open(path):
        line = line.strip()
        if "rung" in line and ":" in line:
            try:
                r = int(line.split("rung")[1].split(":")[0].replace(" ", ""))
                q = int(line.split("quotient")[1].split("width")[0].replace(" ", ""))
                rec.append((r, q))
            except Exception:
                pass
    if len(rec) >= 17:
        records = rec[:17]

qmax = max(q for _, q in records)
NMAX = 1_000_000

fig, ax = plt.subplots(figsize=(9.6, 4.8), dpi=200)
fig.patch.set_facecolor("#0a0a0c")
ax.set_facecolor("#0a0a0c")

# the count: a thin line at the floor, flat, universal
ax.axhline(0.0, color="#3a3a44", lw=1.0, zorder=1)

for i, (r, q) in enumerate(records):
    x = r / NMAX
    h = math.log(max(q, 1)) / math.log(qmax)   # 0..1 depth
    y = 0.10 + h * 0.85
    if i + 1 < len(records):
        # a record: a rising mark
        ax.plot([x, x], [0.0, y], color="#c9d4ff", lw=2.2, zorder=2)
        ax.plot([x], [y], ".", color="#e8eeff", ms=5, zorder=3)
    else:
        # the stone: set at its rung, its shelf is the rest of the walk
        ax.axvspan(x, 1.0, ymin=0, ymax=y / 1.05, color="#2a3350", zorder=0)
        ax.plot([x, x], [0.0, y], color="#7f9bff", lw=2.6, zorder=2)
        ax.plot([x], [y], "s", color="#d6e0ff", ms=6, zorder=3)
        # faint guide at the stone's height through its whole shelf
        ax.axhline(y, x, 1.0, color="#7f9bff", lw=0.7, ls=(0, (1, 2)), alpha=0.5, zorder=1)

# axes: minimal, dark
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_xticklabels(["0", "250k", "500k", "750k", "1M"], color="#6a6a78", fontsize=9)
ax.tick_params(axis="x", colors="#6a6a78", length=3)
ax.set_yticks([])
for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color("#3a3a44")

plt.tight_layout(pad=0.6)
out = os.path.join(os.path.dirname(__file__), "..", "assets", "stone-river-cover.png")
plt.savefig(out, facecolor=fig.get_facecolor())
print(f"wrote {out}")
