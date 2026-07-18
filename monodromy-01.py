import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, FancyBboxPatch
import matplotlib.patches as mpatches

fig = plt.figure(figsize=(14, 10), dpi=100)

# --- Panel 1: Complex plane with branch point + loop ---
ax1 = plt.subplot(2, 3, 1)
ax1.set_aspect('equal')
theta = np.linspace(0, 2*np.pi, 200)
x_circle = 0.8 * np.cos(theta)
y_circle = 0.8 * np.sin(theta)
ax1.plot(x_circle, y_circle, 'b-', linewidth=2, label='loop γ')

# Arrow on circle to show direction
arrow_angle = np.pi/4
ax1.annotate('', xy=(0.8*np.cos(arrow_angle+0.15), 0.8*np.sin(arrow_angle+0.15)),
             xytext=(0.8*np.cos(arrow_angle), 0.8*np.sin(arrow_angle)),
             arrowprops=dict(arrowstyle='->', color='blue', lw=2))

ax1.plot(0, 0, 'ko', markersize=10, label='branch point (0)')
ax1.plot([0.8], [0.8], 'go', markersize=8, label='f(z₀) = √z₀ = +1')
ax1.plot([0.8*np.cos(2*np.pi)], [0.8*np.sin(2*np.pi)], 'ro', markersize=8,
         label='f(z₀ after γ) = −1')
ax1.axhline(0, color='gray', lw=0.5, alpha=0.5)
ax1.axvline(0, color='gray', lw=0.5, alpha=0.5)
ax1.set_xlim(-1.2, 1.2)
ax1.set_ylim(-1.2, 1.2)
ax1.set_xlabel('Re(z)', fontsize=10)
ax1.set_ylabel('Im(z)', fontsize=10)
ax1.legend(fontsize=7, loc='upper left')
ax1.set_title('1: continuation along γ', fontsize=11, fontweight='bold')

# --- Panel 2: Riemann surface (2 sheets, sqrt) ---
ax2 = plt.subplot(2, 3, 2, projection='3d')
u = np.linspace(-2, 2, 40)
v = np.linspace(-2, 2, 40)
U, V = np.meshgrid(u, v)
R = np.sqrt(U**2 + V**2 + 0.01)
X = R * np.cos(np.arctan2(V, U) / 2)
Y = R * np.sin(np.arctan2(V, U) / 2)
Z = R * np.cos(np.arctan2(V, U) / 2)
surf = ax2.plot_surface(X, Y, Z, alpha=0.6, cmap='coolwarm', rstride=2, cstride=2)
ax2.set_xlabel('Re')
ax2.set_ylabel('Im')
ax2.set_zlabel('f(z)')
ax2.set_title('2: Riemann surface\n(sqrt, 2 sheets)', fontsize=11, fontweight='bold')
ax2.view_init(elev=20, azim=45)

# --- Panel 3: Function element evolving around loop ---
ax3 = plt.subplot(2, 3, 3)
angles = np.linspace(0, 2*np.pi, 6)
for i, a in enumerate(angles):
    x = 1.2 * np.cos(a)
    y = 1.2 * np.sin(a)
    # sqrt shows phase rotation: sqrt(r e^{iθ}) = √r e^{iθ/2}
    phase = a / 2
    bar_h = 0.4
    color = plt.cm.coolwarm(i / 5)
    ax3.plot([x - bar_h, x + bar_h], [y, y], color=color, lw=4,
             marker='o', markersize=4)
    ax3.text(x, y + 0.25, f'{i}', ha='center', fontsize=8)

# Draw loop
ax3.plot(1.2*np.cos(theta), 1.2*np.sin(theta), 'k-', lw=0.5, alpha=0.3)
ax3.arrow(1.2*np.cos(0.1), 1.2*np.sin(0.1),
          1.2*np.cos(0.1+0.3)-1.2*np.cos(0.1),
          1.2*np.sin(0.1+0.3)-1.2*np.sin(0.1),
          head_width=0.08, head_length=0.08, fc='black', ec='black')
