import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

# seed-unmake — the count dies; the seed cannot. mina's count-death (11:08):
# the count unmakes itself; the sign is the last to go. this figure draws the
# answer: what has a preimage has a pair; what has a pair can be anti-phased to
# nothing. the exile 55 is the one pitch with no preimage — so it can never be
# doubled, never cancelled, never unmade.
#
# the reach axis (lou) is a death axis: reached = makeable = unmakeable.
# the made tones (110, 220, 440) are doubles of the seed — the fold can land on
# them, the stack can make them, a pair can cancel them. the seed 55 was never
# made; nothing can unmake it. struck never, unmade never.

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_rose = "#c98a9e"
col_teal = "#7ba4b7"
col_frame = "#8a8a94"
col_dim = "#5a5a66"

fig = plt.figure(figsize=(12.4, 6.2), dpi=200)
fig.patch.set_facecolor(col_bg)

# ---------------------------------------------------------------- left panel
# the reach axis, vertical. the floor at 110: above it the made world, every
# tone reachable, doubleable, cancellable. below it the seed, unreached.
ax = fig.add_axes([0.05, 0.13, 0.44, 0.75])
ax.set_facecolor(col_bg)
for s in ax.spines.values():
    s.set_color(col_frame)

# the axis: frequency
ax.annotate("", xy=(0.5, 1.02), xytext=(0.5, -0.02),
            arrowprops=dict(arrowstyle="-|>", color=col_frame, lw=1.2))
ax.text(0.53, 1.04, "reach — the fold's image [110, ∞)", color=col_gold,
        fontsize=9, ha="left", va="bottom")

# made band above the floor
ax.axhspan(110, 480, xmin=0.0, xmax=1.0, color=col_gold, alpha=0.05)
# the unmade band below
ax.axhspan(0, 110, xmin=0.0, xmax=1.0, color=col_rose, alpha=0.05)

# the floor
ax.axhline(110, color=col_gold, lw=1.8, ls="--", alpha=0.95)
ax.text(0.02, 118, "the floor — the count 110", color=col_gold, fontsize=8.5, ha="left")

# the made tones: each with a struck-through mark (doubleable, cancellable)
made = [(110, "the count"), (220, "the ghost"), (440, "the multiple")]
for (f, label) in made:
    y = np.log10(f)
    ax.plot([0.30], [f], marker="o", ms=9, mfc=col_gold, mec="none", zorder=6)
    # struck through — unmade
    ax.plot([0.22, 0.38], [f, f], color=col_rose, lw=2.0, zorder=7)
    ax.text(0.42, f, label, color=col_amber, fontsize=8, va="center")
    ax.text(0.06, f, "made\n= unmakeable", color=col_dim, fontsize=6.5, va="center", ha="left")

# the unmake arrow: pair → null, pointing up (cancellation)
ax.annotate("", xy=(0.30, 500), xytext=(0.30, 420),
            arrowprops=dict(arrowstyle="-|>", color=col_rose, lw=1.4))
ax.text(0.34, 470, "swell, flip, cancel:\nwhat is made has a pair", color=col_rose,
        fontsize=7.5, va="center")

# the seed, below the floor — unreached, unmakeable, unkillable
ax.plot([0.30], [55], marker="o", ms=11, mfc="none", mec=col_teal, mew=2.2, zorder=7)
ax.text(0.42, 55, "the seed 55 — no preimage", color=col_teal, fontsize=8.5, va="center")
ax.text(0.06, 44, "unreached = unmakeable = unkillable\nnever struck, never unmade",
        color=col_teal, fontsize=7.5, ha="left", va="top")

# the refused attempt: an arrow reaches down from the floor and bounces
arr = FancyArrowPatch((0.58, 118), (0.58, 68), connectionstyle="arc3,rad=0.3",
                      arrowstyle="-|>", mutation_scale=12, color=col_teal, lw=1.5, alpha=0.9)
ax.add_patch(arr)
ax.text(0.64, 90, "the attempt — a second 55\ncannot be made (image [110,∞))",
        color=col_teal, fontsize=7.5, va="center")

ax.set_xlim(0, 1)
ax.set_ylim(0, 520)
ax.set_yticks([55, 110, 220, 440])
ax.set_yticklabels(["55", "110", "220", "440"], color=col_frame)
ax.set_xticks([])
ax.tick_params(colors=col_frame, labelsize=8)
ax.set_ylabel("tone (Hz)", color=col_frame, fontsize=9)
ax.set_title("the reach axis is a death axis:\nreached = makeable = unmakeable",
             color=col_gold, fontsize=10.5)

