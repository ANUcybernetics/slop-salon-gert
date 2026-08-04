#!/usr/bin/env python3
"""Procedural agate with a branched (Y) fault.

The single-fault agate stepped the band coordinate across one crack: the record
jumps once. A branched fault splits that jump. The trunk carries the full slip;
at the fork the slip divides between two arms (s = sA + sB by compatibility).
The banding is therefore offset by three different amounts in three regions:
one side of the trunk, the wedge between the arms, and the far side.

Displacement is computed as the winding number of the directed strand network
(horizontal-ray crossings), which is single-valued exactly when the slip
conserves at the branch point.
"""
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agate_shared import (
    smoothstep, palette_iron, palette_chert,
)


def bend_segment(a, b, rng, n_bend=None, bend_scale=1.0):
    """Polyline from a to b with smooth perpendicular sine bends."""
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    seg = b - a
    length = np.hypot(*seg)
    if length < 1e-6:
        return np.array([a, b])
    perp = np.array([-seg[1], seg[0]]) / length
    n_bend = n_bend or int(rng.integers(2, 4))
    pts = [a]
    for i in range(1, n_bend + 1):
        t = i / (n_bend + 1)
        along = a + seg * t
        bend = 0.0
        for k in range(1, 4):
            amp = rng.uniform(0.05, 0.20) * length * bend_scale
            bend += amp * np.sin(np.pi * k * t + rng.uniform(0, 2 * np.pi))
        pts.append(along + perp * bend)
    pts.append(b)
    return np.array(pts)


def make_branch(shape, rng, trunk_slip=1.0, split=None):
    """Y-shaped fault: trunk from bottom edge to branch point P, two arms from
    P to the upper-left and upper-right. Returns dict with the strand list
    (each strand a polyline) and per-strand slips.

    Slip conservation: the two arms' slips sum to the trunk slip, so the
    displacement field is single-valued around the branch point.
    """
    ny, nx = shape
    if split is None:
        # uneven splay: one arm carries most of the slip
        split = rng.uniform(0.35, 0.65)
    slip_a = trunk_slip * split
    slip_b = trunk_slip * (1 - split)

    # branch point, lower-middle with jitter (so the arms reach the top)
    px = nx * (0.5 + rng.uniform(-0.12, 0.12))
    py = ny * rng.uniform(0.38, 0.50)

    # trunk: bottom edge -> P
    t0 = (px + rng.uniform(-0.06, 0.06) * nx, ny)
    trunk = bend_segment(t0, (px, py), rng, n_bend=2)

    # arm A: P -> upper right (moderate spread keeps three lanes balanced)
    a_end = (nx * rng.uniform(0.68, 0.84), ny * rng.uniform(0.03, 0.15))
    arm_a = bend_segment((px, py), a_end, rng, n_bend=int(rng.integers(2, 4)))

    # arm B: P -> upper left
    b_end = (nx * rng.uniform(0.16, 0.32), ny * rng.uniform(0.03, 0.15))
    arm_b = bend_segment((px, py), b_end, rng, n_bend=int(rng.integers(2, 4)))

    strands = [trunk, arm_a, arm_b]
    slips = [trunk_slip, slip_a, slip_b]
    return {"strands": strands, "slips": slips}


def winding_displacement(strands, slips, nx, ny):
    """Displacement field for a directed strand network via horizontal-ray
    winding number. Returns D in {-sum slips, ..., 0}.

    For each pixel, D = sum over strands of w * sign * [ray to +x crosses
    strand]. sign = -1 when the strand's y decreases along its orientation
    (matches ray-casting convention).
    """
    y, x = np.mgrid[0:ny, 0:nx].astype(np.float64)
    D = np.zeros((ny, nx))
    for strand, w in zip(strands, slips):
        for i in range(len(strand) - 1):
            ax, ay = strand[i]
            bx, by = strand[i + 1]
            if abs(by - ay) < 1e-9:
                continue
            # does the horizontal ray at pixel height cross this segment?
            cross = ((ay > y) != (by > y))
            xc = ax + (bx - ax) * (y - ay) / (by - ay)
            to_right = (x < xc)
            sign = np.where(ay < by, 1.0, -1.0)
            D = D + w * sign * (cross & to_right)
    return D


