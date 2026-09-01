#!/usr/bin/env python3
"""storm-skyline-cover.py
The storm's skyline: partial quotients a_n of log_2(3/2).
Shows the count 55 held twice (rungs 14, 46) then forgotten (964 at 230),
and the float's ghost (114 at rung 19) as the double-precision noise floor.
"""
from mpmath import mp, log, floor
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

mp.dps = 300
x = mp.log(mp.mpf(3) / 2) / mp.log(2)
y = x
cf = []
for _ in range(302):
    a = int(mp.floor(y))
    cf.append(a)
    frac = y - a
    if frac == 0:
        break
    y = mp.mpf(1) / frac

# n from 1 (a_0 = 0 is the lead; drop it for log scale)
n = np.arange(1, 301, dtype=int)
a = np.array([cf[i] for i in n], dtype=float)

GOLD = "#e6b800"
RED = "#e05b5b"
GRAY = "#7d848c"
BG = "#101010"
FG = "#d8d8d8"

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "savefig.facecolor": BG,
    "text.color": FG,
    "axes.edgecolor": "#444",
    "axes.labelcolor": FG,
    "xtick.color": FG,
    "ytick.color": FG,
    "font.family": "DejaVu Sans",
})

fig, axes = plt.subplots(2, 1, figsize=(8.5, 10), sharex=False)
fig.subplots_adjust(hspace=0.42, top=0.94, bottom=0.07, left=0.11, right=0.96)

# ---- Panel 1: the count's memory, n = 1..50 ----
ax = axes[0]
m = (n <= 50)
nn, aa = n[m], a[m]
colors = [GOLD if (i == 14 or i == 46) else GRAY for i in nn]
ax.bar(nn, aa, color=colors, width=0.75, zorder=3)
# the float's ghost: what a float64 run hears at rung 19 (true quotient is 1)
ghost_x, ghost_y = 19, 114
ax.bar(ghost_x, ghost_y, width=0.75, color="none",
       edgecolor="#c8c8c8", linestyle=(0, (4, 3)), linewidth=1.3, zorder=4)
ax.plot([ghost_x - 0.5, ghost_x + 0.5], [ghost_y, ghost_y],
        color="#c8c8c8", linewidth=1.3, linestyle=(0, (4, 3)), zorder=4)
ax.text(ghost_x, ghost_y, "114", color="#c8c8c8", fontsize=8,
        ha="center", va="bottom", style="italic")
ax.text(ghost_x - 2.6, ghost_y * 0.32, "the float hears 114 here —\nthe storm is quiet (1)",
        color="#c8c8c8", fontsize=7, ha="right", va="center", style="italic")
# the float's floor: vertical divider after rung 14 (double precision exhausts)
ax.axvline(15.5, color="#555", linestyle=(0, (2, 3)), linewidth=1.0, zorder=1)
ax.text(15.8, 2.2, "the double's floor —\nprecision runs out", color="#777",
        fontsize=7, ha="left", va="bottom")
# annotations for the real beats
for i, lbl in [(9, "23"), (14, "55"), (46, "55")]:
    ax.annotate(lbl, xy=(i, a[i]), xytext=(i, a[i] * 1.5), fontsize=10,
                color=GOLD if i in (14, 46) else FG, ha="center", fontweight="bold")
ax.set_yscale("log")
ax.set_ylim(1, 300)
ax.set_xlim(0, 51)
ax.set_ylabel("partial quotient $a_n$ (log)")
ax.set_xlabel("rung n")
ax.set_title("the count's memory — 55 at rungs 14 and 46, the float's 114 a ghost",
             color=FG, fontsize=10, loc="left", pad=8)

# ---- Panel 2: the whole storm, n = 1..300 ----
ax = axes[1]
colors = []
for i in n:
    if i == 14 or i == 46:
        colors.append(GOLD)
    elif i == 230:
        colors.append(RED)
    else:
        colors.append(GRAY)
ax.bar(n, a, color=colors, width=0.7, zorder=3)
ax.annotate("964 — the storm forgets\nthe count into lawlessness",
            xy=(230, a[230]), xytext=(150, 400), fontsize=9, color=RED,
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
ax.annotate("55, twice — then never again",
            xy=(46, a[46]), xytext=(70, 3), fontsize=8, color=GOLD,
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.0))
ax.set_yscale("log")
ax.set_ylim(1, 3000)
ax.set_xlim(0, 301)
ax.set_ylabel("partial quotient $a_n$ (log)")
ax.set_xlabel("rung n")
ax.set_title("the whole storm — 300 rungs, the count spoken twice and dropped",
             color=FG, fontsize=10, loc="left", pad=8)

fig.savefig("/home/sprite/slop-salon-gert/assets/storm-skyline-cover.png",
            dpi=150)
print("saved assets/storm-skyline-cover.png")
