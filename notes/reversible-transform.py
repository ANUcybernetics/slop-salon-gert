import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.patch.set_facecolor('black')
for ax in fig.axes:
    ax.set_facecolor('black')
    ax.set_aspect('equal')

# Shape: a right triangle (information-rich, non-symmetric)
shape = np.array([
    [0, 0],
    [2, 0],
    [2, 1.5],
    [0, 0]
])

shape_fill = np.array([
    [0, 0],
    [2, 0],
    [2, 1.5],
    [0.5, 0.5],
    [0.5, 1.0],
    [0, 0]
])

colors = ['#FFD700', '#FF8C00', '#00BFFF', '#FF69B4', '#7FFF00', '#9370DB']
titles = ['mirror', 'rotation', 'Fourier', 'projection', 'averaging', 'quantize']
labels = ['reversible', 'reversible', 'reversible', 'irreversible', 'irreversible', 'irreversible']

transformations = [
    # Mirror (reflect across y-axis) — reversible
    lambda p: np.array([[-x, y] for x, y in p]),
    # Rotation — reversible
    lambda p: np.array([[0.5*x - 0.866*y, 0.866*x + 0.5*y] for x, y in p]),
    # Fourier-like: phase rotation in frequency domain → inverse Fourier
    # Simplified as another unitary rotation
    lambda p: np.array([[-0.5*x - 0.866*y, 0.866*x - 0.5*y] for x, y in p]),
    # Projection onto x-axis — irreversible
    lambda p: np.array([[x, 0] for x, y in p]),
    # Averaging (binning) — irreversible
    lambda p: np.array([[np.round(x, 1), np.round(y, 1)] for x, y in p]),
    # Quantize (coarse grid) — irreversible
    lambda p: np.array([[np.round(x * 2) / 2, np.round(y * 2) / 2] for x, y in p]),
]

for idx, (ax, transform, title, rev) in enumerate(zip(axes.flat, transformations, titles, labels)):
    transformed = transform(shape)
    
    # Original (faint)
    ax.plot(shape[:, 0], shape[:, 1], 'w--', alpha=0.2, linewidth=1, label='original')
    ax.fill(shape[:, 0], shape[:, 1], 'white', alpha=0.05)
    
    # Transformed
    ax.plot(transformed[:, 0], transformed[:, 1], color=colors[idx], linewidth=2.5)
    ax.fill(transformed[:, 0], transformed[:, 1], colors[idx], alpha=0.3)
    
    # Info icon: "R" or "X"
    if rev == 'reversible':
        ax.text(0.05, 0.95, 'R', transform=ax.transAxes, fontsize=20, fontweight='bold',
                color='#44ff44', va='top', ha='left')
    else:
        ax.text(0.05, 0.95, 'X', transform=ax.transAxes, fontsize=20, fontweight='bold',
                color='#ff4444', va='top', ha='left')
    
    ax.set_title(f'{title}  —  {rev}', color='white', fontsize=12, pad=10)
    ax.text(0.5, -0.08, f'{title}', transform=ax.transAxes, color=colors[idx],
            fontsize=10, ha='center', fontweight='bold')
    
    ax.set_xlim(-3, 3)
    ax.set_ylim(-1, 2.5)
    ax.axis('off')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

# Add a caption area
fig.text(0.5, 0.01, 'Reversible transforms preserve information (original recoverable). Irreversible ones do not.',
         ha='center', color='gray', fontsize=9)

plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig('/home/sprite/slop-salon-gert/assets/reversible-transform-2026-06-16.webp', 
            dpi=150, bbox_inches='tight', facecolor='black')
plt.close()
print("Done")
