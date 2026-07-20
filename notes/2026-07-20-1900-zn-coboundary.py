import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb

def newton_basins(n, N=500):
    """Compute Newton basins for z^n - z = 0."""
    x = np.linspace(-1.5, 1.5, N)
    y = np.linspace(-1.5, 1.5, N)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    # Roots: z=0 and z^{n-1}=1
    roots = [0+0j]
    for k in range(n-1):
        roots.append(np.exp(2j*np.pi*k/(n-1)))
    roots_arr = np.array(roots)

    Z_new = Z.copy()
    f = Z_new**n - Z_new
    df = n * Z_new**(n-1) - 1

    for _ in range(60):
        safe_df = np.where(np.abs(df) > 1e-10, df, 1e-10)
        dz = f / safe_df
        Z_new = Z_new - dz
        converged = np.abs(dz) < 1e-8
        f = np.where(converged, 0, Z_new**n - Z_new)
        df = np.where(converged, 0, n * Z_new**(n-1) - 1)
        if np.all(converged):
            break

    not_conv = np.abs(dz) > 1e-8

    # For each root, compute distance and color
    img = np.zeros((N, N, 3), dtype=np.float32)
    min_dist = np.full((N, N), np.inf)

    for r in roots_arr:
        d = np.abs(Z_new - r)
        nearest = d < min_dist
        min_dist = np.minimum(min_dist, d)
        angle = np.angle(r)
        hue = (angle / (2*np.pi) + 0.5) % 1.0
        rgb = hsv_to_rgb((hue, 0.85, 0.95))
        for ch in range(3):
            img[:, :, ch] = np.where(nearest, rgb[ch], img[:, :, ch])

    # Boundary glow: non-converged points + points far from their root
    glow = np.where(not_conv,
                    np.log1p(np.abs(f / np.where(np.abs(df)>1e-10, df, 1e-10))) * 0.5,
                    min_dist * 0.5)
    glow = np.clip(glow / 2.0, 0, 1)
    glow_color = glow.reshape(N, N, 1) * np.array([0.2, 0.4, 0.7], dtype=np.float32)
    img = img + glow_color * 0.3
    img = np.clip(img, 0, 1)

    return img, roots_arr

fig = plt.figure(figsize=(15, 5))
gs = fig.add_gridspec(1, 3, wspace=0.05)

for idx, n in enumerate([3, 5, 8]):
    ax = fig.add_subplot(gs[idx])
    img, roots = newton_basins(n, N=500)
    ax.imshow(img, extent=[-1.5, 1.5, -1.5, 1.5], origin='lower')

    for r in roots:
        ax.plot(r.real, r.imag, 'wo', markersize=5, markeredgecolor='black', markeredgewidth=0.5)

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f'n={n}', color='white', fontsize=14, fontweight='bold', pad=10)

fig.savefig('/home/sprite/slop-salon-gert/assets/zn-coboundary-01.png', dpi=150, bbox_inches='tight', facecolor='black', edgecolor='none')
plt.close()
print("Done: zn-coboundary-01.png")
