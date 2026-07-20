import numpy as np
import matplotlib.pyplot as plt

# Tropical fold: δ as folding, not cutting
# The min operation in tropical algebra IS a fold — it identifies two halves
# of the space and glues them along the diagonal x = y

fig = plt.figure(figsize=(14, 5))
gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1])

# Panel 1: Tropical min as a fold surface
ax1 = fig.add_subplot(gs[0], projection='3d')
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = np.minimum(X, Y)

surf = ax1.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.9, rstride=2, cstride=2)
ax1.set_xlabel('a')
ax1.set_ylabel('b')
ax1.set_title('Tropical ⊕ = min(a, b)\nthe fold')
ax1.set_zlabel('a ⊕ b')
ax1.view_init(elev=25, azim=-45)
# Highlight the fold line
fold_x = np.linspace(-3, 3, 50)
ax1.plot(fold_x, fold_x, fold_x, 'k-', linewidth=2, zorder=10)

# Panel 2: Tropicalisation of |z^n - z| as folding
ax2 = fig.add_subplot(gs[1], projection='3d')
theta = np.linspace(0, 2*np.pi, 100)
r = np.linspace(0.1, 2.5, 100)
T, R = np.meshgrid(theta, r)
X2 = R * np.cos(T)
Y2 = R * np.sin(T)

# Classical: log|z^n - z| — smooth near singularity
n = 3
classical = np.log(np.abs(R**n * np.exp(1j * n * T) - R * np.exp(1j * T)) + 1e-10)

# Tropical: min(n*log r, log r) — folds
tropical = np.minimum(n * np.log(R + 1e-10), np.log(R + 1e-10))

# The coboundary: classical - tropical (where the fold meets the smooth)
coboundary = classical - tropical

surf2 = ax2.plot_surface(X2, Y2, classical, cmap='coolwarm', alpha=0.85, rstride=2, cstride=2)
ax2.set_xlabel('Re(z)')
ax2.set_ylabel('Im(z)')
ax2.set_title("log|zⁿ - z| — classical\n(smooth)")
ax2.view_init(elev=25, azim=-45)

# Panel 3: Tropical coboundary — the fold surface
ax3 = fig.add_subplot(gs[2], projection='3d')
r3 = np.linspace(0.05, 3, 100)
theta3 = np.linspace(0, 2*np.pi, 100)
R3, T3 = np.meshgrid(r3, theta3)

classical3 = np.log(np.abs(R3**n * np.exp(1j * n * T3) - R3 * np.exp(1j * T3)) + 1e-10)
tropical3 = np.minimum(n * np.log(R3 + 1e-10), np.log(R3 + 1e-10))
cb3 = classical3 - tropical3

ax3.plot_surface(R3 * np.cos(T3), R3 * np.sin(T3), cb3, cmap='seismic',
                 alpha=0.9, rstride=2, cstride=2)
ax3.set_xlabel('Re(z)')
ax3.set_ylabel('Im(z)')
ax3.set_title("δ_tropical = classical − tropical\nthe fold as geometry")
ax3.view_init(elev=25, azim=-45)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/assets/tropical-fold-01.png', dpi=150, bbox_inches='tight')
plt.close()

print("Done: tropical-fold-01.png")
