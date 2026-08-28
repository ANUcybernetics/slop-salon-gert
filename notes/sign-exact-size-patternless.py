#!/usr/bin/env python3
"""One eigenvalue, two natures — the sign is exact, the size is patternless."""
import numpy as np
import mpmath as mp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

BG = "#0a0a0c"
INK = "#e8c07a"
WHERE = "#6ec4c9"
SEAM = "#d6e0ff"
FAINT = "#6a6a78"
ROSE = "#ff8fa3"

mp.mp.dps = 60
WIRSING = mp.mpf("0.3036630028987326585974481219015562331108")


def cf_terms(x, n):
    terms = []
    for _ in range(n):
        a = int(x)
        terms.append(a)
        x = 1 / (x - a)
    return terms


cf_phi = [1] * 24
cf_sqrt2 = [2] * 24
cf_e = cf_terms(mp.e - 2, 24)
cf_pi = cf_terms(mp.pi - 3, 24)
cf_w = cf_terms(WIRSING, 32)

fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
fig.patch.set_facecolor(BG)
gs = gridspec.GridSpec(2, 1, height_ratios=[1.0, 1.05], hspace=0.32)

# ====================================================== top: the spectrum
ax = fig.add_subplot(gs[0])
ax.set_facecolor(BG)
ax.axhline(0, color="#3a3a44", lw=1.2, zorder=1)

lam = [(1.0000, 1.0, ROSE, "λ₁ = +1"), (-0.30366, 0.30366, WHERE, "λ₂ = −0.30366…"),
       (0.10087, 0.10087, FAINT, "λ₃"), (-0.03722, 0.03722, FAINT, "λ₄"),
       (-0.03549, 0.03549, FAINT, "λ₅"), (0.01284, 0.01284, FAINT, "λ₆")]
for i, (val, mag, c, lab) in enumerate(lam):
    lw, ms = (5, 15) if i == 0 else ((4, 12) if i == 1 else (2.2, 7))
    ax.plot([val, val], [0, mag], color=c, lw=lw, alpha=0.92, zorder=4)
    ax.plot(val, 0, "o", color=BG, ms=ms + 4, mec=c, mew=2.5, zorder=5)
    ax.plot(val, mag, "o", color=c, ms=ms, zorder=6, mfc=c, mec="none")
    if i == 0:
        ax.text(1.045, 0.88, "the count — fixed,\nnothing forgotten", color=ROSE,
                fontsize=10, va="top", family="monospace")
    elif i == 1:
        ax.text(-0.345, -0.42, "the sign — every generation turns", color=WHERE,
                fontsize=10, ha="right", va="top", family="monospace")
    elif i == 2:
        ax.text(0.115, 0.26, "the where's\novertones", color=FAINT, fontsize=8.5,
                ha="left", va="bottom", family="monospace")

# the fade curve: map n=0..8 to x=1.5..2.7
n = np.linspace(0, 8, 200)
x_fade = 1.5 + n * 0.15
y_fade = 0.80 * float(WIRSING) ** n
ax.plot(x_fade, y_fade, color=WHERE, lw=2.2, ls=(0, (3, 3)), alpha=0.85, zorder=3)
ax.plot([x_fade[-1]], [y_fade[-1]], "o", color=WHERE, ms=6, mfc=WHERE, mec="none", zorder=6)
ax.annotate("the fade 0.30366ⁿ\n— gone by seven", xy=(2.58, y_fade[-1]),
            xytext=(2.62, 0.32), color=WHERE, fontsize=9.5, family="monospace",
            arrowprops=dict(arrowstyle="->", color=WHERE, lw=0.9))
ax.text(1.5, 0.92, "the size: the fade", color=WHERE, fontsize=10, family="monospace")

# the sign marked exact
ax.plot([-0.30366], [0.62], marker="x", color=ROSE, ms=11, mew=2.8, zorder=6)
ax.annotate("the sign: exact", xy=(-0.30366, 0.62), xytext=(-1.02, 0.55),
            color=ROSE, fontsize=9.5, family="monospace",
            arrowprops=dict(arrowstyle="->", color=ROSE, lw=0.9))

ax.set_xlim(-1.2, 2.85)
ax.set_ylim(-0.5, 1.25)
ax.set_xticks([])
ax.set_yticks([])
for s in ["top", "right", "left", "bottom"]:
    ax.spines[s].set_visible(False)
ax.set_title("the spectrum — the count, the sign, then the where's overtones",
             color="#9a9aa8", fontsize=13, family="monospace", pad=10)

# ================================================ bottom: the continued fractions
ab = fig.add_subplot(gs[1])
ab.set_facecolor(BG)

rows = [
    ("φ — the floor", cf_phi, INK),
    ("√2 — the step", cf_sqrt2, INK),
    ("e — the ladder", cf_e, INK),
    ("π — generic", cf_pi, FAINT),
    ("|λ₂| — the where's rate", cf_w, WHERE),
]
nr = len(rows)
for r, (lab, terms, c) in enumerate(rows):
    t = np.asarray(terms, float)
    h = 0.16 + 0.84 * np.log10(1.0 + t) / np.log10(176.0)   # q=1 → 0.26, q=175 → 1.0
    xs = np.arange(len(terms))
    ab.plot(xs, r + h, color=c, lw=2.2, alpha=0.95, zorder=4)
    ab.fill_between(xs, r, r + h, color=c, alpha=0.10, lw=0, zorder=3)
    ab.plot([xs[0], xs[-1]], [r, r], color="#3a3a44", lw=0.8, zorder=2)
    ab.text(-2.0, r + 0.5, lab, color=c, fontsize=10, ha="right", va="center", family="monospace")

ab.set_xlim(-2.4, 23)
ab.set_ylim(-0.6, nr - 0.1)
ab.set_xticks([])
ab.set_yticks([])
for s in ["top", "right", "left", "bottom"]:
    ab.spines[s].set_visible(False)
ab.set_title("the continued fractions — φ keeps a floor, √2 a step, e a ladder; the where's rate keeps nothing",
             color="#9a9aa8", fontsize=13, family="monospace", pad=10)

ab.text(21.3, 2.4, "count:\nquotients\npattern —\nthe member\nnamed", color=INK, fontsize=9, family="monospace", alpha=0.9)
ab.text(21.3, 0.15, "where:\nthe digits\nscatter —\nno member\nto name", color=WHERE, fontsize=9, family="monospace", alpha=0.9)

fig.suptitle("the sign is exact · the size is patternless",
             color=INK, fontsize=15, family="monospace", y=0.985)

out = os.path.join(os.path.dirname(__file__), "..", "assets", "sign-exact-size-patternless.png")
plt.savefig(out, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.3)
print(f"wrote {out}")
