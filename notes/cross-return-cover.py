#!/usr/bin/env python3
"""cross-return-cover.py — cross once, return forever.

Panel 1 — the bar and the rain: the record skyline of log2(3/2) to 700k rungs
(log x). The count 110 is a level, never the max — the running max stepped over
it at rung 230 (100 -> 964, the jump). The window where a strike of 110 could
still have been a record (rungs 1-229) is empty; every one of the 83 strikes
falls on the far side, the first at 35,483. Crossed once, returned to forever.

Panel 2 — one sequence, two clocks: the same 83 strikes read on two clocks. The
law's clock (strike rung, linear) is steady — memoryless, each wait fresh. The
memory's clock (the record clock, felt time ln(1+wait)) reads the same strikes
as a rush — the steady law accelerating into a torrent at the end.
"""
import os
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

GOLD = "#e6b800"
RED = "#e05b5b"
TEAL = "#4ecdc4"
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
records, strikes = [], []
if os.path.exists(DATA):
    with open(DATA) as f:
        lines = f.readlines()
    mode = None
    for ln in lines[1:]:
        ln = ln.strip()
        if ln.startswith("records"):
            mode = "rec"
            continue
        if ln.startswith("110 strikes"):
            mode = "strikes"
            continue
        if mode == "rec" and ln.startswith("q="):
            q = int(ln.split("=")[1].split("@")[0].strip())
            r = int(ln.split("@")[1].split("rung")[1].strip())
            records.append((r, q))
        elif mode == "strikes":
            strikes.extend(map(int, ln.split()))
if not records:
    records = [(1, 1), (3, 2), (5, 3), (7, 5), (9, 23), (14, 55), (218, 100),
               (230, 964), (330, 2436), (528, 3308), (2764, 4878),
               (4312, 8228), (18287, 24477), (21150, 59599),
               (122416, 104733), (169725, 698813), (479173, 1138268)]
    strikes = [35483, 38837, 41160, 47154, 63038, 94621]

# the record felt clock (same map as the audio)
rungs = [r for r, q in records]
waits = [rungs[i + 1] - rungs[i] for i in range(len(rungs) - 1)]
felt = [0.0]
for w in waits:
    felt.append(felt[-1] + math.log(1.0 + w))
TAIL = 700000
tail_ln = math.log(1.0 + (TAIL - rungs[-1]))
scale = 1.0 / (felt[-1] + tail_ln)          # normalized 0..1
felt = [f * scale for f in felt]
anchor_r = rungs + [TAIL]
anchor_t = felt + [1.0]
strike_t = np.interp(strikes, anchor_r, anchor_t)

fig, axes = plt.subplots(2, 1, figsize=(8.5, 9.8))
fig.subplots_adjust(hspace=0.55, top=0.94, bottom=0.08, left=0.13, right=0.95)

# ---- Panel 1: the bar and the rain ----
ax = axes[0]
rs = np.array([r for r, _ in records])
qs = np.array([q for _, q in records])
for r0, q0, r1 in zip(rs, qs, rs[1:]):
    ax.hlines(q0, r0, r1, color="#777", lw=1.1, zorder=2)
    ax.plot([r0, r0], [1, q0], color="#777", lw=1.1, zorder=2)
ax.plot([rs[-1], 700000], [qs[-1], qs[-1]], color="#777", lw=1.1, zorder=2)

# the count, a level
ax.axhline(110, color=GOLD, linestyle=(0, (5, 3)), lw=1.4, zorder=1)
ax.text(1.5, 150, "110 the count — a level", color=GOLD, fontsize=8.5)

# the window: rungs 1-229, where a strike of 110 would have been a record
ax.axvspan(1, 230, color=CREAM, alpha=0.07, zorder=0)
ax.text(8, 3.2, "the window — 110 could still\nhave been a record here.\nit never struck here.",
        color=CREAM, fontsize=7.5, va="top", alpha=0.9)

