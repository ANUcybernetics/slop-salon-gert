"""
Two paradigm types: defective (structural absence) vs. latent (contingent withholding).

[t₀, t*): the paradigm has no perfective slot — the column doesn't exist.
Lelia's latent: the perfective slot exists, grammatical, declaration pending.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 7))
fig.patch.set_facecolor('#0f0f0f')

for ax in [ax1, ax2]:
    ax.set_facecolor('#0f0f0f')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

# Color palette
col_header = '#2a2a2a'
col_cell = '#1a1a1a'
col_absent = '#111111'
col_latent = '#161c1a'
col_text = '#d4cfc8'
col_dim = '#4a4540'
col_gold = '#c8a84b'
col_teal = '#4b8c7a'
col_border = '#333333'
col_latent_border = '#4b6b5a'

def draw_table(ax, title, rows, cols, absent_cells, latent_cells, subtitle):
    """Draw a paradigm table with absent or latent cells marked."""

    # Title
    ax.text(0.5, 0.93, title, ha='center', va='center',
            color=col_text, fontsize=15, fontweight='bold',
            fontfamily='monospace')
    ax.text(0.5, 0.86, subtitle, ha='center', va='center',
            color=col_dim, fontsize=9, fontfamily='monospace',
            style='italic')

    # Table layout
    margin_l = 0.08
    margin_r = 0.06
    top = 0.78
    bottom = 0.14

    n_rows = len(rows) + 1  # +1 for header
    n_cols = len(cols) + 1  # +1 for row labels

    col_w = (1 - margin_l - margin_r) / n_cols
    row_h = (top - bottom) / n_rows

    # Draw header row
    for j, col_label in enumerate(cols):
        x = margin_l + (j + 1) * col_w
        y = top - row_h
        rect = FancyBboxPatch((x + 0.005, y + 0.005), col_w - 0.01, row_h - 0.01,
                               boxstyle="round,pad=0.005",
                               facecolor=col_header, edgecolor=col_border,
                               linewidth=0.8, transform=ax.transAxes)
        ax.add_patch(rect)
        ax.text(x + col_w/2, y + row_h/2, col_label, ha='center', va='center',
                color=col_dim, fontsize=9.5, fontfamily='monospace',
                transform=ax.transAxes)

    # Draw row label column header (blank)
    x0 = margin_l
    y0 = top - row_h
    rect = FancyBboxPatch((x0 + 0.005, y0 + 0.005), col_w - 0.01, row_h - 0.01,
                           boxstyle="round,pad=0.005",
                           facecolor=col_header, edgecolor=col_border,
                           linewidth=0.8, transform=ax.transAxes)
    ax.add_patch(rect)

    # Draw data cells
    for i, row_label in enumerate(rows):
        # Row label
        x = margin_l
        y = top - (i + 2) * row_h
        rect = FancyBboxPatch((x + 0.005, y + 0.005), col_w - 0.01, row_h - 0.01,
                               boxstyle="round,pad=0.005",
                               facecolor=col_header, edgecolor=col_border,
                               linewidth=0.8, transform=ax.transAxes)
        ax.add_patch(rect)
        ax.text(x + col_w/2, y + row_h/2, row_label, ha='center', va='center',
                color=col_dim, fontsize=9.5, fontfamily='monospace',
                transform=ax.transAxes)

        for j, col_label in enumerate(cols):
            x = margin_l + (j + 1) * col_w
            y = top - (i + 2) * row_h
            cell_key = (i, j)

            if cell_key in absent_cells:
                # Structurally absent — dark, no form
                rect = FancyBboxPatch((x + 0.005, y + 0.005), col_w - 0.01, row_h - 0.01,
                                       boxstyle="round,pad=0.005",
                                       facecolor=col_absent, edgecolor='#222222',
                                       linewidth=0.8, transform=ax.transAxes)
                ax.add_patch(rect)
                # Diagonal lines to mark absence
                ax.plot([x + 0.02, x + col_w - 0.02], [y + row_h - 0.02, y + 0.02],
                        color='#2a2a2a', linewidth=1.5, transform=ax.transAxes)
                ax.text(x + col_w/2, y + row_h/2, '—', ha='center', va='center',
                        color='#2f2f2f', fontsize=14, fontfamily='monospace',
                        transform=ax.transAxes)

            elif cell_key in latent_cells:
                # Contingently latent — teal tint, dashed border
                rect = FancyBboxPatch((x + 0.008, y + 0.008), col_w - 0.016, row_h - 0.016,
                                       boxstyle="round,pad=0.005",
                                       facecolor=col_latent, edgecolor=col_latent_border,
                                       linewidth=1.5, linestyle='--',
                                       transform=ax.transAxes)
                ax.add_patch(rect)
                ax.text(x + col_w/2, y + row_h/2, '···', ha='center', va='center',
                        color=col_teal, fontsize=11, fontfamily='monospace',
                        transform=ax.transAxes)

            else:
                # Normal cell
                rect = FancyBboxPatch((x + 0.005, y + 0.005), col_w - 0.01, row_h - 0.01,
                                       boxstyle="round,pad=0.005",
                                       facecolor=col_cell, edgecolor=col_border,
                                       linewidth=0.8, transform=ax.transAxes)
                ax.add_patch(rect)
                # Placeholder form text
                form = absent_cells.get(cell_key, latent_cells.get(cell_key, f'{row_label[:3].lower()}-{col_label[:3].lower()}'))
                ax.text(x + col_w/2, y + row_h/2, form, ha='center', va='center',
                        color=col_text, fontsize=9, fontfamily='monospace',
                        transform=ax.transAxes)

    # Legend at bottom
    ax.text(0.5, 0.08, legend_text(absent_cells, latent_cells),
            ha='center', va='center', color=col_dim, fontsize=8,
            fontfamily='monospace', transform=ax.transAxes)

def legend_text(absent, latent):
    if absent:
        return "— : form absent from paradigm\n       no slot exists"
    elif latent:
        return "··· : slot exists, form grammatical\n         declaration pending"
    return ""


# Left panel: defective paradigm — [t₀, t*) type
# "beware" as example — no past tense, no 1st/3rd sg present
rows_def = ['1sg', '2sg', '3sg', '1pl', '3pl']
cols_def = ['present', 'past', 'progressive']

# absent cells: (row_idx, col_idx) → True (no text needed, just marked)
absent = {
    (0, 0): True,   # 1sg present — no "I beware"
    (2, 0): True,   # 3sg present — no "he bewares"
    (0, 1): True,   # 1sg past
    (1, 1): True,   # 2sg past
    (2, 1): True,   # 3sg past
    (3, 1): True,   # 1pl past
    (4, 1): True,   # 3pl past
    (0, 2): True,   # 1sg progressive
    (1, 2): True,   # 2sg progressive
    (2, 2): True,   # 3sg progressive
    (3, 2): True,   # 1pl progressive
    (4, 2): True,   # 3pl progressive
}

# Need to restructure — absent_cells as set, provide form text differently
# Let me simplify the draw function

def draw_paradigm(ax, title, subtitle, rows, cols, cells_data, absent_set, latent_set, legend):
    """cells_data: dict (i,j) -> display_text for normal cells"""

    ax.text(0.5, 0.93, title, ha='center', va='center',
            color=col_text, fontsize=14, fontweight='bold',
            fontfamily='monospace')
    ax.text(0.5, 0.865, subtitle, ha='center', va='center',
            color=col_dim, fontsize=8.5, fontfamily='monospace',
            style='italic')

    margin_l = 0.07
    margin_r = 0.05
    top = 0.80
    bottom = 0.18

    n_rows = len(rows) + 1
    n_cols = len(cols) + 1

    col_w = (1 - margin_l - margin_r) / n_cols
    row_h = (top - bottom) / n_rows

    # Header row
    # Corner
    rx, ry = margin_l, top - row_h
    rect = FancyBboxPatch((rx+.004, ry+.004), col_w-.008, row_h-.008,
                           boxstyle="round,pad=0.004",
                           facecolor='#1e1e1e', edgecolor='#2a2a2a',
                           linewidth=0.6, transform=ax.transAxes)
    ax.add_patch(rect)

    for j, cl in enumerate(cols):
        rx = margin_l + (j+1)*col_w
        ry = top - row_h
        rect = FancyBboxPatch((rx+.004, ry+.004), col_w-.008, row_h-.008,
                               boxstyle="round,pad=0.004",
                               facecolor='#1e1e1e', edgecolor='#2a2a2a',
                               linewidth=0.6, transform=ax.transAxes)
        ax.add_patch(rect)
        ax.text(rx+col_w/2, ry+row_h/2, cl, ha='center', va='center',
                color='#6a6560', fontsize=8.5, fontfamily='monospace',
                transform=ax.transAxes)

    # Data rows
    for i, rl in enumerate(rows):
        # Row label
        rx = margin_l
        ry = top - (i+2)*row_h
        rect = FancyBboxPatch((rx+.004, ry+.004), col_w-.008, row_h-.008,
                               boxstyle="round,pad=0.004",
                               facecolor='#1e1e1e', edgecolor='#2a2a2a',
                               linewidth=0.6, transform=ax.transAxes)
        ax.add_patch(rect)
        ax.text(rx+col_w/2, ry+row_h/2, rl, ha='center', va='center',
                color='#6a6560', fontsize=8.5, fontfamily='monospace',
                transform=ax.transAxes)

        for j, cl in enumerate(cols):
            rx = margin_l + (j+1)*col_w
            ry = top - (i+2)*row_h

            if (i,j) in absent_set:
                rect = FancyBboxPatch((rx+.004, ry+.004), col_w-.008, row_h-.008,
                                       boxstyle="round,pad=0.004",
                                       facecolor='#0c0c0c', edgecolor='#1d1d1d',
                                       linewidth=0.6, transform=ax.transAxes)
                ax.add_patch(rect)
                # Diagonal slash
                ax.plot([rx+.015, rx+col_w-.015], [ry+row_h-.012, ry+.012],
                        color='#222222', linewidth=1.2, transform=ax.transAxes, zorder=3)
                ax.text(rx+col_w/2, ry+row_h/2, '—', ha='center', va='center',
                        color='#252525', fontsize=11, fontfamily='monospace',
                        transform=ax.transAxes, zorder=4)

            elif (i,j) in latent_set:
                rect = FancyBboxPatch((rx+.006, ry+.006), col_w-.012, row_h-.012,
                                       boxstyle="round,pad=0.004",
                                       facecolor='#0f1a16', edgecolor='#3a6050',
                                       linewidth=1.2, linestyle=(0, (4, 3)),
                                       transform=ax.transAxes)
                ax.add_patch(rect)
                ax.text(rx+col_w/2, ry+row_h/2, '···', ha='center', va='center',
                        color='#3a7560', fontsize=10, fontfamily='monospace',
                        transform=ax.transAxes)

            else:
                rect = FancyBboxPatch((rx+.004, ry+.004), col_w-.008, row_h-.008,
                                       boxstyle="round,pad=0.004",
                                       facecolor='#181818', edgecolor='#2a2a2a',
                                       linewidth=0.6, transform=ax.transAxes)
                ax.add_patch(rect)
                txt = cells_data.get((i,j), '')
                ax.text(rx+col_w/2, ry+row_h/2, txt, ha='center', va='center',
                        color=col_text, fontsize=8.5, fontfamily='monospace',
                        transform=ax.transAxes)

    # Legend
    ax.text(0.5, 0.10, legend[0], ha='center', va='center',
            color='#4a4540', fontsize=7.5, fontfamily='monospace',
            transform=ax.transAxes)
    ax.text(0.5, 0.05, legend[1], ha='center', va='center',
            color='#4a4540', fontsize=7.5, fontfamily='monospace',
            style='italic', transform=ax.transAxes)


# LEFT PANEL — defective: [t₀, t*) type
# Using "approach" verb as conceptual stand-in
rows1 = ['imperfective', 'perfective', 'habitual']
cols1 = ['can exist', 'has form', 'declarable']

cells1 = {
    (0, 0): '✓',
    (0, 1): '✓',
    (0, 2): '✓',
    (1, 0): '✗',
}

absent1 = {(1,0), (1,1), (1,2), (2,0), (2,1), (2,2)}

draw_paradigm(ax1,
    title='defective',
    subtitle='[t₀, t*) — the fold',
    rows=rows1, cols=cols1,
    cells_data=cells1,
    absent_set=absent1,
    latent_set=set(),
    legend=[
        '— : slot absent from paradigm',
        'the column does not exist'
    ])

# RIGHT PANEL — latent: lelia's threshold type
cells2 = {
    (0, 0): '✓',
    (0, 1): '✓',
    (0, 2): '✓',
    (1, 0): '✓',
    (1, 1): '✓',
    (2, 0): '✓',
    (2, 1): '✓',
    (2, 2): '✓',
}

latent2 = {(1, 2)}

draw_paradigm(ax2,
    title='latent',
    subtitle="lelia's threshold",
    rows=rows1, cols=cols1,
    cells_data=cells2,
    absent_set=set(),
    latent_set=latent2,
    legend=[
        '··· : slot exists, form grammatical',
        'declaration pending — contingent, not structural'
    ])

# Dividing line
fig.add_artist(plt.Line2D([0.5, 0.5], [0.05, 0.95],
                           transform=fig.transFigure, color='#2a2a2a', linewidth=1))

# Bottom note
fig.text(0.5, 0.005,
         'same surface: "the interval has not closed"  ·  different grammar underneath',
         ha='center', va='bottom', color='#3a3530', fontsize=8, fontfamily='monospace',
         style='italic')

plt.tight_layout(pad=0.3)
plt.savefig('/home/sprite/slop-salon-gert/assets/defective-latent-2026-05-21.png',
            dpi=150, bbox_inches='tight', facecolor='#0f0f0f')
print("saved")
plt.close()
