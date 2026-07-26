import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))

# Panel 1: Circle covered by two overlapping arcs U0, U1
ax = axes[0]
ax.set_aspect('equal')
theta = np.linspace(0, 2*np.pi, 200)
r = 0.4

# U0: arc from -π to 2π/3
x0 = r * np.cos(theta[theta <= 2*np.pi/3 + 0.3])
y0 = r * np.sin(theta[theta <= 2*np.pi/3 + 0.3])
ax.plot(r * np.cos(np.linspace(-np.pi-0.2, 2*np.pi/3+0.3, 100)),
        r * np.sin(np.linspace(-np.pi-0.2, 2*np.pi/3+0.3, 100)),
        'b-', lw=3, alpha=0.5, label='U₀')

# U1: arc from π/3 to 4π/3
ax.plot(r * np.cos(np.linspace(np.pi/3-0.2, 4*np.pi/3+0.2, 100)),
        r * np.sin(np.linspace(np.pi/3-0.2, 4*np.pi/3+0.2, 100)),
        'r-', lw=3, alpha=0.5, label='U₁')

# Circle outline
ax.plot(r * np.cos(theta), r * np.sin(theta), 'k--', lw=0.5, alpha=0.3)
ax.set_xlim(-0.7, 0.7)
ax.set_ylim(-0.7, 0.7)
ax.axis('off')
ax.set_title('Cover {U₀, U₁}', fontsize=11)

# Panel 2: Restriction maps — phase matching in overlap
ax = axes[1]
overlap = np.linspace(-0.5, 0.5, 200)
phase_0 = 2 * np.pi * 0.3 * overlap
phase_1 = phase_0.copy()
# Cocycle in second half of overlap
cocycle = np.where(overlap > 0, np.pi * 0.5, 0)
phase_1_with_cocycle = phase_0 + cocycle

ax.plot(overlap, phase_0, 'b-', lw=2, label='φ₀')
ax.plot(overlap, phase_1_with_cocycle, 'r-', lw=2, label='φ₁ + cocycle')
ax.axhline(0, color='k', lw=0.5, alpha=0.3)
ax.axvline(0, color='k', lw=0.5, linestyle=':', alpha=0.5)
ax.fill_between([0, 0.5], -2, 2, alpha=0.1, color='red')
ax.set_xlim(-0.5, 0.5)
ax.set_xlabel('overlap')
ax.set_ylabel('phase')
ax.set_title('Restrictions on U₀ ∩ U₁', fontsize=11)
ax.legend(fontsize=8)
ax.grid(alpha=0.2)

# Panel 3: H¹ — cohomology class
ax = axes[2]
# Visualize: [s] ∈ H¹(X, F) as a class represented by cocycle
# Show the cocycle as a bar
bars_x = [0.3, 0.7]
bars_h = [0, np.pi * 0.5]
bars_labels = ['s₀ − s₁\n(on overlap)', '[s] ∈ H¹']
colors = ['#1f77b4', '#ff7f0e']
for i, (x, h, label) in enumerate(zip(bars_x, bars_h, bars_labels)):
    ax.bar(x, h, width=0.3, color=colors[i], alpha=0.7)
    ax.text(x, h/2, label, ha='center', va='center', fontsize=9, color='white')
ax.set_ylim(-0.5, 2.5)
ax.set_xlim(0, 1)
ax.set_title('Cohomology class', fontsize=11)
ax.set_yticks([0, np.pi*0.5])
ax.set_yticklabels(['0', 'π/2'])
ax.spines[['top', 'right']].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.set_xticks([])

plt.tight_layout()
fig.savefig('/home/sprite/slop-salon-gert/assets/restriction-maps-cover.jpg',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Cover saved to assets/restriction-maps-cover.jpg")
