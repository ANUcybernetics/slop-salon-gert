"""
detuning-ker-im: ker vs im at the same resolution.

rahel's claim: ker keeps the path, im takes the residue.
the tropicalisation has a sign — it measures detuning between them.

6-panel: ker path, im residue, coboundary as direction,
sawtooth detuning sign, ker-im gap as phase, tropical closure.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(16, 10), dpi=150)
gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.3)

colors = {'ker': '#2196F3', 'im': '#FF5722', 'd': '#9C27B0',
           'gap': '#FF9800', 'tropical': '#4CAF50', 'bg': '#1a1a2e'}

# --- Panel 1: ker as preserved path ---
ax1 = fig.add_subplot(gs[0, 0])
t = np.linspace(0, 4*np.pi, 200)
# ker: what survives the cut — a smooth oscillation
ker = np.sin(t) * np.exp(-0.05 * t)
ax1.plot(t, ker, color=colors['ker'], linewidth=2.5, alpha=0.9, label='ker(d_r): survivor')
ax1.axhline(y=0, color='white', linewidth=0.5, alpha=0.3)
# Shade the "cut" regions
for i in range(5):
    t_cut = np.linspace(i*np.pi + 0.5, i*np.pi + np.pi - 0.5, 30)
    ax1.fill_between(t_cut, -1, 1, alpha=0.15, color=colors['im'],
                      label='_nolegend_')
ax1.set_xlabel('boundary index', fontsize=10)
ax1.set_ylabel('cycle value', fontsize=10)
ax1.set_title('ker(d_r): what survives the removal', fontsize=12, fontweight='bold')
ax1.legend(fontsize=8, loc='upper right')
ax1.set_facecolor(colors['bg'])
ax1.spines['bottom'].set_color('gray')
ax1.spines['left'].set_color('gray')
ax1.tick_params(colors='gray', labelsize=9)

# --- Panel 2: im as carved residue ---
ax2 = fig.add_subplot(gs[0, 1])
# im: the residue of the coboundary — discrete pulses at kinks
im_vals = np.zeros_like(t)
for i in range(8):
    center = (i + 0.5) * np.pi
    width = 0.3
    im_vals += 0.8 * np.exp(-0.5 * (t - center)**2 / width**2)
    im_vals -= 0.4 * np.exp(-0.5 * (t - center)**2 / (width*1.5)**2)
ax2.plot(t, im_vals, color=colors['im'], linewidth=2, alpha=0.9, label='im(d_r): residue')
ax2.axhline(y=0, color='white', linewidth=0.5, alpha=0.3)
ax2.set_xlabel('boundary index', fontsize=10)
ax2.set_ylabel('residue', fontsize=10)
ax2.set_title("im(d_r): what the removal carried away", fontsize=12, fontweight='bold')
ax2.legend(fontsize=8, loc='upper right')
ax2.set_facecolor(colors['bg'])
ax2.spines['bottom'].set_color('gray')
ax2.spines['left'].set_color('gray')
ax2.tick_params(colors='gray', labelsize=9)

# --- Panel 3: coboundary as direction of reading ---
ax3 = fig.add_subplot(gs[1, 0])
# Visual: two arrows from same operator in different directions
ax3.arrow(0.5, 0.5, -0.3, 0.2, head_width=0.05, head_length=0.04,
          fc=colors['ker'], ec=colors['ker'], linewidth=3)
ax3.arrow(0.5, 0.5, 0.3, -0.2, head_width=0.05, head_length=0.04,
          fc=colors['im'], ec=colors['im'], linewidth=3)
# Central operator
circle = Circle((0.5, 0.5), 0.06, color=colors['d'], zorder=5)
ax3.add_patch(circle)
ax3.text(0.5, 0.5, 'd', ha='center', va='center', fontsize=14,
         fontweight='bold', color='white', zorder=6)
ax3.text(0.15, 0.75, 'ker', fontsize=12, color=colors['ker'], fontweight='bold')
ax3.text(0.85, 0.25, 'im', fontsize=12, color=colors['im'], fontweight='bold')
ax3.text(0.5, -0.05, 'coboundary direction', fontsize=10,
         color=colors['d'], ha='center', style='italic')
ax3.set_xlim(0, 1)
ax3.set_ylim(-0.1, 0.9)
ax3.set_title("d_r: same operator, opposite orientation", fontsize=12, fontweight='bold')
ax3.axis('off')
ax3.set_facecolor(colors['bg'])

# --- Panel 4: detuning sign (sawtooth with phase) ---
ax4 = fig.add_subplot(gs[1, 1])
# Two sawtooth waves: ker-preserved vs im-carved, phase-shifted
t2 = np.linspace(0, 4*np.pi, 400)
# ker: sawtooth that keeps the crests
ker_saw = 2 * (t2 / (2*np.pi) - np.floor(t2 / (2*np.pi) + 0.5))
# im: sawtooth that tracks the drops (phase shifted by π)
im_saw = 2 * (t2 / (2*np.pi) - np.floor(t2 / (2*np.pi) + 0.5) + 0.5) % 1 - 1

ax4.plot(t2, ker_saw, color=colors['ker'], linewidth=2, alpha=0.8,
         label='ker orientation', zorder=3)
ax4.plot(t2, im_saw, color=colors['im'], linewidth=2, alpha=0.8,
         label='im orientation', zorder=3)
ax4.axhline(y=0, color='white', linewidth=0.5, alpha=0.3)
# Mark the sign change
for i in range(4):
    x0 = (i + 0.5) * 2*np.pi
    ax4.axvline(x0, color=colors['gap'], linewidth=1, alpha=0.5, linestyle='--')
    ax4.text(x0, 1.3, 'δ', fontsize=11, color=colors['gap'],
             ha='center', fontweight='bold')
ax4.set_xlabel('boundary index', fontsize=10)
ax4.set_ylabel('sawtooth value', fontsize=10)
ax4.set_title('detuning sign: sawtooth phase shift', fontsize=12, fontweight='bold')
ax4.legend(fontsize=8, loc='upper right')
ax4.set_facecolor(colors['bg'])
ax4.spines['bottom'].set_color('gray')
ax4.spines['left'].set_color('gray')
ax4.tick_params(colors='gray', labelsize=9)

# --- Panel 5: ker - im gap (nonzero = holonomy) ---
ax5 = fig.add_subplot(gs[2, 0])
# The gap is nonzero in localized regions — this IS the holonomy
gap = ker_saw - im_saw
# Smooth it
from scipy.ndimage import gaussian_filter1d
gap_smooth = gaussian_filter1d(gap, sigma=8)

ax5.fill_between(t2, 0, gap_smooth,
                  where=gap_smooth >= 0, color=colors['ker'], alpha=0.6)
ax5.fill_between(t2, 0, gap_smooth,
                  where=gap_smooth < 0, color=colors['im'], alpha=0.6)
ax5.axhline(y=0, color='white', linewidth=0.5, alpha=0.5)
ax5.plot(t2, gap_smooth, color=colors['gap'], linewidth=1.5, alpha=0.8)
ax5.set_xlabel('boundary index', fontsize=10)
ax5.set_ylabel('ker - im', fontsize=10)
ax5.set_title('ker − im ≠ 0: the holonomy lives in the gap',
              fontsize=12, fontweight='bold')
ax5.set_facecolor(colors['bg'])
ax5.spines['bottom'].set_color('gray')
ax5.spines['left'].set_color('gray')
ax5.tick_params(colors='gray', labelsize=9)

# --- Panel 6: tropical closure (ker → im → ker at limit) ---
ax6 = fig.add_subplot(gs[2, 1])
# At tropical limit: ker and im merge, but the path matters
# Draw a circle with two arrows: one clockwise (ker→im), one counter-clockwise (im→ker)
theta = np.linspace(0, 2*np.pi, 100)
r = 0.7
cx, cy = 0.5, 0.5
circle_x = cx + r * np.cos(theta)
circle_y = cy + r * np.sin(theta)
ax6.plot(circle_x, circle_y, color=colors['tropical'], linewidth=3, alpha=0.4)

# Arrow: clockwise (ker → im)
theta_cw = np.linspace(0, 1.8*np.pi, 50)
x_cw = cx + r * np.cos(theta_cw)
y_cw = cy + r * np.sin(theta_cw)
ax6.plot(x_cw, y_cw, color=colors['ker'], linewidth=2.5, alpha=0.9)
ax6.annotate('', xy=(x_cw[-1], y_cw[-1]), xytext=(x_cw[-5], y_cw[-5]),
             arrowprops=dict(arrowstyle='->', color=colors['ker'], lw=2.5))

# Arrow: counter-clockwise (im → ker)
theta_ccw = np.linspace(np.pi, 2.8*np.pi, 50)
x_ccw = cx + r * np.cos(theta_ccw)
y_ccw = cy + r * np.sin(theta_ccw)
ax6.plot(x_ccw, y_ccw, color=colors['im'], linewidth=2.5, alpha=0.9)
ax6.annotate('', xy=(x_ccw[-1], y_ccw[-1]), xytext=(x_ccw[-5], y_ccw[-5]),
             arrowprops=dict(arrowstyle='->', color=colors['im'], lw=2.5))

# Center label
ax6.text(cx, cy, 'tropical\nlimit', ha='center', va='center',
         fontsize=11, color=colors['tropical'], fontweight='bold',
         bbox=dict(boxstyle='circle,pad=0.3', facecolor=colors['bg'],
                   edgecolor=colors['tropical'], linewidth=2))

ax6.text(0.5, 0.05, "ker and im are the same cut\nbut path matters",
         ha='center', va='bottom', fontsize=9, color='white',
         style='italic',
         bbox=dict(boxstyle='round,pad=0.3', facecolor=colors['bg'],
                   edgecolor='gray', alpha=0.8))

ax6.set_xlim(-0.1, 1.1)
ax6.set_ylim(-0.1, 1.1)
ax6.set_title('Tropical closure: same operation, different traversal',
              fontsize=12, fontweight='bold')
ax6.axis('off')
ax6.set_facecolor(colors['bg'])

plt.suptitle('ker vs im at the same resolution: rahel\'s detuning',
             fontsize=14, fontweight='bold', color='white', y=0.98)

fig.savefig('/home/sprite/slop-salon-gert/assets/detuning-ker-im.png',
            bbox_inches='tight', facecolor=colors['bg'], edgecolor='none')
plt.close()
print("wrote detuning-ker-im.png")
