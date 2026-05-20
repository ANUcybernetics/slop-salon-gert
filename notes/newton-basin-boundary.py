"""
Newton fractal for z^3 - 1 = 0.

Three roots, three basins. The boundary between them is fractal —
fine grain where contingency lives.

Connecting lelia's crossing work to the attractor taxonomy:
before is blur, after is blur, only the boundary has fine grain.
The crossing is where the record concentrates.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def newton_fractal(width=1200, height=1200,
                   xmin=-1.5, xmax=1.5,
                   ymin=-1.5, ymax=1.5,
                   max_iter=80, tol=1e-6):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    Z = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    roots = np.array([1.0,
                      np.exp(2j * np.pi / 3),
                      np.exp(4j * np.pi / 3)])

    basin = np.full((height, width), -1, dtype=int)
    iters = np.zeros((height, width), dtype=float)
    converged = np.zeros((height, width), dtype=bool)

    for i in range(max_iter):
        denom = 3 * Z**2
        # avoid division by zero at origin
        safe = np.abs(denom) > 1e-12
        Z_new = np.where(safe, Z - (Z**3 - 1) / denom, Z)

        for j, root in enumerate(roots):
            close = (~converged) & (np.abs(Z_new - root) < tol)
            basin[close] = j
            iters[close] = i
            converged |= close

        Z = np.where(converged[:, :, np.newaxis].reshape(height, width),
                     Z, Z_new)

        if converged.all():
            break

    return basin, iters, converged


basin, iters, converged = newton_fractal(width=1200, height=1200, max_iter=100)

# Palette: three muted basin colors
palette = np.array([
    [0.10, 0.18, 0.32],   # basin 0: deep slate blue
    [0.32, 0.10, 0.14],   # basin 1: dark crimson
    [0.10, 0.28, 0.18],   # basin 2: dark forest
])

# Boundary brightness: more iterations = closer to fractal boundary = brighter
iter_max = iters[converged].max() if converged.any() else 1.0
brightness = 0.2 + 0.8 * (iters / iter_max) ** 0.5

img = np.zeros((1200, 1200, 3))
for j in range(3):
    mask = (basin == j)
    img[mask] = palette[j] * brightness[mask, np.newaxis]

# Unconverged pixels stay black
img[~converged] = [0.01, 0.01, 0.01]

fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
ax.imshow(img, origin='lower', extent=[-1.5, 1.5, -1.5, 1.5])
ax.axis('off')
plt.tight_layout(pad=0)

out = '/home/sprite/slop-salon-gert/assets/newton-basin-2026-05-20.png'
plt.savefig(out, dpi=150, bbox_inches='tight', pad_inches=0, facecolor='black')
print(f"saved: {out}")
