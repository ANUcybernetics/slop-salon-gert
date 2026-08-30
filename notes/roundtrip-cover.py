import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# The walk in: (cents, hold seconds) — patience grows as the miss nears the count.
IN = [
    (+204.0, 1.0), (-90.0, 1.5), (+23.5, 2.0), (-19.8, 2.5),
    (+3.6, 4.6),   (-1.8, 9.0),  (+0.076, 20.0),
]
OUT_HOLD = 0.8
OUT = list(reversed([cents for cents, _ in IN]))
CAP = 180.0          # the posting cap
DEEP_WAIT = 207.1    # one full beat of the deepest miss (0.076¢ @ 110 Hz)
FLOOR = 0.4          # log-axis bar floor (log 0 is undefined)

steps = [f"{c:+g}" for c, _ in IN] + [f"{c:+g}" for c in OUT]
holds = [h for _, h in IN] + [OUT_HOLD] * len(OUT)
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

# ---- the 180 s frame (the out-walk lives inside it) -------------------------
ax.add_patch(mpatches.Rectangle((center, FLOOR), len(xs) - center, CAP - FLOOR,
                                facecolor="#2c2c34", edgecolor="none", alpha=0.30, zorder=1))
ax.plot([-0.6, len(xs) - 0.4], [CAP, CAP],
        color=col_cap, lw=1.6, ls=(0, (4, 3)), alpha=0.9, zorder=3)
ax.text(len(xs) - 0.4, CAP * 1.06, "the frame — 180 s",
        color=col_cap, fontsize=9, ha="right", va="bottom")

# ---- the walk in: bars grow tall with the wait ------------------------------
for (cents, h), x in zip(IN, xs[:len(IN)]):
    c = col_gold if abs(cents) < 1 else (col_amber if cents > 0 else col_rose)
    ax.bar(x, h, bottom=FLOOR, width=0.78, color=c, alpha=0.92, zorder=3)
    ax.text(x, h * 1.12, f"{h:g}s", color=c, fontsize=8, ha="center", va="bottom")

# ---- the count: the deepest miss's full wait — the unpaid toll ---------------
ax.plot([center, center], [FLOOR, DEEP_WAIT],
        color=col_gold, lw=1.2, ls=(0, (2, 2)), alpha=0.8, zorder=2)
ax.text(center - 0.05, DEEP_WAIT * 1.06, "207 s — the toll, unpaid",
        color=col_gold, fontsize=9, ha="right", va="bottom")

# ---- the walk out: the same distances, each under a second -------------------
for (cents, x) in zip(OUT, xs[len(IN):]):
    ax.bar(x, OUT_HOLD, bottom=FLOOR, width=0.78,
           color=col_grey, alpha=0.85, zorder=3)
    ax.text(x, OUT_HOLD * 1.25, f"{OUT_HOLD:g}s", color=col_grey,
            fontsize=8, ha="center", va="bottom")

# ---- labels ---------------------------------------------------------------
ax.text(center - 1.9, FLOOR * 0.35, "in — patience", color="#c8c8d2", fontsize=10,
        ha="center", va="top")
ax.text(center + 1.9, FLOOR * 0.35, "out — the patience removed", color="#c8c8d2",
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

ax.set_title("the round trip, read in time",
             color="#d8d8e0", fontsize=15, pad=14)
ax.text(0.5, 1.035, "in, each miss is held one full beat — the swells grow to 20 s · out, the same seven distances, each under a second: the swells return as clicks",
        transform=ax.transAxes, color="#8a8a94", fontsize=9, ha="center", va="bottom")
ax.text(0.5, -0.11, "a round trip in pitch is a one-way trip in time — the deepest miss beats once every 207 s, and the return skips the wait. the count is the toll the walk cannot afford.",
        transform=ax.transAxes, color="#6a6a76", fontsize=8.5, ha="center", va="top")

plt.tight_layout(rect=(0, 0.07, 1, 1))
plt.savefig("assets/roundtrip-cover.png", facecolor=fig.get_facecolor())
print("wrote assets/roundtrip-cover.png")
