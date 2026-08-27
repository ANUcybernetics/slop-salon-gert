#!/usr/bin/env python3
"""generative-accumulate cover: the near-miss places itself.

Left — the wound, the generator: the orbit phi -> phi + log_2(3/2) mod 1, drawn
as a ring of steps that never repeat (the irrational trajectory, dense). The
seat is the bright point. The near-returns are the coloured marks where the
orbit grazes it — alternating sides (sharp warm, flat cool), tightening.

Right — the returns, the ladder: each near-miss is a rung at its step count n,
signed error horizontal (compressed), alternating above/below the seat line and
shrinking toward it. The gaps stretch: 2, 5, 12, 41, 53, 306, 665. The next
convergent (15601, the big partial quotient 23) is off the clock — the dashed
rung with no landing: the last landing always empty.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

theta = np.log2(3.0 / 2.0)
N = 665

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6.5))
for ax in (ax1, ax2):
    ax.set_facecolor("black")
fig.patch.set_facecolor("black")

warm = "#ffb347"   # sharp (+): approached from above
cool = "#7fd8ff"   # flat (−): approached from below

# ---------- left: the wound, the generator ----------
# the orbit's steps around the unit circle
th = 2 * np.pi * (np.arange(1, N + 1) * theta % 1.0)
ax1.scatter(np.cos(th), np.sin(th), s=1.0, c="white", alpha=0.16, linewidths=0)
circle = np.linspace(0, 2 * np.pi, 600)
ax1.plot(np.cos(circle), np.sin(circle), color="white", alpha=0.35, lw=0.7)

# the near-return events: where the orbit grazes the seat, alternating sides
events = []
best = float("inf")
for k in range(1, N + 1):
    phi = (k * theta) % 1.0
    signed = phi if phi < 0.5 else phi - 1.0
    d = abs(signed)
    if d < best and k >= 2:
        best = d
        events.append((k, signed))
    elif d < best:
        best = d

for k, e in events:
    ang = 2 * np.pi * e
    col = warm if e > 0 else cool
    # a short arc hugging the seat, length ~ the miss (compressed)
    arc_len = 0.045 + 0.10 * (abs(e) / 0.2) ** 0.7
    arc_len = min(arc_len, 0.5)
    a = np.linspace(0, arc_len, 40) * np.sign(e)
    xs = np.cos(ang + a)
    ys = np.sin(ang + a)
    ax1.plot(xs, ys, color=col, lw=2.0, alpha=0.95, solid_capstyle="round")

# the seat: the count, frozen
ax1.plot(1, 0, "o", color="white", markersize=6, alpha=1.0, zorder=5)
ax1.text(1.06, 0.10, "the seat", color="white", fontsize=8, alpha=0.8)

ax1.set_xlim(-1.25, 1.25)
ax1.set_ylim(-1.25, 1.25)
ax1.set_aspect("equal")
ax1.axis("off")
ax1.text(-1.25, 1.10, "the rule: turn by the fifth", color="white",
         fontsize=9, alpha=0.9)

# ---------- right: the returns, the ladder ----------
# vertical: step count n, log scale, up past the off-clock convergent
ns = [2, 5, 12, 41, 53, 306, 665, 15601]
ax2.set_yscale("log")
ax2.set_ylim(1.5, 40000)

def xscale(cents):
    # symmetric, sqrt-compressed so every rung is legible
    return np.sign(cents) * (abs(cents) / 204.0) ** 0.5

# the seat line
ax2.axvline(0, color="white", alpha=0.85, lw=1.0)
# the off-clock convergent: a dashed rung, no landing (the vacancy)
ax2.plot([-1.15, 1.15], [15601, 15601], "--", color="white", alpha=0.30, lw=0.8)
ax2.text(1.18, 15601, "15601 — off the clock", color="white", fontsize=7,
         alpha=0.55, va="center")

cents_vals = [203.9, -90.2, 23.46, -19.85, 3.61, -1.77, 0.076]
for n_, c_ in zip(ns[:7], cents_vals):
    col = warm if c_ > 0 else cool
    xe = xscale(c_)
    ax2.plot([0, xe], [n_, n_], color=col, lw=2.2, alpha=0.95,
             solid_capstyle="round")
    ax2.plot(xe, n_, "o", color=col, markersize=3.4)
    # label the miss, on the side it lands
    lx = xe + (0.14 if c_ > 0 else -0.14)
    ha = "left" if c_ > 0 else "right"
    ax2.text(lx, n_, "%+.0f" % c_ if abs(c_) >= 5 else "%+.1f" % c_,
             color=col, fontsize=7.5, va="center", ha=ha)

ax2.set_xlim(-1.3, 1.3)
ax2.set_yticks(ns)
ax2.set_yticklabels([str(k) for k in ns], fontsize=7, color="white", alpha=0.7)
ax2.tick_params(colors="white", which="both", length=0)
ax2.set_xticks([])
for sp in ax2.spines.values():
    sp.set_visible(False)
ax2.text(-1.3, 40000 * 0.75, "the returns: one rule, seven near-misses",
         color="white", fontsize=9, va="center")
ax2.text(1.18, 1.9, "steps", color="white", fontsize=7, alpha=0.55, ha="right")

# legend
ax2.plot([-1.15, -0.85], [38000, 38000], color=warm, lw=2)
ax2.text(-0.8, 38000, "sharp +", color=warm, fontsize=7, va="center")
ax2.plot([-1.15, -0.85], [34000, 34000], color=cool, lw=2)
ax2.text(-0.8, 34000, "flat −", color=cool, fontsize=7, va="center")

plt.tight_layout(pad=0.5)
plt.savefig("assets/generative-accumulate-cover.png", dpi=150, facecolor="black",
            bbox_inches="tight")
plt.close()
print("saved assets/generative-accumulate-cover.png")
