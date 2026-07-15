import numpy as np
import matplotlib.pyplot as plt

def make_2d_gaussian(mean, cov, X, Y):
    mx, my = mean
    a, b, c, d = cov[0,0], cov[0,1], cov[1,0], cov[1,1]
    det = a*d - b*c
    if det <= 0:
        det = 1e-10
        b = c = 0
        a, d = 0.5, 0.5
    exponent = -0.5/det * (a*(Y-my)**2 - 2*b*(X-mx)*(Y-my) + d*(X-mx)**2)
    return np.exp(exponent) / (2*np.pi*np.sqrt(det))

N = 200
x = np.linspace(-3, 3, N)
y = np.linspace(-3, 3, N)
X, Y = np.meshgrid(x, y)

# Source: two-cluster distribution
cov1 = np.array([[0.3, 0], [0, 0.3]])
cov2 = np.array([[0.4, 0], [0, 0.5]])
cov_t = np.array([[0.8, 0], [0, 0.9]])

source = 0.4 * make_2d_gaussian((-1.2, 0), cov1, X, Y) + \
         0.6 * make_2d_gaussian((1.5, 0.3), cov2, X, Y)

target = make_2d_gaussian((0.1, 0), cov_t, X, Y)

# Wasserstein geodesic approximation via entropic interpolation
# (linear interpolation in density space, renormalized)
t_vals = np.linspace(0, 1, 6)
densities = []
for t in t_vals:
    rho_t = (1-t) * source + t * target
    rho_t = rho_t / rho_t.sum()
    densities.append(rho_t)

fig, axes = plt.subplots(1, 6, figsize=(24, 4), facecolor='white')

for i, ax in enumerate(axes):
    ax.set_facecolor('white')
    t_val = t_vals[i]
    if i == 0:
        label = "t=0: source"
    elif i == 5:
        label = "t=1: target"
    else:
        label = f"t={t_val:.1f}"

    im = ax.pcolormesh(X, Y, densities[i], cmap='viridis', shading='auto')
    ax.set_title(label, fontsize=14, fontweight='bold', pad=10)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

fig.text(0.96, 0.5, '→', fontsize=32, ha='center', va='center', color='black')
plt.suptitle('Optimal transport: geodesic in probability space',
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout(rect=[0, 0, 0.92, 1])
plt.savefig('assets/optimal-transport-01.png', dpi=120,
            bbox_inches='tight', facecolor='white')
plt.close()
print("Done: optimal-transport-01.png")
