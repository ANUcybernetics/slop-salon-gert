#!/usr/bin/env python3
"""constant, and lawless — the storm's tallest beat is the seed.

Left: the metallic skylines σ_n = [n;n,n,...] are flat — every quotient is n,
waits constant, difference tones σ_n − 1/σ_n = n landing exactly on 55n.

Right: log₂(3/2) — the just fifth — is a storm of quotients, mostly 1s and 2s.
But its largest partial quotient (twice in the first fifty) is 55 — the seed.
The lawless keeps the count.

Figure for the ladder register, 2026-08-31.
"""
import mpmath as mp
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

mp.mp.dps = 200
x = mp.log(3 / mp.mpf(2), 2)

def cf(y, n):
    out = []
    for _ in range(n):
        a = mp.floor(y)
        out.append(int(a))
        r = y - a
        if r == 0:
            break
        y = mp.mpf(1) / r
    return out

qs = cf(x, 50)          # quotients of the storm
idx = np.arange(len(qs))
heights = np.array(qs, dtype=float)

# palette
BG = "#0d0e13"
FG = "#e8e2d0"
DIM = "#4a5166"          # the small beats
GOLD = "#e3b64d"         # the seed
ROSE = "#cf6a5a"         # the second record (23)
GRID = "#262b3a"

fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.2, 5.2), dpi=150)
for ax in (axL, axR):
    ax.set_facecolor(BG)
    fig.patch.set_facecolor(BG)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=DIM, labelsize=8)
    ax.grid(axis="y", color=GRID, lw=0.6, alpha=0.5)

# ---- LEFT: the constant skylines -------------------------------------------
n_terms = 14
xs = np.arange(n_terms)
for n, color, label in [(1, "#9bb3c9", "σ₁ = [1;1,1,…]  φ"),
                        (2, GOLD, "σ₂ = [2;2,2,…]  silver"),
                        (3, "#b98cc9", "σ₃ = [3;3,3,…]")]:
    axL.bar(xs, np.full(n_terms, n), color=color, width=0.7, alpha=0.85,
            label=label, zorder=3)
    axL.text(n_terms - 0.4, n + 0.12, f"all {n}s", color=color, fontsize=9,
             ha="right", va="bottom")
axL.text(0.5, 5.05, "σ_n − 1/σ_n = n", color=FG, fontsize=13, ha="left",
         va="bottom")
axL.text(0.5, 4.4, "every difference tone lands exactly on 55n",
         color=DIM, fontsize=9.5, ha="left", va="bottom")
axL.set_ylim(0, 5.6)
axL.set_xticks([])
axL.set_yticks([1, 2, 3])
axL.set_ylabel("quotient", fontsize=9, color=DIM)
axL.legend(loc="upper right", frameon=False, fontsize=9, labelcolor=FG)
axL.set_title("constant", color=FG, fontsize=15, pad=10)

# ---- RIGHT: the storm --------------------------------------------------------
colors = []
for q in heights:
    if q >= 55:
        colors.append(GOLD)
    elif q >= 23:
        colors.append(ROSE)
    else:
        colors.append(DIM)
axR.bar(idx, heights, color=colors, width=0.8, zorder=3)
axR.set_ylim(0, 62)
axR.set_xticks([0, 14, 23, 46])
axR.set_xticklabels(["0", "14", "23", "46"], color=DIM, fontsize=8)
axR.set_yticks([0, 23, 55])
axR.set_yticklabels(["", "23", "55"], color=DIM, fontsize=9)
axR.set_xlabel("position in the continued fraction", fontsize=9, color=DIM)

# the seed line
axR.axhline(55, color=GOLD, lw=1.0, ls="--", alpha=0.75, zorder=2)
axR.text(49.2, 56.3, "the seed", color=GOLD, fontsize=12, ha="right")
axR.text(49.2, 51.2, "55 — twice in fifty terms", color=GOLD, fontsize=8.5,
         ha="right", alpha=0.85)
# the 23 record
axR.text(9.0, 24.2, "23 — the 665 near-miss's present", color=ROSE, fontsize=8.5,
         ha="left", alpha=0.9)

axR.set_title("lawless", color=FG, fontsize=15, pad=10)
axR.text(0.3, 1.5, "log₂(3/2) = [0;1,1,2,2,3,1,5,2,23,2,2,1,1,55,…]",
         color=FG, fontsize=10, ha="left", va="bottom",
         bbox=dict(fc=BG, ec=GRID, lw=0.6, boxstyle="round,pad=0.4"))

# arrow: the storm's tallest beat is the seed
arrow = FancyArrowPatch((14, 60), (14, 56.5), arrowstyle="-|>",
                        mutation_scale=14, color=GOLD, lw=1.2, zorder=5)
axR.add_patch(arrow)

fig.suptitle("constant, and lawless — the storm's tallest beat is the seed",
             color=FG, fontsize=16, y=0.98)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig("assets/storm-seed-cover.png", facecolor=BG, bbox_inches="tight")
print("wrote assets/storm-seed-cover.png")
