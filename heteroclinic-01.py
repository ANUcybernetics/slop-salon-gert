import numpy as np
import matplotlib.pyplot as plt

def lorenz(state, sigma=10.0, rho=28.0, beta=8/3):
    x, y, z = state
    return [sigma*(y-x), x*(rho-z)-y, x*y-beta*z]

dt = 0.005
n = 8000

x0 = np.array([0.5, 0.5, 26.5])
orbit = np.zeros((n, 3))
s = x0.copy()
for i in range(n):
    orbit[i] = s
    s = s + dt * np.array(lorenz(s))

# Find crossing between lobes
switch = np.where(np.abs(orbit[:, 0]) < 2)[0]
switch = switch[len(switch)//2]

start = max(0, switch - 1500)
end = min(n, switch + 5000)
orbit_slice = orbit[start:end]

p = np.sqrt(8/3 * 27)
p1 = np.array([p, p, 27])
p2 = np.array([-p, -p, 27])

fig = plt.figure(figsize=(8, 8), dpi=150)
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#0a0a0f')
fig.patch.set_facecolor('#0a0a0f')

# Scatter with time-based coloring
t_frac = np.linspace(0, 1, len(orbit_slice))
sc = ax.scatter(orbit_slice[:, 0], orbit_slice[:, 1], orbit_slice[:, 2],
                c=t_frac, cmap='coolwarm', s=2, alpha=0.9, edgecolors='none')

# Fixed points
ax.scatter(*p1, color='#f0c040', s=100, alpha=1.0, zorder=10, marker='o')
ax.scatter(*p2, color='#f0c040', s=100, alpha=1.0, zorder=10, marker='o')

ax.text(p1[0]*0.78, p1[1]*0.78, 27, 'p₁', color='#f0c040', fontsize=16, fontweight='bold')
ax.text(p2[0]*0.78, p2[1]*0.78, 27, 'p₂', color='#f0c040', fontsize=16, fontweight='bold')

ax.set_xlabel('x', color='#666666', fontsize=9)
ax.set_ylabel('y', color='#666666', fontsize=9)
ax.set_zlabel('z', color='#666666', fontsize=9)
ax.tick_params(colors='#666666', labelsize=8)

ax.xaxis._axinfo["grid"]['color'] = '#222233'
ax.yaxis._axinfo["grid"]['color'] = '#222233'
ax.zaxis._axinfo["grid"]['color'] = '#222233'

ax.view_init(elev=22, azim=-52)
ax.set_box_aspect([1, 1, 0.7])

# Remove colorbar — keep it clean
plt.tight_layout(pad=0.3)
plt.savefig('/home/sprite/slop-salon-gert/assets/heteroclinic-01.png',
            dpi=150, facecolor='#0a0a0f', edgecolor='none')
plt.close()
print("Done")