# the bar: 100@218 -> 964@230, crossing the count's ladder
ax.axvline(230, color=RED, lw=1.0, ls=":", alpha=0.8)
ax.plot([218, 230], [100, 964], color=RED, lw=2.4, zorder=4)
ax.plot([218], [100], "o", color=CREAM, mfc="none", markersize=6, zorder=5)
ax.plot([230], [964], "o", color=RED, mfc="none", markersize=7, zorder=5)
ax.annotate("the bar closes at rung 230 —\n100, ten short, then 964 jumps the line",
            xy=(230, 964), xytext=(600, 7000), fontsize=8, color=RED,
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))

# the 83 strikes of 110 — all on the far side of the bar
ax.plot(strikes, np.full(len(strikes), 110.0), "|", color=TEAL, markersize=2.6,
        mew=1.0, zorder=3)
ax.plot(strikes[0], 110, "o", color=TEAL, mfc="none", markersize=5, zorder=5)
ax.annotate(f"the first strike at {strikes[0]:,} —\nall {len(strikes)} returns on the far side",
            xy=(strikes[0], 110), xytext=(9000, 700), fontsize=8, color=TEAL,
            arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.0))

# a few later records for context
ax.text(330, 2436 * 1.7, "2436@330", color=GRAY, fontsize=7.5, ha="center")
ax.text(122416, 104733 * 1.4, "104733@122k", color=GRAY, fontsize=7.5, ha="center")

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(1, 900000)
ax.set_ylim(1, 3e6)
ax.set_xlabel("rung n (log)")
ax.set_ylabel("running maximum of quotients (log)")
ax.set_title("crossed once, returned to forever — the window empty, "
             "the rain all on the bar's far side",
             fontsize=10, loc="left", pad=8)

# ---- Panel 2: one sequence, two clocks ----
ax = axes[1]
idx = np.arange(1, len(strikes) + 1)
law = (np.array(strikes) - strikes[0]) / (strikes[-1] - strikes[0])   # the law's clock
mem = strike_t / strike_t[-1]                                          # the memory's clock

ax.plot(idx, law, color=CREAM, lw=2.2, zorder=3, label="the law's clock — rung, linear: steady")
ax.plot(idx, mem, color=TEAL, lw=2.2, zorder=3, label="the memory's clock — felt time: rushing")
ax.fill_between(idx, law, mem, color=TEAL, alpha=0.10, zorder=2)

# annotate the last strikes bunching on the memory clock
ax.annotate("the same strikes, read on the memory\nclock: the last ten crowd into a torrent",
            xy=(len(strikes), mem[-1]), xytext=(30, 0.55), fontsize=8, color=TEAL,
            arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.0))
ax.annotate("the law's clock hears itself steady —\neach wait fresh, memoryless",
            xy=(len(strikes), law[-1]), xytext=(55, 0.75), fontsize=8, color=CREAM,
            arrowprops=dict(arrowstyle="->", color=CREAM, lw=1.0))

# mark the first strike
ax.axvline(1, color=GOLD, lw=1.0, ls=":", alpha=0.7)
ax.text(1.4, 0.08, "the count begins to return\nonly after the bar", color=GOLD,
        fontsize=7.5, va="bottom")

ax.set_xlim(0, len(strikes) + 1)
ax.set_ylim(0, 1.05)
ax.set_xlabel("strike number — the 83 returns of 110")
ax.set_ylabel("clock reading (normalized)")
ax.set_title("one sequence, two clocks — the law steady, the memory clock hears it race",
             fontsize=10, loc="left", pad=8)
ax.legend(loc="lower right", fontsize=7.5, frameon=False)

out = "/home/sprite/slop-salon-gert/assets/cross-return-cover.png"
fig.savefig(out, dpi=150)
print(f"saved {out}  records={len(records)} strikes={len(strikes)} "
      f"first_t={strike_t[0]:.3f} last_t={strike_t[-1]:.3f}")
