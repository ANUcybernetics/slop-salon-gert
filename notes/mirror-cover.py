#!/usr/bin/env python3
"""The score for 'the ring and its twin' — three seats, descending octaves,
the halved zeta ladder, the odd note in the gap.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

GOLD  = '#e3b341'
AMBER = '#d08c60'
TEAL  = '#4ec9b0'
ROSE  = '#d25f7f'
INK   = '#0d1117'
GRID  = '#2a3140'
TXT   = '#d6dae0'

gams = np.array([14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918719, 43.327073, 48.005151, 49.773832])
FRINGS = 8.0 * (gams / 2.0)
entries = np.array([8, 14, 20, 26, 32, 38, 44, 50, 56, 62])
FODD = 8.0 * 9.94

fig, ax = plt.subplots(figsize=(11.2, 6.0), dpi=200)
fig.patch.set_facecolor(INK)
ax.set_facecolor(INK)
ax.tick_params(colors=TXT, labelsize=8)
for sp in ax.spines.values():
    sp.set_color(GRID)

ax.set_xlim(0, 80)
ax.set_ylim(np.log2(26.0), np.log2(225.0))
ax.set_yticks(np.log2([27.5, 55, 110, 220]))
ax.set_yticklabels(['27.5', '55', '110', '220'])
ax.set_xlabel('seconds', color=TXT, fontsize=10)
ax.set_ylabel('frequency  (Hz)', color=TXT, fontsize=10)
ax.set_title('the ring and its twin — three seats, the ladder, the gap',
             color=TXT, fontsize=12)

def y(f):
    return np.log2(f)

# the three seats as descending octaves
for f, c, lab in [(110, GOLD, '2⁰ count · the drone'),
                  (55, AMBER, '2⁻¹ shore · the sign'),
                  (27.5, TEAL, '2⁻² the zeros · φ poles at ρ/2')]:
    ax.axhline(y(f), color=c, lw=1.6, ls='--', alpha=0.5)
    ax.text(79.5, y(f) + 0.05, lab, color=c, fontsize=8, ha='right', va='bottom')

# the count drone — a single held line, in phase, survives the fold
ax.plot([0, 80], [y(110), y(110)], color=GOLD, lw=4.5, solid_capstyle='round', zorder=4)
ax.text(1, y(110) + 0.12, 'survives the fold', color=GOLD, fontsize=8, va='bottom')

# the ten rings — each a pole/mirror pair, drawn as a teal stroke + rose twin
for f, t0 in zip(FRINGS[::-1], entries):
    # pole: decays with tau=9s; draw the stroke to ~5 tau
    t_end = min(t0 + 22, 80)
    ax.plot([t0, t_end], [y(f), y(f)], color=TEAL, lw=2.6, alpha=0.9, zorder=3)
    # mirror zero: the same pitch, offset by half a second, dashed rose
    ax.plot([t0 + 0.7, min(t_end + 0.7, 80)], [y(f), y(f)], color=ROSE, lw=1.6,
            ls=(0, (3, 2)), alpha=0.85, zorder=3)

# the odd note — in the gap, not on the ladder, unpins linearly to zero
t_odd = np.linspace(38, 80, 4)
a = np.linspace(1.0, 0.0, 4)
for x, aa in zip(t_odd[:-1], a[:-1]):
    ax.plot([x, x + 0.6], [y(FODD) + 0.04, y(FODD) + 0.04], color=ROSE, lw=2.2*aa + 0.4,
            alpha=0.9, zorder=4)
ax.annotate('odd op t≈9.94 — in the gap\nnot a ζ zero, off-line, identity open',
            xy=(44, y(FODD) + 0.18), xytext=(44, y(190)),
            color=ROSE, fontsize=8, ha='center',
            arrowprops=dict(arrowstyle='->', color=ROSE, lw=0.8, ls=':'))

# fold marker
ax.axvspan(74, 80, color=GOLD, alpha=0.06, zorder=0)
ax.text(77, y(27.5) + 0.1, 'fold', color=GOLD, fontsize=9, ha='center', va='bottom')
ax.text(0.02, 0.02, 'every ring is a pair — fold to mono and the pairs fold in;\nthe mirror is the residue-balance: Σ Res = 0, φφ(1−s) = 1, the drone holds.',
        transform=ax.transAxes, color=TXT, fontsize=8, va='bottom',
        path_effects=[pe.withStroke(linewidth=2, foreground=INK)])

fig.tight_layout()
out = 'assets/mirror-cover.png'
fig.savefig(out, facecolor=INK, bbox_inches='tight')
print('saved', out)
