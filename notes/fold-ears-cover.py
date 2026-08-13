#!/usr/bin/env python3
"""
fold-ears-cover.py — cover for "the octave is the fold between the ears"

A fold down the middle (the +1, the octave). The temperaments throw from both
sides, alternating sharp (even, right) and flat (odd, left), thinning toward
the fold, never crossing it. log2(3) = 1 + log2(3/2) — same tail, one +1 apart.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# (denominator, cents residue, sharp?)
THROWS = [(12, +23.46, True), (41, -19.85, False), (53, +3.61, True),
          (306, -1.76, False), (665, +0.08, True), (15601, -0.03, False)]

fig, ax = plt.subplots(figsize=(14, 9), dpi=150)
fig.patch.set_facecolor('#101418')
ax.set_facecolor('#101418')

# the fold: vertical line down the center
ax.axvline(0, color='#d8c8a8', lw=2.5, alpha=0.95, zorder=3)

# the throws: alternating bars from the fold
x = np.log2([q for q, _, _ in THROWS])          # log scale positions
for q, cents, sharp in THROWS:
    i = THROWS.index((q, cents, sharp))
    xi = x[i]
    h = abs(cents)
    color = '#e8a858' if sharp else '#58a8e8'    # sharp warm, flat cool
    if sharp:
        ax.barh(xi, h, left=0, height=0.35, color=color, alpha=0.9,
                edgecolor='none', zorder=2)
    else:
        ax.barh(xi, -h, left=0, height=0.35, color=color, alpha=0.9,
                edgecolor='none', zorder=2)
    # label the residue
    ha = 'left' if not sharp else 'right'
    ax.text(0 + (0.5 if not sharp else -0.5) * np.sign(cents),
            xi + 0.16, f"{q}  {cents:+.2f}¢", color='#e6dcc8',
            fontsize=11, ha='center', va='bottom')

# faint ghost: the family thinning, dotted toward the fold
ax.plot([0], [x[0]], 'o', color='#d8c8a8', ms=4, zorder=4)

ax.set_xlim(-32, 32)
ax.set_ylim(-0.6, x[-1] + 0.8)

# axis labels
ax.text(0, -0.35, "the fold — the octave, the +1", color='#d8c8a8',
        ha='center', va='top', fontsize=13, style='italic')
ax.text(-30, x[-1] + 0.45, "flat", color='#58a8e8', fontsize=14, ha='left')
ax.text(30, x[-1] + 0.45, "sharp", color='#e8a858', fontsize=14, ha='right')

# header line
ax.text(0, x[-1] + 1.55, "log₂3 = 1 + log₂(3/2)", color='#f0e8d8',
        ha='center', fontsize=20, fontfamily='DejaVu Sans')
ax.text(0, x[-1] + 1.05, "same tail, one +1 apart — the integer part decides which ear",
        color='#9a9080', ha='center', fontsize=12)

for s in ['top', 'right', 'left', 'bottom']:
    ax.spines[s].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/assets/fold-ears-cover.png',
            facecolor=fig.get_facecolor())
print("saved cover")
