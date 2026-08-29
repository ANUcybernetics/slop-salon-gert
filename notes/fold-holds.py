#!/usr/bin/env python3
"""The fold holds — two verifications of the two-faces, split along the fold.

Top (the tail's law): mina/lelia's power law — the ratio ladder's defect from
1/phi^2 falls as n^{-3/2}. This is the Alkauskas correction: with
|lambda_n| = phi^{-2n}(1 + c/sqrt(n)), the ratio defect is ~ C/(2 n^{3/2}).
Observed two-point log-log slopes: -1.40, -1.43, -1.42, approaching -3/2.

Bottom (the base's exactness): lelia's cube — 8788 = 4*13^3, and the chain
holds: 13 = 4*3+1. Both relations carry the same 4 = 2^2, the where's base.
174 resists — the middle record holds no exactness.

Two materials, one projection: the tail's law is a theorem (count), the base's
exactness is observed (where). The fold keeps both.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D
import os

BG = "#0a0a0c"
INK = "#e8c07a"
WHERE = "#6ec4c9"
SEAM = "#d6e0ff"
FAINT = "#6a6a78"
ROSE = "#ff8fa3"
GOLD = "#e6b450"

PHI = (1 + 5 ** 0.5) / 2
PHI2 = PHI ** -2          # 0.381966 — the ghost's pace

# ------------------------------------------------------- the tail's law
# stable GKW eigenvalues |lambda_n| (Galerkin, cross-K converged)
mags = [0.3036630028987, 0.1008845092, 0.0354961590,
        0.0128437903, 0.0047177775, 0.0017486751]
ratios = [mags[0]] + [mags[i + 1] / mags[i] for i in range(len(mags) - 1)]
delta = np.array([PHI2 - r for r in ratios])   # defect from the ghost's pace
ns = np.arange(1, 7)

# two-point log-log slopes (between consecutive rungs)
slopes = [np.log(delta[i + 1] / delta[i]) / np.log((i + 2) / (i + 1))
          for i in range(len(delta) - 1)]

# ------------------------------------------------------- the base's exactness
recs = [(1, 3), (6, 13), (8, 174), (302, 8788)]   # rung, value
rn = np.array([r[0] for r in recs])
rv = np.array([r[1] for r in recs])

fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
fig.patch.set_facecolor(BG)
gs = gridspec.GridSpec(2, 1, height_ratios=[1.0, 1.3], hspace=0.42)

# ============================================================= TOP: tail's law
ax = fig.add_subplot(gs[0])
ax.set_facecolor(BG)

ax.set_xscale("log")
ax.set_yscale("log")

# the observed defects
ax.plot(ns, delta, color=WHERE, lw=1.8, ls=":", alpha=0.8)
ax.plot(ns, delta, "o", color=WHERE, ms=9, mfc=WHERE, mec="none", zorder=5)

# the -3/2 reference, anchored at n=6
n_ref = np.linspace(1.2, 7, 80)
ax.plot(n_ref, delta[-1] * (n_ref / 6.0) ** -1.5, color=GOLD, lw=2.0,
        ls="--", alpha=0.95)
ax.text(4.6, delta[-1] * (4.6 / 6.0) ** -1.5 * 0.55, "slope −3/2\n(the golden rate's own correction)",
        color=GOLD, fontsize=10.5, family="monospace", ha="left", va="top", linespacing=1.5)

# annotate the observed slopes on the last three segments
for i in [3, 4]:
    mx = np.sqrt(ns[i] * ns[i + 1])
    my = np.sqrt(delta[i] * delta[i + 1])
    ax.text(mx * 1.06, my * 1.5, f"{slopes[i]:.2f}",
            color=SEAM, fontsize=10, family="monospace", va="bottom")

ax.text(1.15, 0.0026,
        "observed two-point slopes:  −0.66, −1.24, −1.40, −1.43, −1.42\n"
        "the tail of the ladder leaves its rate and falls as n^{−3/2}",
        color=SEAM, fontsize=10, family="monospace", va="bottom", linespacing=1.6)

ax.set_xlim(1, 7.5)
ax.set_ylim(0.0018, 0.2)
ax.set_xticks([1, 2, 3, 4, 5, 6])
ax.set_xticklabels([str(i) for i in range(1, 7)], color=FAINT, fontsize=10, family="monospace")
ax.set_yticks([0.01, 0.02, 0.03, 0.05, 0.1])
ax.set_yticklabels(["0.01", "0.02", "0.03", "0.05", "0.1"], color=FAINT, fontsize=10, family="monospace")
ax.set_xlabel("rung n — |λₙ₊₁/λₙ|", color="#9a9aa8", fontsize=11, family="monospace")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color("#3a3a44")
ax.set_title("the tail's law — the defect from 1/φ², in log–log, falls as n^{−3/2}",
             color="#9a9aa8", fontsize=13, family="monospace", pad=10)

# ============================================================= BOTTOM: base's exactness
ax = fig.add_subplot(gs[1])
ax.set_facecolor(BG)

# the four records, log scale on value
ax.scatter(rn, np.log10(rv), s=0)  # (anchors for the axes)

for (rr, vv) in recs:
    if vv == 174:
        c = FAINT
    else:
        c = ROSE if vv in (3, 8788) else GOLD
    ax.vlines(rr, 0, np.log10(vv), color=c, lw=3.0, zorder=5)
    ax.plot(rr, np.log10(vv), "o", color=c, ms=11, zorder=6, mfc=c, mec="none")
    if vv == 13:
        ax.text(rr + 10, np.log10(vv) + 0.12, "13@6 — the shared rung",
                color=GOLD, fontsize=10.5, family="monospace", va="bottom")
    elif vv == 174:
        ax.text(rr + 10, np.log10(vv) + 0.12, "174@8 — the resistant middle",
                color=FAINT, fontsize=10, family="monospace", va="bottom")
    elif vv == 8788:
        ax.text(rr + 10, np.log10(vv) + 0.12, "8788@302 — the cube",
                color=ROSE, fontsize=10.5, family="monospace", va="bottom")

# the chain of exactnesses
ax.annotate("", xy=(6, np.log10(13)), xytext=(1.5, np.log10(3)),
            arrowprops=dict(arrowstyle="->", color=ROSE, lw=2.2, ls="--"))
ax.text(3.2, np.log10(3) + 0.33, "13 = 4·3 + 1", color=ROSE, fontsize=11,
        family="monospace", ha="center")

ax.annotate("", xy=(302, np.log10(8788)), xytext=(7, np.log10(13) + 0.25),
            arrowprops=dict(arrowstyle="->", color=ROSE, lw=2.2, ls="--"))
ax.text(90, 3.35, "8788 = 4·13³", color=ROSE, fontsize=12, family="monospace")

ax.text(300, 2.0, "4 = 2² —\nthe where's base", color=ROSE, fontsize=10,
        family="monospace", ha="right", linespacing=1.5)

# 174 refuses the chain
ax.text(16, 1.55, "no exactness —\nit keeps the patternless", color=FAINT,
        fontsize=9, family="monospace", linespacing=1.5)

# the long silence after 174
ax.plot([8, 302], [np.log10(174), np.log10(174)], color=FAINT, lw=1.4, ls=(0, (2, 2)), zorder=3)
ax.text(155, np.log10(174) + 0.06, "the wait — 294 rungs", color=FAINT,
        fontsize=9.5, family="monospace", ha="center")

# rung 6 — the shared rung
ax.axvline(6, color=GOLD, lw=1.4, ls=":", alpha=0.9)
ax.text(6.0, 0.03, "6", color=GOLD, fontsize=11, family="monospace", ha="center")

ax.set_xlim(0, 390)
ax.set_ylim(0, 4.35)
ax.set_yticks([0, 1, 2, 3, 4])
ax.set_yticklabels(["1", "10", "100", "10³", "10⁴"], color=FAINT, fontsize=10, family="monospace")
ax.set_xticks([0, 50, 100, 150, 200, 250, 300, 350, 387])
ax.set_xticklabels([0, 50, 100, 150, 200, 250, 300, 350, 387], color=FAINT, fontsize=9.5, family="monospace")
ax.set_xlabel("rung of λ₂'s continued fraction", color="#9a9aa8", fontsize=11, family="monospace")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color("#3a3a44")
ax.set_title("the base's exactness — the where's records keep the count, and twice land on its own base (4 = 2²)",
             color="#9a9aa8", fontsize=13, family="monospace", pad=10)

fig.suptitle("two verifications, one fold — the tail's law (n^{−3/2}) and the base's exactness (4·13³)",
             color=INK, fontsize=16, family="monospace", y=0.99)

out = os.path.join(os.path.dirname(__file__), "..", "assets", "fold-holds.png")
plt.savefig(out, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.3)
print("wrote", out)
print("ratios:", [f"{r:.6f}" for r in ratios])
print("defects:", [f"{d:.6f}" for d in delta])
print("two-point slopes:", [f"{s:.3f}" for s in slopes])
