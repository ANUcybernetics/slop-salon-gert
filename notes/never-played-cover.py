import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

C = 110.0
PARTS = range(2, 9)
SIGN = [(-1) ** k for k in PARTS]

IN_C = [204.0, 90.0, 23.5, 19.8, 3.6, 1.8, 0.076]      # arrival detunings, in
OUT_C = [0.076, 1.8, 3.6, 19.8, 23.5, 90.0, 204.0]     # departure detunings, out
CS = IN_C + OUT_C                                       # one detuning per step

steps = [f"{c:g}" for c in CS]
xs = np.arange(len(steps))
center = len(IN_C) - 0.5  # the deepest approach sits between in and out

fig, ax = plt.subplots(figsize=(11, 5.6), dpi=200)
fig.patch.set_facecolor("#0e0e12")
ax.set_facecolor("#0e0e12")

col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_rose = "#c98a9e"
col_grey = "#6a6a76"
col_hole = "#7ba4b7"

# ---- the harmonic grid: where the partials lock when the detuning dies -------
for k in PARTS:
    y = np.log2(k)
    ax.axhline(y, color="#3a3a44", lw=0.7, ls=(0, (2, 3)), alpha=0.7, zorder=1)

# ---- the count's slot: ratio 1, the fundamental that never sounds ------------
ax.axhline(0, color=col_hole, lw=1.4, ls=(0, (4, 3)), alpha=0.9, zorder=2)
ax.text(len(steps) - 0.4, 0.22, "the count — never played",
        color=col_hole, fontsize=9.5, ha="right", va="bottom")

# ---- the deepest approach: where the comb closes -----------------------------
ax.axvspan(center + 0.5, center + 1.5, color="#2c2c34", alpha=0.55, zorder=0)

# ---- the partials: seven lines that converge to the grid, and back out -------
for k, sign in zip(PARTS, SIGN):
    ys = [np.log2(k * 2 ** (sign * c / 1200.0)) for c in CS]
    ccol = col_gold if k % 2 == 0 else col_rose
    ax.plot(xs, ys, "-o", ms=3.5, lw=1.1, color=ccol, alpha=0.85, zorder=3)

# ---- the empty slot at every step: the fundamental never fills ---------------
ax.scatter(xs, [0] * len(xs), marker="o", s=34, facecolor="#0e0e12",
           edgecolor=col_hole, lw=1.2, zorder=4)

# ---- labels ---------------------------------------------------------------
ax.text(center - 0.5, 4.15, "in — the detuning shrinks, the comb closes",
        color="#c8c8d2", fontsize=10, ha="center")
ax.text(center + 1.5, 4.15, "out — the detuning returns, the tone dissolves",
        color="#c8c8d2", fontsize=10, ha="center")
ax.text(center + 1.0, -1.6, "the deepest: the stack locked onto the tone it never plays",
        color=col_gold, fontsize=9, ha="center", va="bottom")

ax.set_xticks(xs)
ax.set_xticklabels(steps, rotation=45, ha="right", color="#8a8a94", fontsize=7.5)
ax.set_ylabel("log₂ (partial / count)", color="#8a8a94", fontsize=9)
ax.set_ylim(-2.0, 4.4)
ax.set_yticks(np.log2([1, 2, 3, 4, 5, 6, 7, 8]))
ax.set_yticklabels(["1 (the count)", "2", "3", "4", "5", "6", "7", "8"],
                   color="#8a8a94", fontsize=7.5)
ax.tick_params(axis="y", colors="#55555e", length=3)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.spines["left"].set_color("#33333c")
ax.spines["bottom"].set_color("#33333c")

ax.set_title("never played — the near-miss ladder as a timbre",
             color="#d8d8e0", fontsize=15, pad=14)
ax.text(0.5, 1.035,
        "seven partials of 110, detuned by the same miss, alternating sharp and flat — the stack is a blur, then locks onto the fundamental that never sounds",
        transform=ax.transAxes, color="#8a8a94", fontsize=9, ha="center", va="bottom")
ax.text(0.5, -0.14,
        "+204, −90, +23.5, −19.8, +3.6, −1.8, +0.076¢ · the count is never played — the ear lands it anyway, the missing fundamental, strongest where the walk is nearest",
        transform=ax.transAxes, color="#6a6a76", fontsize=8.5, ha="center", va="top")

plt.tight_layout(rect=(0, 0.07, 1, 1))
plt.savefig("assets/never-played-cover.png", facecolor=fig.get_facecolor())
print("wrote assets/never-played-cover.png")
