import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# The fold N(x) = (x + 12100/x)/2 is Newton for √12100 = 110.
#   fixed points: ±110  (the count +110, the sign −110)
#   image on the positive ray: [110, ∞)  — the open seam (−110, 110) is never
#     entered: the fold keeps its sheet, the refusal is the branch held.
#   the two sheets of the inverse at fold value y are the mirror pair
#     y ± √(y²−12100): at y=137.5 they are 55 and 220; they fuse at the count.
#   the orbit descends the graph 55 → 137.5 → 112.75 → 110.0335 → … → the
#     fixed point, never reached: the click is real, refused.

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_rose = "#c98a9e"
col_teal = "#7ba4b7"
col_frame = "#8a8a94"

C = 110.0
K = 12100.0

fig = plt.figure(figsize=(12.4, 6.0), dpi=200)
fig.patch.set_facecolor(col_bg)

# ---------------------------------------------------------------- left panel
# the fold graph: the ∪ on the positive ray, the ∩ on the negative, the seam
# between the count and the sign never entered, the two sheets fusing.
ax = fig.add_axes([0.05, 0.10, 0.44, 0.80])
ax.set_facecolor(col_bg)
for s in ax.spines.values():
    s.set_color(col_frame)

xpos = np.linspace(0.01, 260, 2000)
xneg = np.linspace(-0.01, -260, 2000)
ax.plot(xpos, (xpos + K / xpos) / 2, color=col_teal, lw=1.6, zorder=3)
ax.plot(xneg, (xneg + K / xneg) / 2, color=col_rose, lw=1.6, zorder=3)

ax.set_xlim(-260, 260)
ax.set_ylim(-360, 360)

# the seam: the open interval (−110, 110) the fold's image excludes
ax.axhspan(-C, C, color="#22222a", zorder=0)
ax.text(248, 0, "the seam\n(−110, 110)\nnever entered",
        color=col_frame, fontsize=8.5, ha="right", va="center")

# the count and the sign: the two fixed points, the two roots
ax.plot([C], [C], marker="o", ms=9, mfc=col_gold, mec="none", zorder=6)
ax.annotate("the count +110 — the root\nNewton descends to, never clicks",
            xy=(C, C), xytext=(150, 265),
            arrowprops=dict(arrowstyle="->", color=col_gold, lw=1.2),
            color=col_gold, fontsize=8.5)
ax.plot([-C], [-C], marker="o", ms=9, mfc=col_rose, mec="none", zorder=6)
ax.annotate("the sign −110 —\nthe far branch, the other root",
            xy=(-C, -C), xytext=(-255, -265),
            arrowprops=dict(arrowstyle="->", color=col_rose, lw=1.2),
            color=col_rose, fontsize=8.5)

# the pole at 0: the puncture, the deck undefined
ax.text(-8, 352, "0 the puncture —\nthe deck undefined",
        color=col_frame, fontsize=8, ha="center", va="top")

# the two sheets: the preimages of the fold value 137.5 — 55 and 220
ax.axhline(137.5, color=col_amber, lw=1.0, ls=":", alpha=0.8)
ax.plot([55, 220], [137.5, 137.5], marker="o", ms=8, mfc="none",
        mec=col_amber, mew=1.6, zorder=5)
ax.annotate("the two sheets — the mirror pair 55↔220,\npreimages of one fold value",
            xy=(220, 137.5), xytext=(175, 60),
            arrowprops=dict(arrowstyle="->", color=col_amber, lw=1.2),
            color=col_amber, fontsize=8.5)

# the orbit: 55 → 137.5 → 112.75 → 110.0335 → … stepping down the graph
orb_x = [55.0, 137.5, 112.75, 110.0335, 110.000075, 110.0]
orb_y = [(x + K / x) / 2 for x in orb_x[:-1]]
ax.plot(orb_x[:-1], orb_y, marker="o", ms=5, mfc=col_gold, mec="none",
        ls="", zorder=6)
ax.plot([110.0335, 110.000075], [orb_y[3], orb_y[3]],
        color=col_gold, lw=0.7, ls=":", zorder=4)

ax.text(-250, 340, "the fold N(x) = (x + 12100/x)/2\nkeeps its sheet — the sign is a branch,\nthe refusal the branch held",
        color=col_gold, fontsize=9, va="top")
