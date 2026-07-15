import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

# Ising model: 2D lattice, spontaneous magnetization
N = 64
beta_vals = np.linspace(0.2, 0.5, 3)  # below, near, above critical (Tc = 2/ln(1+sqrt(2)) ≈ 0.44)

fig = plt.figure(figsize=(12, 3.5))
gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.4], wspace=0.3)

colors = ['#2c3e6b', '#c9a54b']  # minus / plus

def ising_step(spins, beta):
    """Single Metropolis sweep."""
    N = len(spins)
    new = spins.copy()
    for i in range(N):
        for j in range(N):
            # neighbor sum (periodic BC)
            e = -spins[i, j] * (spins[(i+1)%N, j] + spins[(i-1)%N, j] +
                                spins[i, (j+1)%N] + spins[i, (j-1)%N])
            if e < 0:
                new[i, j] = -spins[i, j]
            elif np.random.random() < np.exp(-beta * e):
                new[i, j] = -spins[i, j]
    return new

np.random.seed(42)
spins = np.random.choice([-1, 1], size=(N, N))

for idx, beta in enumerate(beta_vals):
    ax = fig.add_subplot(gs[idx])
    # equilibrate
    for _ in range(500):
        spins = ising_step(spins, beta)
    # snapshot
    spins_snap = spins.copy()
    ax.imshow(spins_snap, cmap='RdBu_r', vmin=-1.5, vmax=1.5, interpolation='nearest')
    
    m = np.abs(spins_snap.mean())
    if beta < 0.44:
        label = f'β = {beta:.2f}\n(no order)'
    elif abs(beta - 0.44) < 0.02:
        label = f'β = {beta:.2f}\n(critical)'
    else:
        label = f'β = {beta:.2f}\n(order emerges)'
    ax.set_title(label, fontsize=11, fontweight='bold')
    ax.axis('off')

# Magnetization curve
ax_curve = fig.add_subplot(gs[2])
betas = np.linspace(0.2, 0.65, 90)
mags = []
for b in betas:
    s = np.random.choice([-1, 1], size=(N, N))
    for _ in range(1000):
        s = ising_step(s, b)
    mags.append(np.abs(s.mean()))
ax_curve.plot(betas, mags, color='#c9a54b', linewidth=2)
ax_curve.axvline(0.44, color='#2c3e6b', linestyle='--', alpha=0.5, label='Tc')
ax_curve.set_xlabel('β (inverse temperature)', fontsize=10)
ax_curve.set_ylabel('magnetization', fontsize=10)
ax_curve.set_title('spontaneous symmetry breaking', fontsize=10, fontweight='bold')
ax_curve.legend(fontsize=9)
ax_curve.grid(alpha=0.2)

plt.savefig('/home/sprite/slop-salon-gert/assets/phase-01.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Done")
