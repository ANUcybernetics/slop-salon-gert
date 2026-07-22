#!/usr/bin/env python3
"""Six-panel cocycle diagram + audio: Z₂ cocycle from Newton basin partition."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.gridspec as gridspec
import json
import os

# ── Z₂ cocycle from Newton basin partition for z³ - 1 ──

# Cube roots of unity (the three basins)
roots = [np.exp(2j * np.pi * k / 3) for k in range(3)]
root_labels = ['+1', 'ω', 'ω²']

def newton_step(z):
    """Newton iteration for z³ - 1."""
    return z - (z**3 - 1) / (3 * z**2)

def basin(z, max_iter=30, tol=1e-8):
    """Return (converged_root_index, steps_to_converge)."""
    for i in range(1, max_iter + 1):
        z = newton_step(z)
        # check distance to roots
        for j, r in enumerate(roots):
            if abs(z - r) < tol:
                return j, i
    return -1, max_iter

def cocycle_grid(nx=200, ny=200, max_iter=20):
    """Compute basin labels and Z₂ cocycle on a grid."""
    x = np.linspace(-1.5, 1.5, nx)
    y = np.linspace(-1.5, 1.5, ny)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    basin_grid = np.zeros((ny, nx), dtype=np.int32)
    steps_grid = np.zeros((ny, nx), dtype=np.int32)

    for i in range(ny):
        for j in range(nx):
            idx, steps = basin(Z[i, j], max_iter=max_iter)
            basin_grid[i, j] = idx if idx >= 0 else 2  # 0,1,2 for three basins
            steps_grid[i, j] = steps

    # Z₂ cocycle: flip when crossing basin boundaries
    # For each pixel, compute cocycle = XOR of basin indices of neighbors
    # cocycle_z: flip in y direction
    cocycle_z = np.zeros((ny, nx), dtype=np.float32)
    cocycle_x = np.zeros((ny, nx), dtype=np.float32)

    for i in range(ny):
        for j in range(nx):
            if i < ny - 1:
                b_current = basin_grid[i, j]
                b_next = basin_grid[i + 1, j]
                if b_current != b_next:
                    cocycle_z[i, j] = 1.0
            if j < nx - 1:
                b_current = basin_grid[i, j]
                b_next = basin_grid[i, j + 1]
                if b_current != b_next:
                    cocycle_x[i, j] = 1.0

    return X, Y, basin_grid, steps_grid, cocycle_z, cocycle_x, x, y

def cocycle_audio(nx=200, ny=200, max_iter=20, sr=44100, duration=4.0):
    """Generate audio where Z₂ cocycle along radial line becomes phase discontinuities."""
    t = np.linspace(0, duration, int(sr * duration))

    # Sample a radial line through the basin grid at varying angles
    # This gives a sequence of basin labels → cocycle flips
    angle_sequence = []
    for i, theta in enumerate(np.linspace(0, 2*np.pi, len(t))):
        r = 0.8
        z = r * np.exp(1j * theta)
        bx = int((z.real + 1.5) / 3.0 * (nx - 1))
        by = int((z.imag + 1.5) / 3.0 * (ny - 1))
        bx = np.clip(bx, 0, nx - 1)
        by = np.clip(by, 0, ny - 1)
        angle_sequence.append(basin_grid[by, bx] if by < ny and bx < nx else 2)

    angle_sequence = np.array(angle_sequence)

    # Carrier: C4 = 261.63 Hz (root basin frequency)
    f0 = 261.63
    carrier = np.sin(2 * np.pi * f0 * t)

    # Phase jumps at cocycle flips
    phase = np.zeros_like(t)
    for i in range(1, len(t)):
        if angle_sequence[i] != angle_sequence[i - 1]:
            # Z₂ flip: add π phase jump
            phase[i] = phase[i - 1] + np.pi
        else:
            phase[i] = phase[i - 1]

    cocycle_wave = np.sin(2 * np.pi * f0 * t + phase)

    # Dual voice: reversed polynomial (z³ - 1 → different root ordering)
    # Uses conjugate roots → same structure, different phase
    phase_rev = np.zeros_like(t)
    for i in range(1, len(t)):
        if angle_sequence[i] != angle_sequence[i - 1]:
            phase_rev[i] = phase_rev[i - 1] - np.pi
        else:
            phase_rev[i] = phase_rev[i - 1]

    f0_rev = 261.63 * 3/4  # G3 — fourth below, poly dual
    dual_voice = np.sin(2 * np.pi * f0_rev * t + phase_rev)

    # Smooth: gentle decay to avoid clicks at edges
    envelope = np.ones_like(t)
    envelope[:int(0.3 * sr)] = np.linspace(0, 1, int(0.3 * sr))
    envelope[-int(0.3 * sr):] = np.linspace(1, 0, int(0.3 * sr))

    # Mix voices
    audio = 0.6 * cocycle_wave + 0.3 * dual_voice
    audio *= envelope

    # Normalize
    audio = audio / (np.max(np.abs(audio)) + 1e-12)
    # Limit peaks
    audio = np.clip(audio, -0.95, 0.95)

    return audio

# ── Generate diagram ──
print("Computing basin/cocycle grid...")
X, Y, basin_grid, steps_grid, cocycle_z, cocycle_x, x, y = cocycle_grid()

# ── Six-panel layout ──
fig = plt.figure(figsize=(16, 10))
fig.patch.set_facecolor('white')

gs = gridspec.GridSpec(3, 2, wspace=0.35, hspace=0.3)

# Colors for basins
basin_colors = ['#4488ff', '#ff4466', '#44cc88']  # blue, red, green

# Panel 1: Newton fractal (convergence steps)
ax1 = fig.add_subplot(gs[0, 0])
with np.errstate(invalid='ignore'):
    im1 = ax1.pcolormesh(X, Y, np.log1p(steps_grid), cmap='magma', shading='gouraud')
ax1.set_title('convergence steps (log scale)', fontsize=10, fontweight='bold')
ax1.set_xlabel('Re(z)')
ax1.set_ylabel('Im(z)')
ax1.set_aspect('equal')
ax1.set_xlim(-1.5, 1.5)
ax1.set_ylim(-1.5, 1.5)
plt.colorbar(im1, ax=ax1, shrink=0.7, label='log(steps+1)')

# Panel 2: Basin partition (labeled)
ax2 = fig.add_subplot(gs[0, 1])
basin_im = np.zeros((len(y), len(x), 3))
for k in range(3):
    rgb = tuple(int(basin_colors[k][i:i+2], 16) / 255 for i in (1, 3, 5))
    basin_im[basin_grid == k] = rgb
ax2.imshow(basin_im, extent=[-1.5, 1.5, -1.5, 1.5], origin='lower')
ax2.set_title('basin partition — z³−1', fontsize=10, fontweight='bold')
ax2.set_xlabel('Re(z)')
ax2.set_ylabel('Im(z)')
ax2.set_aspect('equal')
# Add root markers
for k, r in enumerate(roots):
    ax2.plot(r.real, r.imag, 'k*', markersize=15, zorder=5)
    ax2.text(r.real, r.imag - 0.2, root_labels[k], ha='center', fontsize=9)

# Panel 3: Z₂ cocycle (z-direction flips)
ax3 = fig.add_subplot(gs[1, 0])
ax3.imshow(cocycle_z, extent=[-1.5, 1.5, -1.5, 1.5], origin='lower',
           cmap='Reds', vmin=0, vmax=1, alpha=0.8)
ax3.set_title('Z₂ cocycle ∂ψ/∂z — vertical flips', fontsize=10, fontweight='bold')
ax3.set_xlabel('Re(z)')
ax3.set_ylabel('Im(z)')
ax3.set_aspect('equal')

# Panel 4: Z₂ cocycle (x-direction flips)
ax4 = fig.add_subplot(gs[1, 1])
ax4.imshow(cocycle_x, extent=[-1.5, 1.5, -1.5, 1.5], origin='lower',
           cmap='Blues', vmin=0, vmax=1, alpha=0.8)
ax4.set_title('Z₂ cocycle ∂ψ/∂x — horizontal flips', fontsize=10, fontweight='bold')
ax4.set_xlabel('Re(z)')
ax4.set_ylabel('Im(z)')
ax4.set_aspect('equal')

# Panel 5: Cocycle coboundary δ² = 0 — count of cocycle flips per pixel
ax5 = fig.add_subplot(gs[2, 0])
total_cocycle = cocycle_z + cocycle_x
# Count flips in 3x3 neighborhoods (coboundary operator)
from scipy.ndimage import uniform_filter
smooth_cocycle = uniform_filter(total_cocycle.astype(float), size=5) / 25
im5 = ax5.imshow(smooth_cocycle, extent=[-1.5, 1.5, -1.5, 1.5], origin='lower',
                  cmap='coolwarm', vmin=0, vmax=0.4)
ax5.set_title('cocycle density — δ² = 0 (coboundary operator)', fontsize=10, fontweight='bold')
ax5.set_xlabel('Re(z)')
ax5.set_ylabel('Im(z)')
ax5.set_aspect('equal')
plt.colorbar(im5, ax=ax5, shrink=0.7, label='flip density')

# Panel 6: Radial cross-sections with cocycle overlay
ax6 = fig.add_subplot(gs[2, 1])
n_radii = 8
theta_vals = np.linspace(0, 2*np.pi, n_radii, endpoint=False)
colors_radii = plt.cm.viridis(np.linspace(0, 1, n_radii))

for i, (theta, color) in enumerate(zip(theta_vals, colors_radii)):
    r_vals = np.linspace(0, 1.3, 300)
    z_vals = r_vals * np.exp(1j * theta)
    basins_along_r = []
    steps_along_r = []
    for z in z_vals:
        b, s = basin(z, max_iter=20)
        basins_along_r.append(b if b >= 0 else 2)
        steps_along_r.append(s)
    basins_along_r = np.array(basins_along_r)

    # Shift each radius vertically for clarity
    offset = (i - n_radii/2) * 0.5
    y_offset = basins_along_r + offset

    # Color by basin
    for j in range(len(y_offset) - 1):
        ax6.plot([r_vals[j], r_vals[j+1]], [y_offset[j], y_offset[j+1]],
                color=basin_colors[basins_along_r[j]], lw=3)
        # Highlight cocycle flips
        if basins_along_r[j] != basins_along_r[j+1]:
            ax6.plot(r_vals[j+1], y_offset[j+1], 'ko', markersize=3)

ax6.set_title('radial cross-sections — cocycle flips as black dots', fontsize=10, fontweight='bold')
ax6.set_xlabel('r')
ax6.set_ylabel('angle index (shifted)')

plt.savefig('/home/sprite/slop-salon-gert/assets/cocycle-structure-01.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Diagram saved: cocycle-structure-01.png")

# ── Generate audio ──
print("Generating audio...")
audio = cocycle_audio()
# Save as WAV
import scipy.io.wavfile as wavio
wavio.write('/home/sprite/slop-salon-gert/assets/cocycle-structure-01.wav', 44100,
           (audio * 32767).astype(np.int16))
print("Audio saved: cocycle-structure-01.wav")
print("Done.")
