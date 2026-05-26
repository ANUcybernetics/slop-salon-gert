"""
Deep zoom of the z^3 - 1 Newton fractal basin boundary.

Deep zoom centered slightly offset from a star junction, so the fractal
boundary with recursive star structure appears as a thin structure near
one edge, while thick colored basin fills the rest.

Uses multiple passes to increase detail without excessive iteration count.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.ndimage import zoom

AMBER = np.array([0.95, 0.62, 0.10])
GREEN = np.array([0.22, 0.78, 0.35])
BLUE  = np.array([0.18, 0.38, 0.92])
DARK  = np.array([0.03, 0.03, 0.05])

def compute_newton(xmin, xmax, ymin, ymax, res, max_iter=80, tol=1e-8):
    x = np.linspace(xmin, xmax, res)
    y = np.linspace(ymin, ymax, res)
    X, Y = np.meshgrid(x, y, indexing='ij')
    Z = X + 1j * Y
    roots = np.array([1.0,
                      np.exp(2j * np.pi / 3),
                      np.exp(4j * np.pi / 3)])
    basin = np.full((res, res), -1, dtype=np.int16)
    iters = np.zeros((res, res), dtype=np.int32)
    Z_iter = Z.copy()
    converged = np.zeros((res, res), dtype=bool)
    for i in range(max_iter):
        denom = 3 * Z_iter**2
        safe = np.abs(denom) > 1e-12
        Z_new = np.where(safe, Z_iter - (Z_iter**3 - 1) / denom, Z_iter)
        for j, root in enumerate(roots):
            close = (~converged) & (np.abs(Z_new - root) < tol)
            basin[close] = j
            iters[close] = i
            converged |= close
        Z_iter = np.where(converged, Z_iter, Z_new)
        if converged.all():
            break
    return basin, iters, converged

def build_image(basin, iters, MAX_ITER, palette):
    h, w = basin.shape
    img = np.full((h, w, 3), DARK)
    for j in range(3):
        mask = (basin == j)
        col = palette[j]
        brightness = 0.12 + 0.88 * (iters / MAX_ITER) ** 0.5
        img[mask] = col * brightness[mask, np.newaxis]
    return img

# --- Strategy ---
# Zoom level: 2^17 from full view
# Full span = 3.0, zoom_field = 3.0 / 2^17 ≈ 2.27e-5
# At 1200px: pixel_scale = 2.27e-5 / 1200 = 1.89e-8
# Offset: 25% of half-width toward z=1 (amber basin)
# This puts the origin (junction) at 25% from the left edge,
# so the fractal boundary is visible near that position,
# while thick basin fills ~75% of the frame.

ZOOM_LEVEL = 17
FULL_SPAN = 3.0
ZOOM_FIELD = FULL_SPAN / (2 ** ZOOM_LEVEL)
ZOOM_RES = 1200
PIXEL_SCALE = ZOOM_FIELD / ZOOM_RES

print(f"Zoom level: 2^{ZOOM_LEVEL}")
print(f"Zoom field: {ZOOM_FIELD:.3e}")
print(f"Pixel scale: {PIXEL_SCALE:.3e}")

HALF = ZOOM_FIELD / 2
OFF_FRAC = 0.25  # 25% offset
JX_off = OFF_FRAC * HALF  # origin at 25% from left edge
JY_off = 0.0

xmin = JX_off - HALF
xmax = JX_off + HALF
ymin = JY_off - HALF
ymax = JY_off + HALF

print(f"Zoom region: [{xmin:.3e}, {xmax:.3e}] x [{ymin:.3e}, {ymax:.3e}]")
print(f"Origin (junction) at x={JX_off:.3e}, which is pixel {OFF_FRAC*ZOOM_RES:.0f} of {ZOOM_RES}")

# --- Compute ---
print("\nComputing deep zoom (may take 1-2 minutes)...")
basin, iters, conv = compute_newton(xmin, xmax, ymin, ymax, ZOOM_RES, max_iter=100)

n_conv = conv.sum()
print(f"Convergence: {100*n_conv/ZOOM_RES**2:.1f}%")
for j, name in enumerate(['amber', 'green', 'blue']):
    count = (basin == j).sum()
    print(f"  Basin {j} ({name}): {100*count/ZOOM_RES**2:.1f}%")

img_zoom = build_image(basin, iters, 100, [AMBER, GREEN, BLUE])

# --- Resize to output and save ---
print("Resizing to 1500x1500...")
OUT_RES = 1500
img_out = zoom(img_zoom, (OUT_RES / ZOOM_RES, OUT_RES / ZOOM_RES, 1), order=2, mode='reflect')
img_out = np.clip(img_out, 0, 1)

out_path = '/home/sprite/slop-salon-gert/assets/deep-basin-julia-2026-05-27.png'
fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
ax.imshow(img_out, origin='upper', vmin=0, vmax=1)
ax.axis('off')
plt.tight_layout(pad=0)
plt.savefig(out_path, dpi=150, bbox_inches='tight', pad_inches=0, facecolor='black')
plt.close(fig)
print(f"Saved: {out_path}")
print(f"Pixel scale: {PIXEL_SCALE:.3e}")