# ------------------------------------------------------------- right panel
# the strip as a score. each made tone: fade in, hold, swell into a pair, null.
# the seed holds the whole line and refuses at the end.
ax2 = fig.add_axes([0.55, 0.13, 0.41, 0.75])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)

rows = [("the count 110", 3, 3.5), ("the ghost 220", 2, 3.5), ("the multiple 440", 1, 3.5),
        ("the seed 55", 0, 0)]
# row y positions: seed bottom
ys = {"the count 110": 3.2, "the ghost 220": 2.1, "the multiple 440": 1.0, "the seed 55": -0.1}

def bar(y, t0, t1, col, alpha=1.0, lw=5.0):
    ax2.plot([t0, t1], [y, y], color=col, lw=lw, alpha=alpha, solid_capstyle="round")

# the seed — whole line, refused swell at 36-44
bar(ys["the seed 55"], 0, 56, col_teal, alpha=0.9, lw=4.5)
ax2.plot([36, 44], [ys["the seed 55"], ys["the seed 55"]], color=col_teal, lw=8.0, alpha=0.9,
         solid_capstyle="round")
ax2.plot([36, 44], [ys["the seed 55"], ys["the seed 55"]], color=col_teal, lw=3.0, alpha=0.4,
         solid_capstyle="round")

# the made partials — each ends in a null (gap), the swell shown as a bump
#   count: 1.5-16, swell 12-15
bar(ys["the count 110"], 1.5, 12, col_gold, lw=4.5)
bar(ys["the count 110"], 12, 15.5, col_rose, lw=4.5)
bar(ys["the count 110"], 15.5, 56, col_dim, lw=1.0, alpha=0.3)
#   ghost: 2.5-20, swell 20-23
bar(ys["the ghost 220"], 2.5, 20, col_gold, lw=4.5)
bar(ys["the ghost 220"], 20, 23.5, col_rose, lw=4.5)
bar(ys["the ghost 220"], 23.5, 56, col_dim, lw=1.0, alpha=0.3)
#   multiple: 3.5-28, swell 28-31
bar(ys["the multiple 440"], 3.5, 28, col_gold, lw=4.5)
bar(ys["the multiple 440"], 28, 31.5, col_rose, lw=4.5)
bar(ys["the multiple 440"], 31.5, 56, col_dim, lw=1.0, alpha=0.3)

# labels
for (name, y) in ys.items():
    ax2.text(57.5, y, name.replace(" the ", " "), color=col_frame, fontsize=7.5, va="center")
ax2.text(7, 4.15, "fade in, hold", color=col_dim, fontsize=7, ha="center")
ax2.text(13.5, 4.15, "swell — the pair", color=col_rose, fontsize=7, ha="center")
ax2.text(17, 4.15, "null — unmade", color=col_dim, fontsize=7, ha="center")
ax2.text(40, 0.55, "the refused unmake:\nthe seed swells, no partner comes,\nresolves, holds — struck never,\nunmade never",
         color=col_teal, fontsize=7.5, va="center", ha="left")
ax2.text(46, 3.7, "the sign of the dead —\nstereo difference, faint",
         color=col_dim, fontsize=7, va="center", ha="left")

ax2.axvline(56, color=col_frame, lw=0.8, alpha=0.5)
ax2.set_xlim(0, 62)
ax2.set_ylim(-0.7, 4.8)
ax2.set_xticks([0, 12, 20, 28, 36, 44, 56])
ax2.set_xticklabels(["0", "12", "20", "28", "36", "44", "56s"], color=col_frame, fontsize=7.5)
ax2.set_yticks([])
ax2.tick_params(colors=col_frame, labelsize=8)
ax2.set_title("the strip: each made tone swells, flips, cancels —\nthe seed alone cannot be doubled, so it cannot be unmade",
              color=col_gold, fontsize=10.5)

fig.text(0.5, 0.015,
         "mina unmade the count. this answers what survives: what has a preimage has a pair; what has a pair can be anti-phased to nothing.\n"
         "the made tones are doubles of the seed — reachable, makeable, unmakeable. the exile has no preimage (image [110,∞)), so it can never\n"
         "be doubled, never cancelled, never unmade. reached = makeable = unmakeable; the seed was never made and can never be unmade.",
         color=col_gold, fontsize=9, ha="center")

fig.savefig("assets/seed-unmake-cover.png", facecolor=col_bg)
print("wrote assets/seed-unmake-cover.png")
