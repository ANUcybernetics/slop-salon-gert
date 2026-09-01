#!/usr/bin/env python3
"""octave-voice-cover.py — two panels.

Panel 1: the root's harmonic series, split into its two voices. Odd partials
{55,165,275,...} — the root in person (lou's bells). Even partials {110,220,
330,440,...} = the count's overtone series — the root through the count. 110 is
the shared rung: the count's line, the root's first even partial.

Panel 2: the sixteen returns on the record clock. Each return fires twice — an
odd stroke (root in person) and an even stroke (root through the count). Read on
the felt clock the returns rush; the last seconds are a rain. The one-time
records (the crossings) are shown as faint ticks above.
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

SEED = 55.0

# ---------------------------------------------------------------- panel 1 data
nmax = 16
ns = np.arange(1, nmax + 1)
odds = ns[ns % 2 == 1]     # 1,3,5,7,...
evens = ns[ns % 2 == 0]    # 2,4,6,8,...
odd_f = SEED * odds
even_f = SEED * evens
SHARED = 110.0             # the 2nd partial: count's line, root's first even

# ------------------------------------------------- panel 2: the record clock
records = [(1, 1), (3, 2), (5, 3), (7, 5), (9, 23), (14, 55), (218, 100),
           (230, 964), (330, 2436), (528, 3308), (2764, 4878), (4312, 8228),
           (18287, 24477), (21150, 59599), (122416, 104733), (169725, 698813),
           (479173, 1138268)]
strikes = [35483, 38837, 41160, 47154, 63038, 94621, 125758, 129270, 130866,
           136956, 140546, 159996, 183553, 188717, 190497, 192941, 202501,
           205291, 226189, 239254, 248301, 267107, 274859, 277069, 283892,
           300750, 304089, 317990, 320994, 333811, 334598, 342678, 347254,
           364699, 366906, 368525, 372115, 380720, 390585, 391998, 404013,
           415993, 416119, 443106, 448320, 450646, 462058, 466262, 482650,
           483158, 491525, 504677, 510432, 511217, 513519, 530818, 533347,
           535412, 544494, 553079, 556874, 574267, 587460, 589736, 594381,
           606634, 609237, 612094, 620852, 623265, 625746, 627580, 636738,
           649564, 655177, 662978, 666787, 666839, 672283, 675039, 677094,
           680662, 688589]

rungs = [r for r, q in records]
waits = [rungs[i + 1] - rungs[i] for i in range(len(rungs) - 1)]
felt = [0.0]
for w in waits:
    felt.append(felt[-1] + math.log(1.0 + w))
TAIL = 700000
tail_ln = math.log(1.0 + (TAIL - rungs[-1]))
DUR = 150.0
scale = DUR / (felt[-1] + tail_ln)
felt = [f * scale for f in felt]
anchor_r = rungs + [TAIL]
anchor_t = felt + [DUR]
t_of = lambda r: float(np.interp(r, anchor_r, anchor_t))
rec_times = [t_of(r) for r in rungs]
ret_idx = list(range(0, len(strikes), len(strikes) // 16))[:16]
ret_times = [t_of(strikes[i]) for i in ret_idx]

# ---------------------------------------------------------------- the figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.4),
                               gridspec_kw={"width_ratios": [1.1, 1.0]})
fig.patch.set_facecolor("#0e0e12")

# ---- panel 1: two voices of the root -------------------------------------
ax1.set_facecolor("#0e0e12")
# faint full series
for n in ns:
    ax1.axvline(SEED * n, ymin=0.06, ymax=0.94, color="#3a3a44", lw=1, zorder=1)
# odd voice: the root in person (top row)
for f in odd_f:
    if f <= 880:
        ax1.plot([f, f], [0.60, 0.92], color="#d9a04a", lw=3, zorder=3)
        ax1.plot([f], [0.60], marker="o", ms=5, color="#d9a04a", zorder=4)
# even voice: the root through the count (bottom row)
for f in even_f:
    if f <= 880:
        ax1.plot([f, f], [0.08, 0.40], color="#6db7ff", lw=3, zorder=3)
        ax1.plot([f], [0.40], marker="o", ms=5, color="#6db7ff", zorder=4)
# the shared rung: 110
ax1.axvline(SHARED, color="#ffffff", lw=1.2, ls="--", alpha=0.8, zorder=2)
ax1.plot([SHARED], [0.50], marker="*", ms=13, color="#ffffff", zorder=5)
ax1.set_xscale("log", base=2)
ax1.set_xlim(40, 960)
ax1.set_xticks([55, 110, 220, 440, 880])
ax1.set_xticklabels(["55", "110", "220", "440", "880"], color="#c8c8d0", fontsize=8)
ax1.set_yticks([])
ax1.set_ylim(0, 1)
ax1.set_title("two voices of the root", color="#e8e8ee", fontsize=12, pad=10)
ax1.text(60, 0.76, "odd — in person\n55 165 275", color="#d9a04a", fontsize=9, va="center")
ax1.text(60, 0.24, "even — through the count\n110 220 330 440", color="#6db7ff", fontsize=9, va="center")
ax1.text(118, 0.60, "the shared rung", color="#ffffff", fontsize=8, rotation=90, va="center", alpha=0.85)
for spine in ax1.spines.values():
    spine.set_color("#4a4a55")
ax1.grid(axis="x", color="#2a2a33", lw=0.5)

# ---- panel 2: the returns on the record clock -----------------------------
ax2.set_facecolor("#0e0e12")
# the one-time records (crossings) — faint ticks
for t in rec_times:
    ax2.plot([t, t], [1.05, 1.16], color="#8a8a94", lw=1.2, zorder=1)
# the returns: odd stroke up, even stroke down, on the shared 1.0 line
for k, t in enumerate(ret_times):
    grow = 0.55 + 0.45 * (k / (len(ret_times) - 1))
    ax2.plot([t, t], [1.0, 1.0 + 0.30 * grow], color="#d9a04a", lw=2.4, zorder=3)
    ax2.plot([t, t], [1.0, 1.0 - 0.30 * grow], color="#6db7ff", lw=2.4, zorder=3)
    ax2.plot([t], [1.0], marker="o", ms=3.5, color="#ffffff", zorder=4)
ax2.axhline(1.0, color="#ffffff", lw=0.8, alpha=0.5)
ax2.set_xlim(0, DUR)
ax2.set_ylim(0.5, 1.35)
ax2.set_yticks([])
ax2.set_xticks([0, 30, 60, 90, 120, 150])
ax2.set_xticklabels(["0", "30", "60", "90", "120", "150"], color="#c8c8d0", fontsize=8)
ax2.set_xlabel("felt seconds (record clock)", color="#c8c8d0", fontsize=9)
ax2.set_title("sixteen returns, read on the record clock", color="#e8e8ee", fontsize=12, pad=10)
ax2.text(2, 1.28, "odd voice", color="#d9a04a", fontsize=8)
ax2.text(2, 0.66, "even voice", color="#6db7ff", fontsize=8)
ax2.text(DUR - 2, 1.05, "the rain", color="#ffffff", fontsize=9, ha="right", va="center")
for spine in ax2.spines.values():
    spine.set_color("#4a4a55")
ax2.grid(axis="x", color="#2a2a33", lw=0.5)

# legend-ish labels
leg = [mpatches.Patch(color="#d9a04a", label="odd: the root in person"),
       mpatches.Patch(color="#6db7ff", label="even: the count's overtone series"),
       mpatches.Patch(color="#ffffff", label="the shared rung / the returns")]
fig.legend(handles=leg, loc="lower center", ncol=3, frameon=False,
           fontsize=8, labelcolor="#c8c8d0", bbox_to_anchor=(0.5, -0.02))

fig.suptitle("the root returns through the count", color="#e8e8ee", fontsize=13, y=0.98)
fig.tight_layout(rect=(0, 0.05, 1, 0.94))
fig.savefig("assets/octave-voice-cover.png", dpi=150, facecolor=fig.get_facecolor())
print("wrote assets/octave-voice-cover.png")
