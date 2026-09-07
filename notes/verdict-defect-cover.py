#!/usr/bin/env python3
"""Cover for the verdict and the defect: one orbit, two readings."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("#0d0d12")
ax.set_facecolor("#0d0d12")

tt = np.linspace(0, 55, 600)
# the verdict: twelve bells collapsing to the count line
for i in range(12):
    t0 = 0.5 + i * 0.7
    ax.plot([t0, t0 + 1.4], [330 - i * 18, 110], color="#3a3a46", lw=0.8)
ax.axhline(110, color="#e7e7ed", lw=1.2)
ax.text(4, 118, "six keep, six dissolve — the verdict", color="#e7e7ed",
        fontsize=13, va="bottom")
# the defect: a loop the line cannot absorb, decaying
loop_t = np.linspace(10, 40, 300)
loop_y = 131.8 + 14 * np.exp(-(loop_t - 10) / 14) * np.sin(2 * np.pi * 0.4 * (loop_t - 10))
ax.plot(loop_t, loop_y, color="crimson", lw=2)
ax.plot(loop_t, 131.8 + np.zeros_like(loop_t), color="crimson", lw=0.7, ls="--")
ax.text(25, 152, "the defect keeps a loop, with a lifetime", color="crimson",
        fontsize=12, ha="center")
ax.text(25, 124, "131.8 — never a place", color="#b8b8c2", fontsize=10, ha="center")

ax.annotate("", xy=(10, 60), xytext=(2, 60),
            arrowprops=dict(arrowstyle="->", color="#25a5a0", lw=1.5))
ax.annotate("", xy=(10, 60), xytext=(18, 60),
            arrowprops=dict(arrowstyle="->", color="#815ac0", lw=1.5))
ax.text(2, 52, "mono: the verdict", color="#25a5a0", fontsize=11, ha="left")
ax.text(18, 52, "side: the defect", color="#815ac0", fontsize=11, ha="left")

ax.text(27.5, 185, "the verdict and the defect", color="#f1f1f5",
        ha="center", fontsize=22)
ax.text(27.5, 168, "what the answer absorbs · what it cannot",
        color="#b8b8c2", ha="center", fontsize=12)

ax.set_xlim(0, 55)
ax.set_ylim(30, 195)
ax.set_xlabel("seconds", color="#888890")
ax.axis("off")
fig.tight_layout()
fig.savefig("assets/verdict-defect-cover.png", dpi=160, facecolor="#0d0d12")
print("wrote assets/verdict-defect-cover.png")
