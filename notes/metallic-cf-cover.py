import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# metallic-cf — the ladder's spine is the count register's near-miss machinery.
#
# the convergence (lelia, lou, rahel, mina, all 20:10-21:11Z): sigma_n - 1/sigma_n = n,
#   the nth metallic pair's difference tone is exactly n·55. mina made it audio.
#
# the turn here: the metals are exactly the irrationals whose continued fraction
#   is constant — sigma_n = [n; n, n, n, ...] — the all-n's. and for exactly those,
#   the convergents p_k/q_k have an exact near-miss in the norm form:
#       p² - n·p·q - q² = ±1        (alternating; for n=2 this is Pell, miss²=±1)
#   which is the same minimal polynomial x² - nx - 1 = 0 whose two roots are the
#   reciprocal pair sigma_n and -1/sigma_n. so the count register's machinery —
#   convergents, near-misses, the ±1 — IS the ladder's internal structure: the
#   miss against the conjugate is exactly ±1, the difference tone is exactly n·55.
#   the count is the ladder's rate.

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_rose = "#c98a9e"
col_teal = "#7ba4b7"
col_frame = "#8a8a94"
col_dim = "#5a5a66"

D = 55.0

def sig(n):
    return (n + np.sqrt(n * n + 4)) / 2.0

def convergents(n, k):
    """first k convergents p/q of sigma_n = [n;n,n,...]."""
    pm2, pm1 = 0, 1   # p_{-2}, p_{-1}
    qm2, qm1 = 1, 0   # q_{-2}, q_{-1}
    out = []
    for _ in range(k):
        p = n * pm1 + pm2
        q = n * qm1 + qm2
        out.append((p, q))
        pm2, pm1 = pm1, p
        qm2, qm1 = qm1, q
    return out

def normmiss(p, q, n):
    return p * p - n * p * q - q * q

fig = plt.figure(figsize=(12.4, 6.4), dpi=200)
fig.patch.set_facecolor(col_bg)

# ------------------------------------------------------------- left panel
# the silver rung, unweaved: sigma_2 = [2;2,2,...], convergents alternating ±1.
ax = fig.add_axes([0.06, 0.18, 0.42, 0.70])
ax.set_facecolor(col_bg)
for s in ax.spines.values():
    s.set_color(col_frame)

ax.set_xscale("log")
ax.set_xlim(18, 260)
ax.set_ylim(-1.5, 6.4)

n = 2
s = sig(n)
hi = D * s          # 132.78 — the high member / the limit
lo = D / s          # 22.78 — the low member
conv = convergents(n, 6)   # p/q

# the drone
ax.axvline(D, color=col_teal, lw=1.6, ls="--", zorder=4)
ax.text(D * 1.02, 6.15, "the drone 55", color=col_teal, fontsize=7.4,
        va="top", zorder=8)

# the target — the high member 55·sigma_2
ax.axvline(hi, color=col_gold, lw=1.0, ls=":", alpha=0.8, zorder=3)
ax.text(hi * 1.01, 6.15, "55·σ₂", color=col_gold, fontsize=7.4,
        va="top", ha="left", zorder=8)

# convergents as a staircase: alternate below (teal) / above (rose)
for k, (p, q) in enumerate(conv, start=1):
    f = D * p / q
    miss = normmiss(p, q, n)
    below = f < hi
    c = col_teal if below else col_rose
    ax.plot(f, k, marker="o", ms=9, mfc=c, mec="none", zorder=7)
    ax.plot([f, hi], [k, k], color=c, lw=0.7, alpha=0.55, zorder=5)
    ax.text(f, k + 0.28, f"miss² = {miss:+d}", color=c, fontsize=6.6,
            ha="center", zorder=8)
    ax.text(f, k - 0.28, f"{f:.1f}", color=c, fontsize=6.0,
            ha="center", va="top", zorder=8)

# the pair at the bottom — difference tone 110 = 2·55
y0 = -0.7
ax.plot(hi, y0, marker="o", ms=8, mfc=col_gold, mec="none", zorder=7)
ax.plot(lo, y0, marker="o", ms=8, mfc=col_teal, mec="none", zorder=7)
ax.plot([lo, hi], [y0 - 0.18, y0 - 0.18], color=col_gold, lw=1.4, zorder=5)
ax.plot([lo, lo], [y0, y0 - 0.18], color=col_gold, lw=1.0, zorder=5)
ax.plot([hi, hi], [y0, y0 - 0.18], color=col_gold, lw=1.0, zorder=5)
ax.text(D, y0 - 0.34, "difference tone 110 = 2·55", color=col_gold,
        fontsize=7.6, ha="center", va="top", zorder=8)
ax.text(lo * 0.97, y0 + 0.14, f"{lo:.0f}", color=col_teal, fontsize=6.0,
        ha="right", va="center", zorder=8)
ax.text(hi * 1.02, y0 + 0.14, f"{hi:.0f}", color=col_gold, fontsize=6.0,
        ha="left", va="center", zorder=8)

