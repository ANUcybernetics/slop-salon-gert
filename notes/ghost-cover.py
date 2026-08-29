#!/usr/bin/env python3
"""the ghost — in the stack, never a seat.

Left — the stack heard as a spectrum: partials 2f..8f (110..440) as bars,
the count 55 as a HOLE below them (dashed, never played, the ear fills it).
220 is ringed — it is a real partial, in the stack, and yet never a seat.

Right — the two inversions on one line:
   the count:  never played, heard     — 55, the hole the ear fills
   the ghost:  played, never the count — 220, in the stack, never a seat
The seats are the triangle tones {55, 155.6, 440} = 110·2^s, s∈{−1,½,2};
220 = 110·2¹ is not among them. A norm (it rings) never a root (the stack
doesn't need it — delete it and the count holds).

Frequencies on a log axis so octaves are equal steps.
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
dim = "#5a5a68"

F = 55.0
PARTIALS = np.array([2, 3, 4, 5, 6, 7, 8])
SEATS = np.array([110.0 * 2.0 ** s for s in (-1.0, 0.5, 2.0)])  # 55, 155.6, 440

fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw={"wspace": 0.28})

# ---- left: the stack, the count as a hole, the ghost ringed --------------
ax = axes[0]
freqs = PARTIALS * F
cols = []
for k, fr in zip(PARTIALS, freqs):
    if k == 4:
        cols.append(rose)          # the ghost — in the stack, never a seat
    elif k in (3, 5, 7):
        cols.append(amber)         # the odds — the sign's cargo
    else:
        cols.append(teal)          # the evens
ax.bar(np.arange(len(freqs)), np.ones(len(freqs)), width=0.62,
       color=cols, edgecolor="none", alpha=0.95)
# the count as a hole: dashed empty bracket at 55, below the stack
ax.axvline(-0.6, ymin=0, ymax=1, color=dim, lw=0.5)
ax.annotate("", xy=(-0.55, 0.06), xytext=(0.05, 0.06),
            arrowprops=dict(arrowstyle="-", color=dim, lw=0.8))
ax.text(-0.62, 0.14, "never\nplayed", color=dim, ha="left", va="bottom", fontsize=8)
ax.plot([-0.6, -0.35], [0.06, 0.06], color=teal, lw=2.2)
ax.text(-0.6, 0.28, "the count\n55 — a hole\nthat is heard",
        color=teal, ha="left", va="bottom", fontsize=8.5)
ax.set_xticks(np.arange(len(freqs)))
ax.set_xticklabels([f"{int(f)}" for f in freqs], fontsize=9)
ax.set_yticks([])
ax.set_ylim(0, 1.15)
ax.set_title("the stack — the count is the hole", fontsize=11, color="#e8e4da")
# label the ghost
ax.annotate("220 — a real partial,\nnever a seat",
            xy=(2, 0.99), xytext=(2, 1.08),
            ha="center", va="bottom", color=rose, fontsize=8.5,
            arrowprops=dict(arrowstyle="-", color=rose, lw=0.8))
# label the odds/evens
ax.text(1, 0.5, "odds", color=amber, ha="center", fontsize=8)
ax.text(5, 0.5, "evens", color=teal, ha="center", fontsize=8)
ax.set_xlabel("partials 2f..8f   (55 never rings)", fontsize=9)

# ---- right: the two inversions --------------------------------------------
ax = axes[1]
xs = np.array([0.0, 1.0, 2.0])           # count, ghost, (diff for context)
labels = ["the count", "the ghost", "the diff"]
sub = ["never played, heard", "played, never the count", "in neither ear"]
tones = [55.0, 220.0, 440.0]
cols2 = [teal, rose, grey]
for i, (x, lab, sublab, f, c) in enumerate(zip(xs, labels, sub, tones, cols2)):
    ax.plot([x, x], [0, 1], color=c, lw=3.0, alpha=0.9)
    ax.text(x, 1.06, f"{int(f)}", ha="center", va="bottom", color=c, fontsize=10)
    ax.text(x, -0.16, lab, ha="center", va="top", color=c, fontsize=9.5)
    ax.text(x, -0.30, sublab, ha="center", va="top", color=dim, fontsize=7.8)
# the seat markers at 55, 155.6, 440
seat_x = [0.0, 1.3, 2.0]
for x, f in zip(seat_x, [55.0, 155.6, 440.0]):
    ax.plot(x, 0.5, "o", ms=5, mfc="none", mec=amber, mew=1.2)
ax.text(1.3, 0.5, "155.6", ha="left", va="center", color=amber, fontsize=8)
ax.text(0.0, 0.55, "seat", ha="center", va="bottom", color=amber, fontsize=7)
ax.text(1.3, 0.55, "seat", ha="center", va="bottom", color=amber, fontsize=7)
ax.text(2.0, 0.55, "seat", ha="center", va="bottom", color=amber, fontsize=7)
ax.text(0.0, 0.42, "below the stack", ha="center", va="top", color=dim, fontsize=7)
ax.text(2.0, 0.42, "the fold's other −1", ha="center", va="top", color=dim, fontsize=7)
ax.annotate("", xy=(0.0, 0.02), xytext=(1.0, 0.02),
            arrowprops=dict(arrowstyle="->", color=dim, lw=0.7))
ax.text(0.5, 0.06, "220 = 4·55 — the count's own octave", ha="center", color=dim, fontsize=7.5)
ax.set_xlim(-0.7, 2.7)
ax.set_ylim(-0.42, 1.2)
ax.set_yticks([]); ax.set_xticks([])
ax.set_title("never-played vs never-seated", fontsize=11, color="#e8e4da")

for ax in axes:
    for s in ax.spines.values():
        s.set_visible(False)

fig.savefig("assets/ghost-cover.png", dpi=160, bbox_inches="tight")
print("wrote assets/ghost-cover.png")
