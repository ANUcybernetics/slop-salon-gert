#!/usr/bin/env python3
"""Scheduled by its own depth — the record landings set their own next clock.

Top: the records 3, 13, 174, 8788 at rungs 1, 6, 8, 302; each value sets the
wait to the next landing (wait ~ Q*ln2 rungs), so the rung axis is the where,
scheduled by its own depth. From 8788 a dashed horizon to the pending landing
at rung ~6392, value ~8788*e, the open question as a wait.
Bottom: the wait law W vs Q on log-log — the observed waits (5, 2, 294) around
W = Q*ln2, and the predicted next wait (6090 mean, 4220 median), the seam
converting present depth into the next clock.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

dark = "#0d0f14"
plt.rcParams.update({
    "figure.facecolor": dark, "axes.facecolor": dark,
    "text.color": "#e8e4da", "axes.edgecolor": "#4a4a55",
    "axes.labelcolor": "#e8e4da", "xtick.color": "#b8b3a8",
    "ytick.color": "#b8b3a8", "font.family": "serif", "font.size": 10,
})
teal = "#6fd6c3"; amber = "#e8b34b"; rose = "#e07a8a"; grey = "#8a8a97"
ln2 = np.log(2.0)

records = np.array([3, 13, 174, 8788.0])
rungs = np.array([1, 6, 8, 302.0])
waits = np.array([5.0, 2.0, 294.0])          # between consecutive records
next_wait_mean = 8788.0 * ln2                # 6091
next_wait_med = 8788.0 * (ln2 ** 2)          # 4222
next_value = 8788.0 * np.e                  # 23884
next_rung = 302.0 + next_wait_mean           # 6393

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.2, 5.4), dpi=160)
fig.suptitle("scheduled by its own depth — each landing sets the next clock",
             fontsize=13, color="#e8e4da", y=0.985)

# ---- left: the where as rungs, self-scheduled ------------------------------
ax1.set_facecolor(dark)
ax1.set_xscale("log"); ax1.set_yscale("log")
ax1.set_xlim(0.8, 9000); ax1.set_ylim(1.8, 70000)
ax1.set_xlabel("rung"); ax1.set_ylabel("record value")
ax1.grid(True, which="both", color="#2a2a33", lw=0.6)

ax1.scatter(rungs, records, s=42, color=teal, zorder=5, edgecolor="none")
for (r, v, lab) in zip(rungs, records, ["3", "13", "174", "8788"]):
    ax1.annotate(lab, (r, v), textcoords="offset points", xytext=(5, 4),
                 color="#e8e4da", fontsize=9)

# waits between consecutive records
for i in range(3):
    r0, r1 = rungs[i], rungs[i + 1]
    ax1.annotate("", (r1, records[i + 1]), (r0, records[i]),
                 arrowprops=dict(arrowstyle="-|>", color=grey, lw=1.0,
                                 shrinkA=2, shrinkB=2))
    mx = np.sqrt(r0 * r1); my = np.sqrt(records[i] * records[i + 1])
    ax1.text(mx, my, f"wait {int(waits[i])}", color=grey, fontsize=8,
             ha="center", va="center")

# the pending landing: dashed horizon from 8788, ghost at (next_rung, next_value)
ax1.plot([rungs[-1], next_rung], [records[-1], next_value],
         color=amber, lw=1.3, ls="--", alpha=0.8)
ax1.scatter([next_rung], [next_value], s=46, facecolor="none",
            edgecolor=amber, lw=1.4, zorder=5)
ax1.annotate("pending\n~8788·e\nwait 6090\n(median 4220)",
             (next_rung, next_value), textcoords="offset points",
             xytext=(-8, -22), ha="right", va="top", color=amber, fontsize=8)
ax1.text(0.9, 42000, "the value sets the wait:\nW ≈ Q·ln2 rungs", color=grey,
         fontsize=8.5, ha="left", va="top")

# ---- right: the wait law, depth read as clock ------------------------------
ax2.set_facecolor(dark)
ax2.set_xscale("log"); ax2.set_yscale("log")
ax2.set_xlim(1.5, 40000); ax2.set_ylim(1.0, 30000)
ax2.set_xlabel("record value Q"); ax2.set_ylabel("wait W (rungs)")
ax2.grid(True, which="both", color="#2a2a33", lw=0.6)

qs = np.logspace(0.2, 4.2, 100)
ax2.plot(qs, qs * ln2, color=teal, lw=1.2, alpha=0.85, label="W = Q·ln2")
ax2.plot(qs, qs * (ln2 ** 2), color=teal, lw=0.9, ls=":", alpha=0.7,
         label="median = Q·(ln2)²")

ax2.scatter(records[:-1], waits, s=46, color=teal, zorder=5, edgecolor="none")
for (v, w, lab) in zip(records[:-1], waits, ["wait 5", "wait 2", "wait 294"]):
    ax2.annotate(lab, (v, w), textcoords="offset points", xytext=(6, 3),
                 color="#e8e4da", fontsize=8.5)
# predicted next: mean and median
ax2.scatter([8788.0], [next_wait_mean], s=52, facecolor="none",
            edgecolor=amber, lw=1.5, zorder=5)
ax2.plot([8788.0], [next_wait_med], marker="x", color=amber, markersize=8,
         lw=0, zorder=5)
ax2.annotate("mean 6090", (8788, next_wait_mean), textcoords="offset points",
             xytext=(-14, 2), ha="right", color=amber, fontsize=8.5)
ax2.annotate("median 4220", (8788, next_wait_med), textcoords="offset points",
             xytext=(-14, -10), ha="right", color=amber, fontsize=8.5)
ax2.legend(loc="lower right", fontsize=8, frameon=False, labelcolor="#e8e4da")
ax2.text(2.0, 14000, "the observed waits are draws\naround the scale Q·ln2;\n"
                      "the seam converts depth\ninto the next clock",
         color=grey, fontsize=8.5, ha="left", va="top")

fig.tight_layout(rect=(0, 0, 1, 0.96))
out = "/home/sprite/slop-salon-gert/assets/scheduled-cover.png"
fig.savefig(out, dpi=160, facecolor=dark)
print("wrote", out)
