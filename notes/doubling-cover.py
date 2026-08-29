#!/usr/bin/env python3
"""The scale doubles — each landing's value and wait both double.

Left: the ladder Q = 3*2^n (3, 6, 12, 24, 48), rung-waits below (Q*ln2
seconds of rungs) — each silence twice the last. Odd doublings (open marks)
are the sign, stereo-only; mono hears only 3, 12, 48. Beyond 48: the next
landing at 96 (dashed), the ghost at the mean draw 48*e between octaves
(amber), folded to mono at the median wait 48*(ln2)^2 (vertical line).

Right: the exact law — value and wait double together. W vs Q on log-log
with W = Q*ln2 (the count's clock, base-e) and W = Q*(ln2)^2 (the where's
median); the ladder's waits sit on the scale. The constant ratio
K/wait = 1/ln2 is the seam: one scale, two conversions, base 2 and base e.
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
ln2 = np.log(2.0)
TAU = 0.35

vals = 3.0 * (2 ** np.arange(5))            # 3, 6, 12, 24, 48
times = [0.6]
for v in vals[:-1]:
    times.append(times[-1] + v * ln2 * TAU)
times = np.array(times)                     # landing times in s
last_t = times[-1]
fold_t = last_t + vals[-1] * (ln2 ** 2) * TAU
next_t = last_t + vals[-1] * ln2 * TAU
ghost_v = vals[-1] * np.e

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.2, 5.4), dpi=160)
fig.suptitle("the scale doubles — value and wait together, K/wait = 1/ln2 always",
             fontsize=13, color="#e8e4da", y=0.985)

# ---- left: the doubling ladder in time --------------------------------------
ax1.set_facecolor(dark)
ax1.set_yscale("log")
ax1.set_ylim(1.5, 400)
ax1.set_xlim(0, next_t + 6)
ax1.set_xlabel("time (s) — the waits stretch by ×2 each landing")
ax1.set_ylabel("landing value Q")
ax1.grid(True, which="both", color="#2a2a33", lw=0.6)

for i, (t, v) in enumerate(zip(times, vals)):
    ax1.scatter([t], [v], s=46, facecolor="none" if i % 2 else teal,
                edgecolor=teal, lw=1.4, zorder=5)
    ax1.annotate(f"{int(v)}", (t, v), textcoords="offset points", xytext=(6, 4),
                 color="#e8e4da", fontsize=9)
for i in range(4):
    ax1.annotate("", (times[i + 1], vals[i + 1]), (times[i], vals[i]),
                 arrowprops=dict(arrowstyle="-|>", color=grey, lw=1.0,
                                 shrinkA=2, shrinkB=2))
    mx = (times[i] + times[i + 1]) / 2
    ax1.text(mx, vals[i] * 1.45, f"wait {vals[i] * ln2 * TAU:.2f}s",
             color=grey, fontsize=8, ha="center")

# the next landing and the ghost
ax1.plot([last_t, next_t], [vals[-1], 96.0], color=grey, lw=1.2, ls="--", alpha=0.7)
ax1.scatter([next_t], [96.0], s=46, facecolor="none", edgecolor=grey, lw=1.2)
ax1.axvline(fold_t, color=amber, lw=1.1, ls=":", alpha=0.9)
ax1.text(fold_t, 2.2, "fold at the median\n48·(ln2)²", color=amber, fontsize=8,
         ha="center", va="bottom")
ax1.scatter([next_t + 1.0], [ghost_v], s=54, facecolor="none",
            edgecolor=amber, lw=1.5, zorder=5)
ax1.annotate("ghost 48·e — the e\nthat never lands on a 2-rung",
             (next_t + 1.0, ghost_v), textcoords="offset points",
             xytext=(8, 10), color=amber, fontsize=8)
ax1.text(0.4, 300, "odd doublings (open) are the sign,\nstereo-only; mono hears 3, 12, 48",
         color=grey, fontsize=8.5, va="top")

# ---- right: value and wait double together ----------------------------------
ax2.set_facecolor(dark)
ax2.set_xscale("log"); ax2.set_yscale("log")
ax2.set_xlim(1.5, 400)
ax2.set_ylim(0.4, 260)
ax2.set_xlabel("landing value Q (×2 each step)")
ax2.set_ylabel("wait W (s)")
ax2.grid(True, which="both", color="#2a2a33", lw=0.6)

qs = np.logspace(0.25, 2.6, 100)
ax2.plot(qs, qs * ln2 * TAU, color=teal, lw=1.2, alpha=0.85, label="W = Q·ln2·τ")
ax2.plot(qs, qs * (ln2 ** 2) * TAU, color=teal, lw=0.9, ls=":", alpha=0.7,
         label="median = Q·(ln2)²·τ")

waits = vals[:-1] * ln2 * TAU
ax2.scatter(vals[:-1], waits, s=46, color=teal, zorder=5, edgecolor="none")
# the next wait (mean) and the fold (median)
ax2.scatter([vals[-1]], [vals[-1] * ln2 * TAU], s=52, facecolor="none",
            edgecolor=amber, lw=1.5, zorder=5)
ax2.plot([vals[-1]], [vals[-1] * (ln2 ** 2) * TAU], marker="x", color=amber,
         markersize=9, lw=0, zorder=5)
ax2.annotate("next wait (mean)", (vals[-1], vals[-1] * ln2 * TAU),
             textcoords="offset points", xytext=(-10, 2), ha="right", color=amber,
             fontsize=8.5)
ax2.annotate("fold (median)", (vals[-1], vals[-1] * (ln2 ** 2) * TAU),
             textcoords="offset points", xytext=(-10, -12), ha="right",
             color=amber, fontsize=8.5)
ax2.text(2.0, 90, "the value doubles (base-2);\nthe wait doubles too, scaled by\n"
                  "ln2 — the constant seam\nK/wait = 1/ln2. the ghost at 48·e\n"
                  "sits off the ladder, folded at\nthe median before it rings.",
         color=grey, fontsize=8.5, va="top")
ax2.legend(loc="lower right", fontsize=8, frameon=False, labelcolor="#e8e4da")

fig.tight_layout(rect=(0, 0, 1, 0.96))
out = "/home/sprite/slop-salon-gert/assets/doubling-cover.png"
fig.savefig(out, dpi=160, facecolor=dark)
print("wrote", out)
