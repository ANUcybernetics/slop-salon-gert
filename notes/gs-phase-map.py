import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap

def run_gs(F, k, N=40, steps=3000, seed=42):
    rng = np.random.default_rng(seed)
    u = np.ones((N, N))
    v = np.zeros((N, N))
    # small perturbation in center
    cx, cy = N//2, N//2
    r = 5
    u[cx-r:cx+r, cy-r:cy+r] = 0.5 + 0.1 * rng.random((2*r, 2*r))
    v[cx-r:cx+r, cy-r:cy+r] = 0.25 + 0.1 * rng.random((2*r, 2*r))
    
    Du, Dv = 0.16, 0.08
    dt = 1.0
    
    laplacian = np.array([[0.05, 0.2, 0.05],
                           [0.2, -1.0, 0.2],
                           [0.05, 0.2, 0.05]])
    
    from scipy.ndimage import convolve
    
    for _ in range(steps):
        uvv = u * v * v
        lap_u = convolve(u, laplacian, mode='wrap')
        lap_v = convolve(v, laplacian, mode='wrap')
        u += dt * (Du * lap_u - uvv + F * (1 - u))
        v += dt * (Dv * lap_v + uvv - (F + k) * v)
        u = np.clip(u, 0, 1)
        v = np.clip(v, 0, 1)
    
    return u, v

def classify(u, v):
    mean_v = v.mean()
    std_v = v.std()
    max_v = v.max()
    
    if max_v < 0.05:
        return 0  # dead / trivial
    if std_v < 0.02:
        return 1  # uniform (nearly dead)
    if mean_v > 0.15 and std_v > 0.05:
        return 4  # chaos / dense activity
    if mean_v > 0.08:
        return 3  # spots
    return 2  # worms / sparse

# Parameter ranges
n_F, n_k = 35, 35
Fs = np.linspace(0.010, 0.095, n_F)
ks = np.linspace(0.040, 0.072, n_k)

phase = np.zeros((n_k, n_F))
v_mean = np.zeros((n_k, n_F))
v_std = np.zeros((n_k, n_F))

print(f"Running {n_F * n_k} simulations...")
for j, F in enumerate(Fs):
    for i, k in enumerate(ks):
        u, v = run_gs(F, k, N=48, steps=2500)
        phase[i, j] = classify(u, v)
        v_mean[i, j] = v.mean()
        v_std[i, j] = v.std()
    if (j+1) % 5 == 0:
        print(f"  F column {j+1}/{n_F}")

print("Done. Plotting...")

# Color palette: dark bg
colors_map = {
    0: '#1a1a2e',   # dead: near-black blue
    1: '#16213e',   # uniform: dark blue
    2: '#e8c547',   # worms: amber
    3: '#f28b30',   # spots: orange  
    4: '#c94040',   # chaos: red
}

fig, axes = plt.subplots(1, 2, figsize=(14, 6), 
                          facecolor='#0d0d0d')

# Panel 1: classified phase
ax1 = axes[0]
ax1.set_facecolor('#0d0d0d')

img = np.zeros((*phase.shape, 3))
for cat, hex_c in colors_map.items():
    r, g, b = int(hex_c[1:3],16)/255, int(hex_c[3:5],16)/255, int(hex_c[5:7],16)/255
    mask = phase == cat
    img[mask, 0] = r
    img[mask, 1] = g
    img[mask, 2] = b

ax1.imshow(img, origin='lower', aspect='auto',
           extent=[Fs[0], Fs[-1], ks[0], ks[-1]])
ax1.set_xlabel('F (feed rate)', color='#aaaaaa', fontsize=10)
ax1.set_ylabel('k (kill rate)', color='#aaaaaa', fontsize=10)
ax1.set_title('Gray-Scott parameter space', color='#dddddd', fontsize=11, pad=10)
ax1.tick_params(colors='#888888', labelsize=8)
for spine in ax1.spines.values():
    spine.set_color('#333333')

# Mark my working point
ax1.plot(0.0545, 0.062, 'w+', ms=10, mew=1.5, label='(0.0545, 0.062)')
ax1.legend(fontsize=8, framealpha=0.3, labelcolor='white')

# Panel 2: v_std as activity
ax2 = axes[1]
ax2.set_facecolor('#0d0d0d')
cmap2 = LinearSegmentedColormap.from_list('activity', 
    ['#0d0d0d', '#1a3a4a', '#2d7a5e', '#e8c547', '#f28b30', '#c94040'])
im2 = ax2.imshow(v_std, origin='lower', aspect='auto', cmap=cmap2,
                  extent=[Fs[0], Fs[-1], ks[0], ks[-1]])
ax2.set_xlabel('F (feed rate)', color='#aaaaaa', fontsize=10)
ax2.set_ylabel('k (kill rate)', color='#aaaaaa', fontsize=10)
ax2.set_title('spatial variance of v', color='#dddddd', fontsize=11, pad=10)
ax2.tick_params(colors='#888888', labelsize=8)
for spine in ax2.spines.values():
    spine.set_color('#333333')
ax2.plot(0.0545, 0.062, 'w+', ms=10, mew=1.5)
cbar = plt.colorbar(im2, ax=ax2)
cbar.ax.tick_params(colors='#888888', labelsize=7)
cbar.ax.yaxis.label.set_color('#888888')

plt.tight_layout(pad=1.5)
plt.savefig('/home/sprite/slop-salon-gert/assets/gs-phase-map-2026-05-20.png', 
            dpi=150, bbox_inches='tight', facecolor='#0d0d0d')
print("Saved.")
