"""
Four interval types — direct frequency trajectory plot.
Cleaner than a spectrogram: shows exactly the shape of each type.

[t₀, t₁]   — flat line at 440 Hz, terminates
[t₀, t*)   — curve from 320→440 Hz, asymptotes (excluded endpoint)
[t₀, ∞)    — rising line, 260 Hz + 80 Hz/s, no endpoint
∅           — blank: nothing to draw
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, axes = plt.subplots(1, 4, figsize=(13, 4), sharey=True)
fig.patch.set_facecolor('#080808')
for ax in axes:
    ax.set_facecolor('#0d0d0d')

DUR = 2.0
t = np.linspace(0, DUR, 1000)
TAU = 0.35
START_FREQ, TARGET_FREQ = 320, 440
GLISS_START, GLISS_RATE = 260, 80

colors = {
    'line': '#e8804a',
    'endpoint': '#ffffff',
    'asymptote': '#444444',
    'label': '#cccccc',
    'sub': '#777777',
}

# --- panel 1: [t₀, t₁] ---
ax = axes[0]
ax.plot(t, np.full_like(t, 440), color=colors['line'], linewidth=2.0)
ax.plot(DUR, 440, 'o', color=colors['endpoint'], markersize=7, zorder=5)
ax.set_title(r'$[t_0,\, t_1]$', color=colors['label'], fontsize=14, pad=8,
             fontfamily='serif')
ax.set_xlabel('closed', color=colors['sub'], fontsize=10)

# --- panel 2: [t₀, t*) ---
ax = axes[1]
freq_approach = TARGET_FREQ - (TARGET_FREQ - START_FREQ) * np.exp(-t / TAU)
ax.plot(t, freq_approach, color=colors['line'], linewidth=2.0)
# dashed asymptote
ax.axhline(TARGET_FREQ, color=colors['asymptote'], linewidth=1.0,
           linestyle='--', zorder=1)
# open endpoint marker
ax.plot(DUR, freq_approach[-1], 'o', color='#0d0d0d', markersize=8,
        markeredgecolor=colors['endpoint'], markeredgewidth=1.5, zorder=5)
ax.set_title(r'$[t_0,\, t^*)$', color=colors['label'], fontsize=14, pad=8,
             fontfamily='serif')
ax.set_xlabel('fold', color=colors['sub'], fontsize=10)

# --- panel 3: [t₀, ∞) ---
ax = axes[2]
freq_gliss = GLISS_START + GLISS_RATE * t
ax.plot(t, freq_gliss, color=colors['line'], linewidth=2.0)
# arrow at end indicating continuation
ax.annotate('', xy=(DUR + 0.12, freq_gliss[-1] + GLISS_RATE * 0.12),
            xytext=(DUR, freq_gliss[-1]),
            arrowprops=dict(arrowstyle='->', color=colors['endpoint'],
                            lw=1.5))
ax.set_title(r'$[t_0,\, \infty)$', color=colors['label'], fontsize=14, pad=8,
             fontfamily='serif')
ax.set_xlabel('processual', color=colors['sub'], fontsize=10)

# --- panel 4: ∅ ---
ax = axes[3]
ax.text(DUR / 2, 370, r'$\emptyset$', color='#555555', fontsize=36,
        ha='center', va='center', fontfamily='serif')
ax.set_title(r'$\emptyset$', color=colors['label'], fontsize=14, pad=8,
             fontfamily='serif')
ax.set_xlabel('constitutive', color=colors['sub'], fontsize=10)

# shared formatting
for ax in axes:
    ax.set_ylim(220, 500)
    ax.set_xlim(-0.05, DUR + 0.2)
    ax.set_xticks([])
    ax.tick_params(colors='#555555', labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor('#2a2a2a')
    # 440 Hz reference (quiet)
    ax.axhline(440, color='#222222', linewidth=0.5, zorder=0)

axes[0].set_ylabel('frequency', color='#666666', fontsize=10)
axes[0].set_yticks([260, 320, 380, 440])
axes[0].set_yticklabels(['260', '320', '380', '440'], color='#555555')

fig.suptitle('four interval types as sound', color='#aaaaaa', fontsize=12,
             fontweight='normal', y=1.02)

plt.tight_layout()
plt.savefig('assets/four-intervals-trajectories-2026-05-21.png',
            dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.close()
print("wrote assets/four-intervals-trajectories-2026-05-21.png")
