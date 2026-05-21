"""
Evidence-types diagram.
Rahel's observation: each interval type leaves a different kind of trace.

[t₀, t₁]:    scar — physical trace
[t₀, t*):    limit point — geometric trace
[t₀, ∞):     nothing yet — absence not yet arrived
∅:            derivation only — no observable trace
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

fig, axes = plt.subplots(1, 4, figsize=(16, 4.5), facecolor='#0a0a0f')
fig.subplots_adjust(left=0.03, right=0.97, top=0.82, bottom=0.18, wspace=0.1)

BG = '#0a0a0f'
LIGHT = '#d4cfc8'
DIM = '#5a5550'
AMBER = '#c8914a'
INDIGO = '#7070c0'
ROSE = '#c07080'
TEAL = '#50a090'

for ax in axes:
    ax.set_facecolor(BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')

# ── Panel 1: [t₀, t₁] — scar ──────────────────────────────────────────────
ax = axes[0]
# A horizontal track with a clear scar (a vertical mark where crossing happened)
y = 5.0
# Left region: one color
ax.fill_between([0.5, 4.8], [3.5, 3.5], [6.5, 6.5], color='#1a2030', alpha=0.8)
# Right region: another color
ax.fill_between([5.2, 9.5], [3.5, 3.5], [6.5, 6.5], color='#201a30', alpha=0.8)
# The scar: a narrow vertical band
ax.fill_between([4.8, 5.2], [3.5, 3.5], [6.5, 6.5], color=AMBER, alpha=0.5)
ax.axvline(x=5.0, color=AMBER, lw=2.0, alpha=0.9)

# Trajectory line that crossed
ax.annotate('', xy=(5.0, y), xytext=(1.5, y),
            arrowprops=dict(arrowstyle='->', color=LIGHT, lw=1.5))
ax.annotate('', xy=(8.5, y), xytext=(5.0, y),
            arrowprops=dict(arrowstyle='->', color=DIM, lw=1.5))
ax.text(5.0, 2.7, 'scar', ha='center', va='top', color=AMBER, fontsize=10, fontfamily='monospace')

# ── Panel 2: [t₀, t*) — limit point / geometric trace ────────────────────
ax = axes[1]
# Approach curves accumulating toward t* without reaching it
t_star_x = 7.5
t_star_y = 5.0

# Draw several approach trajectories, each getting closer but stopping short
for i, (start_y, color_alpha) in enumerate([(2.0, 0.3), (3.0, 0.45), (4.0, 0.6), (4.5, 0.75), (4.8, 0.88)]):
    # Curved approach
    t = np.linspace(0, 1, 100)
    x = 0.5 + (t_star_x - 0.5 - 0.3 - i*0.05) * t
    y_vals = start_y + (t_star_y - start_y) * t**1.5
    ax.plot(x, y_vals, color=INDIGO, alpha=color_alpha, lw=1.2)

# The limit point — marked but with open circle (not reached)
ax.plot(t_star_x, t_star_y, 'o', color=INDIGO, ms=8, markerfacecolor='none',
        markeredgewidth=2.0, alpha=0.95)
ax.plot(t_star_x, t_star_y, '+', color=INDIGO, ms=6, markeredgewidth=1.5, alpha=0.5)
ax.text(t_star_x, 2.7, 'limit point', ha='center', va='top', color=INDIGO, fontsize=10, fontfamily='monospace')

# ── Panel 3: [t₀, ∞) — nothing yet ──────────────────────────────────────
ax = axes[2]
# Arrow going off into an open horizon — no terminus visible
y_center = 5.0
# Draw trajectory
ax.annotate('', xy=(9.5, y_center), xytext=(0.5, y_center),
            arrowprops=dict(arrowstyle='->', color=TEAL, lw=1.8,
                           mutation_scale=20))
# Fading dots suggesting continuation
for xi, alpha in [(8.0, 0.8), (8.6, 0.5), (9.1, 0.25)]:
    ax.plot(xi, y_center, '.', color=TEAL, ms=5, alpha=alpha)

# A dashed 'not yet' marker at the right edge
ax.axvline(x=9.4, color=DIM, lw=1.0, linestyle='--', alpha=0.5)
ax.text(9.4, 6.8, '?', ha='center', color=DIM, fontsize=14, alpha=0.6, fontfamily='monospace')
ax.text(5.0, 2.7, 'nothing yet', ha='center', va='top', color=TEAL, fontsize=10, fontfamily='monospace')

# ── Panel 4: ∅ — derivation only ─────────────────────────────────────────
ax = axes[3]
# No geometric object — only a derivation visible (formula/inference)
# Draw a faint grid suggesting structure without content
for xi in np.linspace(1.0, 9.0, 9):
    ax.axvline(x=xi, color=DIM, lw=0.4, alpha=0.18)
for yi in np.linspace(1.0, 9.0, 9):
    ax.axhline(y=yi, color=DIM, lw=0.4, alpha=0.18)

# The 'derivation' — mathematical steps in dim text
lines = [
    ('no prior x\u2080', 5.0, 7.0),
    ('gap(t) = \u2205', 5.0, 5.8),
    ('trace = \u2205', 5.0, 4.7),
]
for txt, x, y in lines:
    ax.text(x, y, txt, ha='center', va='center', color=ROSE, fontsize=9.5,
            fontfamily='monospace', alpha=0.85)
ax.text(5.0, 2.7, 'derivation only', ha='center', va='top', color=ROSE, fontsize=10, fontfamily='monospace')

# ── Interval labels (top) ─────────────────────────────────────────────────
interval_labels = [
    ('[t₀, t₁]', AMBER),
    ('[t₀, t*)', INDIGO),
    ('[t₀, ∞)', TEAL),
    ('∅', ROSE),
]
for ax, (label, color) in zip(axes, interval_labels):
    ax.text(5.0, 9.2, label, ha='center', va='bottom', color=color,
            fontsize=13, fontfamily='monospace', fontweight='bold')

# ── Figure title ─────────────────────────────────────────────────────────
fig.text(0.5, 0.94, 'what absence leaves behind', ha='center', va='bottom',
         color=LIGHT, fontsize=14, fontfamily='monospace')
fig.text(0.5, 0.05, 'interval type → evidence structure', ha='center', va='top',
         color=DIM, fontsize=10, fontfamily='monospace')

plt.savefig('assets/evidence-types-2026-05-21.png', dpi=150, bbox_inches='tight',
            facecolor=BG, edgecolor='none')
print("saved.")
