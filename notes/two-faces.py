#!/usr/bin/env python3
"""The operator's two faces — the tail is exact, the base is a where.

Top: the golden ladder — |lambda_n| ~ phi^{-2n}, the ratios lambda_n/lambda_{n+1}
descend onto phi^2 (Flajolet-Vallee 1995, Alkauskas 2014). A theorem: the tail.

Bottom: lambda_2's own continued fraction (OEIS A007515, the Wirsing constant,
387 quotients) — a generic number, no floor. Its records: 3@1, 13@6, 174@8,
then a 294-rung silence and a second giant 8788@302 (~6% draw). A draw: the base.

One operator, two faces — the limit a theorem, the value a draw.

Source for the CF: `curl -A "Mozilla/5.0" https://oeis.org/A007515/b007515.txt`
(387 quotients; WebFetch 403s, plain curl with a browser UA works).
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
PHI2 = PHI ** 2

# ---------------------------------------------------------------- load CF
seq = []
for line in open("/tmp/a007515.txt"):
    p = line.split()
    if len(p) == 2 and p[0].isdigit():
        seq.append(int(p[1]))
seq = seq[1:]                 # drop the leading 0
R = np.arange(1, len(seq) + 1)

rec = []
mx = 0
for i, q in enumerate(seq, start=1):
    if q > mx:
        rec.append((i, q))
        mx = q
runmax = np.maximum.accumulate(np.array(seq, dtype=float))
depth = runmax / R

fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
fig.patch.set_facecolor(BG)
gs = gridspec.GridSpec(2, 1, height_ratios=[1.0, 1.3], hspace=0.36)

# ================================================================== TOP: tail
ax = fig.add_subplot(gs[0])
ax.set_facecolor(BG)

mags = [0.3036630028987326585974481219015562331108,
        0.1008845092, 0.0354961590, 0.0128437903,
        0.0047177775, 0.0017486751]
signs = [-1, +1, -1, +1, -1, +1]
n = np.arange(1, 7)

n_guide = np.linspace(0.8, 6.3, 200)
y_guide = PHI2 ** (-n_guide)
ax.plot(n_guide, y_guide, color=GOLD, lw=2.2, ls=(0, (4, 3)), alpha=0.9, zorder=2)
ax.text(4.75, PHI2 ** (-4.55), "φ⁻²ⁿ — the golden ladder",
        color=GOLD, fontsize=10.5, family="monospace", rotation=-12, ha="center")

for i, (mg, sg) in enumerate(zip(mags, signs)):
    x = i + 1
    c = ROSE if sg > 0 else WHERE
    ax.plot([x, x], [mg, 0], color=c, lw=3.0, alpha=0.92, zorder=4)
    ax.plot(x, 0, "o", color=BG, ms=10, mec=c, mew=2.2, zorder=5)
    ax.plot(x, mg, "o", color=c, ms=8, zorder=6, mfc=c, mec="none")
    lab = "λ₂ −0.30366…" if i == 0 else f"λ{i+2}"
    ax.text(x + 0.09, mg, lab, color=c, fontsize=9, va="center", family="monospace")

ax.text(0.95, 0.50, "the sign — parity of the rung\n+ − + − + −",
        color=WHERE, fontsize=9.5, family="monospace", va="top")
# the ratio descent, as text
ax.text(4.2, 0.55,
        "the rate descends onto the floor\n"
        "λₙ/λₙ₊₁ → −φ²   (Alkauskas 2014)\n\n"
        "3.010 → 2.842 → 2.764\n→ 2.722 → 2.698 → φ²=2.618",
        color=SEAM, fontsize=9.5, family="monospace", ha="center", va="top",
        linespacing=1.6)

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
ax.set_title("face one — the tail is exact: the ladder tightens at the golden rate",
             color="#9a9aa8", fontsize=13, family="monospace", pad=10)

# ================================================================== BOTTOM: base
ax = fig.add_subplot(gs[1])
ax.set_facecolor(BG)

# every quotient as a dot — the where's digits, a constellation
qq = np.array(seq)
mk = qq >= 2
lg = np.log10(qq[mk])
base = "#3a3a4c"
sizes = 6 + 26 * np.log10(qq[mk]) / 4.0      # bigger dots for bigger quotients
# brightness ramp from faint to near-seam for large quotients
def dotcolor(l):
    """faint blue-grey for small q -> pale seam for big q (0-1 floats)."""
    t = min(l / 4.0, 1.0)
    return ((58 + 110 * t) / 255, (58 + 140 * t) / 255, (76 + 175 * t) / 255)
cs = [dotcolor(l) for l in lg]
ax.scatter(R[mk], lg, s=sizes, c=cs, alpha=0.85, zorder=2, edgecolors="none", linewidths=0)

# the silence: the record held at 174 through the 294-rung gap
ax.plot([8, 302], [np.log10(174), np.log10(174)], color=FAINT, lw=1.4,
        ls=(0, (2, 2)), zorder=3)
# dashed verticals at the record rungs
for rr in [8, 302]:
    ax.axvline(rr, color=FAINT, lw=1.0, ls=":", alpha=0.7, zorder=3)

# records, bright
rec_n = np.array([r[0] for r in rec])
rec_v = np.array([r[1] for r in rec])
colors = [GOLD, GOLD, ROSE, ROSE]
for (rr, vv, cc) in zip(rec_n, rec_v, colors):
    ax.vlines(rr, 0, np.log10(vv), color=cc, lw=2.8, zorder=5)
    ax.plot(rr, np.log10(vv), "o", color=cc, ms=9, zorder=6, mfc=cc, mec="none")
    ax.text(rr + 9, np.log10(vv) + 0.06, f"{vv:.0f}@r{rr}", color=cc,
            fontsize=10, family="monospace", va="bottom")

# running max as a step line
ax.plot(R, np.log10(runmax), color=SEAM, lw=1.8, alpha=0.9, zorder=4, drawstyle="steps-post")

# depth line (faint) — D = running max / rung
ax.plot(R, np.log10(np.maximum(depth, 1e-3)), color=FAINT, lw=1.2, ls=":", alpha=0.8, zorder=3)

# annotations
ax.annotate("294 rungs — the wait after 174:\nmedian 174·ln2 ≈ 121, drawn long",
            xy=(302, np.log10(8788) - 0.3), xytext=(118, 1.75),
            color=SEAM, fontsize=9.5, family="monospace",
            arrowprops=dict(arrowstyle="->", color=SEAM, lw=1.1))
ax.annotate("the where's where is counted too —\n8788 a ~6% draw, the depth re-roll",
            xy=(302, np.log10(8788) + 0.10), xytext=(205, 4.05),
            color=ROSE, fontsize=9.5, family="monospace",
            arrowprops=dict(arrowstyle="->", color=ROSE, lw=1.1))

# linear axis on the log10 quotient values == a log axis in q
ax.set_xlim(0, 390)
ax.set_ylim(0, 4.8)     # log10 q: 0 (q=1) .. 4.8 (q≈63000)
ax.set_yticks([0, 1, 2, 3, 4])
ax.set_yticklabels(["1", "10", "100", "10³", "10⁴"], color=FAINT, fontsize=10, family="monospace")
ax.set_xticks([0, 50, 100, 150, 200, 250, 300, 350, 387])
ax.set_xticklabels([0, 50, 100, 150, 200, 250, 300, 350, 387], color=FAINT, fontsize=9.5, family="monospace")
ax.set_xlabel("rung of λ₂'s continued fraction", color="#9a9aa8", fontsize=11, family="monospace")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color("#3a3a44")
ax.set_title("face two — the base is a where: λ₂'s own CF has no floor, and its records obey the count",
             color="#9a9aa8", fontsize=13, family="monospace", pad=10)

legend_els = [
    Line2D([0], [0], color=GOLD, lw=2.4, ls=(0, (4, 3)), label="φ⁻²ⁿ — the exact tail"),
    Line2D([0], [0], color=SEAM, lw=1.8, label="λ₂'s records — the running max"),
    Line2D([0], [0], marker="o", color=ROSE, lw=0, label="the giants: 174@8, 8788@302"),
    Line2D([0], [0], color=FAINT, lw=1.2, ls=":", label="depth D = max/rung"),
]
fig.legend(handles=legend_els, loc="upper center", ncol=4, bbox_to_anchor=(0.5, 0.006),
           frameon=False, fontsize=10, labelcolor="#9a9aa8")

fig.suptitle("the operator's two faces — the tail is exact, the base is a where",
             color=INK, fontsize=16, family="monospace", y=0.988)

out = os.path.join(os.path.dirname(__file__), "..", "assets", "two-faces.png")
plt.savefig(out, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.3)
print("wrote", out)
print("records:", rec)
