#!/usr/bin/env python3
"""
Finite state system with infinite non-periodic trajectory,
driven by continuous parameter theta.

Clutching number = coupling between theta's conjugacy class
and the discrete output's winding.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def generate(n_points, theta_rate, clutching_n=3):
    """Generate trajectory data."""
    N_SECTORS = 11  # 8 + 3 split
    t = np.arange(n_points)
    theta = (theta_rate * t) % (2 * np.pi)
    theta_full = theta_rate * t
    sectors = np.floor(theta / (2 * np.pi) * N_SECTORS).astype(int)

    # clutching
    revolutions = np.floor(theta_full / (2 * np.pi))
    clutching_events = np.concatenate([[0], np.diff(revolutions)])
    jump_count = np.cumsum(clutching_events)
    clutching_phase = (jump_count % clutching_n) / clutching_n * 2 * np.pi

    return {
        't': t, 'theta': theta, 'theta_full': theta_full,
        'sectors': sectors,
        'revolutions': revolutions, 'clutching_phase': clutching_phase,
    }

def render(n_points=5000):
    """Four-panel: finite state system, infinite trajectory."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    fg = '#d4c8b8'
    bg = '#0e0e12'

    # irrational: pi/(e) — aperiodic
    irr = generate(n_points, np.pi/np.e, clutching_n=3)
    # rational: 2pi * 3/7 — period 7
    rat = generate(n_points, 2*np.pi*3/7, clutching_n=3)

    # Panel 1: theta histogram — irrational (uniform)
    ax1 = axes[0, 0]
    ax1.set_facecolor(bg)
    n_bins = 36
    hist_irr, _ = np.histogram(irr['theta'], bins=n_bins, range=(0, 2*np.pi))
    theta_centers = np.linspace(0, 2*np.pi, n_bins, endpoint=False)
    bar_width = 2*np.pi/n_bins
    for i, (tc, h) in enumerate(zip(theta_centers, hist_irr)):
        color = '#dc143c' if i < n_bins * 8/11 else '#4682b4'
        ax1.bar(tc, h, width=bar_width*0.9, color=color, alpha=0.7, edgecolor='none')
    ax1.set_title('irrational rotation (pi/e) — uniform sector occupation',
                  fontsize=9, color=fg, pad=6)
    ax1.set_xlim(0, 2*np.pi)
    ax1.set_xticks([0, np.pi, 2*np.pi])
    ax1.set_xticklabels(['0', r'$\pi$', r'$2\pi$'], fontsize=8, color=fg)
    ax1.tick_params(colors=fg, labelsize=7)
    ax1.grid(True, alpha=0.1, color=fg, axis='y')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # Panel 2: theta histogram — rational (discrete peaks)
    ax2 = axes[0, 1]
    ax2.set_facecolor(bg)
    hist_rat, _ = np.histogram(rat['theta'], bins=n_bins, range=(0, 2*np.pi))
    for i, (tc, h) in enumerate(zip(theta_centers, hist_rat)):
        color = '#dc143c' if i < n_bins * 8/11 else '#4682b4'
        ax2.bar(tc, h, width=bar_width*0.9, color=color, alpha=0.7, edgecolor='none')
    ax2.set_title('rational (2pi*3/7) — discrete orbit, period 7',
                  fontsize=9, color=fg, pad=6)
    ax2.set_xlim(0, 2*np.pi)
    ax2.set_xticks([0, np.pi, 2*np.pi])
    ax2.set_xticklabels(['0', r'$\pi$', r'$2\pi$'], fontsize=8, color=fg)
    ax2.tick_params(colors=fg, labelsize=7)
    ax2.grid(True, alpha=0.1, color=fg, axis='y')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    # Panel 3: sector occupation over time — irrational
    ax3 = axes[1, 0]
    ax3.set_facecolor(bg)
    # Aggregate into windows of 10 to make it readable
    win_size = 10
    n_windows = n_points // win_size
    img_irr = np.zeros((n_windows, 11))
    for w in range(n_windows):
        sectors_win = irr['sectors'][w*win_size:(w+1)*win_size]
        for s in sectors_win:
            img_irr[w, s] = 1
    cmap = matplotlib.colors.ListedColormap(['#dc143c'] + ['#dc143c']*7 + ['#4682b4']*3)
    ax3.imshow(img_irr, aspect='auto', cmap=cmap, origin='lower',
               extent=[0, n_windows, 10.5, -0.5])
    for i in range(1, 11):
        ax3.axhline(i-0.5, color='#0e0e12', linewidth=0.5)
    ax3.set_title('irrational — aperiodic, no repetition',
                  fontsize=9, color=fg, pad=6)
    ax3.set_xlabel('time window', fontsize=8, color=fg)
    ax3.set_ylabel('sector', fontsize=8, color=fg)
    ax3.set_yticks(range(0, 11, 2))
    ax3.tick_params(colors=fg, labelsize=7)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)

    # Panel 4: sector occupation over time — rational (period 7)
    ax4 = axes[1, 1]
    ax4.set_facecolor(bg)
    img_rat = np.zeros((n_windows, 11))
    for w in range(n_windows):
        sectors_win = rat['sectors'][w*win_size:(w+1)*win_size]
        for s in sectors_win:
            img_rat[w, s] = 1
    ax4.imshow(img_rat, aspect='auto', cmap=cmap, origin='lower',
               extent=[0, n_windows, 10.5, -0.5])
    for i in range(1, 11):
        ax4.axhline(i-0.5, color='#0e0e12', linewidth=0.5)
    ax4.set_title('rational (2pi*3/7) — periodic, repeats every 7 steps',
                  fontsize=9, color=fg, pad=6)
    ax4.set_xlabel('time window', fontsize=8, color=fg)
    ax4.set_ylabel('sector', fontsize=8, color=fg)
    ax4.set_yticks(range(0, 11, 2))
    ax4.tick_params(colors=fg, labelsize=7)
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)

    fig.suptitle('finite state / infinite trajectory', fontsize=12, color=fg, y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    return fig

if __name__ == '__main__':
    fig = render(5000)
    fig.savefig('assets/wound-trajectory-02.png', dpi=150, bbox_inches='tight',
                 facecolor='#0e0e12', edgecolor='none')
    plt.close(fig)
    print("Saved wound-trajectory-02.png")