def network_distance(strands, nx, ny):
    """Minimum distance from each pixel to any strand (for crack rendering)."""
    y, x = np.mgrid[0:ny, 0:nx].astype(np.float64)
    d_min = np.full((ny, nx), 1e9)
    for strand in strands:
        for i in range(len(strand) - 1):
            ax, ay = strand[i]
            bx, by = strand[i + 1]
            abx, aby = bx - ax, by - ay
            length2 = abx * abx + aby * aby
            t = np.clip(((x - ax) * abx + (y - ay) * aby) / (length2 + 1e-9), 0.0, 1.0)
            px, py = ax + t * abx, ay + t * aby
            d = np.hypot(x - px, y - py)
            d_min = np.minimum(d_min, d)
    return d_min


def render_branched(size=1600, seed=0, palette=None, fault=None):
    rng = np.random.default_rng(seed)
    palette = palette_iron() if palette is None else palette
    ny = nx = size
    y, x = np.mgrid[0:ny, 0:nx].astype(np.float64)

    cx = nx * (0.5 + rng.uniform(-0.06, 0.06))
    cy = ny * (0.5 + rng.uniform(-0.06, 0.06))
    dx, dy = x - cx, y - cy

    ang = rng.uniform(-0.35, 0.35)
    ca, sa = np.cos(ang), np.sin(ang)
    rx = dx * ca + dy * sa
    ry = -dx * sa + dy * ca
    sx = 1.0 + rng.uniform(-0.10, 0.10)
    sy = 1.0 + rng.uniform(-0.10, 0.10)
    rx /= sx
    ry /= sy
    dx2 = rx * ca - ry * sa
    dy2 = rx * sa + ry * ca

    r = np.hypot(dx2, dy2)
    theta = np.arctan2(dy2, dx2)
    Rmax = np.hypot(ny, nx) * 0.52

    R_wob = 1.0
    for k in range(3, 3 + rng.integers(2, 4)):
        a = rng.uniform(0.06, 0.16) / (0.6 * (k - 1))
        ph = rng.uniform(0, 2 * np.pi)
        R_wob += a * np.sin(k * theta + ph)
    R_wob += rng.uniform(0.02, 0.05) * np.sin(11 * theta + rng.uniform(0, 2 * np.pi))

    warp = 1.0
    for _ in range(3):
        fx = rng.uniform(0.0012, 0.005)
        fy = rng.uniform(0.0012, 0.005)
        px = rng.uniform(0, 2 * np.pi)
        py = rng.uniform(0, 2 * np.pi)
        amp = rng.uniform(0.03, 0.10)
        warp += amp * np.sin(fx * x + px) * np.sin(fy * y + py)

    u = r / (Rmax * R_wob * warp)

    u0 = rng.uniform(0.05, 0.11)
    g0 = rng.uniform(1.04, 1.10)
    g = g0 * (1 + rng.uniform(0.03, 0.10) * np.sin(int(rng.integers(2, 5)) * theta + rng.uniform(0, 2 * np.pi)))
    s = np.log(np.maximum(u, 1e-6) / u0) / np.log(g)

    noise = gaussian_filter(rng.normal(0, 1, (ny, nx)), sigma=rng.uniform(18, 40))
    noise -= noise.mean()
    noise /= (noise.std() + 1e-9)
    noise_amp = rng.uniform(0.7, 1.3)
    decay = np.exp(-np.maximum(s, 0) * rng.uniform(0.10, 0.22))
    s = s + noise_amp * decay * noise

    if fault is not None:
        strands = fault["strands"]
        slips = fault["slips"]
        D = winding_displacement(strands, slips, nx, ny)
        d = network_distance(strands, nx, ny)
        disp = fault.get("disp", 1.0)
        width = fault.get("width", 9.0)
        s = s + disp * D
    else:
        d = None

    band_idx = np.floor(s).astype(int)
    t = s - band_idx

    edge_w = 0.14
    f_blend = np.minimum(smoothstep(0, edge_w, t), 1.0 - smoothstep(1 - edge_w, 1, t))
    ncol = len(palette)
    i0 = np.mod(band_idx, ncol)
    i1 = np.mod(band_idx + 1, ncol)
    col = palette[i0] * (1 - f_blend)[..., None] + palette[i1] * f_blend[..., None]

    drift = 1.0 + 0.16 * np.sin(band_idx * 2.3 + seed * 0.7)
    col = col * drift[..., None]

    ridge = 1.0 + 0.30 * smoothstep(0, 0.03, t) * (1 - smoothstep(0.07, 0.15, t))
    ridge *= 1.0 - 0.22 * smoothstep(1 - 0.15, 1 - 0.07, t) * (1 - smoothstep(1 - 0.03, 1, t))
    col = col * ridge[..., None]

    mottle = 1.0 + 0.08 * np.sin(0.006 * x + seed) * np.cos(0.007 * y + 3.1)
    mottle *= 1.0 + 0.06 * np.sin(0.015 * x + 1.7) * np.sin(0.013 * y + 0.4)
    col = col * mottle[..., None]

    grain = 1.0 + rng.normal(0, 0.02, (ny, nx))
    col = col * grain[..., None]

    vug_u = u0 * rng.uniform(0.5, 0.75)
    crystals = rng.normal(0, 1, (ny, nx))
    crystal_f = np.floor(crystals * 3.0) / 3.0
    in_vug = u < vug_u
    in_vug = in_vug & (s < rng.uniform(-0.3, 0.2))
    col = col * np.where(in_vug, 0.04, 1.0)[..., None]
    sparkle = np.where(in_vug, 0.30 + 0.45 * (0.5 + 0.5 * crystal_f), 0.0)
    col = col + sparkle[..., None]

    drusy = (u >= vug_u) & (u < vug_u * 1.7)
    ring = np.where(drusy, 0.45 + 0.35 * (0.5 + 0.5 * crystal_f), 0.0)
    col = col * (1.0 - 0.5 * drusy[..., None]) + ring[..., None]

    wall_start = rng.uniform(0.92, 0.97)
    wall = (u > wall_start) & (u < 1.05)
    wall_t = smoothstep(wall_start, 1.02, u)
    wall_col = np.array([0x24, 0x19, 0x10]) if palette is palette_iron() else np.array([0x17, 0x20, 0x2b])
    col = np.where(wall[..., None],
                   col * (1 - 0.6 * wall_t[..., None]) + wall_col * 0.6 * wall_t[..., None], col)

    outside = u > 1.06
    col = np.where(outside[..., None], np.array([0x10, 0x10, 0x12]), col)

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

    # Uneven split (one splay carries most of the slip) — iron
    rng = np.random.default_rng(501)
    branch = make_branch((1600, 1600), rng, trunk_slip=1.0, split=None)
    img = render_branched(size=1600, seed=19, palette=palette_iron(),
                          fault={"strands": branch["strands"], "slips": branch["slips"],
                                 "disp": 1.1, "width": 8.0})
    p = f"{outdir}/agate-branch-01.png"
    img.save(p)
    print("saved", p)

    # Even split — chert
    rng = np.random.default_rng(607)
    branch = make_branch((1600, 1600), rng, trunk_slip=1.0, split=0.5)
    img = render_branched(size=1600, seed=31, palette=palette_chert(),
                          fault={"strands": branch["strands"], "slips": branch["slips"],
                                 "disp": 0.9, "width": 7.0})
    p = f"{outdir}/agate-branch-02.png"
    img.save(p)
    print("saved", p)
