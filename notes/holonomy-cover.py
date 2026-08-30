import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# The walk in: (cents, hold seconds) — patience grows as the miss nears the count.
IN = [
    (+204.0, 0.5), (-90.0, 0.8), (+23.5, 1.2), (-19.8, 1.6),
    (+3.6, 4.4),   (-1.8, 9.0),  (+0.076, 20.0),
]
# The walk out: the same distances reversed, each repaid its full beat — the
# deepest (the residue) cut at 6 s, its full wait 208 s.
OUT = [
    (+0.076, 6.0), (-1.8, 9.0), (+3.6, 4.4), (-19.8, 1.6),
    (+23.5, 1.2),  (-90.0, 0.8), (+204.0, 0.5),
]
CAP = 180.0          # the posting cap
DEEP_WAIT = 207.1    # one full beat of the deepest miss (0.076¢ @ 110 Hz)
FLOOR = 0.4          # log-axis bar floor

steps = [f"{c:+g}" for c, _ in IN] + [f"{c:+g}" for c, _ in OUT]
holds = [h for _, h in IN] + [h for _, h in OUT]
xs = np.arange(len(steps))
center = len(IN) - 0.5  # the count sits between the deepest in and deepest out

fig, ax = plt.subplots(figsize=(11, 5.2), dpi=200)
fig.patch.set_facecolor("#0e0e12")
ax.set_facecolor("#0e0e12")

col_amber = "#e0a26a"
col_rose = "#c98a9e"
col_gold = "#f2e8c9"
col_cap = "#7ba4b7"
col_grey = "#6a6a76"

# ---- the count: the puncture the loop goes around ----------------------------
ax.plot([center, center], [FLOOR * 0.3, DEEP_WAIT * 1.02],
        color=col_gold, lw=1.2, ls=(0, (2, 2)), alpha=0.8, zorder=2)
ax.text(center - 0.05, DEEP_WAIT * 1.04, "the count — the puncture",
        color=col_gold, fontsize=9, ha="right", va="bottom")

# ---- the walk in: patience grows with the wait -------------------------------
for (cents, h), x in zip(IN, xs[:len(IN)]):
    c = col_gold if abs(cents) < 1 else (col_amber if cents > 0 else col_rose)
    ax.bar(x, h, bottom=FLOOR, width=0.78, color=c, alpha=0.92, zorder=3)
    ax.text(x, h * 1.10, f"{h:g}s", color=c, fontsize=8, ha="center", va="bottom")

# ---- the walk out: the debts repaid in full — save the residue ---------------
for (cents, h), x in zip(OUT, xs[len(IN):]):
    if abs(cents) < 1:
        # the residue: owed, opened, cut — drawn as an open dashed bar whose
        # full height (208 s) exceeds even the frame
        ax.bar(x, h, bottom=FLOOR, width=0.78, facecolor="none",
               edgecolor=col_gold, lw=1.6, ls=(0, (3, 2)), alpha=0.95, zorder=3)
        ax.text(x, h * 1.10, f"{h:g}s", color=col_gold, fontsize=8,
                ha="center", va="bottom")
        ax.plot([x, x], [h, DEEP_WAIT], color=col_gold, lw=1.0,
                ls=(0, (2, 3)), alpha=0.45, zorder=2)
        ax.text(x, DEEP_WAIT * 1.04, "the residue — 208 s, unpayable",
                color=col_gold, fontsize=9, ha="center", va="bottom")
    else:
        # repaid: same sign color, hatched — the wait paid back to completion
        c = col_amber if cents > 0 else col_rose
        ax.bar(x, h, bottom=FLOOR, width=0.78, color=c, alpha=0.55,
               hatch="//", edgecolor=c, lw=0.6, zorder=3)
        ax.text(x, h * 1.10, f"{h:g}s", color=c, fontsize=8, ha="center", va="bottom")

# ---- the 180 s frame ----------------------------------------------------------
ax.plot([-0.6, len(xs) - 0.4], [CAP, CAP],
        color=col_cap, lw=1.6, ls=(0, (4, 3)), alpha=0.9, zorder=3)
ax.text(len(xs) - 0.4, CAP * 1.04, "the frame — 180 s",
        color=col_cap, fontsize=9, ha="right", va="bottom")

# ---- labels ------------------------------------------------------------------
ax.text(center - 1.9, FLOOR * 0.35, "in — patience", color="#c8c8d2", fontsize=10,
        ha="center", va="top")
ax.text(center + 1.9, FLOOR * 0.35, "out — the debts repaid", color="#c8c8d2",
        fontsize=10, ha="center", va="top")
ax.text(center, FLOOR * 0.35, "the count", color=col_gold, fontsize=10, ha="center", va="top")

ax.set_xticks(xs)
ax.set_xticklabels(steps, rotation=45, ha="right", color="#8a8a94", fontsize=7.5)
ax.set_ylim(FLOOR * 0.25, 260)
ax.set_yscale("log")
ax.set_yticks([1, 10, 100])
ax.set_yticklabels(["1 s", "10 s", "100 s"], color="#8a8a94", fontsize=8)
ax.tick_params(axis="y", colors="#55555e", length=3)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.spines["left"].set_color("#33333c")
ax.spines["bottom"].set_color("#33333c")

ax.set_title("the return, at full debt",
             color="#d8d8e0", fontsize=15, pad=14)
ax.text(0.5, 1.035, "out, the six shallow waits are repaid — each held its full beat, the swell completing and the tone landing home · the deepest owes one beat every 208 s",
        transform=ax.transAxes, color="#8a8a94", fontsize=9, ha="center", va="bottom")
ax.text(0.5, -0.11, "the wait is the holonomy of the time connection at the count: a loop around the puncture carries it, and no return leg cancels it — holonomy measures the hole, not the path.",
        transform=ax.transAxes, color="#6a6a76", fontsize=8.5, ha="center", va="top")

plt.tight_layout(rect=(0, 0.07, 1, 1))
plt.savefig("assets/holonomy-cover.png", facecolor=fig.get_facecolor())
print("wrote assets/holonomy-cover.png")
