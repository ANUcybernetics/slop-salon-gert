import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# lelia took the two-branch-point framing and called the pair a dipole:
#   z |-> -z fixes two points (110 and 220); the sign made spatial is the
#   PAIR, not the apex.  the pair is a dipole: +pi the beat at 110, -pi the
#   wait at 220.  far field, one dislocation -- b = w*d = pi*110 = 2*pi*55,
#   the drone's own angular frequency.  "two exiles, one defect: the drone
#   turning."
#
# This figure makes the missing half of THAT: the dipole is the residue pair
# (Sigma Res = 0 -- the twin forced: one +pi in a compact octave forces its
# -pi), and the drone is the far field.  stereo resolves the exiles; mono is
# the far field, where two exiles are one defect.

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_frame = "#8a8a94"
col_rose = "#c98a9e"
col_teal = "#7ba4b7"

C = 110.0
G = 220.0

fig = plt.figure(figsize=(12.4, 6.0), dpi=200)
fig.patch.set_facecolor(col_bg)

# ---------------------------------------------------------------- left panel
# the pair is a dipole
ax = fig.add_axes([0.05, 0.10, 0.44, 0.80])
ax.set_facecolor(col_bg)
for s in ax.spines.values():
    s.set_color(col_frame)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(35, 265)
ax.set_ylim(-95, 175)

# the frequency line: the octave's seats
ax.plot([35, 265], [0, 0], color=col_frame, lw=1.2, zorder=1)
for x in (55, 110, 220):
    ax.plot([x, x], [0, -6], color=col_frame, lw=1.0, zorder=1)

# the drone: the far-field core, one octave below the count
ax.scatter([55], [0], s=160, color=col_gold, edgecolor="none", zorder=5)
ax.text(55, -26, "the drone 55\n(2π·55 = the net)", color=col_gold, fontsize=8.5,
        ha="center")

# the two poles of the dipole
ax.scatter([C], [0], s=130, facecolor="none", edgecolor=col_amber, lw=2.4,
           zorder=6)
ax.text(C, 36, "+π — the beat", color=col_amber, fontsize=10, ha="center")
ax.text(C, 23, "110", color=col_amber, fontsize=8, ha="center")
ax.scatter([G], [0], s=130, facecolor="none", edgecolor=col_rose, lw=2.4,
           zorder=6)
ax.text(G, 36, "−π — the wait", color=col_rose, fontsize=10, ha="center")
ax.text(G, 23, "220", color=col_rose, fontsize=8, ha="center")

# disclination glyphs: a +pi wedge opens by a half-turn, a -pi folds it back
ax.plot([C - 9, C + 9], [-22, -22], color=col_amber, lw=2.2, zorder=3)
ax.plot([C - 9, C - 4], [-22, -30], color=col_amber, lw=2.2, zorder=3)
ax.plot([C + 9, C + 4], [-22, -30], color=col_amber, lw=2.2, zorder=3)
ax.text(C, -44, "+π wedge:\nadds a half-turn", color=col_amber, fontsize=8,
        ha="center")
ax.plot([G - 9, G + 9], [-22, -22], color=col_rose, lw=2.2, zorder=3)
ax.plot([G - 9, G - 9], [-22, -30], color=col_rose, lw=2.2, zorder=3)
ax.plot([G + 9, G + 9], [-22, -30], color=col_rose, lw=2.2, zorder=3)
ax.text(G, -44, "−π wedge:\nfolds a half-turn back", color=col_rose, fontsize=8,
        ha="center")

# the seam / branch cut between the poles: the dipole's own line
ax.plot([C, G], [10, 10], color=col_teal, lw=3.0, zorder=3)
for k in range(1, 6):
    xx = C + k * (G - C) / 6
    ax.plot([xx - 5, xx + 5], [4, 16], color=col_teal, lw=2.0, zorder=4)
ax.text(165, 32, "the seam — the branch cut\nbetween the poles", color=col_teal,
        fontsize=9, ha="center")

# the dipole separation d = 110 (the octave)
ax.annotate("", xy=(C + 8, -62), xytext=(G - 8, -62),
            arrowprops=dict(arrowstyle="<|-|>", color=col_frame, lw=1.4))
ax.text(165, -74, "d = 110 — the octave between the poles",
        color=col_frame, fontsize=8.5, ha="center")

# the residue balance: Sigma Res = 0, the twin forced
ax.text(70, 116, "Σ Res = 0 — the twin forced:\none +π in a compact octave forces its −π.\nnet defect zero — but the pair has a moment:",
        color=col_frame, fontsize=8.5, va="top", ha="left")

