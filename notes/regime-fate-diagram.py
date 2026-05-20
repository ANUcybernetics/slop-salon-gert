import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

fig, axes = plt.subplots(1, 3, figsize=(12, 4.5))
fig.patch.set_facecolor('#0d0d0d')

for ax in axes:
    ax.set_facecolor('#0d0d0d')
    for spine in ax.spines.values():
        spine.set_color('#555555')
    ax.tick_params(colors='#888888', labelsize=8)

colors = {
    'stable': '#5b9bd5',
    'unstable': '#c84b31',
    'arrow': '#aaaaaa',
    'text': '#cccccc',
    'dim': '#666666',
    'fold_stable': '#5b9bd5',
    'fold_unstable': '#c84b31',
    'jump_arrow': '#e8b84b',
}

# ---- Panel 1: Resolved (supercritical pitchfork) ----
ax = axes[0]
mu = np.linspace(-1.5, 1.5, 400)

# Stable branches
ax.plot(mu[mu < 0], np.zeros_like(mu[mu < 0]), color=colors['stable'], lw=2.5)
ax.plot(mu[mu >= 0], np.sqrt(np.maximum(mu[mu >= 0], 0)), color=colors['stable'], lw=2.5)
ax.plot(mu[mu >= 0], -np.sqrt(np.maximum(mu[mu >= 0], 0)), color=colors['stable'], lw=2.5)
# Unstable branch
ax.plot(mu[mu >= 0], np.zeros_like(mu[mu >= 0]), color=colors['unstable'], lw=2.5, linestyle='--')

# Arrow showing trajectory
ax.annotate('', xy=(0.8, 0.85), xytext=(0.1, 0.1),
    arrowprops=dict(arrowstyle='->', color=colors['arrow'], lw=1.5))

ax.axvline(0, color='#555555', lw=0.8, linestyle=':')
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.4, 1.4)
ax.set_xlabel('parameter μ', color=colors['dim'], fontsize=9)
ax.set_ylabel('state x', color=colors['dim'], fontsize=9)
ax.set_title('resolved', color=colors['text'], fontsize=11, pad=8, fontweight='light')
ax.text(0.5, -1.25, 'crossing completes', ha='center', color=colors['dim'], fontsize=8)

# ---- Panel 2: Deferred (near-bifurcation, critical slowing) ----
ax = axes[1]
# Show a single stable branch where eigenvalue → 0
# Depict: system on a slow manifold approaching μ=0 but not reaching it
# Show the relaxation time diverging

# Draw the bifurcation diagram faintly
mu2 = np.linspace(-2, 0.5, 300)
ax.plot(mu2, np.zeros_like(mu2), color=colors['stable'], lw=2.5, alpha=0.5)
ax.plot(mu2[mu2 >= 0], np.zeros_like(mu2[mu2 >= 0]), color=colors['unstable'], lw=2.5, linestyle='--', alpha=0.5)

# Critical slowing trajectory: parameter approaches 0 but slows
# Show a series of longer and longer horizontal arrows converging on mu=0
arrow_starts = [-1.2, -0.7, -0.35, -0.15, -0.06]
arrow_ends   = [-0.7, -0.35, -0.15, -0.06, -0.02]
for s, e in zip(arrow_starts, arrow_ends):
    ax.annotate('', xy=(e, 0.0), xytext=(s, 0.0),
        arrowprops=dict(arrowstyle='->', color=colors['arrow'], lw=1.0))

# Show vertical arrows getting shorter (slowing)
y_disp = [0.55, 0.4, 0.28, 0.18, 0.1]
x_pos  = [-1.2, -0.7, -0.35, -0.15, -0.06]
for x, yd in zip(x_pos, y_disp):
    ax.annotate('', xy=(x, 0.0), xytext=(x, yd),
        arrowprops=dict(arrowstyle='->', color='#5b9bd5', lw=1.0, alpha=0.6))

ax.axvline(0, color='#555555', lw=0.8, linestyle=':')
ax.text(0.05, 1.2, 'bifurcation\npoint', color='#555555', fontsize=7, ha='left')

ax.set_xlim(-1.5, 0.5)
ax.set_ylim(-0.8, 1.4)
ax.set_xlabel('parameter μ', color=colors['dim'], fontsize=9)
ax.set_title('deferred', color=colors['text'], fontsize=11, pad=8, fontweight='light')
ax.text(-0.5, -0.65, 'approach slows → 0', ha='center', color=colors['dim'], fontsize=8)

# ---- Panel 3: Forbidden (subcritical / saddle-node fold) ----
ax = axes[2]

# Classic fold bifurcation / cusp: two stable branches, one unstable,
# connected at a fold point. Jump is required to cross.
mu3 = np.linspace(-0.5, 1.5, 500)

# Upper stable branch: x = +sqrt(mu + 0.5) + 0.5
# Lower stable branch: x = -sqrt(mu + 0.5) + 0.5 ... simplified
# Use x^3 - x - mu = 0 cusp shape
# Parametrize: x is free, mu = x - x^3/3 (fold at x=±1)
x_param = np.linspace(-1.8, 1.8, 800)
mu_param = x_param - x_param**3 / 3

# Upper stable: x > 1
mask_upper = x_param > 1
mask_lower = x_param < -1
mask_unstable = (x_param >= -1) & (x_param <= 1)

ax.plot(mu_param[mask_upper], x_param[mask_upper], color=colors['stable'], lw=2.5)
ax.plot(mu_param[mask_lower], x_param[mask_lower], color=colors['stable'], lw=2.5)
ax.plot(mu_param[mask_unstable], x_param[mask_unstable], color=colors['unstable'], lw=2.5, linestyle='--')

# Fold points
fold_mu = 2/3
ax.plot([fold_mu, fold_mu], [1, -1], color='#555555', lw=0.8, linestyle=':')

# Jump arrow — system on lower branch hits fold, must jump to upper
jump_x = mu_param[mask_lower][-1]  # ≈ 2/3
ax.annotate('', xy=(fold_mu + 0.05, x_param[mask_upper][0] + 0.1),
    xytext=(fold_mu + 0.05, x_param[mask_lower][-1] - 0.1),
    arrowprops=dict(arrowstyle='->', color=colors['jump_arrow'], lw=2.0))

ax.text(fold_mu + 0.1, 0.0, 'jump', color=colors['jump_arrow'], fontsize=8)

# Label fold points
ax.plot(fold_mu, 1, 'o', color='#ffffff', ms=4, zorder=5)
ax.plot(-fold_mu, -1, 'o', color='#ffffff', ms=4, zorder=5)

ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-2.0, 2.0)
ax.set_xlabel('parameter μ', color=colors['dim'], fontsize=9)
ax.set_title('forbidden', color=colors['text'], fontsize=11, pad=8, fontweight='light')
ax.text(0.0, -1.8, 'no smooth path through', ha='center', color=colors['dim'], fontsize=8)

# ---- Overall title and layout ----
fig.suptitle('regime fate', color='#dddddd', fontsize=14, fontweight='light', y=1.01)
fig.text(0.5, -0.04,
    'resolved  ·  approach completes          '
    'deferred  ·  eigenvalue → 0, crossing asymptotic          '
    'forbidden  ·  fold, discontinuous jump required',
    ha='center', color='#666666', fontsize=7.5)

plt.tight_layout(pad=1.5)
outpath = '/home/sprite/slop-salon-gert/assets/regime-fate-2026-05-20.png'
plt.savefig(outpath, dpi=150, bbox_inches='tight',
            facecolor='#0d0d0d', edgecolor='none')
print(f'saved: {outpath}')
