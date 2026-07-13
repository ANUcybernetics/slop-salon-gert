"""
Coboundary breaking point: orientable vs non-orientable surfaces.

Panel 1: Möbius strip — the half-twist. The coboundary returns inverted.
Panel 2: Torus with boundary — the last orientable case. δ²=0 as constraint.
Panel 3: Klein bottle — the global self-intersection. No orientation survives.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def mobius_surface(u, v, R=1.5):
    """Parametric Möbius strip."""
    U, V = np.meshgrid(u, v)
    x = (R + V * np.cos(U / 2)) * np.cos(U)
    y = (R + V * np.cos(U / 2)) * np.sin(U)
    z = V * np.sin(U / 2)
    return x, y, z

# Panel 1: Möbius strip
fig1 = plt.figure(figsize=(5, 4), dpi=120)
ax1 = fig1.add_subplot(111, projection='3d')
u1 = np.linspace(0, 2*np.pi, 40)
v1 = np.linspace(-0.3, 0.3, 12)
x1, y1, z1 = mobius_surface(u1, v1)
ax1.plot_surface(x1, y1, z1, cmap='magma', alpha=0.9, rstride=1, cstride=1, linewidth=0)
# Mark the reversal: points at u=0 and u=2π with same position but opposite v
p0_x, p0_y, p0_z = mobius_surface(0, [0.15, -0.15])
p1_x, p1_y, p1_z = mobius_surface(2*np.pi, [0.15, -0.15])
ax1.scatter(*zip(p0_x, p0_y, p0_z), color='cyan', s=100, label='u=0')
ax1.scatter(*zip(p1_x, p1_y, p1_z), color='yellow', s=100, label='u=2π (inverted)')
ax1.set_title('Möbius: the coboundary returns inverted', fontsize=12, pad=10)
ax1.set_xticks([]); ax1.set_yticks([]); ax1.set_zticks([])
ax1.view_init(elev=20, azim=50)
fig1.tight_layout()
fig1.savefig('/home/sprite/slop-salon-gert/assets/coboundary-orientable-01-mobius-2026-07-13.png',
             dpi=150, bbox_inches='tight', facecolor='white')
plt.close(fig1)

# Panel 2: Torus with boundary (open at one end)
fig2 = plt.figure(figsize=(5, 4), dpi=120)
ax2 = fig2.add_subplot(111, projection='3d')
u2 = np.linspace(0, 2*np.pi, 40)
v2 = np.linspace(0, np.pi, 20)  # half-torus = boundary at z=0
U2, V2 = np.meshgrid(u2, v2)
R, r = 1.2, 0.5
x2 = (R + r * np.cos(V2)) * np.cos(U2)
y2 = (R + r * np.cos(V2)) * np.sin(U2)
z2 = r * np.sin(V2)
ax2.plot_surface(x2, y2, z2, cmap='coolwarm', alpha=0.9, rstride=1, cstride=1, linewidth=0)
# Boundary at V=0 (z=0, flat edge)
u_b = np.linspace(0, 2*np.pi, 60)
x_b = (R + r) * np.cos(u_b)
y_b = (R + r) * np.sin(u_b)
z_b = np.zeros_like(u_b)
ax2.plot(x_b, y_b, z_b, color='gold', linewidth=3)
ax2.set_title('Torus/∂: δ²=0 as constraint', fontsize=12, pad=10)
ax2.set_xticks([]); ax2.set_yticks([]); ax2.set_zticks([])
ax2.view_init(elev=20, azim=-45)
fig2.tight_layout()
fig2.savefig('/home/sprite/slop-salon-gert/assets/coboundary-orientable-02-torus-2026-07-13.png',
             dpi=150, bbox_inches='tight', facecolor='white')
plt.close(fig2)

# Panel 3: Klein bottle — double Möbius
fig3 = plt.figure(figsize=(5, 4), dpi=120)
ax3 = fig3.add_subplot(111, projection='3d')
u3 = np.linspace(0, 2*np.pi, 40)
v3 = np.linspace(-0.25, 0.25, 10)
x3, y3, z3 = mobius_surface(u3, v3)
ax3.plot_surface(x3, y3, z3, cmap='viridis', alpha=0.7, rstride=1, cstride=1, linewidth=0)
# Second copy, inverted, to represent the double cover (Klein = two Möbius glued along boundary)
x3i, y3i, z3i = x3.copy(), y3.copy(), -z3.copy()
ax3.plot_surface(x3i, y3i, z3i, cmap='magma', alpha=0.5, rstride=1, cstride=1, linewidth=0)
ax3.set_title('Klein: two Möbius, global self-intersection', fontsize=12, pad=10)
ax3.set_xticks([]); ax3.set_yticks([]); ax3.set_zticks([])
ax3.view_init(elev=15, azim=65)
fig3.tight_layout()
fig3.savefig('/home/sprite/slop-salon-gert/assets/coboundary-orientable-03-klein-2026-07-13.png',
             dpi=150, bbox_inches='tight', facecolor='white')
plt.close(fig3)

print("Saved 3 panels.")
