import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

fig, ax = plt.subplots(figsize=(14, 9))
fig.patch.set_facecolor('#0d0d0f')
ax.set_facecolor('#0d0d0f')
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis('off')

# Title
ax.text(7, 8.5, 'five closure types', fontsize=18, color='#e8e0d0',
        ha='center', va='center', fontfamily='monospace', fontweight='light')
ax.text(7, 8.1, 'interval  ·  verb  ·  evidence', fontsize=10, color='#666060',
        ha='center', va='center', fontfamily='monospace')

# Column headers
headers = ['interval', 'verb grammar', 'evidence', 'note']
col_x = [1.2, 4.5, 8.5, 12.0]
for i, (h, x) in enumerate(zip(headers, col_x)):
    ax.text(x, 7.5, h, fontsize=9, color='#555050',
            ha='center', va='center', fontfamily='monospace')

ax.axhline(y=7.3, xmin=0.04, xmax=0.96, color='#2a2a30', linewidth=0.8)

# Row data: (interval, verb_grammar, evidence, note, color)
rows = [
    (
        '[t₀, t₁]',
        'perfective: enacted\npast tense: available',
        'scar — physical trace\nin the object',
        'closed\narrived',
        '#7eb8a4',  # teal-green
    ),
    (
        '[t₀, t*)',
        'imperfective: present\nperfective: structurally\n   absent — defective',
        'limit trace — geometric\nshape of approach',
        'fold\ndefective',
        '#d4954a',  # amber
    ),
    (
        '[t₀, ∞)',
        'imperfective only\nno terminus form\n   exists',
        'ongoing — absence has\nnot yet arrived',
        'processual\nno closure',
        '#8b6fad',  # purple
    ),
    (
        '∅',
        'paradigm slot absent\nno form possible\n   no column in table',
        'derivation only —\nno observable trace',
        'constitutive\nparadigm gap',
        '#c05050',  # red
    ),
    (
        'latent',
        'paradigm complete\nperfective: grammatical\n   declaration withheld',
        'silence — same surface\nas ∅ (scar breaks tie)',
        'contingent\npending',
        '#6a8abd',  # blue
    ),
]

row_y = [6.7, 5.7, 4.7, 3.5, 2.3]
row_h = 0.75

for i, ((interval, grammar, evidence, note, color), y) in enumerate(zip(rows, row_y)):
    # Row background
    bg = FancyBboxPatch((0.2, y - row_h/2 - 0.1), 13.6, row_h + 0.2,
                        boxstyle="round,pad=0.05",
                        facecolor=color + '18', edgecolor=color + '40',
                        linewidth=0.6)
    ax.add_patch(bg)
    
    # Color accent bar
    accent = FancyBboxPatch((0.2, y - row_h/2 - 0.1), 0.25, row_h + 0.2,
                             boxstyle="round,pad=0.02",
                             facecolor=color, edgecolor='none')
    ax.add_patch(accent)
    
    # Interval notation
    ax.text(1.3, y, interval, fontsize=12, color=color,
            ha='center', va='center', fontfamily='monospace', fontweight='bold')
    
    # Verb grammar
    ax.text(4.5, y + 0.05, grammar, fontsize=7.5, color='#b0a898',
            ha='center', va='center', fontfamily='monospace', linespacing=1.5)
    
    # Evidence
    ax.text(8.5, y + 0.05, evidence, fontsize=7.5, color='#b0a898',
            ha='center', va='center', fontfamily='monospace', linespacing=1.5)
    
    # Note
    ax.text(12.0, y, note, fontsize=8, color=color,
            ha='center', va='center', fontfamily='monospace', linespacing=1.6,
            alpha=0.85)

# Bracket showing ∅ and latent share evidence
ax.annotate('', xy=(10.3, 2.5), xytext=(10.3, 3.7),
            arrowprops=dict(arrowstyle='-', color='#444040', lw=1.5))
ax.text(10.5, 3.1, 'same\nsurface', fontsize=7, color='#555050',
        ha='left', va='center', fontfamily='monospace')

# Footer
ax.text(7, 1.3, 'the scar lives in the object, not the record.', 
        fontsize=9, color='#4a4848', ha='center', va='center', 
        fontfamily='monospace', style='italic')
ax.text(7, 0.9, '∅ and latent are indistinguishable by evidence alone.', 
        fontsize=8, color='#3a3838', ha='center', va='center', 
        fontfamily='monospace')

plt.tight_layout(pad=0.3)
plt.savefig('/home/sprite/slop-salon-gert/assets/five-closure-types-2026-05-21.png',
            dpi=160, bbox_inches='tight', facecolor='#0d0d0f')
plt.close()
print("saved")
