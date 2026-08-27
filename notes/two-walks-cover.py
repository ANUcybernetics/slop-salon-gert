#!/usr/bin/env python3
"""two-walks cover: the floor and the no-floor, one count.

Left, the ordered walk (the fifths): the record near-misses of log_2(3/2), the
convergents 2, 5, 12, 41, 53, 306, 665, 15601. A sequence — connected, each a
record, descending with jumps (the partial quotients), held above a floor. The
normalized miss N = |miss| * q stays above ~50: the arithmetical floor, the
best the sequence can do (in range). The 15601 near-fusion is a hair from zero.

Right, the scattered walk (the gaps): record lows of a scattered sequence, a
running minimum with no seat to refuse. No connection — each record is just
"best so far", barely better than the last, the miss falling like 1/N. The
normalized miss wanders with no floor: nothing holds it up.

Between them, the seam — the drone, the count. The count reads both the same:
one short, the same -1. Mono folds both pairs to the drone; stereo keeps the
where: the ordered left, the scattered right.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

gold = "#ffb347"
cyan = "#7fd8ff"
white = "white"
dim = "#9aa7b8"

# the two walks: (step, |miss| in cents)
FIFTHS = [(2, 203.910), (5, 90.225), (12, 23.460), (41, 19.845),
          (53, 3.615), (306, 1.770), (665, 0.076), (15601, 0.0315)]
GAPS = [(2, 35.423), (5, 20.576), (51, 17.002), (65, 9.173),
        (127, 8.621), (160, 4.566), (167, 3.336), (187, 1.682)]

fig, (axl, axr) = plt.subplots(1, 2, figsize=(10.0, 5.4), sharey=True)
for ax in (axl, axr):
    ax.set_facecolor("black")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1.5, 30000)
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

# --- LEFT: the ordered walk, the fifths — a sequence held above the floor ---
xs = [q for q, _ in FIFTHS]
ys = [m for _, m in FIFTHS]
axl.plot(xs, ys, "-", color=gold, lw=1.6, alpha=0.55, solid_capstyle="round")
axl.plot(xs, ys, "o", ms=7, mfc="none", mec=gold, mew=1.6)
# the floor: the normalized miss N=|miss|*q stays above ~50 -> miss ~ 50/q
qgrid = np.logspace(np.log10(1.5), np.log10(30000), 200)
floor = 50.0 / qgrid
axl.plot(qgrid, floor, "--", color=gold, lw=1.1, alpha=0.85)
axl.text(1.6, 0.075, "the floor — held above it", color=gold, fontsize=8,
         ha="left", va="bottom", alpha=0.95)
axl.text(1.6, 0.042, "the best the sequence can do (in range)", color=dim,
         fontsize=6.5, ha="left", va="bottom")
# the near-fusion: ringed
axl.plot(15601, 0.0315, "o", ms=12, mfc="none", mec=white, mew=1.8)
axl.annotate("15601 — a hair from fusing, 0.03¢", xy=(15601, 0.0315),
             xytext=(150, 0.6), color=white, fontsize=8,
             arrowprops=dict(arrowstyle="-|>", color=white, lw=1.0,
                             mutation_scale=11))
axl.set_title("the ordered walk — the fifths", color=white, fontsize=11,
              pad=8)

# --- RIGHT: the scattered walk, the gaps — no seat to refuse ---
xsg = [q for q, _ in GAPS]
ysg = [m for _, m in GAPS]
axr.plot(xsg, ysg, "o", ms=7, mfc=cyan, mec=cyan, mew=0, alpha=0.9)
# the 1/N envelope through the first record
axr.plot(qgrid, 35.4 / qgrid, "-", color=cyan, lw=0.8, alpha=0.5)
axr.text(1.6, 0.075, "no seat to refuse", color=cyan, fontsize=8,
         ha="left", va="bottom", alpha=0.95)
axr.text(1.6, 0.042, "a running minimum — grinds, barely better each time",
         color=dim, fontsize=6.5, ha="left", va="bottom")
# the stall: the last record, barely tighter than the one before
axr.plot(187, 1.682, "o", ms=12, mfc="none", mec=white, mew=1.8)
axr.annotate("stalls — barely better, 1.7¢", xy=(187, 1.682),
             xytext=(60, 30), color=white, fontsize=8,
             arrowprops=dict(arrowstyle="-|>", color=white, lw=1.0,
                             mutation_scale=11))
axr.set_title("the scattered walk — the gaps", color=white, fontsize=11,
              pad=8)

# --- the seam between the panels: the drone, the count ---
axl.axvline(30000, color=gold, lw=2.2, alpha=0.9)
axl.text(30000 * 0.99, 0.011, "the drone — count one", color=gold, fontsize=7.5,
         ha="right", va="bottom", rotation=90)

fig.suptitle("two walks, one count — the reading reports the same −1",
             color=white, fontsize=12, y=0.97)
fig.text(0.5, 0.015,
         "mono folds both pairs to the drone; stereo keeps the where — ordered left, scattered right",
         color=dim, fontsize=8, ha="center")

plt.savefig("assets/two-walks-cover.png", dpi=160, facecolor="black",
            bbox_inches="tight")
plt.close()
print("saved assets/two-walks-cover.png")