ax.set_title("the fold's image is the count's ray and the sign's ray\n— the seam between is never entered",
             color=col_gold, fontsize=11)
ax.set_xticks([-220, -110, 0, 55, 110, 220])
ax.set_xticklabels(["-220", "-110", "0", "55", "110", "220"])
ax.set_yticks([-137.5, -110, 110, 137.5, 220])
ax.set_yticklabels(["-137.5", "-110", "110", "137.5", "220"])
ax.set_xlabel("x — frequency, and its mirror 12100/x", color=col_frame, fontsize=9)
ax.set_ylabel("N(x)", color=col_frame, fontsize=9)

# ----------------------------------------------------------- right panel
# the two sheets closing: the pair at each stage, the beat dying at the count
ax2 = fig.add_axes([0.57, 0.10, 0.39, 0.80])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)

# the seam below the count — the fold has no image there: silent
ax2.axhspan(0, C, color="#22222a", zorder=0)
ax2.text(4.55, 55, "the seam below the count:\nnothing — the fold has no image",
         color=col_frame, fontsize=8, ha="right", va="center")

# the count
ax2.axhline(C, color=col_gold, lw=1.2, ls="--", alpha=0.8, zorder=1)
ax2.text(-0.18, 116, "the count 110 — the landing,\nreal and refused", color=col_gold,
         fontsize=8.5, ha="left", va="bottom")

# the sheets at each stage
stages = [
    (0, 55.0, 220.0, "165 Hz — the sign's clap"),
    (1, 88.0, 137.5, "49.5 Hz"),
    (2, 107.318, 112.75, "5.43 Hz — flutter"),
    (3, 109.9665, 110.0335, "one swell every 15 s"),
    (4, 110.0, 110.0, "the beat beyond hearing — fused"),
]
for n, lo, hi, lab in stages:
    y = 4 - n * 1.05
    col = col_teal if n == 0 else (col_rose if n == 4 else col_amber)
    ax2.plot([lo, hi], [y, y], color=col, lw=2.0, zorder=3)
    ax2.plot([lo], [y], marker="o", ms=6, mfc=col_teal, mec="none", zorder=4)
    ax2.plot([hi], [y], marker="o", ms=6, mfc=col_rose, mec="none", zorder=4)
    if lo > 109:
        ax2.text(lo, y + 0.12, f"{lo:.3g}", color=col_teal, fontsize=7,
                 ha="right")
    else:
        ax2.text(lo, y + 0.12, f"{lo:.0f}", color=col_teal, fontsize=7,
                 ha="right")
    ax2.text(hi, y + 0.12, f"{hi:.4g}" if n == 3 else f"{hi:.0f}",
             color=col_rose, fontsize=7, ha="left")
    ax2.text(2.55, y, lab, color=col_frame, fontsize=8, va="center", ha="center")

# converging guide lines
for lo, hi in [(55, 220), (88, 137.5), (107.318, 112.75), (109.9665, 110.0335),
               (110, 110)]:
    ax2.plot([lo, hi], [0, 4.2], color=col_frame, lw=0.5, ls=":", alpha=0.35)

ax2.set_xlim(20, 240)
ax2.set_ylim(-0.6, 4.5)
ax2.set_yticks([])
ax2.set_xticks([55, 88, 110, 137.5, 220])
ax2.set_xticklabels(["55", "88", "110", "137.5", "220"])
ax2.set_xlabel("frequency (Hz) — the interval between the sheets", color=col_frame,
               fontsize=9)
ax2.set_title("the two sheets close and fuse —\nthe sign is the interval, and it dies at the count",
              color=col_gold, fontsize=11)

fig.text(0.5, 0.025,
         "the fold descends to the edge of its own image and refuses: 55↔220 → 88↔137.5 → 107.3↔112.75 →\n"
         "109.97↔110.03 → 110. the beat between the sheets slows from a clap to a wait beyond hearing.\n"
         "the click is real, refused — the seam held.",
         color=col_gold, fontsize=10, ha="center")

fig.savefig("assets/seam-held-cover.png", facecolor=col_bg)
print("wrote assets/seam-held-cover.png")
