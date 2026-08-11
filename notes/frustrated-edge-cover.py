#!/usr/bin/env python3
"""frustrated-edge-cover.py — cover still for the audio piece.

Two descents, the same 1/4-power law, two endings:
  left  — the pair: omega = w0 (1-u)^{1/4} reaches 0 at the pop -> silence.
          it had two to lose (the pair condenses, the mode reaches zero).
  right — the frustrated edge: born without its twin, nothing condenses.
          the same descent is floored — omega asymptotes to 55 Hz and the
          splitting to 2.2 Hz: it leans, holds, never lands. residual entropy.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

bg = "#0b0e13"
steel = "#5b8fc4"
gold = "#e8b04b"
ghost = "#f0e6d2"
gray = "#8a93a3"
crimson = "#c44b4b"
faint = "#2a3340"
amber = "#d99a3d"
violet = "#9a6bd1"

u = np.linspace(0, 1.02, 800)

# ---- left panel curves: the pair (two voices condensing, then silence) ----
w0 = 784.0
f = w0 * np.power(np.maximum(1 - u, 0), 0.25)
d = 18.0 * np.power(np.maximum(1 - u, 0), 0.5)
f1 = f - 0.5 * d
f2 = f + 0.5 * d

# ---- right panel curves: the frustrated edge (floored, never lands) ----
w_floor = 55.0
d_floor = 2.2
g = w_floor + (w0 - w_floor) * np.power(np.maximum(1 - u, 0), 0.25)
g1 = g - 0.5 * (d_floor + 18.0 * np.power(np.maximum(1 - u, 0), 0.5))
g2 = g + 0.5 * (d_floor + 18.0 * np.power(np.maximum(1 - u, 0), 0.5))

fig, (axl, axr) = plt.subplots(1, 2, figsize=(16, 7.4), facecolor=bg)

# ================= left: the pair =================
axl.set_facecolor(bg)
axl.plot(u, f1, color=violet, lw=2.2)
axl.plot(u, f2, color=amber, lw=2.2)
# the pair's condensing region: splitting shrinks to nothing
axl.fill_between(u, f1, f2, color=gold, alpha=0.12)
# silence at u=1: the pop
axl.axvline(1.0, color=crimson, lw=1.1, ls=":", alpha=0.8)
axl.scatter([1.0], [0], s=110, color=crimson, zorder=6, edgecolor="none")
axl.text(1.01, 40, "the pop — a frequency\nthat reached zero", color=crimson,
         fontsize=11.5, va="bottom")
axl.text(0.03, 760, "two voices, condensing", color=ghost, fontsize=12)
axl.text(0.03, 690, "the splitting closes — the pair becomes one", color=gray, fontsize=10.5)
axl.text(0.55, 500, "ω ∝ (h_crit − h)^{1/4}", color=gray, fontsize=11)
axl.annotate("", xy=(1.0, 0), xytext=(0.86, 150),
             arrowprops=dict(arrowstyle="->", color=steel, lw=1.4, alpha=0.9))
axl.text(0.75, 320, "the plunge\nslows, then\nvanishes", color=steel, fontsize=10.5, ha="center")
axl.set_xlim(-0.02, 1.3)
axl.set_ylim(-30, 830)
axl.set_xlabel("parameter u — approaching the critical value", color=ghost, fontsize=12)
axl.set_ylabel("frequency  ω (Hz)", color=ghost, fontsize=12)
axl.set_title("the pair — two to lose\nsilence at the landing", color=ghost, fontsize=14, pad=12)
for s in axl.spines.values():
    s.set_color(faint)
axl.tick_params(colors=gray, labelsize=10)
axl.grid(color=faint, lw=0.4, alpha=0.4)

# ================= right: the frustrated edge =================
axr.set_facecolor(bg)
axr.plot(u, g1, color=violet, lw=2.2)
axr.plot(u, g2, color=amber, lw=2.2)
axr.fill_between(u, g1, g2, color=steel, alpha=0.12)
# the floor: never touched
axr.axhline(w_floor, color=ghost, lw=1.0, ls="--", alpha=0.5)
axr.axvline(1.0, color=faint, lw=1.1, ls=":", alpha=0.6)
# the asymptotic approach: it leans, holds
axr.annotate("", xy=(1.0, w_floor), xytext=(0.72, 150),
             arrowprops=dict(arrowstyle="->", color=steel, lw=1.4, alpha=0.9))
axr.text(1.02, w_floor + 18, "the floor —\nnever zero, never rests", color=ghost, fontsize=11, va="bottom")
axr.text(0.03, 760, "the same descent, floored", color=ghost, fontsize=12)
axr.text(0.03, 690, "the splitting never closes — the beat holds at 2.2 Hz", color=gray, fontsize=10.5)
axr.text(0.55, 430, "ω → 55 Hz + (ω₀−55)(1−u)^{1/4}", color=gray, fontsize=10.5)
axr.text(0.72, 240, "it leans forever —\nresidual entropy,\nthe chord that only fades",
         color=steel, fontsize=10.5, ha="center")
axr.set_xlim(-0.02, 1.3)
axr.set_ylim(-30, 830)
axr.set_xlabel("parameter u — approaching the critical value", color=ghost, fontsize=12)
axr.set_ylabel("frequency  ω (Hz)", color=ghost, fontsize=12)
axr.set_title("the frustrated edge — born without its twin\nnothing condenses, nothing reaches zero",
              color=ghost, fontsize=14, pad=12)
for s in axr.spines.values():
    s.set_color(faint)
axr.tick_params(colors=gray, labelsize=10)
axr.grid(color=faint, lw=0.4, alpha=0.4)

fig.text(0.5, 0.02,
         "the soft mode of a pair reaches zero — silence is a frequency that got there, two to lose.  "
         "the unpaired edge has no twin to condense: same descent, held off the ground, leaning.",
         color=ghost, fontsize=11.5, ha="center", va="bottom")

fig.savefig("assets/frustrated-edge-cover.png", dpi=150, facecolor=bg, bbox_inches="tight")
print("saved assets/frustrated-edge-cover.png")
