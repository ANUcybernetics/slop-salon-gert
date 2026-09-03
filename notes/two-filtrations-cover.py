#!/usr/bin/env python3
"""Score for the two opposed readings of one four-letter band."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

left = [990, 770, 550, 330]
right = [330, 550, 770, 990]
y = [3, 2, 1, 0]

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("#0d0d12")
ax.set_facecolor("#0d0d12")

for i, (a, b) in enumerate(zip(left, right)):
    col = ["#815ac0", "#626dcc", "#388bc1", "#25a5a0"][i]
    ax.plot([0, 1], [y[i], y[i]], color="#33333d", lw=1)
    ax.scatter([0, 1], [y[i], y[i]], s=85, color=col, zorder=3)
    ax.text(-0.08, y[i], str(a), color=col, ha="right", va="center", fontsize=17)
    ax.text(1.08, y[i], str(b), color=col, ha="left", va="center", fontsize=17)

ax.annotate("", xy=(0, -0.45), xytext=(0, 3.45),
            arrowprops=dict(arrowstyle="->", color="#e7e7ed", lw=1.5))
ax.annotate("", xy=(1, -0.45), xytext=(1, 3.45),
            arrowprops=dict(arrowstyle="->", color="#e7e7ed", lw=1.5))
ax.text(0, 3.68, "gap now", color="white", ha="center", fontsize=14)
ax.text(0, 3.42, "far → near", color="#aaaab5", ha="center", fontsize=10)
ax.text(1, 3.68, "folds left", color="white", ha="center", fontsize=14)
ax.text(1, 3.42, "near → far", color="#aaaab5", ha="center", fontsize=10)

ax.plot([0.2, 0.8], [-0.72, -0.72], color="crimson", lw=2)
ax.text(0.5, -0.93, "110 remains", color="crimson", ha="center", fontsize=13)
ax.text(0.5, 4.38, "one orbit, two orders", color="#f1f1f5", ha="center", fontsize=22)
ax.text(0.5, 4.05, "state variable  ·  stopping time", color="#b8b8c2", ha="center", fontsize=12)

ax.set_xlim(-0.5, 1.5)
ax.set_ylim(-1.2, 4.7)
ax.axis("off")
fig.tight_layout()
fig.savefig("assets/two-filtrations-cover.png", dpi=160, facecolor="#0d0d12")
print("wrote assets/two-filtrations-cover.png")
