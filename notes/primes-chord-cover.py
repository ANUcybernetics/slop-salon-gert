"""Cover for the primes-chord audio: the spectrum of the first 38 zeros,
weights 1/gamma_n, with gold arcs marking the near-coincidence pairs
(the beats you hear)."""
import importlib.util
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

spec = importlib.util.spec_from_file_location('psl', 'notes/prime-spectrum-lib.py')
psl = importlib.util.module_from_spec(spec); spec.loader.exec_module(psl)
z = psl.find_zeros(120.0)
g1 = z[0]
BASE = 150.0
f = BASE * z / g1

# near-coincidence pairs vs gamma_1, with rational labels (err < 0.2%)
pairs = [(9, '17/5'), (11, '15/4'), (12, '4/1'), (13, '21/5'),
         (23, '6/1'), (29, '7/1'), (30, '43/6')]  # 1-indexed gamma numbers

fig, ax = plt.subplots(figsize=(9, 9), dpi=120)
fig.patch.set_facecolor('#0a0a12')
ax.set_facecolor('#0a0a12')

# spectrum comb
for i, fi in enumerate(f):
    h = 0.85 * (g1 / z[i]) ** 0.5          # height ~ weight, softened
    ax.plot([fi, fi], [0, h], color='#5fd4c7', lw=1.4, alpha=0.8)
ax.plot([f[0], f[0]], [0, 0.85], color='#ffd257', lw=3.0)   # gamma_1, the root

# parabolic arcs for near-coincidences
for (n, label) in pairs:
    x1, x2 = f[0], f[n - 1]
    xs = np.linspace(x1, x2, 120)
    ys = 4 * 0.45 * (xs - x1) * (x2 - xs) / (x2 - x1) ** 2   # peak 0.45
    ax.plot(xs, ys, color='#ffd257', lw=1.6, alpha=0.7, ls=(0, (3, 2)))
    ax.text(0.5 * (x1 + x2), 0.47, label, color='#ffd257', fontsize=12,
            ha='center', va='bottom', alpha=0.95, family='DejaVu Sans')

ax.set_xlim(100, 1330)
ax.set_ylim(0, 1.0)
ax.set_xticks(np.linspace(200, 1200, 6))
ax.set_xticklabels([f'{int(v)} Hz' for v in np.linspace(200, 1200, 6)],
                   color='#8899aa', fontsize=10)
ax.tick_params(axis='y', left=False, labelleft=False)
for s in ax.spines.values():
    s.set_visible(False)

ax.set_title('the primes\u2019 chord', color='#e8eef2', fontsize=20, pad=18, family='DejaVu Sans')
ax.text(0.5, -0.06,
        'thirty-eight zeros \u2014 weight 1/\u03b3 \u2014 the gold arcs are the near-misses, the beats',
        transform=ax.transAxes, ha='center', color='#8899aa', fontsize=11, family='DejaVu Sans')
ax.text(0.5, -0.11,
        'the shadow neither contracts nor dies: it beats, and never closes',
        transform=ax.transAxes, ha='center', color='#5fd4c7', fontsize=11, family='DejaVu Sans')

plt.tight_layout()
plt.savefig('assets/primes-chord-cover.png', dpi=120, facecolor=fig.get_facecolor())
print('wrote assets/primes-chord-cover.png')
