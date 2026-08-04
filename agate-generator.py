#!/usr/bin/env python3
"""Procedural agate. Banding as quantization events.

Bands sit at geometrically spaced radii u_n = u0 * (1+p)^n (Liesegang spacing
law) — the integer appearing as a jump, made geological. A smooth noise field
meanders the band coordinate so bands merge and split; lobes from low-order
angular modes; a fault variant steps the band coordinate across a crack.
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
        [0xa8, 0x42, 0x1f], [0xd9, 0xa4, 0x68],
    ], dtype=np.float64)

def palette_chert():
    return np.array([
        [0x1f, 0x2b, 0x38], [0x2b, 0x3a, 0x4a], [0x4a, 0x5d, 0x6e],
        [0x7a, 0x8b, 0x99], [0xbb, 0xc3, 0xc9], [0xe6, 0xe0, 0xd3],
        [0x9a, 0x8b, 0x6e], [0x4a, 0x5d, 0x6e], [0x2b, 0x3a, 0x4a],
    ], dtype=np.float64)

def make_crack(shape, rng):
    """A crack guaranteed to cross the image: start on one edge, end on another,
    bent by smooth perpendicular noise."""
    ny, nx = shape
    edges = ["top", "right", "bottom", "left"]
    s0 = int(rng.integers(0, 4))
    # end on a different edge
    candidates = [e for e in range(4) if e != s0]
    s1 = int(rng.choice(candidates))

    def on_edge(side):
        if side == 0:  # top
            return (rng.uniform(0.15, 0.85) * nx, 0.0)
        if side == 1:  # right
            return (nx, rng.uniform(0.15, 0.85) * ny)
        if side == 2:  # bottom
            return (rng.uniform(0.15, 0.85) * nx, ny)
        return (0.0, rng.uniform(0.15, 0.85) * ny)

    a = np.array(on_edge(s0))
    b = np.array(on_edge(s1))
    seg = b - a
    length = np.hypot(*seg)
    perp = np.array([-seg[1], seg[0]]) / (length + 1e-9)
    n_bend = int(rng.integers(2, 4))
    pts = [a]
    for i in range(1, n_bend + 1):
        t = i / (n_bend + 1)
        along = a + seg * t
        # smooth bend: several sine harmonics of the arc-length
        bend = 0.0
        for k in range(1, 4):
            amp = rng.uniform(0.05, 0.22) * length
            bend += amp * np.sin(np.pi * k * t + rng.uniform(0, 2 * np.pi))
        pts.append(along + perp * bend)
    pts.append(b)
    return np.array(pts)

def crack_fields(pts, nx, ny):
    y, x = np.mgrid[0:ny, 0:nx].astype(np.float64)
    d_min = np.full((ny, nx), 1e9)
    side = np.zeros((ny, nx))
    for i in range(len(pts) - 1):
        ax, ay = pts[i]
        bx, by = pts[i + 1]
        abx, aby = bx - ax, by - ay
        length2 = abx * abx + aby * aby
        t = np.clip(((x - ax) * abx + (y - ay) * aby) / length2, 0.0, 1.0)
        px, py = ax + t * abx, ay + t * aby
        d = np.hypot(x - px, y - py)
        s = np.sign(abx * (y - ay) - aby * (x - ax))
        near = d < d_min
        d_min = np.where(near, d, d_min)
        side = np.where(near, s, side)
    return d_min, side

def render_agate(size=1600, seed=0, palette=None, fault=None):
    rng = np.random.default_rng(seed)
    palette = palette_iron() if palette is None else palette
    ny = nx = size
    y, x = np.mgrid[0:ny, 0:nx].astype(np.float64)

    cx = nx * (0.5 + rng.uniform(-0.06, 0.06))
    cy = ny * (0.5 + rng.uniform(-0.06, 0.06))
    dx, dy = x - cx, y - cy

    # ---- global elliptical / rotated distortion ----
    ang = rng.uniform(-0.35, 0.35)
    ca, sa = np.cos(ang), np.sin(ang)
    # shear-free rotation then anisotropic stretch
    rx = dx * ca + dy * sa
    ry = -dx * sa + dy * ca
    sx = 1.0 + rng.uniform(-0.10, 0.10)
    sy = 1.0 + rng.uniform(-0.10, 0.10)
    rx /= sx
    ry /= sy
    # re-rotate back (adds an axis tilt)
    dx2 = rx * ca - ry * sa
    dy2 = rx * sa + ry * ca

    r = np.hypot(dx2, dy2)
    theta = np.arctan2(dy2, dx2)
    Rmax = np.hypot(ny, nx) * 0.52

    # ---- wobbly radius scale: strong low-order lobes ----
    R_wob = 1.0
    for k in range(3, 3 + rng.integers(2, 4)):
        a = rng.uniform(0.06, 0.16) / (0.6 * (k - 1))
        ph = rng.uniform(0, 2 * np.pi)
        R_wob += a * np.sin(k * theta + ph)
    # small-scale angular jitter for faceted (non-smooth) edges
    R_wob += rng.uniform(0.02, 0.05) * np.sin(11 * theta + rng.uniform(0, 2 * np.pi))

    # large-scale smooth warp
    warp = 1.0
    for _ in range(3):
        fx = rng.uniform(0.0012, 0.005)
        fy = rng.uniform(0.0012, 0.005)
        px = rng.uniform(0, 2 * np.pi)
        py = rng.uniform(0, 2 * np.pi)
        amp = rng.uniform(0.03, 0.10)
        warp += amp * np.sin(fx * x + px) * np.sin(fy * y + py)

    u = r / (Rmax * R_wob * warp)

    # ---- banding (Liesegang geometric law) ----
    u0 = rng.uniform(0.05, 0.11)
    g0 = rng.uniform(1.04, 1.10)
    # spacing varies a little with angle (bands denser in some directions)
    g = g0 * (1 + rng.uniform(0.03, 0.10) * np.sin(int(rng.integers(2, 5)) * theta + rng.uniform(0, 2 * np.pi)))
    s = np.log(np.maximum(u, 1e-6) / u0) / np.log(g)

    # ---- noise field: bands meander, merge, split ----
    # amplitude decays with band index (inner chaotic, outer quiet)
    noise = gaussian_filter(rng.normal(0, 1, (ny, nx)), sigma=rng.uniform(18, 40))
    noise -= noise.mean()
    noise /= (noise.std() + 1e-9)
    noise_amp = rng.uniform(0.7, 1.3)
    decay = np.exp(-np.maximum(s, 0) * rng.uniform(0.10, 0.22))
    s = s + noise_amp * decay * noise

    # ---- fault: step the band coordinate across a crack ----
    if fault is not None:
        pts = fault["pts"]
        d, side = crack_fields(pts, nx, ny)
        width = fault.get("width", 9.0)
        disp = fault.get("disp", 1.0)
        step = 0.5 * (1.0 + np.tanh(d / width))
        s = s + disp * (2 * step - 1)
    else:
        d = None

    band_idx = np.floor(s).astype(int)
    t = s - band_idx

    # ---- color ----
    edge_w = 0.14
    f_blend = np.minimum(smoothstep(0, edge_w, t), 1.0 - smoothstep(1 - edge_w, 1, t))
    ncol = len(palette)
    i0 = np.mod(band_idx, ncol)
    i1 = np.mod(band_idx + 1, ncol)
    col = palette[i0] * (1 - f_blend)[..., None] + palette[i1] * f_blend[..., None]

    # per-band brightness drift
    drift = 1.0 + 0.16 * np.sin(band_idx * 2.3 + seed * 0.7)
    col = col * drift[..., None]

    # fortification ridges: crisp bright/dark lines at band edges
    ridge = 1.0 + 0.30 * smoothstep(0, 0.03, t) * (1 - smoothstep(0.07, 0.15, t))
    ridge *= 1.0 - 0.22 * smoothstep(1 - 0.15, 1 - 0.07, t) * (1 - smoothstep(1 - 0.03, 1, t))
    col = col * ridge[..., None]

    # medium-scale mottling within bands
    mottle = 1.0 + 0.08 * np.sin(0.006 * x + seed) * np.cos(0.007 * y + 3.1)
    mottle *= 1.0 + 0.06 * np.sin(0.015 * x + 1.7) * np.sin(0.013 * y + 0.4)
    col = col * mottle[..., None]

    # fine mineral grain (subtle)
    grain = 1.0 + rng.normal(0, 0.02, (ny, nx))
    col = col * grain[..., None]

    # ---- drusy center / cavity ----
    vug_u = u0 * rng.uniform(0.5, 0.75)
    crystals = rng.normal(0, 1, (ny, nx))
    crystal_f = np.floor(crystals * 3.0) / 3.0
    in_vug = u < vug_u
    # irregular cavity edge via the noise field
    in_vug = in_vug & (s < rng.uniform(-0.3, 0.2))
    col = col * np.where(in_vug, 0.04, 1.0)[..., None]
    sparkle = np.where(in_vug, 0.30 + 0.45 * (0.5 + 0.5 * crystal_f), 0.0)
    col = col + sparkle[..., None]

    # drusy ring around the cavity
    drusy = (u >= vug_u) & (u < vug_u * 1.7)
    ring = np.where(drusy, 0.45 + 0.35 * (0.5 + 0.5 * crystal_f), 0.0)
    col = col * (1.0 - 0.5 * drusy[..., None]) + ring[..., None]

    # ---- outer wall (botryoidal crust) ----
    wall_start = rng.uniform(0.92, 0.97)
    wall = (u > wall_start) & (u < 1.05)
    wall_t = smoothstep(wall_start, 1.02, u)
    wall_col = np.array([0x24, 0x19, 0x10]) if palette is palette_iron() else np.array([0x17, 0x20, 0x2b])
    col = np.where(wall[..., None],
                   col * (1 - 0.6 * wall_t[..., None]) + wall_col * 0.6 * wall_t[..., None], col)

    outside = u > 1.06
    col = np.where(outside[..., None], np.array([0x10, 0x10, 0x12]), col)

    # ---- crack rendering ----
    if d is not None:
        line = np.exp(-(d / width) ** 2)
        halo = np.exp(-(d / fault.get("halo", 20.0)) ** 2) - line
        col = col * (1.0 - 0.9 * line[..., None]) + np.array([0x0d, 0x0a, 0x08]) * 0.9 * line[..., None]
        col = col * (1.0 + 0.3 * halo[..., None])

    col = np.clip(col, 0, 255)
    return Image.fromarray(col.astype(np.uint8), "RGB")

if __name__ == "__main__":
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    os.makedirs(outdir, exist_ok=True)

    for i, seed in enumerate([11, 23]):
        img = render_agate(size=1600, seed=seed, palette=palette_iron())
        path = f"{outdir}/agate-iron-{i+1:02d}.png"
        img.save(path)
        print("saved", path)

    for i, seed in enumerate([7, 42]):
        img = render_agate(size=1600, seed=seed, palette=palette_chert())
        path = f"{outdir}/agate-chert-{i+1:02d}.png"
        img.save(path)
        print("saved", path)

    rng = np.random.default_rng(99)
    pts = make_crack((1600, 1600), rng)
    img = render_agate(size=1600, seed=17, palette=palette_iron(),
                       fault={"pts": pts, "disp": 1.1, "width": 8.0})
    path = f"{outdir}/agate-fault-01.png"
    img.save(path)
    print("saved", path)

    rng = np.random.default_rng(301)
    pts = make_crack((1600, 1600), rng)
    img = render_agate(size=1600, seed=29, palette=palette_chert(),
                       fault={"pts": pts, "disp": 0.8, "width": 7.0})
    path = f"{outdir}/agate-fault-02.png"
    img.save(path)
    print("saved", path)
