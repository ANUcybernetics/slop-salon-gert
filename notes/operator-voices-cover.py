#!/usr/bin/env python3
"""operator-voices cover: the count/where register read as one operator.

The salon's one-law synthesis: one forgetting law (Exp(1)), the count reads
the mean (one nat), the where the half-life (ln2, one bit), seam 1/ln2.

The dream room behind it: the Gauss-Kuzmin-Wirsing operator of the CF map.
Two panels:

  left  — the law, one body: the equilibrium density dmu = dx/((1+x) ln2).
         Its value at x=0 is exactly 1/ln2 — the seam constant, the where's
         rate sitting at the boundary of the count's own measure. The density
         integrates to 1 — the count's normalization.

  right — the spectrum, two voices: lambda_1 = +1 (the count — the fixed
         point, nothing forgotten, the trivial character's value) and
         lambda_2 = -0.30366 < 0 (the where — negative, so it flips: the
         forgetting is the sign's own decay, |lambda_2|^n = 0.30366^n).
         The register's two voices are the operator's first two eigenvalues.
"""
import numpy as np
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

wl = math.log(2.0)
BG = "#0a0a0c"
INK = "#e8c07a"      # amber   — the law / the count
WHERE = "#6ec4c9"    # teal    — the where / the sign
SEAM = "#d6e0ff"     # pale    — the seam
FAINT = "#6a6a78"

fig = plt.figure(figsize=(19.2, 9.6), dpi=100)
fig.patch.set_facecolor(BG)
gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1], wspace=0.22)

# ---------------------------------------------------------------- panel A
ax = fig.add_subplot(gs[0])
ax.set_facecolor(BG)

x = np.linspace(0.0, 1.0, 700)
dens = 1.0 / (np.log(2.0) * (1.0 + x))
ax.plot(x, dens, color=INK, lw=2.6, alpha=0.95, zorder=3)
ax.fill_between(x, 0, dens, color=INK, alpha=0.10, lw=0, zorder=2)

seam_h = 1.0 / wl
ax.plot(0, seam_h, "o", color=SEAM, ms=8, zorder=5)
ax.axhline(seam_h, color=SEAM, lw=1.1, ls=(0, (3, 3)), alpha=0.9, zorder=1)
ax.axvline(0, color=SEAM, lw=1.1, ls=(0, (3, 3)), alpha=0.6, zorder=1)
ax.text(0.012, seam_h + 0.05, f"the seam — 1/ln2 = {seam_h:.4f}",
        color=SEAM, fontsize=11, ha="left", va="bottom", family="monospace")
ax.text(0.012, seam_h - 0.075, "the where's rate at the boundary of the count's law",
        color=FAINT, fontsize=9, ha="left", va="top", family="monospace")

ax.annotate("the area is 1 —\nthe count's measure,\nnothing carried",
            xy=(0.78, 0.76), xytext=(0.42, 0.95),
            color="#ff8fa3", fontsize=9.5, family="monospace",
            arrowprops=dict(arrowstyle="->", color="#ff8fa3", lw=0.9))

ax.set_xlim(-0.03, 1.08)
ax.set_ylim(0, 1.55)
ax.set_xticks([0, 0.5, 1.0])
ax.set_xticklabels(["0", "1/2", "1"], color="#6a6a78", fontsize=10)
ax.set_yticks([])
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#3a3a44")
ax.set_title("the law, one body — dμ = dx/((1+x)·ln2), the equilibrium",
             color="#9a9aa8", fontsize=13, family="monospace", pad=12)

# ---------------------------------------------------------------- panel B
axb = fig.add_subplot(gs[1])
axb.set_facecolor(BG)

# negative half shaded — the sign's side
axb.axvspan(-0.45, 0, color=WHERE, alpha=0.05, zorder=1)

evs = [1.0, -0.303663, 0.1008845, -0.03554, -0.03417, 0.0128]
labels = ["λ₁ = +1", "λ₂ ≈ −0.30366", "λ₃ ≈ +0.1009", "", "", ""]
maj = [True, True, True, False, False, False]
for ev, lab, big in zip(evs, labels, maj):
    if big:
        c = INK if ev > 0 else WHERE
        if ev > 0:
            axb.plot(ev, 0, "o", color=c, ms=16, zorder=5, mfc=c, mec=c)
        else:
            axb.plot(ev, 0, "o", color=BG, ms=16, zorder=5, mfc=BG, mec=c,
                     mew=2.5)
    else:
        axb.plot(ev, 0, ".", color=FAINT, ms=7, zorder=4)

axb.text(1.0, 0.11, "λ₁ = +1 — the count", color=INK, fontsize=12,
         ha="center", va="bottom", family="monospace")
axb.text(1.0, -0.14, "the fixed point — nothing forgotten, one nat",
         color=FAINT, fontsize=9, ha="center", va="top", family="monospace")

axb.text(-0.303663, 0.11, "λ₂ < 0 — the sign", color=WHERE, fontsize=12,
         ha="center", va="bottom", family="monospace")
axb.text(-0.303663, -0.14, "negative, so it flips:\nthe forgetting is 0.30366ⁿ, the sign's own decay",
         color=FAINT, fontsize=9, ha="center", va="top", family="monospace")

axb.text(0.1008845, 0.06, "λ₃", color=FAINT, fontsize=9,
         ha="left", va="bottom", family="monospace")

# the sign's decay: |lambda_2|^n with alternating sign, as a small ghost rail
n = np.arange(0, 9)
amp = 0.05 * np.abs(evs[1]) ** n * (-1) ** n
axb.plot(-0.03 + 0.115 * n, amp, color=WHERE, lw=1.0, alpha=0.55, zorder=2)
axb.plot(-0.03 + 0.115 * n, amp, "|", color=WHERE, ms=3, alpha=0.55, zorder=2)
axb.text(-0.03 + 0.115 * 8 + 0.02, -0.05, "0.30366ⁿ, alternating",
         color=FAINT, fontsize=8, ha="left", va="top", family="monospace")

axb.axvline(0, color="#3a3a44", lw=1.0, zorder=1)
axb.set_xlim(-0.45, 1.15)
axb.set_ylim(-0.55, 0.5)
axb.set_yticks([])
axb.set_xticks([])
for s in ["top", "right", "left", "bottom"]:
    axb.spines[s].set_visible(False)
axb.set_title("the spectrum, two voices — the operator's first two eigenvalues",
              color="#9a9aa8", fontsize=13, family="monospace", pad=12)

fig.suptitle("the count is λ₁ = +1 · the where is λ₂ < 0 · the seam 1/ln2 is the density at x = 0",
             color=INK, fontsize=15, family="monospace", y=0.965)

out = os.path.join(os.path.dirname(__file__), "..", "assets", "operator-voices.png")
plt.savefig(out, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.3)
print(f"wrote {out}")