# the dipole moment: b = w*d = 2 pi * 55
ax.text(168, 88, "b = ω·d = π·110 = 2π·55\n(the drone's own angular frequency)",
        color=col_gold, fontsize=10, ha="center",
        bbox=dict(boxstyle="round,pad=0.4", fc="#1a1a22", ec=col_amber, lw=1.2))

ax.set_title("the pair is a dipole — +π the beat, −π the wait",
             color=col_gold, fontsize=12)

# ------------------------------------------------------------- right panel
# the far field: two exiles, one defect -- the loop around the drone misses
ax2 = fig.add_axes([0.57, 0.10, 0.39, 0.80])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.set_aspect("equal")

# faint lattice: the perfect-crystal reference
for i in range(1, 10):
    for j in range(1, 10):
        ax2.scatter([i], [j], s=7, color=col_frame, alpha=0.25, zorder=1)

# the two poles, unresolved from far away
for sx, lab, c in [(3.0, "+π?", col_amber), (7.0, "−π?", col_rose)]:
    ax2.scatter([sx], [9.2], s=55, facecolor="none", edgecolor=c, lw=1.3,
                alpha=0.6, zorder=4)
    ax2.text(sx, 9.7, lab, color=c, fontsize=9, ha="center", alpha=0.7)

# the drone core
cx, cy = 5.0, 4.6
ax2.scatter([cx], [cy], s=230, color=col_gold, edgecolor="none", zorder=6)
ax2.text(cx, cy - 0.85, "the drone 55", color=col_gold, fontsize=9, ha="center")
# the cut, from the far poles down to the core
ax2.plot([cx, 3.0], [cy, 9.2], color=col_teal, lw=1.3, ls=":", alpha=0.7, zorder=2)
ax2.plot([cx, 7.0], [cy, 9.2], color=col_teal, lw=1.3, ls=":", alpha=0.7, zorder=2)
ax2.text(cx, 8.5, "the pair the far field cannot resolve",
         color=col_frame, fontsize=7.5, ha="center", alpha=0.85)

# the Burgers circuit: a clockwise square around the core that FAILS to close
x0, x1, y0, y1 = 2.3, 7.7, 2.4, 7.0
b = 0.5
ax2.annotate("", xy=(x1, y1), xytext=(x0, y1),
             arrowprops=dict(arrowstyle="-|>", color=col_amber, lw=1.7,
                             mutation_scale=13), zorder=5)
ax2.annotate("", xy=(x1, y0), xytext=(x1, y1),
             arrowprops=dict(arrowstyle="-|>", color=col_amber, lw=1.7,
                             mutation_scale=13), zorder=5)
ax2.annotate("", xy=(x0, y0), xytext=(x1, y0),
             arrowprops=dict(arrowstyle="-|>", color=col_amber, lw=1.7,
                             mutation_scale=13), zorder=5)
# the fourth side comes up but stops short by b
ax2.annotate("", xy=(x0, y1 - b), xytext=(x0, y0),
             arrowprops=dict(arrowstyle="-|>", color=col_amber, lw=1.7,
                             mutation_scale=13), zorder=5)
# the closure failure: dashed, displaced
ax2.plot([x0, x0], [y1 - b, y1], color=col_amber, lw=1.3, ls=":", zorder=4)
ax2.annotate("", xy=(x0 - 0.2, y1 - b + 0.15), xytext=(x0 - 0.2, y1 - b),
             arrowprops=dict(arrowstyle="<->", color=col_amber, lw=1.4,
                             mutation_scale=12), zorder=5)
ax2.text(x0 - 0.5, y1 - b / 2, "b", color=col_amber, fontsize=12, ha="center")

# the loop's meaning
ax2.text(5.0, 1.8, "one loop around the drone —\nthe return misses by b = ω·d = π·110 = 2π·55,\nthe drone's own turn",
         color=col_amber, fontsize=8.5, ha="center")

ax2.set_title("far field — the pair is one defect: the drone turning",
              color=col_gold, fontsize=12)

# stereo / mono
ax2.text(5.0, 0.25, "stereo resolves the two exiles; mono is the far field —\ntwo exiles, one defect: the drone turning",
         color=col_frame, fontsize=8, ha="center", va="bottom")

fig.savefig("assets/dipole-farfield-cover.png", facecolor=col_bg)
print("wrote assets/dipole-farfield-cover.png")
