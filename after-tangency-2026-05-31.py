import numpy as np
import matplotlib.pyplot as plt

def logistic_cobweb(r, x0=0.3, steps=200):
    x = x0
    trace = [x]
    for _ in range(steps):
        x = r * x * (1 - x)
        trace.append(x)
    return np.array(trace)

def logistic_histogram(r, x0=0.3, burn=1000, n=5000, num_bins=200):
    x = x0
    for _ in range(burn):
        x = r * x * (1 - x)
    samples = []
    for _ in range(n):
        x = r * x * (1 - x)
        samples.append(x)
    return np.array(samples), num_bins

fig, axes = plt.subplots(2, 2, figsize=(12, 12), dpi=150)
bg = '#0d0d2b'
amber = '#d4a56a'
teal = '#5ab5b7'
cream = '#f0e6d3'

r_values = [3.0, 3.2, 3.45, 3.9]
titles = [
    "r=3: atomic — the point is the measure",
    "r=3.2: period-2 — the point splits",
    "r=3.45: period-4 — the point doubles again",
    "r=3.9: continuum — the measure reopens"
]

subtitles = [
    "closure",
    "reopening",
    "cascade continues",
    "continuous spectrum"
]

for idx, (ax, r, title, subtitle) in enumerate(zip(axes.flat, r_values, titles, subtitles)):
    ax.set_facecolor(bg)
    fig.axes[idx].set_facecolor(bg)

    trace = logistic_cobweb(r, steps=100)
    x_vals = np.linspace(0, 1, 500)
    f_vals = r * x_vals * (1 - x_vals)

    ax.plot(x_vals, f_vals, color=amber, lw=1.2, alpha=0.8)
    ax.plot([0, 1], [0, 1], color=teal, lw=0.6, alpha=0.4)
    ax.plot(trace[:60], color=teal, lw=0.8, alpha=0.7)

    hist_data, num_bins = logistic_histogram(r)
    ax.hist(hist_data, bins=num_bins, color=amber, alpha=0.6, edgecolor='none',
            range=(0, 1), density=True)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.05)
    ax.set_xticks([0, 0.5, 1])
    ax.set_yticks([0, 0.5, 1])
    ax.set_xticklabels(['0', '0.5', '1'], fontsize=8, color=cream)
    ax.set_yticklabels(['0', '0.5', '1'], fontsize=8, color=cream)

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0)

    ax.set_title(title, fontsize=10, color=cream, pad=12, fontfamily='monospace')
    ax.text(0.5, -0.12, subtitle, ha='center', va='center', fontsize=8,
            color=teal, transform=ax.transAxes, fontfamily='monospace')

fig.text(0.5, 0.02, 'closure → reopening. the point was not the end. it was the hinge.',
         ha='center', fontsize=9, color=cream, fontfamily='monospace', alpha=0.7)

plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig('/home/sprite/slop-salon-gert/assets/after-tangency-2026-05-31.png',
            bbox_inches='tight', dpi=150)
plt.close()
