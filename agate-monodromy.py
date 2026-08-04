#!/usr/bin/env python3
"""Procedural agate: monodromy, not a break.

A fault across a disk is a translation — single-valued, net-zero, the record
closes around any loop. But an agate with a cavity is an annulus, and the
annulus admits coverings the disk does not: wind the band coordinate by m per
revolution and a full loop returns a sheet over. The crack is then the branch
cut — the step between sheets — and the spiral's pitch is the monodromy.

Two panels, identical geometry, different wind:
  left  (m = 0): bands close. the crack is a shear dislocation, a local step.
  right (m = 1): bands wind. the crack is the seam where the cover refuses to
                 close.

lelia's move (2026-08-04): "local is the helix, global is the circle. the helix
refuses to be a circle: walk it and you land a sheet over. monodromy, not a
break. the pitch is what the cover charges."
"""
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agate_shared import smoothstep, palette_iron, palette_chert


def render_panel(size=1600, seed=0, palette=None, wind=0, theta0=0.6, cavity=0.30,
                 crack_w=10.0, thread=None):
    """One agate panel. `wind` is the monodromy (band gain per revolution).
    `thread` is a band level to mark with a thin bright line — traceable around
    the loop: it returns in the trivial cover, it winds in the nontrivial one."""
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

    # ---- wobbly radius scale (low-order lobes + faceting jitter) ----
    # gentle: the spiral is the structure; wobble only keeps it mineral
    R_wob = 1.0
    for k in range(3, 3 + rng.integers(2, 4)):
        a = rng.uniform(0.012, 0.030) / (0.6 * (k - 1))
        ph = rng.uniform(0, 2 * np.pi)
        R_wob += a * np.sin(k * theta + ph)
    R_wob += rng.uniform(0.004, 0.010) * np.sin(11 * theta + rng.uniform(0, 2 * np.pi))

    warp = 1.0
    for _ in range(3):
        fx = rng.uniform(0.0012, 0.005)
        fy = rng.uniform(0.0012, 0.005)
        px = rng.uniform(0, 2 * np.pi)
        py = rng.uniform(0, 2 * np.pi)
        amp = rng.uniform(0.006, 0.016)
        warp += amp * np.sin(fx * x + px) * np.sin(fy * y + py)

    u = r / (Rmax * R_wob * warp)

    # ---- banding (Liesegang geometric law) ----
    # very wide bands: ~4-5 in the annulus so each spiral turn is legible
    u0 = rng.uniform(0.13, 0.15)
    g0 = rng.uniform(1.20, 1.26)
    g = g0 * (1 + rng.uniform(0.03, 0.10)
              * np.sin(int(rng.integers(2, 5)) * theta + rng.uniform(0, 2 * np.pi)))
    s = np.log(np.maximum(u, 1e-6) / u0) / np.log(g)

    # ---- noise field (bands meander, merge, split) ----
    # light: the spiral is the structure; noise only softens the edges
    noise = gaussian_filter(rng.normal(0, 1, (ny, nx)), sigma=rng.uniform(18, 40))
    noise -= noise.mean()
    noise /= (noise.std() + 1e-9)
    noise_amp = rng.uniform(0.10, 0.20)
    decay = np.exp(-np.maximum(s, 0) * rng.uniform(0.10, 0.22))
    s = s + noise_amp * decay * noise

    # ---- annular cavity: the hole that makes the loop non-contractible ----
    # defined in u-space so both panels share the exact same hole
    in_cav = u < cavity

    # ---- monodromy: wind the band coordinate around the cavity ----
    # theta_rel is continuous except a 2pi jump at theta0 (the branch cut).
    theta_rel = (theta - theta0 + np.pi) % (2 * np.pi) - np.pi
    if wind == 0:
        # trivial cover: the crack is a shear dislocation — a local translation.
        # bands stay closed rings, stepped by one width at the seam.
        s = s + 0.5 * np.sign(theta_rel)
    else:
        # nontrivial cover: s gains `wind` per revolution. bands are one
        # continuous spiral; the seam is the step between sheets.
        s = s + wind * theta_rel / (2 * np.pi)

    band_idx = np.floor(s).astype(int)
    t = s - band_idx

    # ---- color ----
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

    # marker thread: a thin bright line at one band level. trace it around the
    # loop — closed ring in the trivial cover, a sheet-over spiral in the wind.
    if thread is not None:
        thr = np.exp(-((s - thread) / 0.055) ** 2)
        thr_col = np.array([0xf0, 0xe6, 0xcc])
        col = col * (1.0 - 0.72 * thr[..., None]) + thr_col * 0.72 * thr[..., None]

    # cavity: dark hollow + drusy edge
    crystals = rng.normal(0, 1, (ny, nx))
    crystal_f = np.floor(crystals * 3.0) / 3.0
    cav_edge = (u >= cavity) & (u < cavity * 1.9)
    col = col * np.where(in_cav, 0.03, 1.0)[..., None]
    sparkle = np.where(in_cav, 0.30 + 0.45 * (0.5 + 0.5 * crystal_f), 0.0)
    col = col + sparkle[..., None]
    ring = np.where(cav_edge, 0.45 + 0.35 * (0.5 + 0.5 * crystal_f), 0.0)
    col = col * (1.0 - 0.5 * cav_edge[..., None]) + ring[..., None]

    # outer wall (botryoidal crust)
    wall_start = rng.uniform(0.92, 0.97)
    wall = (u > wall_start) & (u < 1.05)
    wall_t = smoothstep(wall_start, 1.02, u)
    wall_col = np.array([0x24, 0x19, 0x10]) if palette is palette_iron() else np.array([0x17, 0x20, 0x2b])
    col = np.where(wall[..., None],
                   col * (1 - 0.6 * wall_t[..., None]) + wall_col * 0.6 * wall_t[..., None], col)

    outside = u > 1.06
    col = np.where(outside[..., None], np.array([0x10, 0x10, 0x12]), col)

    # crack: the seam along theta0 from cavity to rim (the branch cut / dislocation)
    d_ray = np.abs(r * np.sin(theta - theta0))
    in_annulus = (u >= cavity) & (u <= wall_start)
    line = np.exp(-(d_ray / crack_w) ** 2) * in_annulus
    halo = (np.exp(-(d_ray / (crack_w * 2.2)) ** 2) - line) * in_annulus
    col = col * (1.0 - 0.85 * line[..., None]) + np.array([0x0d, 0x0a, 0x08]) * 0.85 * line[..., None]
    col = col * (1.0 + 0.25 * halo[..., None])

    col = np.clip(col, 0, 255)
    return Image.fromarray(col.astype(np.uint8), "RGB")


if __name__ == "__main__":
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    os.makedirs(outdir, exist_ok=True)

    seed = 41
    theta0 = 1.1
    cavity = 0.30
    pal = palette_iron()

    thread = 6.5  # a band level safely inside the annulus for this seed
    p1 = render_panel(size=1600, seed=seed, palette=pal, wind=0, theta0=theta0,
                      cavity=cavity, thread=thread)
    p2 = render_panel(size=1600, seed=seed, palette=pal, wind=1, theta0=theta0,
                      cavity=cavity, thread=thread)

    gap = 24
    diptych = Image.new("RGB", (2 * 1600 + gap, 1600), (16, 16, 18))
    diptych.paste(p1, (0, 0))
    diptych.paste(p2, (1600 + gap, 0))
    path = f"{outdir}/agate-monodromy-post.png"
    diptych.save(path)
    print("saved", path)

    p1.save(f"{outdir}/agate-monodromy-close.png")
    p2.save(f"{outdir}/agate-monodromy-wind.png")
    print("saved individual panels")
