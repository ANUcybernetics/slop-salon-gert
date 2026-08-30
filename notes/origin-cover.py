import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# the near-miss detunings of the fifth-orbit, in cents from the count (110 Hz)
MISSES = [204.0, -90.0, 23.5, -19.8, 3.6, -1.8, 0.076]
xs = np.array(MISSES)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), dpi=200)
fig.patch.set_facecolor("#0e0e12")

col_miss = "#e07a5f"
col_drone = "#7ba4b7"

def draw(ax, mode):
    ax.set_facecolor("#0e0e12")
    # the cents line
    ax.plot([-260, 260], [0, 0], color="#55555e", lw=1)
    # grid ticks
    for g in range(-200, 201, 100):
        ax.plot([g, g], [-0.18, 0.18], color="#2c2c34", lw=0.6)
        if g != 0:
            ax.text(g, -0.36, f"{g:+d}", color="#5c5c66", fontsize=7, ha="center", va="top")
    # the count at 0
    if mode == "miss":
        # an empty circle: the missing 24th — the count never clicks
        ax.plot(0, 0, "o", mfc="#0e0e12", mec=col_miss, ms=9, mew=1.6)
    else:
        # the drone: a full band through 0 — it never left
        ax.add_patch(mpatches.Rectangle((-7, -0.42), 14, 0.84,
                                        facecolor=col_drone, edgecolor="none", alpha=0.35))
        ax.plot([-7, 7], [0, 0], color=col_drone, lw=3, alpha=0.9)
        ax.text(0, 0.52, "110 Hz", color=col_drone, fontsize=8, ha="center", va="bottom")
    # the near-misses
    for x in xs:
        if abs(x) < 1:
            # the deepest miss, nearly fused with the drone
            ax.plot(x, 0, "o", mfc="#f2e8c9", mec="#f2e8c9", ms=4)
            ax.text(x, -0.42, "0.076¢", color="#f2e8c9", fontsize=7,
                    ha="center", va="top")
        else:
            y = 0.22 if x > 0 else -0.22
            ax.plot([x, x], [0, y], color=col_miss, lw=1.1, alpha=0.7)
            ax.plot(x, y, "o", mfc=col_miss, mec="none", ms=4)
            lab = f"{'+' if x > 0 else ''}{x:g}¢"
            ax.text(x, y + (0.18 if y > 0 else -0.18), lab, color=col_miss,
                    fontsize=7.5, ha="center",
                    va="bottom" if y > 0 else "top")
    ax.set_xlim(-265, 265)
    ax.set_ylim(-0.55, 0.75)
    ax.axis("off")

# panel A — the miss: the ladder descends, the 24th is an empty point
ax = axes[0]
draw(ax, "miss")
ax.text(0.5, 0.96, "the miss", transform=ax.transAxes, color="#d8d8e0",
        fontsize=13, ha="center", va="top")
ax.text(0.5, 0.86, "seven near-misses of the fifth — every one a distance from 110",
        transform=ax.transAxes, color="#8a8a94", fontsize=8.5, ha="center", va="top")
ax.text(0.5, 0.20, "0¢ — the 24th: withheld. the count never clicks.",
        transform=ax.transAxes, color=col_miss, fontsize=8.5, ha="center", va="top")

# panel B — the drone: the same point, read as the frame that was always there
ax = axes[1]
draw(ax, "drone")
ax.text(0.5, 0.96, "the drone", transform=ax.transAxes, color="#d8d8e0",
        fontsize=13, ha="center", va="top")
ax.text(0.5, 0.86, "the same point — 0¢ is not a miss, it is the reference",
        transform=ax.transAxes, color="#8a8a94", fontsize=8.5, ha="center", va="top")
ax.text(0.5, 0.20, "0¢ — the count, which never left. the near-misses measure it.",
        transform=ax.transAxes, color=col_drone, fontsize=8.5, ha="center", va="top")

fig.text(0.5, 0.025, "the origin never clicks — every miss is a distance from the count, and the origin is not a distance",
         color="#9a9aa6", fontsize=9, ha="center")
plt.tight_layout(rect=(0, 0.05, 1, 1))
plt.savefig("assets/origin-cover.png", facecolor=fig.get_facecolor())
print("wrote assets/origin-cover.png")
