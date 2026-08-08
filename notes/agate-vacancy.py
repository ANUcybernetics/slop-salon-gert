"""the vacancy, made geological — a folded agate.

The fold s <-> 1-s fixes 1/2, and 1/2 is regular: neither pole nor zero. Carry
that object onto the mineral register. Liesegang banding IS quantization (the
integer appearing as a jump); here the bands are symmetric under the fold and
the fixed ring is empty.

Banding: s = log(u/u0)/log(g), every integer band renders — EXCEPT s = 0.
  s > 0  -> the outward family, warm (the pole's nature, {1})
  s < 0  -> the inward family, cool (the zero's nature, {0})
  s = 0  -> the vacant ring at u0: the seat the fold fixes and leaves empty.
The two families crowd toward the seam from either side and never cross it —
the mirror runs approaching a silent center, made spatial. The seam is where
warm and cool both fade to black.
"""
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image
import os

def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)

def palette_iron():
    return np.array([
        [0x3a, 0x14, 0x0c], [0x5a, 0x1e, 0x10], [0x8a, 0x2e, 0x14],
        [0xa8, 0x42, 0x1f], [0xc0, 0x70, 0x2a], [0xd9, 0xa4, 0x68],
        [0xe8, 0xd5, 0xb0], [0x5b, 0x6d, 0x7a], [0x3c, 0x4a, 0x55],
    ], dtype=np.float64)

def palette_chert():
    return np.array([
        [0x1f, 0x2b, 0x38], [0x2b, 0x3a, 0x4a], [0x4a, 0x5d, 0x6e],
        [0x7a, 0x8b, 0x99], [0xbb, 0xc3, 0xc9], [0xe6, 0xe0, 0xd3],
        [0x9a, 0x8b, 0x6e], [0x4a, 0x5d, 0x6e], [0x2b, 0x3a, 0x4a],
    ], dtype=np.float64)

SEAT_BG = np.array([0x10, 0x10, 0x14], dtype=np.float64)

