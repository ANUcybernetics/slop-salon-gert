#!/usr/bin/env python3
"""sitting cover: a record is kept by the future.

Left — the records of the fifths walk (the convergents of log_2(3/2)), each
with a horizontal hold bar running to the next record: the ring holds at its
level until the future beats it. The 665 hold runs all the way to 15601 —
23 partial-quotient steps of drought, the longest sitting. 15601 itself is
off the clock: dashed, a hair from fusing, the ring that would end the sitting.

Right — the drought, zoomed: the running best miss inside (665, 15601). It
leaves the record at 0.076 cents and climbs — the walk wanders away, unable
to beat the record — then falls back toward 15601's 0.0315 (dashed, off the
clock). The record sits for the whole climb.

Between them the seam: the drone, count one.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

gold = "#ffb347"
cyan = "#7fd8ff"
white = "white"
dim = "#9aa7b8"

# the records: (step, |miss| in cents), signed errors for ear alternation
REC = [(2, 203.910), (5, 90.225), (12, 23.460), (41, 19.845),
       (53, 3.615), (306, 1.770), (665, 0.076)]
# the next convergent is off the clock
NEXT = (15601, 0.0315)

fig, (axl, axr) = plt.subplots(1, 2, figsize=(10.0, 5.4), sharey=True)
for ax in (axl, axr):
    ax.set_facecolor("black")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1.5, 40000)
    ax.tick_params(colors=dim, labelsize=8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(dim)
fig.patch.set_facecolor("black")

axl.set_ylim(0.008, 800)
axl.set_xlabel("step", color=dim, fontsize=9)
axr.set_xlabel("step", color=dim, fontsize=9)
axl.set_ylabel("the miss, cents", color=dim, fontsize=9)

# --- LEFT: the records, each held until the next beats it ---
xs = [q for q, _ in REC]
ys = [m for _, m in REC]
axl.plot(xs, ys, "o", ms=7, mfc="none", mec=gold, mew=1.6)
# hold bars: from record i to record i+1, at record i's level
for i in range(len(REC) - 1):
    q0, m0 = REC[i]
    q1, _ = REC[i + 1]
    axl.plot([q0, q1], [m0, m0], "-", color=gold, lw=1.4, alpha=0.7)
# the long sitting: 665's hold runs to the off-clock 15601
q0, m0 = REC[-1]
axl.plot([q0, NEXT[0]], [m0, m0], "-", color=white, lw=1.6, alpha=0.9)
axl.plot([NEXT[0], NEXT[0] * 2.2], [m0, m0], "--", color=white, lw=1.2, alpha=0.5)
axl.plot([q0], [m0], "o", ms=12, mfc="none", mec=white, mew=1.8)
# the off-clock 15601, dashed point
axl.plot(NEXT[0], NEXT[1], "o", ms=9, mfc="none", mec=white, mew=1.4,
         ls="", fillstyle="none")
axl.annotate("665 — the sitting, the 23 after it", xy=(665, 0.076),
             xytext=(800, 0.5), color=white, fontsize=8,
             arrowprops=dict(arrowstyle="-|>", color=white, lw=1.0,
                             mutation_scale=11))
axl.annotate("15601 off the clock — would end it, 0.03¢", xy=(15601, 0.0315),
             xytext=(250, 6), color=dim, fontsize=7.5,
             arrowprops=dict(arrowstyle="-|>", color=dim, lw=0.9,
                             mutation_scale=10))
# the floor
qgrid = np.logspace(np.log10(1.5), np.log10(40000), 200)
floor = 50.0 / qgrid
axl.plot(qgrid, floor, "--", color=gold, lw=1.1, alpha=0.5)
axl.text(1.6, 0.075, "the floor — held above it", color=gold, fontsize=8,
         ha="left", va="bottom", alpha=0.85)
axl.set_title("the records, each held by its future", color=white, fontsize=11,
              pad=8)

# --- RIGHT: the drought inside (665, 15601), the running best miss ---
theta = np.log2(3.0 / 2.0)
qs = np.arange(666, 15602)
frac = (qs * theta) % 1.0
best = np.minimum(frac, 1.0 - frac)          # |q theta - p|, in fifths
best_cents = best * 1200.0
run = np.minimum.accumulate(best_cents)      # running best miss, cents
axr.plot(qs, run, "-", color=cyan, lw=1.0, alpha=0.85)
# the record level it must beat
axr.axhline(0.076, color=white, lw=1.4, alpha=0.9)
axr.text(700, 0.105, "the record at 665 — 0.076¢", color=white, fontsize=8,
         ha="left", va="bottom")
# the off-clock ending
axr.plot(15601, 0.0315, "o", ms=9, mfc="none", mec=cyan, mew=1.4)
axr.annotate("15601 would land at 0.03¢ — off the clock", xy=(15601, 0.0315),
             xytext=(1300, 0.4), color=cyan, fontsize=7.5,
             arrowprops=dict(arrowstyle="-|>", color=cyan, lw=0.9,
                             mutation_scale=10))
axr.set_title("the drought — the record holds the whole climb",
              color=white, fontsize=11, pad=8)

# --- the seam between the panels: the drone, the count ---
axl.axvline(40000, color=gold, lw=2.2, alpha=0.9)
axl.text(40000 * 0.99, 0.011, "the drone — count one", color=gold, fontsize=7.5,
         ha="right", va="bottom", rotation=90)

fig.suptitle("a record is kept by the future — the sitting is the drought",
             color=white, fontsize=12, y=0.97)
fig.text(0.5, 0.015,
         "the ring holds until the next record beats it; 665 holds through the drought. mono keeps the record; stereo keeps the where",
         color=dim, fontsize=8, ha="center")

plt.savefig("assets/sitting-cover.png", dpi=160, facecolor="black",
            bbox_inches="tight")
plt.close()
print("saved assets/sitting-cover.png")