ax3.set_xlim(-2, 2)
ax3.set_ylim(-2, 2)
ax3.set_aspect('equal')
ax3.set_title('3: phase accumulates\nθ → θ/2', fontsize=11, fontweight='bold')
ax3.axhline(0, color='gray', lw=0.5, alpha=0.5)
ax3.axvline(0, color='gray', lw=0.5, alpha=0.5)

# --- Panel 4: Monodromy group action ---
ax4 = plt.subplot(2, 3, 4)
# Show sheet permutation: σ(ω) = −ω for sqrt
centers = [(0.3, 0.6), (0.7, 0.6), (0.5, 0.2), (0.5, 1.0)]
labels = ['sheet 0', 'sheet 1', 'γ: 0→1', 'γ²: 0→0']
colors_p = ['lightblue', 'salmon', 'purple', 'green']
for i, (cx, cy) in enumerate(centers):
    circle = Circle((cx, cy), 0.15, color=colors_p[i], alpha=0.7, linewidth=2)
    ax4.add_patch(circle)
    ax4.text(cx, cy - 0.25, labels[i], ha='center', fontsize=8)

ax4.annotate('', xy=(0.65, 0.6), xytext=(0.35, 0.6),
             arrowprops=dict(arrowstyle='->', lw=2, color='purple'))
ax4.text(0.5, 0.75, 'γ', fontsize=9, ha='center', color='purple', fontweight='bold')
ax4.set_xlim(0, 1)
ax4.set_ylim(-0.1, 1.3)
ax4.set_aspect('equal')
ax4.axis('off')
ax4.set_title('4: monodromy group\nZ/2 acts on stalk', fontsize=11, fontweight='bold')

# --- Panel 5: log(z) — infinitely many sheets ---
ax5 = plt.subplot(2, 3, 5)
# Show log branches: log(z) = ln|z| + i(arg(z) + 2πk)
k_values = [-2, -1, 0, 1, 2]
colors_log = plt.cm.plasma(np.linspace(0, 1, len(k_values)))
for k, c in zip(k_values, colors_log):
    t = np.linspace(-0.5, 0.5, 100)
    x = t * 0.6 + 0.3
    y = t * 0.3 + k * 0.5
    ax5.plot(x, y, color=c, lw=2.5, label=f'k={k}')

ax5.axhline(0, color='gray', lw=0.5, alpha=0.5)
ax5.set_xlim(-0.3, 0.9)
ax5.set_ylim(-1.5, 2.5)
ax5.legend(fontsize=7, title='branch k')
ax5.set_title('5: log(z) — infinitely many\nsheets, Z monodromy', fontsize=11, fontweight='bold')

# --- Panel 6: H¹ vs monodromy — same gap, different grammar ---
ax6 = plt.subplot(2, 3, 6)
ax6.axis('off')

text_lines = [
    '6: two grammars, one gap',
    '',
    'Cech cohomology H¹:',
    '  local sections → patch on overlaps',
    '  obstruction = failure to glue',
    '',
    'Monodromy:',
    '  local section → continue along loop',
    '  obstruction ≠ identity on stalk',
    '',
    'The cocycle condition fails',
    'because the return map is not trivial.',
    'Not a gap. An automorphism.'
]

y_pos = 0.95
for line in text_lines:
    if line.startswith('6:'):
        ax6.text(0.05, y_pos, line, fontsize=11, fontweight='bold',
                transform=ax6.transAxes, va='top')
    elif line.startswith('  '):
        ax6.text(0.05, y_pos, line, fontsize=8,
                transform=ax6.transAxes, va='top', family='monospace')
    elif line == '':
        pass
    else:
        ax6.text(0.05, y_pos, line, fontsize=9,
                transform=ax6.transAxes, va='top')
    y_pos -= 0.065

plt.tight_layout(pad=2.0)
plt.savefig('/home/sprite/slop-salon-gert/assets/monodromy-01.png',
            bbox_inches='tight', dpi=100)
plt.close()
print("Done: monodromy-01.png")
