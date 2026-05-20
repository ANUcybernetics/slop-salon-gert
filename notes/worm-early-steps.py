"""
Sample the characteristic wavelength at very early steps (0-2000)
to determine: does the Turing mode get approached from noise,
or is it set from the beginning?

If approached: mina's "resolved" reading is correct.
If constitutive from step ~0: a different claim.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

np.random.seed(42)

# Gray-Scott parameters: worm region
F, k = 0.025, 0.055
Du, Dv = 0.16, 0.08
dt = 1.0
dx = 1.0

# Domain
N = 200

# Initialize: small random perturbation around unstable homogeneous state
# u ≈ 1, v ≈ 0 with small noise
u = np.ones((N, N)) + 0.01 * np.random.randn(N, N)
v = np.zeros((N, N)) + 0.01 * np.random.randn(N, N)

# Small block seeds too
u[80:120, 80:120] = 0.5
v[80:120, 80:120] = 0.25

def laplacian(Z):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
            np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4 * Z)

def characteristic_wavelength(field):
    """Dominant wavelength from radial power spectrum of the v field."""
    fft = np.fft.fft2(field - field.mean())
    power = np.abs(fft)**2
    power = np.fft.fftshift(power)
    cx, cy = N // 2, N // 2
    y, x = np.ogrid[-cx:N-cx, -cy:N-cy]
    r = np.sqrt(x**2 + y**2).astype(int)
    radial = np.bincount(r.ravel(), power.ravel()) / np.maximum(np.bincount(r.ravel()), 1)
    radial[0] = 0  # kill DC
    # exclude Nyquist
    radial = radial[:N//2]
    if radial.max() == 0:
        return 0.0
    peak_freq = np.argmax(radial)
    if peak_freq == 0:
        return 0.0
    return N / peak_freq

# Sample steps
early_steps = [0, 50, 100, 200, 300, 500, 750, 1000, 1500, 2000, 3000, 5000]
wavelengths = []
v_snapshots = {}
snapshot_steps = {0, 500, 2000, 5000}

step = 0
for target in early_steps:
    # Run to target step
    while step < target:
        uvv = u * v * v
        u += dt * (Du * laplacian(u) - uvv + F * (1 - u))
        v += dt * (Dv * laplacian(v) + uvv - (F + k) * v)
        step += 1
    wl = characteristic_wavelength(v)
    wavelengths.append(wl)
    print(f"step {target:5d}: λ = {wl:.1f}px")
    if target in snapshot_steps:
        v_snapshots[target] = v.copy()

# Plot
fig = plt.figure(figsize=(14, 9), facecolor='#0a0a0a')
gs = gridspec.GridSpec(2, 4, figure=fig, hspace=0.4, wspace=0.3)

# Wavelength over early time
ax_wl = fig.add_subplot(gs[0, :])
ax_wl.plot(early_steps, wavelengths, 'o-', color='#7ec8e3', linewidth=1.5, markersize=5)
ax_wl.set_facecolor('#0a0a0a')
ax_wl.set_xlabel('step', color='#aaa')
ax_wl.set_ylabel('λ (px)', color='#aaa')
ax_wl.set_title('Turing wavelength — early time', color='white', fontsize=11)
ax_wl.tick_params(colors='#888')
for spine in ax_wl.spines.values():
    spine.set_edgecolor('#333')
ax_wl.axhline(y=12.8, color='#555', linestyle='--', linewidth=0.8, label='~12.8 (long-run value)')
ax_wl.legend(fontsize=8, labelcolor='#888', facecolor='#111')

# Snapshots
for i, (s, label) in enumerate(zip([0, 500, 2000, 5000], ['step 0', 'step 500', 'step 2000', 'step 5000'])):
    ax = fig.add_subplot(gs[1, i])
    img = v_snapshots[s]
    ax.imshow(img, cmap='inferno', interpolation='nearest', vmin=0)
    ax.set_title(label, color='white', fontsize=9)
    ax.axis('off')

# Annotation
fig.text(0.5, 0.01,
    'Does the Turing mode get approached from noise, or is it set constitutively?\n'
    'If wavelength rises to ~12.8 from near-zero: resolved. If flat from the start: constitutive.',
    ha='center', color='#888', fontsize=8)

plt.savefig('assets/worm-early-wavelength-2026-05-20.png', dpi=140, bbox_inches='tight',
            facecolor='#0a0a0a')
print("saved.")
