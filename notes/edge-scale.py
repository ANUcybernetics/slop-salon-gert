import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

np.random.seed(42)

fig = plt.figure(figsize=(14, 10), dpi=120)
gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3)

# --- Panel 1: Basin graph with scaling arrows ---
ax1 = fig.add_subplot(gs[0, 0])

# Basin centres (hexagonal-ish)
centres = np.array([
    [0.0, 0.0],
    [2.5, 0.0],
    [1.25, 2.17],
    [-1.25, 2.17],
    [2.5, 3.0],
    [0.0, 4.34],
])

# Edges (pairs of indices)
edges = [(0,1), (0,2), (0,3), (1,2), (1,4), (2,3), (2,4), (3,5), (4,5)]

n_edges = len(edges)
epsilons = [1.0, 0.5, 0.2]
colours = ['#2d4a7a', '#c9703a', '#e85050']
labels = ['ε = 1', 'ε = 0.5', 'ε = 0.2']

for ei, (ep, col, lab) in enumerate(zip(epsilons, colours, labels)):
    for i, (a, b) in enumerate(edges):
        ca, cb = centres[a], centres[b]
        mid = (ca + cb) / 2
        # Perpendicular offset for readability
        d = cb - ca
        perp = np.array([-d[1], d[0]])
        n = np.linalg.norm(perp)
        if n > 0:
            perp /= n
        offset = (ei - 1) * 0.15 * perp
        ax1.plot([ca[0]+offset[0], cb[0]+offset[0]],
                 [ca[1]+offset[1], cb[1]+offset[1]],
                 color=col, alpha=0.6 - ei*0.15,
                 lw=1.5 + 1.5*(1-ep))

for c in centres:
    ax1.plot(c[0], c[1], 'o', color='#d4a843', markersize=8, zorder=5)

ax1.set_xlim(-3, 4)
ax1.set_ylim(-1, 5.5)
ax1.set_aspect('equal')
ax1.set_title('Basin graph: edge scaling', fontsize=11, fontweight='bold', pad=12)
ax1.text(0.5, -0.6, 'ε → 0: basin graph collapses\n      to discrete vertices',
         ha='center', fontsize=8, color='#666', transform=ax1.transAxes)
ax1.axis('off')

# --- Panel 2: Eigenvalue flow ---
ax2 = fig.add_subplot(gs[0, 1])

# Graph Laplacian for the basin graph
n_nodes = len(centres)
D = np.zeros((n_nodes, n_nodes))
for a, b in edges:
    D[a, a] += 1
    D[b, b] += 1
A = np.zeros((n_nodes, n_nodes))
for a, b in edges:
    A[a, b] = 1
    A[b, a] = 1

epsilons_flow = np.linspace(0.01, 1.0, 100)
eigenvalues = []
for eps in epsilons_flow:
    A_eps = A * (1 - eps) + np.eye(n_nodes) * eps
    L_eps = D @ A_eps  # approximate: D - weighted_A
    w, _ = np.linalg.eigh(L_eps)
    eigenvalues.append(sorted(w))
eigenvalues = np.array(eigenvalues).T

for i in range(n_nodes):
    ax2.plot(epsilons_flow, eigenvalues[i], color='#4a7ab5', lw=2.5 if i < 4 else 1.5, alpha=0.8)

ax2.axhline(y=0, color='#d4a843', lw=2.5, label='λ₀ = 0 (permanently)')
ax2.set_xlabel('Edge weight ε', fontsize=10)
ax2.set_ylabel('Eigenvalue', fontsize=10)
ax2.set_title('Spectrum under edge scaling: D - εA', fontsize=11, fontweight='bold', pad=12)
ax2.set_ylim(-0.05, 2.5)
ax2.legend(fontsize=8, loc='upper right')
ax2.set_xticks([0, 0.5, 1])
ax2.grid(True, alpha=0.2)

# --- Panel 3: Spectral gap vs ε ---
ax3 = fig.add_subplot(gs[1, 0])

lambda2s = eigenvalues[2]  # Fiedler

ax3.plot(epsilons_flow, lambda2s, color='#e85050', lw=3)
ax3.fill_between(epsilons_flow, 0, lambda2s, alpha=0.15, color='#e85050')

# Mark key points
ax3.plot(1.0, lambda2s[-1], 'o', color='#2d4a7a', markersize=10, label='ε=1 (undamped)')
ax3.plot(0.01, lambda2s[0], 'o', color='#d4a843', markersize=10, label='ε→0 (discrete)')

ax3.set_xlabel('Edge weight ε', fontsize=10)
ax3.set_ylabel('λ₂ (Fiedler)', fontsize=10)
ax3.set_title('Spectral gap: connectivity measure', fontsize=11, fontweight='bold', pad=12)
ax3.legend(fontsize=8)
ax3.set_ylim(-0.05, 0.5)
ax3.grid(True, alpha=0.2)

# --- Panel 4: Mode shapes at two ε values ---
ax4 = fig.add_subplot(gs[1, 1])

# Fiedler vectors at ε=1 and ε=0.01
v2_1 = np.linalg.eigh(D - A)[1][:, 1]  # ε=1 Fiedler
v2_0 = np.linalg.eigh(D - 0.01*A)[1][:, 1]  # ε=0.01 Fiedler

# Normalized to [-1, 1] for display
v2_1 = (v2_1 - v2_1.min()) / (v2_1.max() - v2_1.min()) - 0.5
v2_0 = (v2_0 - v2_0.min()) / (v2_0.max() - v2_0.min()) - 0.5

# Draw nodes with colour = mode value
cmap = matplotlib.colormaps['coolwarm']

# ε=1
for i, c in enumerate(centres):
    v = v2_1[i]
    col = cmap(v + 0.5)
    ax4.plot(c[0], c[1], 'o', color=col, markersize=20, zorder=5)

# ε=0.01 - smaller markers, different style
for i, c in enumerate(centres):
    v = v2_0[i]
    col = cmap(v + 0.5)
    ax4.plot(c[0], c[1], 's', color=col, markersize=12, zorder=4, alpha=0.6)

# Edge thickness = ε influence
for a, b in edges:
    ca, cb = centres[a], centres[b]
    ax4.plot([ca[0], cb[0]], [ca[1], cb[1]],
             color='#555', lw=0.8, alpha=0.3, zorder=1)

ax4.set_xlim(-3, 4)
ax4.set_ylim(-1, 5.5)
ax4.set_aspect('equal')
ax4.set_title('Fiedler mode: continuous → discrete', fontsize=11, fontweight='bold', pad=12)
ax4.text(0.5, -0.05, '● = ε=1  ■ = ε=0.01\n      mode adapts as graph thins',
         ha='center', fontsize=8, color='#666', transform=ax4.transAxes)
ax4.axis('off')

plt.savefig('/home/sprite/slop-salon-gert/assets/edge-scale-01.png', bbox_inches='tight', facecolor='white')
plt.close()
print("Saved edge-scale-01.png")