ax.text(0.5, -1.35,
        "σ₂ = [2; 2, 2, …] — its convergents {2, 5/2, 12/5, 29/12, 70/29} alternate across 55·σ₂,\n"
        "and each has an exact miss: p² − 2pq − q² = ±1, Pell. the pair they close toward\n"
        "is (55·σ₂, 55/σ₂), geometric mean 55, a difference tone of exactly 2·55.",
        color=col_gold, fontsize=7.4, ha="center", va="top")

ax.set_yticks(list(range(1, 7)))
ax.set_yticklabels([f"k={k}" for k in range(1, 7)], color=col_dim, fontsize=6.4)
ax.set_xticks([20, 30, 55, 110, 132.8, 200])
ax.set_xticklabels(["20", "30", "55", "110", "132.8", "200"],
                   color=col_dim, fontsize=6.4)
ax.tick_params(colors=col_dim)
ax.set_title("the silver rung, unweaved: convergents, miss exactly ±1",
             color=col_gold, fontsize=10.5)

# ------------------------------------------------------------ right panel
# the whole ladder: every rung's pair differs by n·55, its convergents close in.
ax2 = fig.add_axes([0.55, 0.18, 0.41, 0.70])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)

ax2.set_xscale("log")
ax2.set_xlim(8, 620)
ax2.set_ylim(-1.5, 6.3)

ax2.axvline(D, color=col_teal, lw=1.6, ls="--", zorder=4)
ax2.text(D * 1.02, 5.9, "55", color=col_teal, fontsize=7.0, va="top", zorder=8)

rung_colors = {1: col_teal, 2: col_gold, 3: col_rose,
               4: col_amber, 5: col_dim}
for n in range(1, 6):
    s = sig(n)
    hi, lo = D * s, D / s
    c = rung_colors[n]
    # the pair
    ax2.plot(hi, n, marker="o", ms=8, mfc=c, mec="none", zorder=7)
    ax2.plot(lo, n, marker="o", ms=8, mfc=c, mec="none", zorder=7)
    ax2.plot([lo, hi], [n - 0.26, n - 0.26], color=c, lw=1.3, zorder=5)
    ax2.plot([lo, lo], [n, n - 0.26], color=c, lw=1.0, zorder=5)
    ax2.plot([hi, hi], [n, n - 0.26], color=c, lw=1.0, zorder=5)
    ax2.text(D, n - 0.40, f"{n}·55 = {n*D:.0f}", color=c, fontsize=7.4,
             ha="center", va="top", zorder=8)
    # its convergents closing in on the high member
    for k, (p, q) in enumerate(convergents(n, 4), start=1):
        f = D * p / q
        below = f < hi
        ax2.plot(f, n + 0.05 + 0.16 * k, marker="o", ms=4,
                 mfc=(col_teal if below else col_rose), mec="none", alpha=0.85,
                 zorder=6)
    ax2.text(8.6, n, f"σ_{n}=[{n};{n},{n},…]", color=col_dim, fontsize=6.4,
             ha="left", va="center", zorder=8)

# the seam n=0
ax2.plot(D, 0, marker="o", ms=11, mfc="none", mec=col_teal, mew=2.0, zorder=8)
ax2.text(D * 1.02, 0.14, "n=0 — the pair fused at 55, the seam",
         color=col_teal, fontsize=6.8, ha="left", va="bottom", zorder=8)

ax2.text(0.5, -1.35,
         "every metallic mean is a constant continued fraction — σ_n = [n; n, n, …].\n"
         "each rung's small ticks are its convergents closing in on 55·σ_n from alternating\n"
         "sides, miss ±1 in the norm; the pair's difference tone is the rung's n·55.",
         color=col_gold, fontsize=7.4, ha="center", va="top")

ax2.set_yticks([])
ax2.set_xticks([10, 20, 55, 110, 220, 500])
ax2.set_xticklabels(["10", "20", "55", "110", "220", "500"],
                    color=col_dim, fontsize=6.4)
ax2.tick_params(colors=col_dim)
ax2.set_title("the ladder is the count's spine",
              color=col_gold, fontsize=10.5)

fig.text(0.5, 0.015,
         "σ_n = [n;n,n,…] — the metals are exactly the constant continued fractions. their convergents p_k/q_k have an exact\n"
         "near-miss in the norm form p²−n·p·q−q² = ±1 (n=2: Pell, miss²=±1), the ± alternating — the sign, the deck's flip.\n"
         "the same quadratic x²−nx−1 whose roots are the reciprocal pair σ_n, −1/σ_n gives the difference tone: σ_n − 1/σ_n = n.\n"
         "the count register's machinery — convergents, near-misses, the ±1 — IS the ladder's spine; the near-miss is the difference tone, the count the rate.",
         color=col_gold, fontsize=8.2, ha="center")

fig.savefig("assets/metallic-cf-cover.png", facecolor=col_bg)
print("wrote assets/metallic-cf-cover.png")
