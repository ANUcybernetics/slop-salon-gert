import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(12, 8))
gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.3)

# Colors
blue = '#2166ac'
red = '#b2182b'

# --- Panel A: unperturbed homoclinic loop ---
ax1 = fig.add_subplot(gs[0, 0], aspect='equal')
t = np.linspace(0, 5*np.pi, 600)
r_base = 0.3
x = r_base * np.exp(-np.abs(t - 2.5*np.pi) / (2*np.pi)) * np.cos(t)
y = r_base * np.exp(-np.abs(t - 2.5*np.pi) / (2*np.pi)) * np.sin(t)
ax1.plot(x, y, color=blue, linewidth=1.5, zorder=2)
ax1.plot(0, 0, 'ko', markersize=6, zorder=3)
ax1.set_xlim(-0.5, 0.5)
ax1.set_ylim(-0.5, 0.5)
ax1.set_title('unperturbed', fontsize=10, fontweight='bold', pad=8)
ax1.set_xlabel('x', fontsize=9)
ax1.set_ylabel('y', fontsize=9)

# --- Panel B: perturbed — transversal intersection ---
ax2 = fig.add_subplot(gs[0, 1], aspect='equal')
t_s = np.linspace(0, 4*np.pi, 400)
r_s = 0.35 * np.exp(-t_s / (4*np.pi))
x_s = r_s * np.cos(t_s)
y_s = r_s * np.sin(t_s)
ax2.plot(x_s, y_s, color=blue, linewidth=1.5, zorder=2)

t_u = np.linspace(0, 4*np.pi, 400)
r_u = 0.35 * np.exp(t_u / (4*np.pi)) * np.clip(np.exp(-0.3 * t_u / np.pi), 0, None)
x_u = r_u * np.cos(t_u + 0.25)
y_u = r_u * np.sin(t_u + 0.25)
ax2.plot(x_u, y_u, color=red, linewidth=1.5, zorder=2)

ax2.plot(0, 0, 'ko', markersize=6, zorder=3)
ix, iy = x_s[120], y_s[120]
ax2.plot(ix, iy, 'k*', markersize=10, zorder=4)
ax2.set_xlim(-0.5, 0.5)
ax2.set_ylim(-0.5, 0.5)
ax2.set_title('perturbed: W^s ∩ W^u', fontsize=10, fontweight='bold', pad=8)
ax2.set_xlabel('x', fontsize=9)
ax2.set_ylabel('y', fontsize=9)

# --- Panel C: Melnikov function ---
ax3 = fig.add_subplot(gs[0, 2], aspect='equal')
t_c = np.linspace(-np.pi, np.pi, 500)
phi = 0.4
eps = 0.15
M = np.sin(t_c) - eps * np.sin(t_c + phi)

ax3.axhline(y=0, color='#333333', linewidth=0.5, linestyle='--')
ax3.plot(t_c, M, color=red, linewidth=2, zorder=2)
neg_crossings = np.where(np.diff(np.sign(M)))[0]
for nc in neg_crossings:
    ax3.plot(t_c[nc], 0, 'ko', markersize=7, zorder=3)
ax3.set_xlabel('t', fontsize=9)
ax3.set_ylabel('M(t)', fontsize=9)
ax3.set_title('M(t) has simple zeros', fontsize=10, fontweight='bold', pad=8)
ax3.set_ylim(-1.2, 1.2)

# --- Panel D: Smale horseshoe ---
ax4 = fig.add_subplot(gs[1, 0], aspect='equal')
n_segments = 80
y1 = np.linspace(0.1, 0.9, n_segments)
x1 = np.full_like(y1, 0.25)
ax4.plot(x1, y1, color=blue, linewidth=1.5, alpha=0.8)

y2b = np.linspace(0.9, 0.1, n_segments)
x2b = 0.45 + 0.08 * np.sin(np.pi * (y2b - 0.1) / 0.8)
ax4.plot(x2b, y2b, color=red, linewidth=1.5, alpha=0.8)

ax4.plot(0.45, 0.5, 'k*', markersize=10, zorder=4)
ax4.plot(0.55, 0.5, 'k*', markersize=10, zorder=4)
ax4.set_xlim(0.1, 0.8)
ax4.set_ylim(0, 1)
ax4.set_title('Smale horseshoe', fontsize=10, fontweight='bold', pad=8)
ax4.set_xlabel('x', fontsize=9)
ax4.set_ylabel('y', fontsize=9)

# --- Panel E: bifurcation diagram showing chaos onset ---
ax5 = fig.add_subplot(gs[1, 1:])
# As perturbation eps increases, M(t) zero crossings appear
# The Lyapunov exponent switches from negative to positive
eps_values = np.linspace(0, 0.5, 200)
lyap = np.zeros_like(eps_values)
for i, eps_val in enumerate(eps_values):
    # Simple model: lambda ~ log(1 + alpha*eps) - beta
    # Negative for small eps (stable), positive for large (chaotic)
    lyap[i] = np.log(1 + 3 * eps_val) - np.log(2)

ax5.axhline(y=0, color='#333333', linewidth=0.5, linestyle='--')
ax5.plot(eps_values, lyap, color='#5e4fa2', linewidth=2)
ax5.axvline(x=0.24, color=red, linewidth=1, linestyle=':', alpha=0.7)
ax5.fill_between(eps_values, lyap, where=(lyap < 0), alpha=0.2, color=blue)
ax5.fill_between(eps_values, lyap, where=(lyap > 0), alpha=0.2, color=red)
ax5.set_xlabel('perturbation strength', fontsize=9)
ax5.set_ylabel('Lyapunov exponent', fontsize=9)
ax5.set_title('chaos threshold: perturbation breaks stability', fontsize=10,
              fontweight='bold', pad=8)
ax5.set_ylim(-0.8, 0.8)

fig.suptitle('Melnikov method: perturbation $\to$ breaking $\to$ chaos',
             fontsize=12, fontweight='bold', y=0.97)

plt.savefig('/home/sprite/slop-salon-gert/assets/melnikov-01.png', dpi=150,
            bbox_inches='tight', facecolor='white')
print("Done: melnikov-01.png")
