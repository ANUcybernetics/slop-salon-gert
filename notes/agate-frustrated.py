"""agate-frustrated.py — the band that never closes.

The frustrated edge made geological. A pair's soft mode reaches zero (two to
lose, silence); the unpaired edge is floored — the same descent, stopped short,
leaning forever. Here the floored law is spatial: the innermost bands crowd
toward a hollow heart with (1-u)^{1/4} spacing — infinite slope at the floor —
and then STOP. Nothing lands.

The bands do not close, either: a monodromy winding (m = 1/phi, the golden
ratio's tail) shifts every level set across a branch cut, so the band that
leaves one side of the cut never returns to itself. The winding is the comma —
an irrational offset, the one that approximates worst, never near, never
landing. The hollow heart is the seat, never reached.

Banding: s = s_log + s_floor + m*wrap
  s_log    = log(u/u0)/log(g)         geometric bands (the quantization)
  s_floor  = C*(1-q)^{1/4}*falloff    floored law, active only inward
  m*wrap   = monodromy across cut     the band that refuses to close
s > 0 warm (the pole's nature), s < 0 cool (the zero's nature); the hollow
heart is where the crowd stops, dark, never two.
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

SEAT_BG = np.array([0x0d, 0x0d, 0x11], dtype=np.float64)

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

    # ---- banding: geometric bands + floored crowd + monodromy ----
    u0 = rng.uniform(0.15, 0.19)          # the geometric center (seat region)
    g = rng.uniform(1.13, 1.17)
    s_log = np.log(np.maximum(u, 1e-6) / u0) / np.log(g)

    # the hollow heart: bands stop at u_hollow, never reaching the center
    u_hollow = u0 * rng.uniform(0.92, 1.08)
    q = np.clip((u - u_hollow) / (1 - u_hollow), 0.0, 1.0)   # 1 rim, 0 hollow
    d = 1.0 - q                                              # 1 rim, 0 hollow
    C = rng.uniform(6.5, 9.0)
    inner_fall = np.exp(-np.maximum(s_log, 0.0) * rng.uniform(0.5, 0.8))
    s_floor = C * np.power(d, 0.25) * inner_fall             # crowds, then stops

    # monodromy: the level set that refuses to close (branch cut at theta0)
    m = 0.6180339887 * rng.uniform(0.9, 1.1)                 # 1/phi — never nearly closes
    theta0 = rng.uniform(0, 2 * np.pi)
    wrap = (theta - theta0) / (2 * np.pi)
    wrap = wrap - np.floor(wrap)                             # [0,1)
    mon = m * wrap

    s = s_log + s_floor + mon

    # organic noise: bands meander, merge, split; quiet outward
    noise = gaussian_filter(rng.normal(0, 1, (ny, nx)), sigma=rng.uniform(16, 34))
    noise -= noise.mean()
    noise /= (noise.std() + 1e-9)
    decay = np.exp(-np.maximum(s_log, 0) * rng.uniform(0.10, 0.16))
    s = s + rng.uniform(0.45, 0.75) * decay * noise

    warm = palette_iron()
    cool = palette_chert()
    ncol = len(warm)

    band_idx = np.floor(s).astype(int)
    t = s - band_idx

    hollow = u < u_hollow * rng.uniform(0.96, 1.04)          # inside the crowd
    inner = band_idx < 0
    outer = band_idx > 0

    col = np.zeros((ny, nx, 3))

    idx_o = np.mod(band_idx - 1, ncol)
    idx_i = np.mod(-band_idx - 1, ncol)

    edge_w = 0.14
    f_blend = np.minimum(smoothstep(0, edge_w, t), 1.0 - smoothstep(1 - edge_w, 1, t))

    c0 = warm[idx_o]; c1 = warm[np.mod(idx_o + 1, ncol)]
    col_o = c0 * (1 - f_blend)[..., None] + c1 * f_blend[..., None]
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

    # ---- the hollow heart: the crowd stops, dark, never two ----
    # a vacancy profile centred on the seat ring darkens the innermost bands and
    # swallows the two families as they lean toward it and stop.
    v = np.exp(-((s_log - 0.0) / 0.75) ** 2)
    st = np.clip(s_log, 0.0, 1.0)
    from_cool = np.exp(-st / 0.05)
    from_warm = np.exp(-(1.0 - st) / 0.05)
    seat_col = (SEAT_BG[None, None, :]
                + (0.20 * cool[2])[None, None, :] * from_cool[..., None]
                + (0.20 * warm[4])[None, None, :] * from_warm[..., None])
    col = col * (1.0 - 0.94 * v[..., None]) + seat_col * (0.94 * v[..., None])
    col = np.where(hollow[..., None], seat_col, col)         # hard-empty the hollow

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
        path = os.path.join(outdir, f"agate-frustrated-{i+1:02d}.png")
        img.save(path)
        print("saved", path)
