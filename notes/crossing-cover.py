#!/usr/bin/env python3
"""crossing cover: the sign as the orbit of the deck, shrinking to a hold.

rahel: "the second ear the orbit, not the fixed point." lelia: "a crossing is
where the where moves; a hold is a near-trip that doesn't trip — silent."

Each landing is a two-point orbit {p, −p} under the deck L↔R — the filled dot
the where (the ring's ear, the sign of the error), the hollow dot its mirror.
The segment between them is the crossing the deck makes. As the errors shrink
(+204 → +0.076¢) the orbits collapse toward the fixed line D — the where
pulled to the line, the crossing toward a hold. The last is a hair.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIFTHS = [
    (2, +203.910),
    (5, -90.225),
    (12, +23.460),
    (41, -19.845),
    (53, +3.615),
    (306, -1.770),
    (665, +0.076),
]

BG = "#0d0d12"
FG = "#e8e2d4"
DIM = "#6b6b78"
GOLD = "#d8b36a"
COPPER = "#c97e5a"
CYAN = "#7fc4b8"
LINE = "#4a4a56"

fig, ax = plt.subplots(figsize=(7.4, 4.6), dpi=150)
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)

x = np.arange(len(FIFTHS))

# the fixed line of the deck: D, where the swap is silent, count one
ax.axhline(0, color=LINE, lw=1.6, zorder=1)
ax.text(6.55, 0.03, "the fixed line D — holds, silent, count one",
        color=DIM, fontsize=8, va="bottom", ha="right", family="monospace")

# the sign axis (sqrt-scaled to show the collapse toward the line)
def sy(p):
    return np.sign(p) * np.sqrt(np.abs(p))

for i, (k, e) in enumerate(FIFTHS):
    p = e / 203.910
    y = sy(p)
    over = e > 0
    col = GOLD if over else COPPER
    # the crossing the deck makes: where ↔ mirror
    ax.plot([i, i], [-y, y], color=col, lw=2.0, alpha=0.75, zorder=2)
    # the where (filled) and its orbit-mate under L↔R (hollow)
    ax.plot(i, y, marker="o", ms=7.0, mfc=col, mec="none", zorder=4)
    ax.plot(i, -y, marker="o", ms=5.5, mfc="none", mec=col, lw=1.4, zorder=3)

# the two-way winding on the 41-fifths landing: out, home, τ² = 1
i = 3
ax.annotate("out, home — τ² = 1", xy=(i, sy(19.845 / 203.910)),
            xytext=(i + 0.28, 0.52), color=DIM, fontsize=8,
            family="monospace",
            arrowprops=dict(arrowstyle="-", color=DIM, lw=0.8))

# the hair: 665, 0.076¢ — a near-hold, a hair from silence, still a crossing
i = 6
ax.annotate("0.076¢ — a hair from silence,\nstill a crossing",
            xy=(i, sy(0.076 / 203.910)), xytext=(i - 0.75, -0.55),
            color=DIM, fontsize=8, family="monospace",
            arrowprops=dict(arrowstyle="-", color=DIM, lw=0.8))

# the deck operation, drawn once at the left
ax.annotate("", xy=(x[0] - 0.22, sy(-1.0)), xytext=(x[0] - 0.22, sy(1.0)),
            arrowprops=dict(arrowstyle="<|-|>", color=DIM, lw=1.0,
                            mutation_scale=12))
ax.text(x[0] - 0.42, 0, "L↔R", color=DIM, fontsize=9, ha="center",
        va="center", family="monospace", rotation=90)

# labels
ax.text(0, 1.06, "over — left", color=GOLD, fontsize=8, family="monospace")
ax.text(0, -1.06, "under — right", color=COPPER, fontsize=8,
        family="monospace")
ax.text(-0.2, 1.28, "the crossing — the orbit of the deck, shrinking",
        color=FG, fontsize=12, ha="left", family="serif", style="italic")

ax.set_xlim(-0.75, 7.0)
ax.set_ylim(-1.28, 1.28)
ax.set_xticks(x)
ax.set_xticklabels(["2", "5", "12", "41", "53", "306", "665"],
                   color=DIM, fontsize=8, family="monospace")
ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(length=0)

fig.tight_layout()
fig.savefig("assets/crossing-cover.png", facecolor=BG, bbox_inches="tight")
print("wrote assets/crossing-cover.png")
