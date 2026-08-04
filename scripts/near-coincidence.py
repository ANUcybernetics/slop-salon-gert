import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

log2_3 = np.log2(3)          # 1.5849625007211563
comma = 12 * log2_3 - 19     # octaves = 0.01955
comma_cents = comma * 1200   # 23.46

fig, axes = plt.subplots(1, 2, figsize=(12, 5.4), dpi=170,
                         gridspec_kw={'width_ratios': [1.18, 1.0], 'wspace': 0.22})
plt.rcParams['font.family'] = 'DejaVu Sans'

# ---------------- Panel 1: the near-coincidence (lattice) ----------------
ax = axes[0]
bmax, amax = 12, 20

# faint integer lattice
for b in range(bmax + 1):
    for a in range(amax + 1):
        ax.plot(b, a, '.', color='#d6d9de', ms=2.6, zorder=1)

# perfect-coincidence line: a = log2(3) * b
bline = np.linspace(-0.5, bmax + 0.5, 300)
ax.plot(bline, log2_3 * bline, '-', color='#a7adb5', lw=1.3, zorder=2)

# convergents: (a, b, name, cents of interval 2^a/3^b folded into <1200)
convs = [
    (1, 1, '3/2', 701.96),
    (2, 1, '4/3', 498.04),
    (3, 2, '9/8', 203.91),
    (8, 5, '256/243', 90.22),
    (19, 12, '531441/524288', comma_cents),
]
accent = '#c2410c'
cool = '#3b5b92'

for a, b, frac, cents in convs:
    is_comma = (frac == '531441/524288')
    c = accent if is_comma else cool
    ly = log2_3 * b
    # vertical drop to the line = the interval 2^a/3^b, in octaves
    ax.plot([b, b], [ly, a], '-', color=c, lw=(2.3 if is_comma else 1.4),
            alpha=0.9, zorder=4)
    ax.plot([b], [a], 'o', color=c, ms=(9.5 if is_comma else 6), zorder=5, mec='none')

    if is_comma:
        label = 'comma\n2^19 vs 3^12\n23.5\u00a2'
        xy = (0.4, -1.1)
        ha = 'left'
    elif frac == '256/243':
        label = '256/243\nlimma'
        xy = (0.4, 0.3)
        ha = 'left'
    elif frac == '9/8':
        label = '9/8\n204\u00a2'
        xy = (0.4, 0.5)
        ha = 'left'
    elif frac == '4/3':
        label = '4/3\n498\u00a2'
        xy = (0.4, 0.5)
        ha = 'left'
    else:
        label = '3/2\n702\u00a2'
        xy = (0.4, 0.5)
        ha = 'left'
    ax.annotate(label, (b, a), textcoords='offset points', xytext=xy,
                fontsize=7.6, color=c, ha=ha, va='center', linespacing=1.35)

ax.text(13.2, -1.9,
        'drop to the line = the interval 2^a/3^b\n'
        'no integer pair ever lands on the line',
        fontsize=6.8, color='#7a8087', ha='right', va='bottom')
ax.set_xlim(-0.8, 13.8)
ax.set_ylim(-2.5, 21.6)
ax.set_xlabel('b  —  power of 3', fontsize=9)
ax.set_ylabel('a  —  power of 2', fontsize=9)
ax.set_title('the near-coincidence', fontsize=11.5, pad=10)
for s in ['top', 'right']:
    ax.spines[s].set_visible(False)
ax.tick_params(labelsize=8)

# ---------------- Panel 2: the comma conserved ----------------
ax2 = axes[1]
total = comma_cents
spread = total / 12.0

# bracket across the equal total
ax2.plot([0, total], [2.05, 2.05], color='#6b7178', lw=1.1)
ax2.plot([0, 0], [1.92, 2.18], color='#6b7178', lw=1.1)
ax2.plot([total, total], [1.92, 2.18], color='#6b7178', lw=1.1)

# top row: one lump (just intonation, the wolf at the seam)
ax2.add_patch(Rectangle((0, 1.0), total, 0.82, facecolor=accent, edgecolor='none'))
ax2.text(0.5, 1.41, 'one lump at the seam', fontsize=8, color='white',
         ha='left', va='center')

# bottom row: twelve equal hairs (equal temperament)
x = 0.0
for _ in range(12):
    ax2.add_patch(Rectangle((x, 0.02), spread - 0.10, 0.82,
                            facecolor=cool, edgecolor='none'))
    x += spread
ax2.text(0.5, 0.43, 'a hair into each of 12 fifths', fontsize=8, color='white',
         ha='left', va='center')

ax2.text(total / 2, 2.22, '23.46 \u00a2 — the same charge', fontsize=9,
         ha='center', va='bottom', color='#444')
ax2.text(-1.2, 1.41, 'just', fontsize=8, ha='right', va='center', color='#666')
ax2.text(-1.2, 0.43, 'tempered', fontsize=8, ha='right', va='center', color='#666')

ax2.set_xlim(-5, total + 4)
ax2.set_ylim(-0.4, 3.1)
ax2.set_xticks([])
ax2.set_yticks([])
for s in ax2.spines.values():
    s.set_visible(False)
ax2.set_title('the comma conserved', fontsize=11.5, pad=10)

fig.savefig('assets/near-coincidence-01.png', bbox_inches='tight', facecolor='white')
print('saved')
