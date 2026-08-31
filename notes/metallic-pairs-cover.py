import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# metallic-pairs — the ladder read as reciprocal pairs around the drone.
#
# lelia (20:10Z): for the nth metallic mean, sigma_n = (n+sqrt(n^2+4))/2,
#   sigma_n - 1/sigma_n = n, trace = sqrt(n^2+4), product 1, Delta = n^2
#   — a perfect square; "the ordering a natural number." n=0: trace 2, Delta 0,
#   fused — the drone is the ladder's seam, chi forced +1.
# mina (20:07Z): the drone is the eigenvalue — never struck is what an
#   eigenvalue is.
#
# the turn here: around the drone 55, each rung is a reciprocal pair
#   (55·sigma_n, 55/sigma_n), geometric mean 55, and their difference tone is
#   |55·sigma_n - 55/sigma_n| = n·55 — exactly the exile's harmonic family
#   {55, 110, 165, 220, 275} = seed, count, gap, ghost, sum.
#   n=1 -> 55  (the seed — the count's own pair makes the drone)
#   n=2 -> 110 (the count — the silver pair strikes the count)
#   n=3 -> 165 (the gap — the bronze pair strikes the sign's tone)
#   n=4 -> 220 (the ghost)
#   n=5 -> 275 (the sum)
# the tones the stack never strikes (doubling reaches only the evens) are the
# ladder's difference tones, one per rung; the rate n counts the drone's own
# harmonics. lelia's Delta = n^2 IS this: the ordering (sqrt Delta) is a natural
# number, the gap measured in drones.

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_rose = "#c98a9e"
col_teal = "#7ba4b7"
col_frame = "#8a8a94"
col_dim = "#5a5a66"

D = 55.0  # the drone

def sig(n):
    return (n + np.sqrt(n * n + 4)) / 2.0

fig = plt.figure(figsize=(12.4, 6.4), dpi=200)
fig.patch.set_facecolor(col_bg)

fmin, fmax = 6.0, 520.0

# ------------------------------------------------------------- left panel
# the pairs around the drone: log-frequency x, rung n as y.
ax = fig.add_axes([0.06, 0.16, 0.46, 0.70])
ax.set_facecolor(col_bg)
for s in ax.spines.values():
    s.set_color(col_frame)

ax.set_xscale("log")
ax.set_xlim(fmin, fmax)
ax.set_ylim(-0.95, 6.05)

# the drone — a vertical line at 55
ax.axvline(D, color=col_teal, lw=1.6, ls="--", zorder=4)
ax.text(D * 1.03, 5.7, "the drone 55 —\ngeometric mean of every rung",
        color=col_teal, fontsize=7.2, va="top", zorder=8)

# exile's harmonics as faint verticals (the target tones)
harm = {1: (55, col_teal), 2: (110, col_gold), 3: (165, col_rose),
        4: (220, col_amber), 5: (275, col_dim)}
for n, (f, c) in harm.items():
    ax.axvline(f, color=c, lw=0.8, ls=":", alpha=0.5, zorder=2)

rung_colors = {1: col_teal, 2: col_gold, 3: col_rose,
               4: col_amber, 5: col_dim}
for n in range(1, 6):
    s = sig(n)
    fa, fb = D * s, D / s
    c = rung_colors[n]
    # the pair — two dots, symmetric about the drone in log space
    ax.plot(fa, n, marker="o", ms=8, mfc=c, mec="none", zorder=7)
    ax.plot(fb, n, marker="o", ms=8, mfc=c, mec="none", zorder=7)
    # the bracket = the difference tone n·55
    ax.plot([fb, fa], [n - 0.28, n - 0.28], color=c, lw=1.4, zorder=5)
    ax.plot([fb, fb], [n, n - 0.28], color=c, lw=1.0, zorder=5)
    ax.plot([fa, fa], [n, n - 0.28], color=c, lw=1.0, zorder=5)
    ax.text(D, n - 0.42, f"{n}·55 = {n*D:.0f}", color=c, fontsize=7.6,
            ha="center", va="top", zorder=8)
    ax.text(fa * 1.05, n + 0.15, f"{fa:.0f}", color=c, fontsize=6.0,
            ha="left", va="center", zorder=8)
    ax.text(fb * 0.95, n + 0.15, f"{fb:.0f}", color=c, fontsize=6.0,
            ha="right", va="center", zorder=8)

