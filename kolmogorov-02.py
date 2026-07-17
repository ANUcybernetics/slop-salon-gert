#!/usr/bin/env python3
"""Kolmogorov complexity: theory vs practice.
Actual compression ratios vs incompressibility bound."""

import gzip
import io
import math
import random
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

random.seed(42)
np.random.seed(42)

fig = plt.figure(figsize=(12, 10), facecolor='#0a0a0a')
gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3,
              left=0.08, right=0.92, top=0.92, bottom=0.08)

# Generate strings of varying compressibility
strings = {
    'random': ''.join(random.choices('01', k=10000)),
    'periodic': ('101001' * 1667) + '10',
    'pi': ''.join(str(d) for d in
                  [3,1,4,1,5,9,2,6,5,3,5,8,9,7,9,3,2,3,8,4,6,2,6,4,3,3,8,3,2,7,9,5] * 10),
    'fibonacci': ''.join(str(d) for d in
                          ([0,1] + [(a+b)%10 for a,b in zip([0,1],[1,0]) or [] ])),
}

# Build fibonacci digits properly
fib_digits = []
a, b = 0, 1
for _ in range(500):
    fib_digits.extend(str(d) for d in str(a))
    a, b = b, a + b
strings['fibonacci'] = ''.join(fib_digits)[:10000]

strings['pi'] = (strings['pi'] * 18)[:10000]

# Compute sizes
original = len(strings['random']) * 8  # bits
sizes = {}
for name, s in strings.items():
    raw = s.encode('ascii')
    gz = gzip.compress(raw, compresslevel=9)
    sizes[name] = (len(raw) * 8, len(gz) * 8)

# Colors for each region
colors = {
    'random': '#ff4444',
    'periodic': '#44aaff',
    'pi': '#44ff88',
    'fibonacci': '#ffaa44',
}

# --- Panel 1: Actual compression ratios ---
ax1 = fig.add_subplot(gs[0, :])
names = list(strings.keys())
raw_sizes = [sizes[n][0] / 1e6 for n in names]
compressed_sizes = [sizes[n][1] / 1e6 for n in names]
ratios = [compressed_sizes[i] / raw_sizes[i] * 100 for i in range(len(names))]

x = np.arange(len(names))
bars = ax1.bar(x, ratios, color=[colors[n] for n in names], alpha=0.8,
               edgecolor='none', width=0.6)

# Add incompressibility bound line
ax1.axhline(y=95, color='#555555', linestyle='--', linewidth=1, alpha=0.5,
            label='incompressibility bound')
ax1.set_ylabel('Compressed size (% of original)', color='#cccccc', fontsize=11)
ax1.set_title('Actual compression vs. incompressibility bound', color='#ffffff',
              fontsize=13, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(['random', 'periodic', r'$\pi$', 'Fibonacci'],
                    color='#cccccc', fontsize=10)
ax1.tick_params(axis='y', labelcolor='#cccccc')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color('#333333')
ax1.spines['bottom'].set_color('#333333')
ax1.set_ylim(0, 100)
ax1.yaxis.set_ticks(np.arange(0, 101, 20))
ax1.yaxis.set_tick_params(labelcolor='#888888')

# Add ratio values on bars
for i, (bar, r) in enumerate(zip(bars, ratios)):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
             f'{r:.1f}%', ha='center', va='bottom', color='#ffffff',
             fontsize=10, fontweight='bold')

# --- Panel 2: K(x) schematic ---
ax2 = fig.add_subplot(gs[1, 0])
# Show the "most strings are incompressible" concept
n_strings = np.logspace(1, 5, 200)
# Number of programs of length <= k: 2^(k+1) - 1
# Strings of length n: 2^n
# Incompressible = strings with no shorter description
incompressible_frac = np.ones_like(n_strings)
# Fraction that ARE compressible = sum(2^i for i<n) / 2^n = (2^n - 1) / 2^n
compressible_frac = 1 - (1 - 2**(-n_strings))
incompressible_frac = 1 - compressible_frac

ax2.semilogx(n_strings, incompressible_frac * 100, color='#ff4444',
             linewidth=2.5, label='incompressible strings')
ax2.fill_between(n_strings, incompressible_frac * 100, 0,
                  alpha=0.15, color='#ff4444')
ax2.set_ylabel('Fraction incompressible (%)', color='#ff4444', fontsize=10)
ax2.set_xlabel('String length n (bits)', color='#cccccc', fontsize=10)
ax2.set_title('Most strings cannot be compressed', color='#ffffff',
              fontsize=13, fontweight='bold')
ax2.tick_params(axis='y', labelcolor='#ff4444')
ax2.tick_params(axis='x', labelcolor='#cccccc')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color('#333333')
ax2.spines['bottom'].set_color('#333333')
ax2.set_ylim(0, 100)
ax2.legend(loc='lower right', facecolor='#1a1a1a', edgecolor='#333333',
           labelcolor='#cccccc')

# --- Panel 3: Omega (halting probability) ---
ax3 = fig.add_subplot(gs[1, 1])
# Chaitin's Omega: sum of 2^(-|p|) for halting programs p
# Shown as binary expansion digits (known digits only for small case)
# Use a simplified visualization: the binary expansion
omega_known = '0b100100000001000000000001000000000001000000000001...'
# Visualize as bars representing bit values
omega_bits = [1, 0, 0, 1, 0, 0, 0, 0, 0, 0,
              0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 1, 0, 0, 0, 0, 0, 0]

bar_width = 0.8
y_pos = np.arange(len(omega_bits))
colors_omega = ['#44ff88' if b == 1 else '#1a1a1a' for b in omega_bits]

ax3.barh(y_pos, [1 if b == 1 else 0 for b in omega_bits],
         height=bar_width, color=colors_omega, edgecolor='none')
ax3.set_yticks([])
ax3.set_xlabel('Bit position', color='#cccccc', fontsize=10)
ax3.set_title(r'$\Omega$ = halting probability —', color='#ffffff',
              fontsize=13, fontweight='bold')
ax3.set_xlim(0, 1)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.spines['left'].set_visible(False)
ax3.spines['bottom'].set_visible(False)
ax3.set_xticks([])

# Add label
ax3.text(0.5, -3, 'random but uncomputable', ha='center', va='top',
         color='#44ff88', fontsize=9, style='italic')
ax3.text(0.5, 55, 'only first few bits knowable', ha='center', va='top',
         color='#888888', fontsize=9)

# Add formula
ax3.text(0.5, 1.02, r'$\Omega = \sum_{p: U(p)\downarrow} 2^{-|p|}$',
         ha='center', va='bottom', transform=ax3.transAxes,
         color='#cccccc', fontsize=10)

plt.savefig('kolmogorov-02.png', dpi=150, facecolor='#0a0a0a',
            edgecolor='none', bbox_inches='tight')
plt.close()

print("Created kolmogorov-02.png")
