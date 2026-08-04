"""Shared helpers for the procedural agate family."""
import numpy as np


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
