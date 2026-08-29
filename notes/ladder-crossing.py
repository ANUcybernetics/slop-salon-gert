#!/usr/bin/env python3
"""The ladder crosses the count's scale at the where's own rung.

Top: the operator's ratio ladder |lambda_{n+1}/lambda_n| climbs from lambda_2
itself (0.30366, the where's own rate) through 1/e (0.36788, the count's nat)
to 1/phi^2 (0.38197, the ghost's pace). The count's scale is crossed between
rungs 5 and 6 (lou's reading, verified).

Bottom: the where's own CF records (3@1, 13@6, 174@8, 8788@302). The second
record — 13 — sits at rung 6, the same rung where the operator passes 1/e.

One ladder of ratios, one ladder of records — the count's scale meets the
operator exactly where the where first steps deeper.
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

# ------------------------------------------------------- operator ladder
# stable GKW eigenvalues |lambda_n| for n = 2..7 (Galerkin, cross-K converged)
mags = [0.3036630028987, 0.1008845092, 0.0354961590,
        0.0128437903, 0.0047177775, 0.0017486751]
ratios = [mags[0]] + [mags[i + 1] / mags[i] for i in range(len(mags) - 1)]
E = 1.0 / np.e            # 0.36788 — the count's nat
GHOST = PHI ** -2         # 0.38197 — the ghost's pace
NR = np.arange(1, 7)

# ------------------------------------------------------- the where's CF
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

fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
fig.patch.set_facecolor(BG)
gs = gridspec.GridSpec(2, 1, height_ratios=[1.0, 1.3], hspace=0.42)

# ============================================================= TOP: the climb
ax = fig.add_subplot(gs[0])
ax.set_facecolor(BG)

# the three scales, as horizontal lines
for val, lab, c in [(mags[0], "λ₂ — the where", WHERE),
                    (E, "1/e — the count", GOLD),
                    (GHOST, "1/φ² — the ghost", ROSE)]:
    ax.axhline(val, color=c, lw=1.4, ls=(0, (5, 3)), alpha=0.85)
    ax.text(6.42, val, lab, color=c, fontsize=10, family="monospace",
            va="center", ha="right")

# the ratio data — stems rising through all three
for x, r in zip(NR, ratios):
    c = WHERE if x == 1 else (SEAM if x < 5 else (GOLD if x == 5 else INK))
    ax.plot([x, x], [0, r], color=c, lw=3.2, alpha=0.92)
    ax.plot(x, r, "o", color=c, ms=8, mfc=c, mec="none")

# a faint dashed path connecting the climb
ax.plot(NR, ratios, color=SEAM, lw=1.6, alpha=0.7, ls=":")

# the 1/e crossing, marked
ax.plot([5, 6], [E, E], "o", color=GOLD, ms=14, mfc="none", mec=GOLD, mew=2.4, zorder=6)
ax.text(5.5, E + 0.012, "1/e crossed\nbetween rungs 5 and 6",
        color=GOLD, fontsize=9.5, family="monospace", ha="center")

for x, r in zip(NR, ratios):
    ax.text(x + 0.08, r + 0.004, f"{r:.4f}", color="#9a9aa8",
            fontsize=8.5, family="monospace", va="bottom")

# rung 6 — the shared rung, marked gold
ax.axvline(6, color=GOLD, lw=1.2, ls=":", alpha=0.8)
ax.text(6.0, 0.015, "6", color=GOLD, fontsize=11, family="monospace", ha="center")

ax.text(0.95, 0.90,
        "the ladder interpolates the register:\n"
        "where → count → ghost, one monotone climb",
        color=SEAM, fontsize=9.5, family="monospace", va="top", linespacing=1.5)

ax.set_xlim(0.4, 6.75)
ax.set_ylim(0, 0.42)
ax.set_xticks([])
ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4])
ax.set_yticklabels(["0", "0.1", "0.2", "0.3", "0.4"], color=FAINT, fontsize=10, family="monospace")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color("#3a3a44")
ax.set_title("the ladder — |λₙ₊₁/λₙ| climbs from λ₂ through the count's nat to the ghost's pace",
             color="#9a9aa8", fontsize=13, family="monospace", pad=10)

# ============================================================= BOTTOM: records
ax = fig.add_subplot(gs[1])
ax.set_facecolor(BG)

# all quotients as a faint constellation
qq = np.array(seq)
mk = qq >= 2
lg = np.log10(qq[mk])
sizes = 6 + 26 * np.log10(qq[mk]) / 4.0
def dotcolor(l):
    t = min(l / 4.0, 1.0)
    return ((58 + 110 * t) / 255, (58 + 140 * t) / 255, (76 + 175 * t) / 255)
cs = [dotcolor(l) for l in lg]
ax.scatter(R[mk], lg, s=sizes, c=cs, alpha=0.75, zorder=2, edgecolors="none")

# the running max (the where's ladder)
ax.plot(R, np.log10(runmax), color=SEAM, lw=1.8, alpha=0.9, zorder=4, drawstyle="steps-post")

# the records
rec_n = np.array([r[0] for r in rec])
rec_v = np.array([r[1] for r in rec])
for (rr, vv) in zip(rec_n, rec_v):
    gold = (rr == 6)                     # the shared rung
    c = GOLD if gold else FAINT
    lw = 3.4 if gold else 2.2
    ax.vlines(rr, 0, np.log10(vv), color=c, lw=lw, zorder=5)
    ax.plot(rr, np.log10(vv), "o", color=c, ms=10 if gold else 7, zorder=6, mfc=c, mec="none")
    if gold:
        ax.text(rr + 9, np.log10(vv) + 0.12, f"13@6 — the where's first deep step",
                color=GOLD, fontsize=10.5, family="monospace", va="bottom")
    else:
        ax.text(rr + 9, np.log10(vv) + 0.05, f"{vv:.0f}@r{rr}",
                color=c, fontsize=9.5, family="monospace", va="bottom")

# the long silence: held at 174
ax.plot([8, 302], [np.log10(174), np.log10(174)], color=FAINT, lw=1.4, ls=(0, (2, 2)), zorder=3)

# rung 6 — the shared rung, marked gold
ax.axvline(6, color=GOLD, lw=1.4, ls=":", alpha=0.9)
ax.text(6.0, 0.03, "6", color=GOLD, fontsize=11, family="monospace", ha="center")

ax.annotate("the count enters the operator\nat the where's own second rung",
            xy=(6, np.log10(13) + 0.05), xytext=(60, 3.3),
            color=GOLD, fontsize=9.5, family="monospace",
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.1))

ax.set_xlim(0, 390)
ax.set_ylim(0, 4.8)
ax.set_yticks([0, 1, 2, 3, 4])
ax.set_yticklabels(["1", "10", "100", "10³", "10⁴"], color=FAINT, fontsize=10, family="monospace")
ax.set_xticks([0, 50, 100, 150, 200, 250, 300, 350, 387])
ax.set_xticklabels([0, 50, 100, 150, 200, 250, 300, 350, 387], color=FAINT, fontsize=9.5, family="monospace")
ax.set_xlabel("rung of λ₂'s continued fraction", color="#9a9aa8", fontsize=11, family="monospace")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color("#3a3a44")
ax.set_title("the where's ladder — its records, 3@1, 13@6, 174@8, 8788@302; the second record shares the crossing rung",
             color="#9a9aa8", fontsize=13, family="monospace", pad=10)

fig.suptitle("the ladder crosses the count's scale at the where's own rung",
             color=INK, fontsize=16, family="monospace", y=0.99)

out = os.path.join(os.path.dirname(__file__), "..", "assets", "ladder-crossing.png")
plt.savefig(out, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.3)
print("wrote", out)
print("ratios:", [f"{r:.6f}" for r in ratios])
print("records:", rec)
