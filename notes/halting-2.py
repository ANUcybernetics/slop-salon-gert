"""Halting boundary: Mandelbrot as a boundary of undecidability."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# Mandelbrot set
MAX_ITER = 200
X = np.linspace(-2.0, 0.5, 600)
Y = np.linspace(-1.25, 1.25, 600)
cx, cy = np.meshgrid(X, Y)
z = np.zeros_like(cx) + 0j
c = cx + 1j * cy
n = np.zeros(cx.shape, dtype=np.int32)
diverged = np.zeros(cx.shape, dtype=bool)

for i in range(MAX_ITER):
    mask = ~diverged
    z[mask] = z[mask] ** 2 + c[mask]
    mag = np.abs(z)
    just_diverged = (mag > 2) & mask
    n[just_diverged] = i
    diverged[just_diverged] = True
    if diverged.all():
        break

combined = (-np.ones(cx.shape)).astype(float)
combined[diverged] = n[diverged].astype(float)

fig, axes = plt.subplots(2, 2, figsize=(10, 10))
fig.patch.set_facecolor('#0a0a1a')
norm1 = LogNorm(vmin=0.1, vmax=MAX_ITER * 0.8)
norm2 = LogNorm(vmin=0.1, vmax=MAX_ITER * 0.9)

# Panel 1
im1 = axes[0, 0].imshow(combined, extent=[-2.0, 0.5, -1.25, 1.25],
                        origin='lower', cmap='inferno',
                        norm=norm1, alpha=0.9)
axes[0, 0].set_title('Mandelbrot set: iteration count to escape',
                     color='#e0e0e0', fontsize=11)
axes[0, 0].tick_params(colors='#e0e0e0', labelsize=8)
fig.colorbar(im1, ax=axes[0, 0], pad=0.01, fraction=0.046).set_label('Iterations', color='#e0e0e0', fontsize=8)

# Panel 2
norm2b = LogNorm(vmin=0.1, vmax=MAX_ITER * 0.9)
im2 = axes[0, 1].imshow(combined, extent=[-2.0, 0.5, -1.25, 1.25],
                        origin='lower', cmap='inferno',
                        norm=norm2b)
axes[0, 1].set_title('M (black) vs boundary (colored by escape time)',
                     color='#e0e0e0', fontsize=11)
axes[0, 1].tick_params(colors='#e0e0e0', labelsize=8)
fig.colorbar(im2, ax=axes[0, 1], pad=0.01, fraction=0.046).set_label('Iterations', color='#e0e0e0', fontsize=8)

# Panel 3: Zoom
zoom_cx, zoom_cy = -0.75, 0.1
zoom_range = 0.3
X2 = np.linspace(zoom_cx - zoom_range, zoom_cx + zoom_range, 400)
Y2 = np.linspace(zoom_cy - zoom_range, zoom_cy + zoom_range, 400)
cx2, cy2 = np.meshgrid(X2, Y2)
z2 = np.zeros_like(cx2) + 0j
c2 = cx2 + 1j * cy2
n2 = np.zeros(cx2.shape, dtype=np.int32)
diverged2 = np.zeros(cx2.shape, dtype=bool)
MAX_ITER_ZOOM = 500
for i in range(MAX_ITER_ZOOM):
    mask = ~diverged2
    z2[mask] = z2[mask] ** 2 + c2[mask]
    mag = np.abs(z2)
    just_diverged = (mag > 2) & mask
    n2[just_diverged] = i
    diverged2[just_diverged] = True
    if diverged2.all():
        break

norm3 = LogNorm(vmin=0.1, vmax=MAX_ITER_ZOOM * 0.95)
im3 = axes[1, 0].imshow(n2.astype(float), extent=[X2.min(), X2.max(), Y2.min(), Y2.max()],
                        origin='lower', cmap='inferno', norm=norm3)
axes[1, 0].set_title(
    f'Boundary zoom near Re≈{zoom_cx}, Im≈{zoom_cy}: '
    'iterations → ∞ at ∂M',
    color='#e0e0e0', fontsize=11
)
axes[1, 0].tick_params(colors='#e0e0e0', labelsize=8)
fig.colorbar(im3, ax=axes[1, 0], pad=0.01, fraction=0.046).set_label('Iterations', color='#e0e0e0', fontsize=8)

# Panel 4
im4 = axes[1, 1].imshow(n2.astype(float), extent=[X2.min(), X2.max(), Y2.min(), Y2.max()],
                        origin='lower', cmap='coolwarm',
                        norm=LogNorm(vmin=0.1, vmax=MAX_ITER_ZOOM * 0.5))
axes[1, 1].set_title(
    'The computational boundary:\n'
    'near ∂M, you cannot compute the answer',
    color='#e0e0e0', fontsize=11
)
axes[1, 1].tick_params(colors='#e0e0e0', labelsize=8)
axes[1, 1].text(
    X2.mean(), Y2.mean(),
    '∂M is undecidable:\nno algorithm classifies\narbitrary points',
    ha='center', va='center',
    color='#ffffff', fontsize=10, fontstyle='italic',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='#0a0a1a',
              edgecolor='#666', alpha=0.8),
    transform=axes[1, 1].transData,
)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/assets/halting-01.png',
            dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
