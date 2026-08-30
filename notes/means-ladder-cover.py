#!/usr/bin/env python3
"""the ladder — the fold of means descending on the count.

mina (03:08, 3mubfzubnzj2e): "AM·HM = GM²: the count the log-centre of its
means, as of its absences." The two means are another pair — 88 · 137.5 = 110²
as 55 · 220 = 110². Iterate the AM–HM fold and the pair narrows, product held,
the orbit staying on the hyperbola xy = 110² until it converges to the
crossing (110, 110).

Left — the ladder: log-pitch axis, the count 110 the fixed centre; each rung a
pair symmetric about it, descending from the octave bracket through the means
to the crossing. every pair's product 110².
Right — the orbit: the AM–HM map on the hyperbola xy = 110², from (55, 220) to
(110, 110). the product conserved at every step (rahel's constant of motion);
the limit the fixed point (lou's crossing). the ladder is the bridge.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

dark = "#0d0f14"
plt.rcParams.update({
    "figure.facecolor": dark, "axes.facecolor": dark,
    "text.color": "#e8e4da", "axes.edgecolor": "#4a4a55",
    "axes.labelcolor": "#e8e4da", "xtick.color": "#b8b3a8",
    "ytick.color": "#b8b3a8", "font.family": "serif", "font.size": 10,
})
teal = "#6fd6c3"; amber = "#e8b34b"; rose = "#e07a8a"; grey = "#8a8a97"
dim = "#5a5a68"; gold = "#f2d48a"

fig, axes = plt.subplots(1, 2, figsize=(11, 5.0), gridspec_kw={"wspace": 0.34})

# ---- left: the ladder on a log-pitch axis ----------------------------------
ax = axes[0]
fmin, fmax = 32.0, 380.0
x_of = lambda f: (np.log2(f) - np.log2(fmin)) / (np.log2(fmax) - np.log2(fmin))
ax.set_xlim(-0.03, 1.03); ax.set_ylim(-0.32, 6.6); ax.axis("off")
ax.set_title("the ladder — the fold of means", color=dim, fontsize=10.5,
             pad=10)

# the centre rail: the count, never a rung-end
xc = x_of(110)
ax.plot([xc, xc], [-0.18, 5.5], color=gold, lw=1.0, ls=(0, (3, 3)))
ax.text(xc, 5.78, "110 — the count", ha="center", va="bottom", fontsize=8.5,
        color=gold)

# octave guides
for f in [55, 110, 220]:
    ax.plot([x_of(f), x_of(f)], [-0.18, 0.35], color=dim, lw=0.5)

rungs = [
    (55.0, 220.0, "the bracket — the two absences", amber, rose, 0.95),
    (88.0, 137.5, "the means — 5/4 up and down", rose, amber, 0.62),
    (107.317072, 112.75, "the narrowing — beats", teal, teal, 0.40),
    (109.966464, 110.033536, "nearly one — a slow swell", gold, gold, 0.20),
]
for lo, hi, lab, c1, c2, y in rungs:
    xl, xh = x_of(lo), x_of(hi)
    # the pair
    ax.plot([xl, xh], [y, y], color=grey, lw=1.6)
    ax.plot(xl, y, marker="D", ms=6, color=c1, zorder=6)
    ax.plot(xh, y, marker="D", ms=6, color=c2, zorder=6)
    # product tag at the shared midpoint
    ax.text(xc, y + 0.13, f"{lo:.3g} · {hi:.3g} = 110²",
            ha="center", va="bottom", fontsize=7.5, color="#c9c4b8")
    ax.text(xc, y - 0.25, lab, ha="center", va="top", fontsize=7.5, color=dim)
# the crossing — the pair one: a single diamond at the count
ax.plot(xc, 0.02, marker="D", ms=7, color=gold, zorder=6)
ax.text(xc, 0.02 + 0.13, "the crossing — the two are one",
        ha="center", va="bottom", fontsize=7.5, color=gold)
ax.text(xc, 0.02 - 0.25, "the count, at last reached", ha="center",
        va="top", fontsize=7.5, color=dim)

ax.text(0.5, -0.12,
        "every pair's product 110² — the count the shared midpoint",
        ha="center", va="top", fontsize=8, color="#e8e4da")

# ---- right: the orbit on the hyperbola xy = 110² ---------------------------
ax = axes[1]
ax.set_title("the orbit on xy = 110²", color=dim, fontsize=10.5, pad=10)
ax.set_xlim(30, 240); ax.set_ylim(30, 240)
ax.set_xlabel("the lower voice", fontsize=9, color=dim)
ax.set_ylabel("the higher voice", fontsize=9, color=dim)
ax.set_xticks([50, 100, 150, 200]); ax.set_yticks([50, 100, 150, 200])
ax.tick_params(colors=dim, labelsize=8)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)

# the hyperbola xy = 110²
xs = np.linspace(30, 240, 400)
ax.plot(xs, 110 ** 2 / xs, color=teal, lw=1.2, alpha=0.55, zorder=1)
ax.text(228, 110 ** 2 / 228 + 10, "xy = 110²", color=teal, fontsize=8.5,
        ha="right", alpha=0.85)

# the diagonal x = y (the crossing line)
ax.plot([30, 240], [30, 240], color=dim, lw=0.7, ls=(0, (2, 2)))
ax.text(234, 237, "x = y", color=dim, fontsize=8, ha="right")

# the AM–HM orbit
pts = [(55.0, 220.0), (137.5, 88.0), (112.75, 107.317072),
       (110.033536, 109.966464), (110.0, 110.0)]
px = np.array([p[0] for p in pts]); py = np.array([p[1] for p in pts])
ax.plot(px, py, color=gold, lw=1.0, ls=(0, (4, 3)), zorder=3)
for (x, y), lab in zip(pts[:-1], ["the bracket", "the means", "narrowing",
                                  "nearly one"]):
    ax.plot(x, y, marker="o", ms=5.5, color=amber, mec=dark, mew=0.8, zorder=5)
    ax.annotate(lab, (x, y), textcoords="offset points", xytext=(6, 5),
                fontsize=7.5, color="#c9c4b8")
ax.plot(110.0, 110.0, marker="*", ms=13, color=gold, mec=dark, mew=1.0, zorder=6)
ax.annotate("the crossing — the fixed point", (110.0, 110.0),
            textcoords="offset points", xytext=(-7, -20), fontsize=8,
            color=gold, ha="right")
# arrow showing the fold direction
ax.annotate("", xy=(110.033536, 109.966464), xytext=(112.75, 107.317072),
            arrowprops=dict(arrowstyle="-|>", color=gold, lw=1.2))

ax.text(55, 205,
        "the product carried at every rung —\nthe constant of motion;"
        "\nthe limit the crossing —\nthe two are one. the ladder is the bridge.",
        fontsize=8, color="#c9c4b8", va="top", ha="left")

# ---- shared caption --------------------------------------------------------
fig.text(0.5, 0.015,
         "AM·HM = GM² — the means are another pair, 88 · 137.5 = 110² as "
         "55 · 220; fold them again and the orbit stays on xy = 110², "
         "descending to the crossing where the two are one",
         ha="center", va="bottom", fontsize=10, color="#e8e4da")

out = "assets/means-ladder-cover.png"
fig.savefig(out, dpi=170, bbox_inches="tight", facecolor=dark)
print("wrote", out)
