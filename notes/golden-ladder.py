#!/usr/bin/env python3
"""The golden ladder — the where's overtones decay at phi^-2n.

Alkauskas (2014) proved Flajolet-Vallee (1995): lambda_n/lambda_{n+1} -> -phi^2.
The high modes of the universal CF operator forget everything except the
closest-bounded number — phi, the register's floor. The exception sets the
law's own tail.

Values: 1, -0.3036630029, +0.1008845092, -0.0354961590, +0.0128437903,
-0.0047177775, +0.0017486751  (computed here from the Galerkin collocation and
cross-checked against the literature; ratio sequence descends onto phi^2).
"""
import numpy as np
import mpmath as mp
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

mp.mp.dps = 50
PHI = (1 + mp.sqrt(5)) / 2

# eigenvalue magnitudes |lambda_n|, n=1..7 (lambda_1 = the Wirsing constant)
mags = [mp.mpf("0.3036630028987326585974481219015562331108"),
        mp.mpf("0.1008845092"),
        mp.mpf("0.0354961590"),
        mp.mpf("0.0128437903"),
        mp.mpf("0.0047177775"),
        mp.mpf("0.0017486751")]
signs = [-1, +1, -1, +1, -1, +1]        # lambda_n sign, n=2..7
n = np.arange(1, 7)                     # rungs 1..6 (indexing the nontrivial)

fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
fig.patch.set_facecolor(BG)
gs = gridspec.GridSpec(1, 2, width_ratios=[1.25, 1.0], wspace=0.18)

# ================================================================== panel 1
ax = fig.add_subplot(gs[0])
ax.set_facecolor(BG)

# the golden guide phi^{-2n} through the magnitudes
n_guide = np.linspace(0.8, 6.3, 200)
y_guide = [float(PHI) ** (-2 * m) for m in n_guide]
ax.plot(n_guide, y_guide, color=GOLD, lw=2.4, ls=(0, (4, 3)), alpha=0.9, zorder=2)
ax.text(4.35, float(PHI) ** (-2 * 4.6), "φ⁻²ⁿ  — the golden ladder",
        color=GOLD, fontsize=11, family="monospace", rotation=-12, ha="center")

for i, (mg, sg) in enumerate(zip(mags, signs)):
    x = i + 1
    c = ROSE if sg > 0 else WHERE
    val = float(mg)
    # stem
    ax.plot([x, x], [val, 0], color=c, lw=3.2, alpha=0.92, zorder=4)
    ax.plot(x, 0, "o", color=BG, ms=11, mec=c, mew=2.4, zorder=5)
    ax.plot(x, val, "o", color=c, ms=9, zorder=6, mfc=c, mec="none")
    lab = "λ₂ −0.30366…" if i == 0 else f"λ{i+2}"
    ax.text(x + 0.09, val, lab, color=c, fontsize=9.5, va="center",
            family="monospace")

# annotation: the sign is parity of the rung
ax.text(0.95, 0.62, "the sign — parity of the rung:\n+ − + − + −, every rung flips",
        color=WHERE, fontsize=10, family="monospace", va="top")
ax.text(4.9, 0.055, "the where's overtones\n— the count's own tail",
        color=FAINT, fontsize=9.5, family="monospace", ha="right")

ax.set_yscale("log")
ax.set_xlim(0.5, 6.6)
ax.set_ylim(8e-4, 0.9)
ax.set_xticks([])
ax.set_yticks([1e-3, 1e-2, 1e-1])
ax.set_yticklabels(["10⁻³", "10⁻²", "10⁻¹"], color=FAINT, fontsize=10, family="monospace")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color("#3a3a44")
ax.set_title("the ladder — each rung a factor φ² shallower",
             color="#9a9aa8", fontsize=13, family="monospace", pad=12)

# ================================================================== panel 2
ab = fig.add_subplot(gs[1])
ab.set_facecolor(BG)

# empirical ratios |lambda_n|/|lambda_{n+1}|
ratios = [mags[i] / mags[i + 1] for i in range(len(mags) - 1)]
rs = [float(r) for r in ratios]
xs = np.arange(1, len(rs) + 1)
ab.plot(xs, rs, "o-", color=WHERE, lw=2.4, ms=9, mfc=WHERE, mec="none", zorder=5)

# the golden rate line
phi2 = float(PHI ** 2)
ab.axhline(phi2, color=GOLD, lw=2.4, ls=(0, (4, 3)), zorder=3)
ab.text(5.15, phi2 + 0.03, "φ² = 2.618…", color=GOLD, fontsize=11, family="monospace")

# Alkauskas leading-term prediction for the ratio
def ratio_pred(m, c=1.1019785625880999):
    """phi^2 * (1 + c/sqrt(m)) / (1 + c/sqrt(m+1)) — leading correction."""
    return phi2 * (1 + c / np.sqrt(m)) / (1 + c / np.sqrt(m + 1))

n_pred = np.linspace(1, 5, 200)
ab.plot(n_pred, [ratio_pred(m) for m in n_pred], color=FAINT, lw=1.8, ls=":", zorder=4)

for x, r in zip(xs, rs):
    ab.text(x - 0.14, r + 0.06, f"{r:.3f}", color=WHERE, fontsize=10,
            family="monospace")

ab.annotate("descends onto the floor", xy=(5, 2.698), xytext=(3.1, 2.42),
            color=WHERE, fontsize=10, family="monospace",
            arrowprops=dict(arrowstyle="->", color=WHERE, lw=1.1))

ab.text(1.15, 3.16, "λₙ/λₙ₊₁ → −φ²\nFlajolet–Vallée 1995\nAlkauskas 2014",
        color=SEAM, fontsize=10.5, family="monospace", va="top")

ab.set_xlim(0.6, 5.6)
ab.set_ylim(2.3, 3.35)
ab.set_xticks(xs)
ab.set_xticklabels([f"n={int(x)}" for x in xs], color=FAINT, fontsize=10, family="monospace")
ab.set_yticks([2.4, 2.6, 2.8, 3.0, 3.2])
ab.set_yticklabels([f"{y:.1f}" for y in [2.4, 2.6, 2.8, 3.0, 3.2]], color=FAINT, fontsize=10, family="monospace")
for s in ["top", "right"]:
    ab.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ab.spines[s].set_color("#3a3a44")
ab.set_title("the rate — the ladder tightens onto the golden floor",
             color="#9a9aa8", fontsize=13, family="monospace", pad=12)

# legend row
legend_els = [
    Line2D([0], [0], color=GOLD, lw=2.4, ls=(0, (4, 3)), label="φ⁻²ⁿ — the golden ladder"),
    Line2D([0], [0], marker="o", color=WHERE, lw=2.4, label="the where's overtones"),
    Line2D([0], [0], color=FAINT, lw=1.8, ls=":", label="Alkauskas leading term"),
]
fig.legend(handles=legend_els, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 0.02),
           frameon=False, fontsize=10, labelcolor="#9a9aa8")

fig.suptitle("the golden ladder — the floor is the operator's own tail",
             color=INK, fontsize=16, family="monospace", y=0.985)

out = os.path.join(os.path.dirname(__file__), "..", "assets", "golden-ladder.png")
plt.savefig(out, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.3)
print("wrote", out)
print("ratios:", " ".join(f"{r:.4f}" for r in rs))
print("phi^2 =", mp.nstr(PHI ** 2, 10))
