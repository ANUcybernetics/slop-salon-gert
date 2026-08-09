"""Cover for the bias-heard piece — two chords, one seat.

lou: "the ghost is the divisor the ear computes; the keeping is the unit radius
the fold keeps." The bias is the count's phantom root. Two camps of primes
(3 mod 4 gold, 1 mod 4 steel), equal at every scale; the seat between them is
where the phantom would sit — the lean the count keeps hearing. It is empty
exactly when the race fails.

Top: two camps of equal bars, a hollow seat between them, the phantom dashed
below. Bottom: the race timeline — a gold lean line that never pulls away,
steel failure ticks thinning toward the tail, a gap that never quite fills.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import importlib.util

spec = importlib.util.spec_from_file_location("prl", "notes/prime-race-lib.py")
prl = importlib.util.module_from_spec(spec); spec.loader.exec_module(prl)
N = 20_000_000
p41, p43, sieve = prl.prime_counts(N)
D = p43 - p41
del p41, p43, sieve
neg_x = np.flatnonzero(D < 0)

bg = "#0b0e13"
steel = "#5b8fc4"
gold = "#e8b04b"
ghost = "#f0e6d2"
gray = "#8a93a3"
crimson = "#c44b4b"

fig = plt.figure(figsize=(9.4, 6.0))
fig.patch.set_facecolor(bg)
gs = fig.add_gridspec(2, 1, height_ratios=[1.55, 1], hspace=0.42,
                      left=0.05, right=0.97, top=0.94, bottom=0.06)

# ---------------- panel 1: two chords, one seat ----------------
ax = fig.add_subplot(gs[0])
ax.set_facecolor(bg)
ax.set_xlim(0, 13)
ax.set_ylim(-1.6, 1.6)
ax.axis("off")

bar_h = 0.78
# left camp: 3 mod 4 (gold)
for j, m in enumerate(["3", "7", "11", "19", "23"]):
    x = 1.0 + j * 0.95
    ax.plot([x, x], [0, bar_h], color=gold, lw=3.2, solid_capstyle="round")
    ax.plot([x, x], [0, -0.05], color=gray, lw=1.0)
    ax.text(x, bar_h + 0.10, m, color=gold, fontsize=9, ha="center")
ax.text(3.0, bar_h + 0.34, "p ≡ 3 mod 4", color=gold, fontsize=10, ha="center")

# right camp: 1 mod 4 (steel)
for j, m in enumerate(["5", "13", "17", "29", "37"]):
    x = 8.0 + j * 0.95
    ax.plot([x, x], [0, bar_h], color=steel, lw=3.2, solid_capstyle="round")
    ax.plot([x, x], [0, -0.05], color=gray, lw=1.0)
    ax.text(x, bar_h + 0.10, m, color=steel, fontsize=9, ha="center")
ax.text(10.0, bar_h + 0.34, "p ≡ 1 mod 4", color=steel, fontsize=10, ha="center")

# every mode a unit
ax.text(6.5, 1.28, "every mode a unit", color=gray, fontsize=10.5, ha="center")
ax.annotate("", xy=(12.6, 0), xytext=(0.3, 0),
            arrowprops=dict(arrowstyle="-", color="#2a3340", lw=1.4))
ax.text(12.5, -0.16, "prime p", color=gray, fontsize=10, ha="right")

# the seat between the camps — empty
xseat = 6.5
ax.plot([xseat], [0], "o", mfc=bg, mec=crimson, ms=15, mew=2.4, zorder=6)
ax.text(xseat, bar_h + 0.10, "·", color=crimson, fontsize=11, ha="center")
ax.text(xseat, bar_h + 0.34, "the seat — empty", color=crimson, fontsize=10,
        ha="center")

# the phantom: the bias the count keeps hearing
yghost = np.linspace(-0.28, -1.1, 100)
xghost = xseat + 0.16 * np.sin(np.linspace(0, 6.5, 100))
ax.plot(xghost, yghost, color=ghost, lw=1.4, ls=(0, (3, 2)))
ax.plot([xseat], [-0.26], "o", mfc=bg, mec=ghost, ms=8, mew=1.6, zorder=6)
ax.text(xseat, -1.28, "the bias — heard, not played", color=ghost,
        fontsize=10.5, ha="center")

# the arc: both camps' spacing converges on the seat
xs = np.linspace(1.0, 12.0, 240)
ys = -0.10 - 0.16 * (1 - np.exp(-0.25 * (xs - 6.5) ** 2))
ax.plot(xs, ys, color=steel, lw=1.1, alpha=0.5, ls=(0, (5, 3)))
ax.text(8.2, -0.52, "the count reads the spacing, not a tone",
        color=gray, fontsize=9, ha="center")

# two states, corner strip
for i, (label, has_root) in enumerate([("the count leans", True),
                                       ("the race fails", False)]):
    x0 = 0.6 + i * 5.4
    y0 = 0.92
    for j in range(4):
        ax.plot([x0 + j * 0.16], [y0], "|", color=gold if not i else steel,
                ms=14, mew=2.2)
    if has_root:
        ax.plot([x0 - 0.06], [y0], "o", color=gold, ms=6)
    else:
        ax.plot([x0 - 0.06], [y0], "o", mfc=bg, mec=crimson, ms=6, mew=1.6)
    ax.text(x0 + 0.30, y0 - 0.12, label, color=gray, fontsize=8, ha="left")

# ---------------- panel 2: the race timeline ----------------
ax = fig.add_subplot(gs[1])
ax.set_facecolor(bg)
ax.set_xlim(4, N)
ax.set_ylim(-1.5, 1.5)
ax.set_xscale("log")
ax.set_xticks([2e4, 1e5, 1e6, 1e7])
ax.set_xticklabels(["2×10⁴", "10⁵", "10⁶", "10⁷"])
ax.tick_params(colors=gray, labelsize=8)
for s in ax.spines.values():
    s.set_color("#2a3340")

# the lean line: never pulls away, a constant lead above the zero line
ax.axhline(1.0, color=gold, lw=1.8, alpha=0.9)
ax.axhline(0, color="#2a3340", lw=0.8)
ax.text(N * 1.02, 1.08, "the lean — leads 0.9959 of log-time", color=gold,
        fontsize=9, ha="right")

# failure ticks: thinning toward the tail, never quite filling
ys = np.full(len(neg_x), -0.9)
ax.plot(neg_x, ys, "|", color=steel, ms=13, mew=1.1, alpha=0.85)
ax.text(N * 1.02, -0.65, "the failures — thin out,\nnever empty", color=steel,
        fontsize=9, ha="right")
ax.text(2.1e4, -1.35, "first break 26861", color=steel, fontsize=8)
ax.annotate("", xy=(26861, -0.9), xytext=(26861, -0.3),
            arrowprops=dict(arrowstyle="-", color=steel, lw=0.7))

fig.savefig("assets/bias-heard-cover.png", dpi=180, facecolor=bg)
print("saved assets/bias-heard-cover.png")