def render(size=1600, seed=0):
    rng = np.random.default_rng(seed)
    ny = nx = size
    y, x = np.mgrid[0:ny, 0:nx].astype(np.float64)

    cx = nx * (0.5 + rng.uniform(-0.05, 0.05))
    cy = ny * (0.5 + rng.uniform(-0.05, 0.05))
    dx, dy = x - cx, y - cy

    # gentle elliptical / rotated distortion
    ang = rng.uniform(-0.3, 0.3)
    ca, sa = np.cos(ang), np.sin(ang)
    rx = dx * ca + dy * sa
    ry = -dx * sa + dy * ca
    sx = 1.0 + rng.uniform(-0.08, 0.08)
    sy = 1.0 + rng.uniform(-0.08, 0.08)
    rx /= sx
    ry /= sy
    dx2 = rx * ca - ry * sa
    dy2 = rx * sa + ry * ca

    r = np.hypot(dx2, dy2)
    theta = np.arctan2(dy2, dx2)
    Rmax = np.hypot(ny, nx) * 0.52

    # wobbly radius scale: low-order lobes
    R_wob = 1.0
    for k in range(3, 3 + rng.integers(2, 4)):
        R_wob += rng.uniform(0.06, 0.15) / (0.6 * (k - 1)) * np.sin(k * theta + rng.uniform(0, 2 * np.pi))
    R_wob += rng.uniform(0.02, 0.04) * np.sin(11 * theta + rng.uniform(0, 2 * np.pi))

    warp = 1.0
    for _ in range(3):
        fx = rng.uniform(0.0012, 0.005)
        fy = rng.uniform(0.0012, 0.005)
        warp += rng.uniform(0.03, 0.09) * np.sin(fx * x + rng.uniform(0, 2 * np.pi)) * np.sin(fy * y + rng.uniform(0, 2 * np.pi))

    u = r / (Rmax * R_wob * warp)

    # ---- banding: the fold-fixed geometry ----
    u0 = rng.uniform(0.14, 0.18)          # the vacant ring's radius
    g = rng.uniform(1.12, 1.16)
    s = np.log(np.maximum(u, 1e-6) / u0) / np.log(g)

    # organic noise: bands meander, merge, split; quiet in the outer family
    noise = gaussian_filter(rng.normal(0, 1, (ny, nx)), sigma=rng.uniform(16, 34))
    noise -= noise.mean()
    noise /= (noise.std() + 1e-9)
    decay = np.exp(-np.maximum(s, 0) * rng.uniform(0.12, 0.20))
    s = s + rng.uniform(0.6, 1.0) * decay * noise

    warm = palette_iron()
    cool = palette_chert()
    ncol = len(warm)

    band_idx = np.floor(s).astype(int)
    t = s - band_idx

    seat = band_idx == 0                     # the vacant band: s in [0, 1)
    inner = band_idx < 0                     # the zero's family
    outer = band_idx > 0                     # the pole's family

    # ---- colour the two families, then empty the seat ----
    col = np.zeros((ny, nx, 3))

    idx_o = np.mod(band_idx - 1, ncol)       # outer family index
    idx_i = np.mod(-band_idx - 1, ncol)      # inner family index (band -1 -> 0)

    edge_w = 0.14
    f_blend = np.minimum(smoothstep(0, edge_w, t), 1.0 - smoothstep(1 - edge_w, 1, t))

    # outer: interpolate warm palette
    c0 = warm[idx_o]; c1 = warm[np.mod(idx_o + 1, ncol)]
    col_o = c0 * (1 - f_blend)[..., None] + c1 * f_blend[..., None]
    # inner: interpolate cool palette
    c0 = cool[idx_i]; c1 = cool[np.mod(idx_i + 1, ncol)]
    col_i = c0 * (1 - f_blend)[..., None] + c1 * f_blend[..., None]

    col = np.where(outer[..., None], col_o, col)
    col = np.where(inner[..., None], col_i, col)

    # per-band brightness drift
    drift = 1.0 + 0.14 * np.sin(band_idx * 2.3 + seed * 0.7)
    col = col * drift[..., None]

    # fortification ridges
    ridge = 1.0 + 0.28 * smoothstep(0, 0.03, t) * (1 - smoothstep(0.07, 0.15, t))
    ridge *= 1.0 - 0.20 * smoothstep(1 - 0.15, 1 - 0.07, t) * (1 - smoothstep(1 - 0.03, 1, t))
    col = col * ridge[..., None]

    # ---- the seat: warm and cool both fade into the dark, never meeting ----
    # a vacancy profile in s-space, centred on the fixed ring (s = 1/2), that
    # darkens the seat band and swallows the two bands that crowd toward it.
    v = np.exp(-((s - 0.5) / 0.85) ** 2)
    st = np.clip(s, 0.0, 1.0)
    from_cool = np.exp(-st / 0.05)                       # bleeds from the inner edge
    from_warm = np.exp(-(1.0 - st) / 0.05)               # bleeds from the outer edge
    seat_col = (SEAT_BG[None, None, :]
                + (0.22 * cool[2])[None, None, :] * from_cool[..., None]
                + (0.22 * warm[4])[None, None, :] * from_warm[..., None])
    col = col * (1.0 - 0.92 * v[..., None]) + seat_col * (0.92 * v[..., None])
    col = np.where(seat[..., None], seat_col, col)   # hard-empty the exact seat

    # mottling
    mottle = 1.0 + 0.06 * np.sin(0.006 * x + seed) * np.cos(0.007 * y + 3.1)
    col = col * mottle[..., None]
    grain = 1.0 + rng.normal(0, 0.02, (ny, nx))
    col = col * grain[..., None]

    # ---- outer wall ----
    wall_start = rng.uniform(0.90, 0.95)
    wall = (u > wall_start) & (u < 1.05)
    wall_t = smoothstep(wall_start, 1.02, u)
    wall_col = np.array([0x24, 0x19, 0x10])
    col = np.where(wall[..., None],
                   col * (1 - 0.6 * wall_t[..., None]) + wall_col * 0.6 * wall_t[..., None], col)
    outside = u > 1.06
    col = np.where(outside[..., None], np.array([0x10, 0x10, 0x12]), col)

    col = np.clip(col, 0, 255)
    return Image.fromarray(col.astype(np.uint8), "RGB")

if __name__ == "__main__":
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    os.makedirs(outdir, exist_ok=True)
    for i, seed in enumerate([31, 47]):
        img = render(size=1600, seed=seed)
        path = os.path.join(outdir, f"agate-vacancy-{i+1:02d}.png")
        img.save(path)
        print("saved", path)