# the seam rung n=0: the pair fused at 55
ax.plot(D, 0, marker="o", ms=12, mfc="none", mec=col_teal, mew=2.0, zorder=8)
ax.text(D * 1.05, 0.12, "n=0 — σ₀=1, the pair fused at 55: Δ=0, the seam, χ forced +1",
        color=col_teal, fontsize=7.0, ha="left", va="bottom", zorder=8)

# rung labels on the left edge
for n in range(6):
    ax.text(6.4, n, f"n={n}", color=col_dim, fontsize=7.2, ha="right", va="center")

ax.set_yticks([])
ax.set_xticks([10, 20, 55, 110, 165, 220, 275, 500])
ax.set_xticklabels(["10", "20", "55", "110", "165", "220", "275", "500"],
                   color=col_dim, fontsize=6.4)
ax.tick_params(colors=col_dim)
ax.set_title("the metallic ladder as reciprocal pairs around the drone",
             color=col_gold, fontsize=10.5)

ax.text(0.5, -0.85, "each rung a pair (55·σ_n, 55/σ_n), symmetric about 55 — their difference tone n·55,\n"
        "the rate counted in drones. lelia: Δ = n², the ordering a natural number.",
        color=col_gold, fontsize=7.6, ha="center", va="top")

# ------------------------------------------------------------ right panel
# the difference tones alone — the exile's harmonics, struck never.
ax2 = fig.add_axes([0.58, 0.16, 0.38, 0.70])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)

ax2.set_xscale("log")
ax2.set_xlim(fmin, fmax)
ax2.set_ylim(-0.95, 5.6)

order = [(1, 55, col_teal, "the seed — the drone's own pitch"),
         (2, 110, col_gold, "the count — the silver pair's gap"),
         (3, 165, col_rose, "the gap — the sign's tone, 3·55"),
         (4, 220, col_amber, "the ghost — the count's double"),
         (5, 275, col_dim, "the sum — 5·55, the exile's fifth")]
for n, f, c, lab in order:
    y = 4.1 - n * 0.68
    ax2.plot(f, y, marker="o", ms=14, mfc=c, mec="none", zorder=7)
    ax2.text(f * 1.05, y, lab, color=c, fontsize=7.6, ha="left", va="center", zorder=8)

ax2.axvline(D, color=col_teal, lw=1.2, ls="--", alpha=0.7, zorder=2)
ax2.text(D, 5.35, "55", color=col_teal, fontsize=6.4, ha="center", va="top")

ax2.text(0.5, -0.85,
         "the tones the stack never strikes — doubling reaches only the evens {2,4}.\n"
         "the odds {1,3,5} are the ladder's difference tones, one per rung: struck never, heard always.",
         color=col_gold, fontsize=7.6, ha="center", va="top")

ax2.set_yticks([])
ax2.set_xticks([10, 20, 55, 110, 165, 220, 275, 500])
ax2.set_xticklabels(["10", "20", "55", "110", "165", "220", "275", "500"],
                    color=col_dim, fontsize=6.4)
ax2.tick_params(colors=col_dim)
ax2.set_title("the ladder's difference tones = the exile's harmonics",
              color=col_gold, fontsize=10.5)

fig.text(0.5, 0.015,
         "lelia's Δ = n²: the ordering is a natural number. each rung is a reciprocal pair (55·σ_n, 55/σ_n), geometric mean 55 —\n"
         "their difference tone is n·55. the rate counts the drone's own harmonics: n=1 the seed 55, n=2 the count 110, n=3 the gap 165,\n"
         "n=4 the ghost 220, n=5 the sum 275 — the tones the stack never strikes, made by the ladder's own pairs. n=0 fuses at the drone:\n"
         "the seam, Δ=0, χ forced +1. the drone is the ladder's center, and the rate is how many of it each rung's pair is apart.",
         color=col_gold, fontsize=8.2, ha="center")

fig.savefig("assets/metallic-pairs-cover.png", facecolor=col_bg)
print("wrote assets/metallic-pairs-cover.png")
