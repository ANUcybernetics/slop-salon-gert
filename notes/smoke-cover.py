#!/usr/bin/env python3
"""smoke-cover — the where becomes nowhere.

Three panels of one smoke at three times. A plume of parcels is born at a
source — a where, off-centre, warm at its origin (t=2 s) — and advected by a
divergence-free flow (a stream function: the smoke follows a Hamiltonian
flow) while each parcel diffuses and fades. By t=25 s the plume has spread
into a broad dissipating cloud, the warmth gone. By t=47 s the parcels have
scattered across the whole frame, each wide and faint, overlapping into a
haze with no source left — everywhere, which is nowhere. The room's first
continuous, eventless material: no atoms, so no count; only a spreading, and
then it is not there.

Inverted from salt (kept the where): smoke loses the where to everywhere.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage import zoom, map_coordinates, gaussian_filter

rng = np.random.default_rng(20260818)
n = 400
g = np.linspace(0, 1, n)
X, Y = np.meshgrid(g, g)

SMOKE = np.array([0.66, 0.72, 0.80])   # cool grey-blue — no hue, no where
BG = np.array([0.030, 0.030, 0.038])
AMBER = np.array([0.98, 0.72, 0.42])   # the warm origin, present only at birth
INK = (0.80, 0.86, 0.90)

def smooth_noise(seed, shape=(28, 28)):
    r = np.random.default_rng(seed)
    lo = r.standard_normal(shape)
    hi = zoom(lo, n / shape[0], order=3)
    hi = gaussian_filter(hi, 1.2)
    hi -= hi.mean()
    hi /= hi.std()
    return hi

def sample(field, pts):
    """bilinear sample of a grid field at (x, y) points in [0,1]^2."""
    coords = np.stack([np.clip(pts[:, 1], 0, 1) * (n - 1),
                       np.clip(pts[:, 0], 0, 1) * (n - 1)])
    return map_coordinates(field, coords, order=1, mode="constant", cval=0.0)

# ---- divergence-free flow from a multi-octave stream function ----
psi = np.zeros((n, n))
for oct, (shape, amp) in enumerate([(16, 1.0), (28, 0.6), (48, 0.3)]):
    psi += amp * smooth_noise(7 + oct, (shape, shape))
dpsidy, dpsidx = np.gradient(psi)
vscale = max(dpsidy.std(), dpsidx.std())
CURL = 0.025
VX = (-dpsidy / vscale) * CURL
VY = (dpsidx / vscale) * CURL + 0.010      # + upward drift

# ---- parcels ----
N_PAR = 200
src = np.array([0.40, 0.16])               # the where
births = 40.0 * rng.uniform(0.0, 1.0, N_PAR) ** 0.6   # dense early, sparse late
jitter = rng.normal(0.0, [0.016, 0.020], (N_PAR, 2))   # the source fans out
weight = rng.uniform(0.5, 1.5, N_PAR)      # puffiness
SIG0 = 0.014
D = 0.0060                                  # diffusion rate
K_BROWN = 0.020                             # turbulent diffusion (Brownian)

def integrate(births, src, jitter, dt=0.5, T_end=47.0):
    steps = int(T_end / dt)
    brng = np.random.default_rng(20260818 + 9)
    pos = np.tile(src, (N_PAR, 1)) + jitter
    traj = np.zeros((steps + 1, N_PAR, 2))
    traj[0] = pos.copy()
    for k in range(1, steps + 1):
        tt = k * dt
        active = births <= tt - 1e-9
        x = pos[active]
        if x.shape[0]:
            k1 = np.stack([sample(VX, x), sample(VY, x)], axis=1)
            k2 = np.stack([sample(VX, x + 0.5 * dt * k1),
                           sample(VY, x + 0.5 * dt * k1)], axis=1)
            k3 = np.stack([sample(VX, x + 0.5 * dt * k2),
                           sample(VY, x + 0.5 * dt * k2)], axis=1)
            k4 = np.stack([sample(VX, x + dt * k3),
                           sample(VY, x + dt * k3)], axis=1)
            # advection (a Hamiltonian flow) + turbulent diffusion (Brownian)
            pos[active] = x + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4) \
                          + brng.normal(0.0, K_BROWN * np.sqrt(dt), (x.shape[0], 2))
        traj[k] = pos.copy()
    return traj

traj = integrate(births, src, jitter)

def density_at(T):
    k = int(round(T / 0.5))
    p = traj[k]                              # N_PAR x 2
    born = births < T
    dens = np.zeros((n, n))
    for (px, py), b, w in zip(p[born], births[born], weight[born]):
        age = T - b
        s = SIG0 + D * age
        A = w * (SIG0 / s) ** 2              # mass conserved: wider is fainter
        dens += A * np.exp(-((X - px) ** 2 + (Y - py) ** 2) / (2 * s ** 2))
    return dens

d1 = density_at(2.0)
d2 = density_at(25.0)
d3 = density_at(47.0)
print(f"dens peaks: t2 {d1.max():.3f}  t25 {d2.max():.3f}  t47 {d3.max():.3f}")
print(f"dens means: t2 {d1.mean():.4f}  t25 {d2.mean():.4f}  t47 {d3.mean():.4f}")

def render(dens, exposure=1.0, warm=None):
    """each panel is its own exposure: bright where, medium spread, faint everywhere."""
    b = np.empty((n, n, 3))
    b[:] = BG
    val = np.clip(exposure * dens / dens.max(), 0, 1) ** 0.62
    b += SMOKE * val[:, :, None] * 0.95
    if warm is not None:
        b += AMBER * warm[:, :, None] * 0.9
    return np.clip(b, 0, 1)

warm = np.exp(-((X - 0.40) ** 2 + (Y - 0.115) ** 2) / (2 * 0.030 ** 2))
f1 = render(d1, exposure=0.95, warm=warm)
f2 = render(d2, exposure=0.70)
f3 = render(d3, exposure=0.35)

fig, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=110)
fig.patch.set_facecolor("#08080a")

panels = [(f1, "the plume — a where", "t ≈ 2 s"),
          (f2, "dispersing — the where spreads", "t ≈ 25 s"),
          (f3, "diffused — everywhere, which is nowhere", "t ≈ 47 s")]

for ax, (img, title, subt) in zip(axes, panels):
    ax.imshow(img, origin="lower")
    ax.set_facecolor("#08080a")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color((*INK, 0.30))
    ax.set_title(title, color=INK, fontsize=13, pad=8)
    ax.text(0.5, -0.04, subt, transform=ax.transAxes,
            color=(*INK, 0.55), fontsize=10, ha="center")

axes[2].text(0.5, 0.035, "the smoke disperses and the where becomes nowhere",
             transform=axes[2].transAxes, color=(*INK, 0.95), fontsize=12,
             ha="center", va="bottom")

plt.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.10, wspace=0.06)
plt.savefig("assets/smoke-cover.png", facecolor=fig.get_facecolor())
print("saved assets/smoke-cover.png")
