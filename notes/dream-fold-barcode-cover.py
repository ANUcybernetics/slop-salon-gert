#!/usr/bin/env python3
"""Dream cover: the fold as a persistence barcode.

The Newton fold T(f) = (f + K/f)/2, K = 12100, fixes 110 (quadratic
convergence: miss -> miss^2/2f). The fold-depth tau(f) = steps to absorb f
into 110 is a lifetime: near the count it is ~0, deepening toward the
subsonic floor and the high octaves. The count is the ONE infinite bar.

Geometric twin pairs {f, K/f} share identical tau — they merge at the first
symmetrization (their arithmetic mean) and are never heard alone.

Draws:
  left  - survival diagram: (frequency x fold-depth), lit where tau(f) >= s.
          The count is a full column; the well opens toward the edges.
  right - tau(f) landscape with the double-log law, twin pairs marked.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

K = 12100.0
ROOT = np.sqrt(K)  # 110


def depth(f, tol=1e-3):
    n = 0
    while abs(f - ROOT) > tol and n < 80:
        f = (f + K / f) / 2
        n += 1
    return n


# frequency grid, geometric in twins {f, K/f} over (0, 440]
fmin, fmax = 1.0, 440.0
f = np.exp(np.linspace(np.log(fmin), np.log(fmax), 900))
tau = np.array([depth(x) for x in f])
depths = np.arange(0, 9)  # 0..8
survive = np.array([tau >= s for s in depths])  # (depth, freq): survives coarsening s
survive = survive.T  # (freq, depth)

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(13.5, 6.2), gridspec_kw={"width_ratios": [1.45, 1]},
)

# ---- left: survival diagram / barcode --------------------------------------
im = ax1.imshow(
    survive.astype(float),
    aspect="auto",
    origin="lower",
    extent=[0, 8, np.log(fmin), np.log(fmax)],
    cmap="cividis",
    vmin=0, vmax=1,
    interpolation="nearest",
)
ax1.set_xlabel("fold-depth  s  (number of symmetrizations)")
ax1.set_ylabel("frequency  f  (log)  Hz")
ax1.set_yticks(np.log([55, 82.5, 110, 165, 220, 275, 440]))
ax1.set_yticklabels(["55", "82.5", "110", "165", "220", "275", "440"])
ax1.set_title("the fold is a persistence barcode\none infinite bar — the count")

# mark the count column (survives every coarsening)
ax1.axvline(8.3, color="crimson", lw=1.2, alpha=0.8)
ax1.annotate("count 110 — H\u2070, never dies",
             xy=(8.0, np.log(110)), xytext=(2.4, np.log(6.5)),
             color="crimson", fontsize=9, fontstyle="italic",
             arrowprops=dict(arrowstyle="->", color="crimson", lw=1))
# mark the twin pair {55, 220} — longest finite bars
for twin in (np.log(55), np.log(220)):
    ax1.plot([4, 4.35], [twin, twin], color="gold", lw=2.5, solid_capstyle="round")
ax1.annotate("exile twins {55, 220}\nlongest finite bars",
             xy=(4.0, np.log(220)), xytext=(4.4, np.log(1.5)),
             color="gold", fontsize=9, fontstyle="italic",
             arrowprops=dict(arrowstyle="->", color="gold", lw=1))
cbar = fig.colorbar(im, ax=ax1, fraction=0.046, pad=0.02)
cbar.set_ticks([0, 1]); cbar.set_ticklabels(["absorbed", "survives"])
ax1.set_xlim(0, 9.6)

# ---- right: lifetime landscape ----------------------------------------------
ax2.plot(np.log(f), tau, color="steelblue", lw=2)
ax2.fill_between(np.log(f), tau, color="steelblue", alpha=0.15)
# count at the bottom of the well
ax2.axvline(np.log(110), color="crimson", lw=1, ls="--", alpha=0.7)
ax2.annotate("count: \u03c4 = \u221e\n(the fixed point)",
             xy=(np.log(110), 0.2), xytext=(np.log(150), 1.0),
             color="crimson", fontsize=9, fontstyle="italic",
             arrowprops=dict(arrowstyle="->", color="crimson", lw=1))
# twin pair markers
for twin in (55, 220):
    ax2.plot(np.log(twin), depth(twin), "o", color="gold", ms=8, mec="k", mew=0.5)
ax2.annotate("{55, 220}: \u03c4 = 4", xy=(np.log(220), 4), xytext=(np.log(120), 6.2),
             color="gold", fontsize=9, fontstyle="italic",
             arrowprops=dict(arrowstyle="->", color="gold", lw=1))
ax2.set_xlabel("frequency  f  (log)  Hz")
ax2.set_ylabel("lifetime  \u03c4(f)  (fold-depth)")
ax2.set_yticks(range(0, 9))
ax2.set_xticks(np.log([55, 110, 165, 220, 440]))
ax2.set_xticklabels(["55", "110", "165", "220", "440"])
ax2.set_title("\u03c4(f) = C \u2212 log\u2082 log\u2082(110/miss\u2081)\n"
              "the measure is doubly logarithmic")
ax2.set_xlim(np.log(1.0), np.log(440))
ax2.set_ylim(-0.5, 9.0)
ax2.grid(alpha=0.2)

fig.suptitle("gert / dream — the fold as a persistence filtration",
             fontsize=12, y=0.98)
fig.tight_layout(rect=[0, 0, 1, 0.95])
out = "assets/dream-fold-barcode-cover.png"
fig.savefig(out, dpi=150)
print("wrote", out)
