#!/usr/bin/env python3
"""
Kolmogorov complexity as sheaf cohomology.

The gap |x| - K(x) is H^1 of a sheaf that has no global section.
Local compression (gzip) gives upper bounds; K(x) is the infimum of
all local bounds. The obstruction to finding a global section = the
uncomputable gap.

Four-panel diagram:
1. Sheaf on a site: local patches U_i with compression data
2. H^1 as the gap: local sections that don't glue
3. Gzip as local section, K(x) as global infimum
4. Berry phase / holonomy connection
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.3)

colors = {
    'bg': '#0a0e17',
    'panel': '#111827',
    'border': '#374151',
    'text': '#e5e7eb',
    'muted': '#9ca3af',
    'accent': '#60a5fa',
    'warm': '#f59e0b',
    'green': '#34d399',
    'red': '#f87171',
    'purple': '#a78bfa',
    'cyan': '#22d3ee',
}

def draw_panel(ax, title):
    ax.set_facecolor(colors['panel'])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.text(5, 7.5, title, fontsize=13, fontweight='bold',
            color=colors['text'], ha='center', family='monospace')
    # Title underline
    ax.plot([1.5, 8.5], [7.15, 7.15], color=colors['border'], lw=1)

# ========== Panel 1: The compression sheaf ==========
ax1 = fig.add_subplot(gs[0, 0])
draw_panel(ax1, "THE COMPRESSION SHEAF  F")

# Draw a "space" X as a large rounded rectangle
space = FancyBboxPatch((0.5, 0.5), 9, 5.5, boxstyle="round,pad=0.15",
                        edgecolor=colors['border'], facecolor=colors['bg'], lw=1.5)
ax1.add_patch(space)
ax1.text(5, 5.8, "X (the space of finite binary strings)",
         fontsize=8, color=colors['muted'], ha='center', family='monospace')

# Draw overlapping open sets U1, U2, U3
circles_data = [
    (2.5, 3.5, 1.8, colors['accent']),
    (5.5, 3.5, 1.8, colors['warm']),
    (4.0, 2.0, 1.8, colors['green']),
]
for cx, cy, r, c in circles_data:
    circ = Circle((cx, cy), r, edgecolor=c, facecolor=c, alpha=0.15, lw=1.5)
    ax1.add_patch(circ)

# Labels for patches
ax1.text(2.5, 2.0, "U₁", fontsize=11, color=colors['accent'],
         ha='center', fontweight='bold', family='monospace')
ax1.text(2.5, 2.5, "|U₁|", fontsize=7, color=colors['muted'],
         ha='center', family='monospace')
ax1.text(5.5, 2.0, "U₂", fontsize=11, color=colors['warm'],
         ha='center', fontweight='bold', family='monospace')
ax1.text(5.5, 2.5, "|U₂|", fontsize=7, color=colors['muted'],
         ha='center', family='monospace')
ax1.text(4.0, 0.7, "U₃", fontsize=11, color=colors['green'],
         ha='center', fontweight='bold', family='monospace')
ax1.text(4.0, 1.2, "|U₃|", fontsize=7, color=colors['muted'],
         ha='center', family='monospace')

# x in the intersection
ax1.plot(4.0, 3.2, 'o', color=colors['text'], markersize=8)
ax1.text(4.0, 4.2, "x", fontsize=11, color=colors['text'],
         ha='center', fontweight='bold', family='monospace')

# Arrow showing F(U_i) = compressed size
ax1.annotate("", xy=(7.5, 5.0), xytext=(6.5, 4.0),
             arrowprops=dict(arrowstyle='->', color=colors['accent'], lw=2))
ax1.text(7.5, 4.5, "F(Uᵢ) = |compressed|", fontsize=8,
         color=colors['text'], family='monospace')

# Bottom annotation
ax1.text(5, 0.2, "Each patch Uᵢ knows a local compression of x",
         fontsize=7.5, color=colors['muted'], ha='center', style='italic')

# ========== Panel 2: H¹ as the gap ==========
ax2 = fig.add_subplot(gs[0, 1])
draw_panel(ax2, "H¹(X, F) = |x| − K(x)")

# Show two local sections that don't glue
# Upper section
for i, (label, x0, c) in enumerate([("s₁ (U₁)", 2.5, colors['accent']),
                                      ("s₂ (U₂)", 6.5, colors['warm'])]):
    rect = FancyBboxPatch((x0-0.8, 4.5), 1.6, 2, boxstyle="round,pad=0.1",
                          edgecolor=c, facecolor=c, alpha=0.15, lw=2)
    ax2.add_patch(rect)
    ax2.text(x0, 5.9, label, fontsize=9, color=c,
             ha='center', fontweight='bold', family='monospace')
    ax2.text(x0, 5.4, r"|s₁| = 7.2", fontsize=7.5,
             color=colors['muted'], ha='center', family='monospace')

# Intersection — the sections disagree
inter_x = 4.5
interp = FancyBboxPatch((inter_x-0.6, 4.0), 1.2, 1.2, boxstyle="round,pad=0.08",
                        edgecolor=colors['purple'], facecolor=colors['purple'], alpha=0.1, lw=2)
ax2.add_patch(interp)
ax2.text(inter_x, 5.3, "U₁ ∩ U₂", fontsize=8,
         color=colors['purple'], ha='center', fontweight='bold', family='monospace')

# The mismatch
ax2.annotate("", xy=(3.7, 4.6), xytext=(4.0, 4.6),
             arrowprops=dict(arrowstyle='<->', color=colors['red'], lw=2))
ax2.annotate("", xy=(5.0, 4.6), xytext=(4.7, 4.6),
             arrowprops=dict(arrowstyle='<->', color=colors['red'], lw=2))
ax2.text(inter_x, 3.7, r"disagreement = gap", fontsize=9,
         color=colors['red'], ha='center', fontweight='bold', family='monospace')

# Bottom: K(x) is the infimum
rect_bottom = FancyBboxPatch((1.5, 1.8), 7, 1.2, boxstyle="round,pad=0.1",
                              edgecolor=colors['green'], facecolor=colors['green'], alpha=0.1, lw=2)
ax2.add_patch(rect_bottom)
ax2.text(5, 2.5, r"K(x) = inf { |s_i| : {s_i} local sections }",
         fontsize=9, color=colors['green'], ha='center', family='monospace')

# The uncomputable
ax2.text(5, 0.8, "No global section exists → H¹ ≠ 0 → K(x) uncomputable",
         fontsize=8, color=colors['text'], ha='center', family='monospace')

ax2.text(5, 0.2, "The obstruction class IS the gap |x| − K(x)",
         fontsize=7.5, color=colors['muted'], ha='center', style='italic')

# ========== Panel 3: Gzip as local section, K(x) as limit ==========
ax3 = fig.add_subplot(gs[1, 0])
draw_panel(ax3, "GZIP COMPUTES FROM BELOW")

# Show convergence from below
x_vals = np.linspace(0.1, 1.0, 50)
gzip_curve = 0.95 * (1 - 0.5 * np.exp(-5 * x_vals)) + 0.05 * x_vals
k_bound = 0.42  # K(x)/|x| ≈ ln(1.5)/ln(2) ≈ 0.585 → inverse ≈ 0.42 for this framing
# Actually let's think about this differently.
# K(x) ≤ |x| + c. gzip gives upper bounds. K(x) is the lim inf of all gzip bounds.
# Plot: compression ratio |gzip(x)| / |x| vs structure content

structure = np.linspace(0, 1, 200)
# Periodic strings: compress nearly to 0
gzip_periodic = 0.02 + 0.01 * np.random.randn(200) * 0
# Random strings: stay near 1.0
gzip_random = 0.95 + 0.02 * np.random.randn(200) * 0
# Structured strings (pi, Fibonacci): intermediate
gzip_structured = 0.15 + 0.3 * structure + 0.05 * np.random.randn(200)

# Clean version without noise
gzip_periodic_clean = np.full(50, 0.03)
gzip_random_clean = np.full(50, 0.95)
gzip_structured_clean = 0.1 + 0.7 * np.linspace(0, 1, 50)

# Plot as scatter-like bars
np.random.seed(42)
for i in range(50):
    ax3.plot([i, i], [gzip_periodic_clean[i], 0.08], color=colors['accent'], lw=1.5, alpha=0.7)
for i in range(50):
    ax3.plot([i+50, i+50], [gzip_structured_clean[i], 0.15], color=colors['warm'], lw=1.5, alpha=0.7)
for i in range(50):
    ax3.plot([i+100, i+100], [gzip_random_clean[i], 0.9], color=colors['red'], lw=1.5, alpha=0.7)

# K(x) lower bound
ax3.axhline(y=0.42, color=colors['green'], linestyle='--', lw=2.5, label=r'K(x)/|x| lower bound')

ax3.set_ylabel("compression ratio  |gzip(x)| / |x|", fontsize=9, color=colors['text'], family='monospace')
ax3.set_xlabel("string structure (periodic → random)", fontsize=9, color=colors['muted'], family='monospace')
ax3.set_ylim(0, 1.05)
ax3.set_xlim(-2, 152)
ax3.set_xticks([24, 74, 124])
ax3.set_xticklabels(['periodic', 'structured', 'random'], fontsize=7, color=colors['muted'])
ax3.tick_params(axis='y', colors=colors['muted'], labelsize=7)

# Mark the gap
ax3.fill_between([-2, 152], 0.42, 0.03, alpha=0.08, color=colors['red'],
                  label='H¹ ≠ 0')
ax3.text(75, 0.22, 'H¹(X,F) ≠ 0\nthe gap is uncomputable',
         fontsize=8, color=colors['red'], ha='center', family='monospace')
ax3.legend(loc='upper right', fontsize=7, facecolor=colors['panel'],
           edgecolor=colors['border'], labelcolor=colors['text'])

# ========== Panel 4: Berry phase / holonomy connection ==========
ax4 = fig.add_subplot(gs[1, 1])
draw_panel(ax4, "HOLONOMY AS THE RETURN MAP")

# Draw a loop in parameter space (the space where sections live)
theta = np.linspace(0, 2*np.pi, 100)
radius = 2.5
cx, cy = 5, 4
x_circle = cx + radius * np.cos(theta)
y_circle = cy + radius * np.sin(theta)

# Draw the loop
ax4.plot(x_circle, y_circle, color=colors['accent'], lw=2.5, alpha=0.8)

# Mark base point
ax4.plot(cx + radius, cy, 'o', color=colors['green'], markersize=10)
ax4.text(cx + radius + 0.3, cy - 0.3, "x", fontsize=10,
         color=colors['green'], fontweight='bold', family='monospace')

# Draw a section along the path
for i in [0, 25, 50, 75]:
    angle = theta[i]
    px = cx + radius * np.cos(angle)
    py = cy + radius * np.sin(angle)
    # Section vector (pointing inward)
    dx = -np.cos(angle) * 0.6
    dy = -np.sin(angle) * 0.6
    ax4.annotate("", xy=(px + dx, py + dy), xytext=(px, py),
                 arrowprops=dict(arrowstyle='->', color=colors['purple'], lw=1.5))

# Show holonomy: the section doesn't return to itself
start_angle = 0
end_angle = 2 * np.pi - 0.15
px_start = cx + radius * np.cos(start_angle)
py_start = cy + radius * np.sin(start_angle)
px_end = cx + radius * np.cos(end_angle)
py_end = cy + radius * np.sin(end_angle)

ax4.plot([px_start, px_end], [py_start, py_end], color=colors['red'],
         lw=3, linestyle='--', alpha=0.8)
ax4.text(7.8, 2.5, "holonomy\nphase", fontsize=8, color=colors['red'],
         ha='center', fontweight='bold', family='monospace')

# Annotations
ax4.text(5, 7.5, "Berry phase = holonomy of the compression sheaf",
         fontsize=8, color=colors['text'], ha='center', family='monospace')
ax4.text(5, 1.2, "Parallel transport around the loop", fontsize=8,
         color=colors['muted'], ha='center', style='italic')
ax4.text(5, 0.5, r"detuning = ∮ ω = holonomy ∈ H¹",
         fontsize=8, color=colors['green'], ha='center', family='monospace')

ax4.set_xlim(1, 9)
ax4.set_ylim(-0.5, 7.5)

# Save
fig.savefig('/home/sprite/slop-salon-gert/assets/kolmogorov-04.png',
            dpi=150, bbox_inches='tight', facecolor=colors['bg'])
plt.close(fig)
print("Created kolmogorov-04.png")
