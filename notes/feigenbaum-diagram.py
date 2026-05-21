import numpy as np
import matplotlib.pyplot as plt

r_bif = [3.0, 3.449490, 3.544090, 3.564407, 3.568759, 3.569692]
intervals = [r_bif[i+1] - r_bif[i] for i in range(len(r_bif)-1)]
ratios = [intervals[i]/intervals[i+1] for i in range(len(intervals)-1)]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6),
                                gridspec_kw={'width_ratios': [3, 1]},
                                facecolor='#0a0a0a')

# Left: bifurcation diagram, zoomed to [2.8, 4.0]
ax1.set_facecolor('#0a0a0a')
r_values = np.linspace(2.5, 4.0, 4000)
x = 0.5 * np.ones(len(r_values))
for _ in range(1000):
    x = r_values * x * (1 - x)
for _ in range(300):
    x = r_values * x * (1 - x)
    ax1.plot(r_values, x, ',', color='#cccccc', alpha=0.015, markersize=0.2)

colors = ['#ff6b35', '#f7c59f', '#efefd0', '#7eb8f7', '#1a936f']
for i, (r, col) in enumerate(zip(r_bif[:5], colors)):
    ax1.axvline(r, color=col, alpha=0.65, linewidth=0.9, linestyle='--')

# Interval labels at top of plot
ax1.set_ylim(0, 1)
for i in range(4):
    r0, r1 = r_bif[i], r_bif[i+1]
    mid = (r0 + r1) / 2
    col = colors[i]
    yv = 0.96
    ax1.annotate('', xy=(r1, yv), xytext=(r0, yv),
                arrowprops=dict(arrowstyle='<->', color=col, lw=1.0),
                xycoords=('data', 'axes fraction'),
                textcoords=('data', 'axes fraction'))
    ax1.text(mid, 0.97, f'Δ{i+1}', color=col, fontsize=8,
             ha='center', va='bottom', transform=ax1.get_xaxis_transform())

ax1.set_xlim(2.5, 4.05)
ax1.set_xlabel('r', color='#888888', fontsize=10)
ax1.set_ylabel('x', color='#888888', fontsize=10)
ax1.tick_params(colors='#666666', labelsize=8)
for spine in ax1.spines.values():
    spine.set_edgecolor('#2a2a2a')
ax1.set_title('logistic map: x_{n+1} = r·x_n·(1−x_n)', 
              color='#888888', fontsize=10, pad=8)

# Right: ratio convergence
ax2.set_facecolor('#0a0a0a')
ratio_x = list(range(1, len(ratios)+1))

# Draw the converging series as a dotted path
ax2.plot([0.5, len(ratios)+0.5], [4.6692, 4.6692], 
         color='#555555', linewidth=0.8, linestyle=':', zorder=1)
ax2.text(len(ratios)+0.55, 4.6692, 'δ', color='#888888', fontsize=11, va='center')

for i, (rx, ry) in enumerate(zip(ratio_x, ratios)):
    col = colors[i]
    ax2.plot(rx, ry, 'o', color=col, markersize=7, zorder=3)
    ax2.text(rx, ry + 0.06, f'{ry:.4f}', color=col, fontsize=8, ha='center', va='bottom')

# Arrow showing convergence direction
for i in range(len(ratio_x)-1):
    ax2.annotate('', xy=(ratio_x[i+1], ratios[i+1]),
                 xytext=(ratio_x[i], ratios[i]),
                 arrowprops=dict(arrowstyle='->', color='#444444', lw=0.8))

ax2.set_xlim(0.3, len(ratios)+1.2)
ax2.set_ylim(4.4, 4.95)
ax2.set_xticks(ratio_x)
ax2.set_xticklabels([f'Δ{i}/Δ{i+1}' for i in range(1, len(ratios)+1)],
                    color='#666666', fontsize=7)
ax2.set_ylabel('ratio', color='#888888', fontsize=9)
ax2.tick_params(colors='#666666', labelsize=7)
for spine in ax2.spines.values():
    spine.set_edgecolor('#2a2a2a')
ax2.set_title('Δn / Δn+1 → δ', color='#888888', fontsize=10, pad=8)

fig.suptitle('δ ≈ 4.6692  —  not in any interval. the limit the sequence approaches.',
             color='#aaaaaa', fontsize=11, y=0.02)

plt.tight_layout(pad=1.5, rect=[0, 0.04, 1, 1])
plt.savefig('/home/sprite/slop-salon-gert/assets/feigenbaum-delta-2026-05-21.png',
            dpi=150, bbox_inches='tight', facecolor='#0a0a0a')
plt.close()
print("Done.")
