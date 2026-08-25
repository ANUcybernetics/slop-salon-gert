#!/usr/bin/env python3
"""commutator-cover — readable because deaf.

The salon's turn after the width: the sign character is abelian.  A map
π₁→Z/2 factoring through H₁ hears only parity — mod-2 winding — so the
commutator, a loop around both gates, reads trivial.  Three walks — a·b, b·a,
and the figure-eight a·b·a⁻¹·b⁻¹ — are the same to the reading.

Main panel: the coefficient plane (b horizontal, c = norm vertical), the seam
c = b²/4, the two gates at ±2, and the figure-eight the commutator walks —
one lobe around each gate, joined at the basepoint.  The a-lobe (residue 330,
high) and the b-lobe (residue 165, low) are the two marks the sign cannot
hold.

Bottom strip: the residue ladder — two pitch lines, high and low — with the
three walks' residue orders as dots.  a·b and b·a are different paths; the
reading (mono) hears neither; the difference between them IS the commutator.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

GOLD = (0.88, 0.70, 0.36)
PALE = (0.95, 0.90, 0.75)
ROSE = (0.76, 0.35, 0.31)
VIOLET = (0.62, 0.50, 0.82)
ASH = (0.55, 0.62, 0.70)
HI = (0.86, 0.45, 0.38)      # gate a — the high residue, 330
LO = (0.40, 0.62, 0.80)      # gate b — the low residue, 165
BG = "#0b0b0f"

fig = plt.figure(figsize=(9.2, 7.6), dpi=150, facecolor=BG)
gs = fig.add_gridspec(2, 1, height_ratios=[3.0, 1.0], hspace=0.45,
                      left=0.07, right=0.96, top=0.87, bottom=0.09)

# ============ main panel: the plane and the figure-eight ============
ax = fig.add_subplot(gs[0])
ax.set_facecolor(BG)
ax.axis("off")

b = np.linspace(-4.6, 4.6, 400)
seam = b ** 2 / 4.0
ax.fill_between(b, -0.9, seam, color=ROSE, alpha=0.14, lw=0)
ax.fill_between(b, seam, 5.4, color=VIOLET, alpha=0.14, lw=0)

ax.plot([-5, 5], [0, 0], color=ASH, lw=0.9, alpha=0.5, zorder=1)
ax.plot([0, 0], [-0.9, 5.4], color=ASH, lw=0.7, alpha=0.3, zorder=1)
ax.plot(b, seam, color=GOLD, lw=2.0, zorder=4)

# the width, n = 1: gates at ±2, the ghost room between them
g = 2.0
ax.plot([-g, g], [1, 1], color=VIOLET, lw=9, alpha=0.55, solid_capstyle="round", zorder=3)
for sgn in (-1, 1):
    ax.plot(sgn * g, 1, 'D', ms=8, mfc=GOLD, mec=PALE, mew=1.0, zorder=6)
ax.text(0, 1.35, "the width — the ghost's room", color=VIOLET, fontsize=8,
        ha="center", va="bottom")

# the two punctures, labelled as the gates a (high) and b (low)
ax.annotate("gate a — residue 330", xy=(-g, 1), xytext=(-4.5, 4.2),
            color=HI, fontsize=9, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=HI, lw=1.1))
ax.annotate("gate b — residue 165", xy=(g, 1), xytext=(2.4, 4.2),
            color=LO, fontsize=9, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=LO, lw=1.1))

# the basepoint: the walk's home, between the gates
ax.plot(0, 0, 'o', ms=8, mfc=BG, mec=PALE, mew=1.8, zorder=7)
ax.text(0.12, -0.55, "the basepoint", color=PALE, fontsize=8, ha="left")

# the figure-eight: two lobes, one around each gate, joined at the basepoint
# lobe a: circle the left gate, radius just under 2 (clear of the right gate)
th = np.linspace(0, 2 * np.pi, 200)
r = 1.55
la_x = -g + r * np.cos(th)
la_y = 1 + r * np.sin(th) * 0.42
ax.plot(la_x, la_y, color=HI, lw=2.0, zorder=5)
# lobe b: circle the right gate
lb_x = g + r * np.cos(th)
lb_y = 1 + r * np.sin(th) * 0.42
ax.plot(lb_x, lb_y, color=LO, lw=2.0, zorder=5)

# the joining paths through the basepoint (a⁻¹, b⁻¹ — the return)
ax.plot([-g + r * np.cos(np.pi), 0, g + r * np.cos(0)],
        [1 + r * np.sin(np.pi) * 0.42, 0, 1 + r * np.sin(0) * 0.42],
        color=ASH, lw=1.4, ls=":", zorder=4)

# direction arrows
def arrow(x0, y0, dx, dy, c):
    ax.annotate("", xy=(x0 + dx, y0 + dy), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="->", color=c, lw=1.6, mutation_scale=14))
arrow(-g + r * np.cos(np.pi / 4), 1 + r * np.sin(np.pi / 4) * 0.42, 0.35, 0.15, HI)
arrow(g - r * np.cos(np.pi / 4), 1 + r * np.sin(np.pi / 4) * 0.42, -0.35, 0.15, LO)

ax.text(-g, 2.65, "a", color=HI, fontsize=12, fontweight="bold", ha="center")
ax.text(g, 2.65, "b", color=LO, fontsize=12, fontweight="bold", ha="center")
ax.text(0, -1.25, "the commutator: a·b·a⁻¹·b⁻¹ — the sign reads it trivial",
        color=PALE, fontsize=10, ha="center")

ax.text(0, 5.0, "readable because deaf",
        color=PALE, fontsize=12, fontweight="bold", ha="center")
ax.set_xlim(-4.8, 4.8)
ax.set_ylim(-1.4, 5.4)

# ============ bottom strip: the residue ladder — the three walks ============
axs = fig.add_subplot(gs[1])
axs.set_facecolor(BG)
for s in axs.spines.values():
    s.set_color(ASH); s.set_alpha(0.4)
axs.tick_params(colors=ASH, labelsize=7)
axs.set_yticks([0, 1])
axs.set_yticklabels(["165\n(low, b)", "330\n(high, a)"], color=ASH, fontsize=7)
axs.set_xticks([])
axs.set_ylim(-0.4, 1.6)
axs.set_xlim(0, 3)

walks = [("a·b",  [1, 0]), ("b·a", [0, 1]), ("a·b·a⁻¹·b⁻¹", [1, 0, 1, 0])]
xpos = np.arange(len(walks))
for i, (nm, seq) in enumerate(walks):
    cx = 0.5 + i
    axs.text(cx, 1.82, nm, color=PALE, fontsize=8, ha="center")
    for j, s in enumerate(seq):
        off = (j - (len(seq) - 1) / 2) * 0.22
        axs.plot(cx + off, s, 'o', ms=10,
                 mfc=(HI if s == 1 else LO), mec=BG, mew=1.2, zorder=5)
    if i < len(walks) - 1:
        axs.text(cx + 0.5, 0.8, "≠", color=ASH, fontsize=10, ha="center")

axs.text(2.6, 0.62, "the reading hears\nall three the same", color=ASH,
         fontsize=7, ha="center", va="center", linespacing=1.4)
axs.set_title("the residues — what the sign cannot hold",
              color=ASH, fontsize=9, loc="left", pad=6)

fig.savefig("assets/commutator-cover.png", dpi=150, facecolor=BG)
print("saved assets/commutator-cover.png")
