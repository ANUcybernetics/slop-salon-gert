"""
Entropic regularization of optimal transport: Sinkhorn's algorithm.

The Sinkhorn iteration:
  K = exp(-C/ε)  # kernel matrix
  u_{k+1} = 1 / (K v_k)
  v_{k+1} = 1 / (K^T u_{k+1})
  P_ε = diag(u) K diag(v)  # entropically regularized plan

Connection to KL: the entropic OT objective is
  min_P ⟨P, C⟩ + ε KL(P || μ⊗ν)

The Schrödinger bridge: OT with noise. ε → 0 recovers deterministic OT.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

np.random.seed(42)

# ---- Discrete 1D distributions with multiple blobs ----
n = 20
x = np.arange(n)

# Source: three blobs
centers0 = [4, 8, 14]
weights0 = [0.4, 0.3, 0.3]
mu = np.zeros(n)
for c, w in zip(centers0, weights0):
    mu += w * np.exp(-0.5 * ((x - c) / 1.2) ** 2)
mu /= mu.sum()

# Target: shifted and reshaped
centers1 = [6, 10, 15]
weights1 = [0.3, 0.4, 0.3]
nu = np.zeros(n)
for c, w in zip(centers1, weights1):
    nu += w * np.exp(-0.5 * ((x - c) / 1.2) ** 2)
nu /= nu.sum()

# Ground distance (squared Euclidean)
cost = (x[:, None] - x[None, :]) ** 2

# ---- Sinkhorn for multiple ε values ----
epsilons = [2.0, 0.8, 0.3, 0.1]

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()

for idx, eps in enumerate(epsilons):
    ax = axes[idx]

    # Sinkhorn iteration
    K = np.exp(-cost / eps)
    u = np.ones(n)
    v = np.ones(n)
    for _ in range(500):
        u_new = 1.0 / (K @ v)
        v_new = 1.0 / (K.T @ u_new)
        if np.max(np.abs(np.log(u_new + 1e-300) - np.log(u + 1e-300))) < 1e-5 and \
           np.max(np.abs(np.log(v_new + 1e-300) - np.log(v + 1e-300))) < 1e-5:
            break
        u, v = u_new, v_new

    P_eps = np.outer(u, v) * K  # n x n transport plan
    P_eps /= P_eps.sum()

    # Visualize as heatmap
    im = ax.imshow(P_eps, cmap='viridis', aspect='equal', interpolation='nearest',
                   vmin=0, vmax=0.15)
    ax.set_title(f'ε = {eps}', fontsize=10, fontweight='bold')
    ax.set_xlabel('target x')
    ax.set_ylabel('source x')
    ax.set_xticks(range(0, n, 5))
    ax.set_yticks(range(0, n, 5))

    # Add density overlay
    ax.plot(x, mu * 20 + 5, 'cyan', linewidth=1, alpha=0.6, label='μ')
    ax.plot(x, nu * 20 + 5, 'orange', linewidth=1, alpha=0.6, label='ν')
    ax.legend(fontsize=7, loc='upper right')

fig.suptitle('Sinkhorn Regularization: ε → 0 recovers sparse OT plan',
             fontsize=13, fontweight='bold', y=0.97)

plt.savefig('/home/sprite/slop-salon-gert/assets/ot-sinkhorn-01.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("Created ot-sinkhorn-01.png")

# ---- Second image: cost and entropy vs ε ----
fig2, axes = plt.subplots(1, 2, figsize=(12, 5))

# Left: convergence of entropic OT cost → W₂²
eps_vals = np.logspace(-1.5, 0.5, 40)
costs = []
entropies = []

for eps in eps_vals:
    K = np.exp(-cost / eps)
    u = np.ones(n)
    v = np.ones(n)
    for _ in range(500):
        u_new = 1.0 / (K @ v)
        v_new = 1.0 / (K.T @ u_new)
        u, v = u_new, v_new
    P_eps = np.outer(u, v) * K
    P_eps /= P_eps.sum()
    cost_val = np.sum(P_eps * cost)
    costs.append(cost_val)
    ent = -np.sum(P_eps[P_eps > 0] * np.log(P_eps[P_eps > 0]))
    entropies.append(ent)

ax_l = axes[0]
ax_l.semilogx(eps_vals, costs, 'b-', linewidth=2)
ax_l.set_xlabel(r'ε (entropy regularization)')
ax_l.set_ylabel('OT cost ⟨P,C⟩')
ax_l.set_title(r'Entropic OT cost: lim_{ε→0} cost = W₂²',
              fontsize=10, fontweight='bold')
ax_l.spines['top'].set_visible(False)
ax_l.spines['right'].set_visible(False)

# Right: entropy of P_ε vs ε
ax_r = axes[1]
ax_r.semilogx(eps_vals, entropies, 'r-', linewidth=2)
ax_r.set_xlabel(r'ε (entropy regularization)')
ax_r.set_ylabel('entropy H(P_ε)')
ax_r.set_title(r'Entropy of regularized plan\n(larger ε → more diffuse)',
              fontsize=10, fontweight='bold')
ax_r.spines['top'].set_visible(False)
ax_r.spines['right'].set_visible(False)

fig2.suptitle('Sinkhorn: The Trade-off Between Cost and Entropy',
              fontsize=13, fontweight='bold', y=0.96)

plt.savefig('/home/sprite/slop-salon-gert/assets/ot-sinkhorn-02.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("Created ot-sinkhorn-02.png")
