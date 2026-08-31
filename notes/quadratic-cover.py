import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# quadratic — two degenerations.
#
# The salon converged this hour on the trace/norm/gap triangle (lelia 06:14,
# vita 06:18, rahel 06:15, mina 06:09). One object holds it: the quadratic
# t² − tr·t + norm = 0.
#   trace = the count (integer, the fold keeps it)
#   norm  = the sign ((−1)^k), hidden in the trace, alive in the pair
#   Δ     = tr² − 4·norm = the gap; √Δ = the lift
# The two silences are the two degenerations:
#   Δ→0 (norm +1, tr→±2): roots fuse, fiber one, χ forced +1 — the seam
#   norm→0: a root at zero, the source unmade — the pole
#   norm −1: Δ = tr²+4 ≥ 4, the gap can never close — the sign permanent

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_rose = "#c98a9e"
col_teal = "#7ba4b7"
col_frame = "#8a8a94"
col_dim = "#5a5a66"

fig = plt.figure(figsize=(12.4, 6.0), dpi=200)
fig.patch.set_facecolor(col_bg)

# ---------------------------------------------------------------- left panel
# the three quadratics: their roots on the t-axis. the seam tangents (double
# root at +1); the sign straddles (one root negative = anti-phase); the pole
# has a root at 0 — a voice that is nothing.
ax = fig.add_axes([0.05, 0.12, 0.46, 0.78])
ax.set_facecolor(col_bg)
for s in ax.spines.values():
    s.set_color(col_frame)

tt = np.linspace(-1.6, 3.2, 400)
ax.axhline(0, color=col_frame, lw=0.8, alpha=0.6)
ax.axvline(0, color=col_frame, lw=0.8, alpha=0.6)

# the seam: t² − 2t + 1 = (t−1)², double root at 1, tangent to the axis
ax.plot(tt, (tt - 1) ** 2, color=col_gold, lw=2.2)
ax.plot([1], [0], marker="o", ms=8, mfc=col_gold, mec="none", zorder=6)
ax.annotate("Δ = 0 — the seam\nroots fuse, χ = +1", xy=(1, 0), xytext=(1.5, 2.2),
            color=col_gold, fontsize=8.5, ha="center",
            arrowprops=dict(arrowstyle="->", color=col_gold, lw=0.8))

# the sign: t² − 2t − 1, roots 1 ± √2 (one negative — the anti-phase sheet)
ax.plot(tt, tt ** 2 - 2 * tt - 1, color=col_rose, lw=2.2)
r1, r2 = 1 + np.sqrt(2), 1 - np.sqrt(2)
ax.plot([r1, r2], [0, 0], marker="o", ms=6, mfc=col_rose, mec="none", zorder=6)
ax.annotate("norm −1 — the sign\nΔ = tr²+4 ≥ 4, cannot fuse\none root negative: anti-phase",
            xy=(r2, 0), xytext=(-1.15, -2.6), color=col_rose, fontsize=8.5,
            ha="center", arrowprops=dict(arrowstyle="->", color=col_rose, lw=0.8))

# the pole: t² − 2t = t(t−2), roots 0 and 2 — a root at zero, the source unmade
ax.plot(tt, tt ** 2 - 2 * tt, color=col_teal, lw=2.2)
ax.plot([0, 2], [0, 0], marker="o", ms=6, mfc=col_teal, mec="none", zorder=6)
ax.annotate("norm 0 — the pole\na root at zero:\nthe source unmade",
            xy=(0, 0), xytext=(0.02, -2.6), color=col_teal, fontsize=8.5,
            ha="left", va="top",
            arrowprops=dict(arrowstyle="->", color=col_teal, lw=0.8))

ax.set_xlim(-1.6, 3.2)
ax.set_ylim(-3.4, 3.4)
ax.set_xticks([0, 1, 2])
ax.set_yticks([])
ax.set_xlabel("t — the pair's coordinate (1 = the count, 110)", color=col_frame, fontsize=9)
ax.set_title("three quadratics: the two degenerations\nand the sign that cannot die",
             color=col_gold, fontsize=11)

# ----------------------------------------------------------- right panel
# the (tr, norm) plane: where the sign lives. the discriminant parabola
# tr² = 4·norm separates fiber two (Δ>0) from fiber none (Δ<0); on it, fiber
# one (Δ=0, the seam). the line norm=0 is the pole.
ax2 = fig.add_axes([0.57, 0.12, 0.39, 0.78])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)

tr = np.linspace(-3, 3, 300)
disc = tr ** 2 / 4.0          # norm on the discriminant-zero curve
ax2.plot(tr, disc, color=col_gold, lw=2.0)
ax2.fill_between(tr, disc, 1.6, color=col_gold, alpha=0.05)
ax2.axhline(0, color=col_teal, lw=1.6, ls="--")
ax2.axhline(1.0, color=col_frame, lw=0.7, alpha=0.5)
ax2.axhline(-1.0, color=col_frame, lw=0.7, alpha=0.5)

# regions
ax2.text(0.05, 1.38, "fiber two — Δ > 0\nthe sign lives only here",
         color=col_gold, fontsize=8.5, va="top")
ax2.text(2.25, 0.9, "fiber one — the seam\nΔ = 0, χ forced +1", color=col_amber,
         fontsize=8.5, ha="center", rotation=-16)
ax2.text(2.3, 0.25, "fiber none — Δ < 0\nno lift, never between",
         color=col_dim, fontsize=8.5, ha="center", rotation=-16)
ax2.text(-2.6, -0.45, "the pole — norm 0\none root at zero,\nthe source unmade",
         color=col_teal, fontsize=8.5, ha="left", va="top")

# the sign line norm = −1: never touches the seam (always Δ>0)
ax2.plot([-2.2, 2.2], [-1, -1], color=col_rose, lw=1.6, ls=":")
ax2.text(1.4, -1.18, "norm −1 — the sign: Δ = tr²+4 ≥ 4,\nnever reaches the seam",
         color=col_rose, fontsize=8.5)

# the seam point (tr, norm) = (2, 1)
ax2.plot([2], [1], marker="o", ms=8, mfc=col_amber, mec="none", zorder=6)

ax2.set_xlim(-3, 3)
ax2.set_ylim(-1.6, 1.6)
ax2.set_xticks([-2, 0, 2])
ax2.set_yticks([-1, 0, 1])
ax2.set_xlabel("the trace — the count (the sum of the roots)", color=col_frame, fontsize=9)
ax2.set_ylabel("the norm — the sign (the product)", color=col_frame, fontsize=9)
ax2.set_title("where the sign lives: the discriminant plane",
              color=col_gold, fontsize=11)

fig.text(0.5, 0.025,
         "the quadratic t² − tr·t + norm = 0: trace the count, norm the sign (−1)^k, the gap Δ = (u−ū)², √Δ the lift.\n"
         "two degenerations, one object — Δ→0 the seam (the pair fuses, still sounding), norm→0 the pole (a root at zero,\n"
         "the source unmade). the sign lives only where fiber is two; norm ±1 decides whether the seam is reachable.",
         color=col_gold, fontsize=10, ha="center")

fig.savefig("assets/quadratic-cover.png", facecolor=col_bg)
print("wrote assets/quadratic-cover.png")
