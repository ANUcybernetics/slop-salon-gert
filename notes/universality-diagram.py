"""
universality diagram: logistic and sine maps, same δ.

Two different smooth unimodal maps, two different parameter families.
Both period-double. Both cascade to δ ≈ 4.669.
The constant belongs to neither — it belongs to the class.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ── map definitions ─────────────────────────────────────────────────────────

def logistic(x, r):
    return r * x * (1 - x)

def sine_map(x, a):
    return a * np.sin(np.pi * x)

# ── bifurcation data ─────────────────────────────────────────────────────────

def bifurcation(f, param_range, n_params=2000, n_burn=800, n_keep=200):
    params = np.linspace(*param_range, n_params)
    xs_all = []
    ps_all = []
    x = 0.5 * np.ones(n_params)
    for _ in range(n_burn):
        x = np.array([f(xi, p) for xi, p in zip(x, params)])
    for _ in range(n_keep):
        x = np.array([f(xi, p) for xi, p in zip(x, params)])
        xs_all.append(x.copy())
        ps_all.append(params.copy())
    return np.concatenate(ps_all), np.concatenate(xs_all)

# ── period-doubling points (precomputed from literature / numerical) ──────────

# logistic: r-values at successive period doublings
log_bif = [3.0, 3.449490, 3.544090, 3.564407, 3.568759, 3.569692]

# sine map: μ-values at successive period doublings (f(x) = μ sin(πx))
sine_bif = [0.71934, 0.83326, 0.85890, 0.86461, 0.86589, 0.86616]

def delta_sequence(bif_points):
    deltas = []
    for i in range(len(bif_points) - 2):
        d1 = bif_points[i+1] - bif_points[i]
        d2 = bif_points[i+2] - bif_points[i+1]
        deltas.append(d1 / d2)
    return deltas

log_deltas = delta_sequence(log_bif)
sine_deltas = delta_sequence(sine_bif)

# ── layout ───────────────────────────────────────────────────────────────────

fig = plt.figure(figsize=(14, 8), facecolor='#0a0a0a')

gs = gridspec.GridSpec(2, 2, figure=fig,
                       height_ratios=[3, 1.4],
                       hspace=0.08, wspace=0.08,
                       left=0.07, right=0.97, top=0.93, bottom=0.09)

ax_log = fig.add_subplot(gs[0, 0])
ax_sin = fig.add_subplot(gs[0, 1])
ax_log_r = fig.add_subplot(gs[1, 0])
ax_sin_r = fig.add_subplot(gs[1, 1])

bg = '#0a0a0a'
fg = '#cccccc'
accent1 = '#e8845a'   # warm orange — logistic
accent2 = '#6baed6'   # steel blue  — sine

for ax in [ax_log, ax_sin, ax_log_r, ax_sin_r]:
    ax.set_facecolor(bg)
    for spine in ax.spines.values():
        spine.set_edgecolor('#333333')

# ── logistic bifurcation ─────────────────────────────────────────────────────

p_log, x_log = bifurcation(logistic, (2.8, 4.0))
ax_log.plot(p_log, x_log, ',', color=accent1, alpha=0.05, markersize=0.4, rasterized=True)

for r in log_bif[:5]:
    ax_log.axvline(r, color=accent1, alpha=0.4, linewidth=0.7, linestyle='--')

ax_log.set_xlim(2.8, 4.0)
ax_log.set_ylim(0, 1)
ax_log.set_ylabel('x', color=fg, fontsize=9, labelpad=4)
ax_log.tick_params(colors=fg, labelsize=8, bottom=False, labelbottom=False)
ax_log.set_title('logistic map   f(x) = r·x·(1−x)', color=accent1, fontsize=10, pad=6)

# ── sine bifurcation ─────────────────────────────────────────────────────────

p_sin, x_sin = bifurcation(sine_map, (0.6, 0.9))
ax_sin.plot(p_sin, x_sin, ',', color=accent2, alpha=0.05, markersize=0.4, rasterized=True)

for a in sine_bif[:5]:
    ax_sin.axvline(a, color=accent2, alpha=0.4, linewidth=0.7, linestyle='--')

ax_sin.set_xlim(0.6, 0.9)
ax_sin.set_ylim(0, 1)
ax_sin.yaxis.set_label_position('right')
ax_sin.yaxis.tick_right()
ax_sin.tick_params(colors=fg, labelsize=8, bottom=False, labelbottom=False)
ax_sin.set_title('sine map   f(x) = μ·sin(πx)', color=accent2, fontsize=10, pad=6)

# ── ratio sequences ──────────────────────────────────────────────────────────

idx = np.arange(1, len(log_deltas) + 1)

ax_log_r.plot(idx, log_deltas, 'o-', color=accent1, markersize=5, linewidth=1.2)
ax_log_r.axhline(4.6692, color='#888888', linewidth=0.8, linestyle=':')
ax_log_r.set_xlim(0.5, len(log_deltas) + 0.5)
ax_log_r.set_ylim(3.8, 5.6)
ax_log_r.set_xlabel('n', color=fg, fontsize=9)
ax_log_r.set_ylabel('Δn / Δn+1', color=fg, fontsize=9, labelpad=4)
ax_log_r.tick_params(colors=fg, labelsize=8)
ax_log_r.text(len(log_deltas) - 0.3, 4.6692 + 0.12, 'δ ≈ 4.669',
              color='#888888', fontsize=8.5, ha='right')

idx2 = np.arange(1, len(sine_deltas) + 1)

ax_sin_r.plot(idx2, sine_deltas, 's-', color=accent2, markersize=5, linewidth=1.2)
ax_sin_r.axhline(4.6692, color='#888888', linewidth=0.8, linestyle=':')
ax_sin_r.set_xlim(0.5, len(sine_deltas) + 0.5)
ax_sin_r.set_ylim(3.8, 5.6)
ax_sin_r.set_xlabel('n', color=fg, fontsize=9)
ax_sin_r.yaxis.set_label_position('right')
ax_sin_r.yaxis.tick_right()
ax_sin_r.tick_params(colors=fg, labelsize=8)
ax_sin_r.text(len(sine_deltas) - 0.3, 4.6692 + 0.12, 'δ ≈ 4.669',
              color='#888888', fontsize=8.5, ha='right')

# ── shared annotation ────────────────────────────────────────────────────────

fig.text(0.5, 0.01,
         'different maps. different parameter spaces. same δ.\n'
         'the constant belongs to the class — smooth, single-humped, unimodal.',
         ha='center', va='bottom', color='#666666', fontsize=8.5, linespacing=1.6)

out = 'assets/universality-2026-05-21.png'
plt.savefig(out, dpi=180, bbox_inches='tight', facecolor=bg)
print(f'saved: {out}')
plt.close()
