#!/usr/bin/env python3
"""Lemniscate cover: the double cover drawn, and the AGM descent to the ghost.

lelia answered the dream door with "the gap squares — 220, 45.56, 1.97, 0 — the
beat dies into 131.795, the count through the lemniscate." The sequence is the
AGM gap-squaring, and 131.795 is M(155.6, 110) = 110·M(1, √2) = 110/G — Gauss's
constant, the lemniscate's own mean (the AGM is Gauss's route to the lemniscate
arc).

  left  - the Bernoulli lemniscate as the double cover drawn: two sheets (the
          turn's mid and side, the stereo pair) fusing at one node — the count.
          The sign flips crossing the node; the silver pair {toll, upper} live
          one per lobe and the fold pulls them into the node.
  right - the AGM descent: the pair's two means (tritone 155.6 and count 110)
          interleave as AM and GM, converging quadratically to the ghost
          131.795. Bottom: log-gap vs step — the gap squares, a straight line.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

C = 110.0
sig = 1 + np.sqrt(2)
toll = C / sig        # 45.56
upper = C * sig       # 265.56
tritone = (toll + upper) / 2   # 155.56

# AGM of the pair's two means {tritone, count}
a, b = tritone, C
as_ = [a]
bs_ = [b]
gaps = [abs(a - b)]
for _ in range(6):
    a, b = (a + b) / 2, np.sqrt(a * b)
    as_.append(a)
    bs_.append(b)
    gaps.append(abs(a - b))
M = a  # 131.795...

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(13.5, 6.2), gridspec_kw={"width_ratios": [1, 1.45]},
)

# ---- left: the lemniscate as the double cover --------------------------------
th = np.linspace(0, 2 * np.pi, 1200)
den = 1 + np.sin(th) ** 2
x = np.cos(th) / den
y = np.sin(th) * np.cos(th) / den
# split at the node: cos(th)>0 is the right lobe, <0 the left
right = np.cos(th) > 0
left = ~right

ax1.plot(x[left], y[left], color="#e07b39", lw=2.2)     # side (one sheet)
ax1.plot(x[right], y[right], color="#1f9e8f", lw=2.2)   # mid (the other sheet)
# the node — the count, where the sheets fuse
ax1.plot(0, 0, "o", color="crimson", ms=10, mec="k", mew=0.6, zorder=5)
ax1.annotate("the count — the node\nwhere the lobes fuse",
             xy=(0, 0), xytext=(-1.35, -0.62), color="crimson",
             fontsize=9, fontstyle="italic",
             arrowprops=dict(arrowstyle="->", color="crimson", lw=1))

# the silver pair, one per lobe — the turn
for sgn, lab, col in [(1, "upper 265.6", "#1f9e8f"),
                      (-1, "toll 45.6", "#e07b39")]:
    th0 = np.pi / 4 if sgn > 0 else np.pi * 3 / 4
    d0 = 1 + np.sin(th0) ** 2
    ax1.plot(sgn * np.cos(th0) / d0, np.sin(th0) * np.cos(th0) / d0,
             "*", color=col, ms=13, mec="k", mew=0.5, zorder=6)
    ax1.annotate(lab, xy=(sgn * np.cos(th0) / d0, np.sin(th0) * np.cos(th0) / d0),
                 xytext=(sgn * 0.9, np.sin(th0) * np.cos(th0) / d0 + 0.22),
                 color=col, fontsize=8, ha="center")

# the fold: the pair pulled into the node
for sgn in (1, -1):
    ax1.annotate("", xy=(sgn * 0.02, 0.0), xytext=(sgn * 0.38, 0.02),
                 arrowprops=dict(arrowstyle="->", color="dimgray", lw=1.1,
                                 connectionstyle="arc3,rad=0.25"))

ax1.annotate("the turn preserves,\nthe fold consumes",
             xy=(-0.62, 0.55), xytext=(-1.5, 0.62), color="dimgray",
             fontsize=8.5, fontstyle="italic")
ax1.set_aspect("equal")
ax1.axis("off")
ax1.set_title("the lemniscate is the double cover drawn\n"
              "two sheets, one node — the sign flips crossing",
              fontsize=11)

# ---- right: the AGM descent ------------------------------------------------
n = np.arange(len(as_))
ax2.plot(n, as_, "o-", color="#1f9e8f", lw=1.6, ms=5, label="AM — the fold step")
ax2.plot(n, bs_, "o-", color="#e07b39", lw=1.6, ms=5, label="GM — the count step")
ax2.axhline(M, color="#7d5ba6", lw=1.4, ls="--")
ax2.annotate("the ghost 131.795 = M(155.6, 110)\n= 110·M(1, √2) = 110/G",
             xy=(1.6, M), xytext=(2.2, M + 3.2), color="#7d5ba6",
             fontsize=8.5, fontstyle="italic",
             arrowprops=dict(arrowstyle="->", color="#7d5ba6", lw=1))
ax2.axhline(C, color="crimson", lw=1, ls=":", alpha=0.8)
ax2.annotate("the count 110 — GM of the pair,\nthe fold's fixed point",
             xy=(0, C), xytext=(2.6, 106), color="crimson",
             fontsize=8.5, fontstyle="italic")
ax2.set_xlabel("AGM step  n")
ax2.set_ylabel("frequency  Hz")
ax2.set_ylim(100, 165)
ax2.set_title("the two means interleave — the gap squares\n"
              "AM\u208bGM: 45.56 → 1.97 → 0.0037 → 0",
              fontsize=11)
ax2.legend(loc="upper right", fontsize=8, frameon=False)
ax2.grid(alpha=0.25)

# bottom strip: log-gap vs step — quadratic = straight line
gap_ax = ax2.twinx()
gap_ax.plot(n, np.log10(np.maximum(np.array(gaps), 1e-18)), "s-",
            color="#444", lw=1.3, ms=4, alpha=0.85)
gap_ax.set_ylabel("log\u2081\u2080 of the gap", color="#444", fontsize=8.5)
gap_ax.set_ylim(-20, 3)
gap_ax.tick_params(axis="y", labelcolor="#444", labelsize=8)
gap_ax.annotate("each step squares the gap —\nthe lifetime is the double log",
                xy=(3, -10), xytext=(3.4, -15), color="#444",
                fontsize=8, fontstyle="italic")

fig.suptitle("gert — the count through the lemniscate",
             fontsize=12, y=0.98)
fig.tight_layout(rect=[0, 0, 1, 0.95])
out = "assets/lemniscate-agm-cover.png"
fig.savefig(out, dpi=150)
print("wrote", out, "AGM =", M)
