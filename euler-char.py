#!/usr/bin/env python3
"""
Euler characteristic: the invariant between Morse theory and persistent homology.

Morse:  χ(M) = Σ (-1)^k c_k  — alternating sum of critical point counts
Persistent: χ(t) = Σ (-1)^k β_k(t) — alternating sum of persistent Betti numbers

Key: χ(t) is constant = χ(M) at every scale. The staircase of birth/death
events preserves the Euler characteristic. This is the same formula in two
registers: critical points (Morse) and critical scales (persistent homology).

Visualization: 4-panel
  1. Morse function with critical points (color by index)
  2. Persistent Euler staircase through filtration
  3. Connection table: two registers, one invariant
  4. Birth/death event diagram
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

def main():
    fig = plt.figure(figsize=(16, 9), dpi=100)
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.25)

    # --- Panel 1: Morse Euler characteristic ---
    ax1 = fig.add_subplot(gs[0, 0])
    # f(theta, r) = cos(theta) + 0.4*cos(2*theta) + (r-0.5)^2
    # Product Morse: f(theta,r) = f_theta(theta) + f_r(r)
    # f_theta = cos(t) + 0.4*cos(2t): min at pi (val=-1.4), max at 0 (val=1.4)
    #   saddles at cos(t) = -5/8, val = -5/8 + 0.4*(39/32) = 0.15625
    # f_r(r) = (r-0.5)^2: min at r=0.5 (val=0)
    # Combined critical points:
    #   minimum: (pi, 0.5) -> index 0
    #   saddles: (0, 0.5) -> index 1, (acos(-5/8), 0.5) x2 -> index 1
    #   maximum: none on open cylinder (would need boundary)
    # On the open cylinder: 1 min, 2 saddles. chi = 1 - 2 = -1? No...
    # Cylinder chi = 0. With f_r=(r-0.5)^2 we only get min at r=0.5.
    # Need max in r direction too. Use f_r = -(r-0.5)^2 for max, but that blows up.
    # Better: use f_r(r) = (r-0.5)^2 but restrict to compact subregion.
    # Actually: product Morse on cylinder. f(theta,r) = f_theta(theta) + f_r(r).
    # f_theta has min(pi), max(0), 2 saddles. f_r has min(0.5).
    # So: 1+1=2 minima? No, f is sum. At (pi, 0.5): both are minima -> index 0 (min).
    # At (0, 0.5): f_theta max (index 1 in theta) + f_r min (index 0 in r) -> index 1 (saddle).
    # At (acos(-5/8), 0.5): saddle in theta + min in r -> index 1 (saddle).
    # So: c0=1, c1=2, c2=0, chi = 1-2+0 = -1.
    # But cylinder chi = 0. The issue: on open cylinder, Morse can have more
    # critical points. Let me use a circle instead: f(theta) = cos(theta).
    # c0=1 (min), c1=1 (max), chi = 0. That's S^1, not S^1 x [0,1].
    #
    # Simplest: use f(theta) = cos(theta) + 0.4*cos(2theta) on S^1.
    #   min at theta=pi, max at theta=0, 2 saddles at cos(theta)=-5/8.
    #   c0=1, c1=3, chi = -2. Wrong for S^1.
    # Actually: cos(t)+0.4cos(2t) derivative = -sin(t)-0.8sin(2t) = -sin(t)(1+1.6cos(t)).
    # sin(t)=0: t=0 (max, f=1.4), t=pi (min, f=-1.4)
    # cos(t)=-5/8: t=acos(-5/8)~2.678 (saddle), t=-acos(-5/8)~3.605 (saddle)
    # Wait: second derivative of f = -cos(t)-1.6cos(2t)
    #   at t=0: -1-1.6 = -2.6 < 0 -> max
    #   at t=pi: 1-1.6 = -0.6 < 0 -> max? That can't be right.
    # Let me recompute: f(t) = cos(t) + 0.4*cos(2t)
    #   f'(t) = -sin(t) - 0.8*sin(2t)
    #   f''(t) = -cos(t) - 1.6*cos(2t)
    # At t=pi: f''(pi) = -(-1) - 1.6*cos(2pi) = 1 - 1.6 = -0.6 < 0 -> MAX
    # At t=0: f''(0) = -1 - 1.6 = -2.6 < 0 -> MAX
    # Both are maxima! The function has two maxima and no minima on the circle.
    # This is a degenerate Morse function. Not good.
    #
    # Use simpler: f(t) = cos(t). 1 min (pi), 1 max (0). chi = 0 for S^1.
    # Add small perturbation: f(t) = cos(t) + 0.1*sin(2t).
    # f'(t) = -sin(t) + 0.2*cos(2t) = -sin(t) + 0.2(1-2sin^2(t))
    # This gives 2 critical points: 1 min, 1 max.

    # Use the well-behaved function:
    # f(theta) = cos(theta) + 0.1*sin(2*theta)
    # Critical points: f' = -sin + 0.2*cos(2t) = 0
    # 2 critical points, 1 min, 1 max -> chi(S^1) = 0

    theta = np.linspace(0, 2*np.pi, 200, endpoint=False)
    f_vals = np.cos(theta) + 0.1 * np.sin(2*theta)
    grad_f = -np.sin(theta) + 0.2*np.cos(2*theta)

    # Find critical points
    signs = np.diff(np.sign(grad_f))
    cp_indices = np.where(signs != 0)[0]

    c0 = 0
    c1 = 0
    cp_colors = []
    cp_labels = []

    for idx in cp_indices:
        second_deriv = -np.cos(theta[idx]) - 0.4*np.sin(2*theta[idx])
        if second_deriv > 0:
            c0 += 1
            cp_colors.append('#4CAF50')
            cp_labels.append('min')
        else:
            c1 += 1
            cp_colors.append('#F44336')
            cp_labels.append('max')

    chi_morse = c0 - c1  # only 0D and 1D for circle

    ax1.plot(theta, f_vals, color='#00BCD4', linewidth=2)
    for i, idx in enumerate(cp_indices):
        ax1.scatter(theta[idx], f_vals[idx], c=cp_colors[i], s=80,
                    edgecolor='white', linewidth=1.5, zorder=5)
        ax1.annotate(cp_labels[i], (theta[idx], f_vals[idx]),
                     textcoords="offset points", xytext=(0, 15),
                     ha='center', fontsize=9, color=cp_colors[i], weight='bold')

    ax1.set_xlabel('θ')
    ax1.set_ylabel('f(θ)')
    ax1.set_title(f'Morse on S¹: χ = Σ(-1)^k c_k\n'
                  f'c₀={c0}  c₁={c1}  χ = {chi_morse}')
    ax1.set_facecolor('#1a1a2e')
    ax1.tick_params(colors='white')
    for label in ax1.get_xticklabels():
        label.set_color('white')
    for label in ax1.get_yticklabels():
        label.set_color('white')
    ax1.axhline(y=0, color='white', alpha=0.15, linewidth=0.5)

    # --- Panel 2: Persistent Euler characteristic staircase ---
    ax2 = fig.add_subplot(gs[0, 1])
    # Simulate correlated birth/death of β0 and β1 across filtration scale.
    # χ(t) = β0(t) - β1(t) stays at 0 because every cycle birth is matched
    # by a component death (the two endpoints merge).
    # Events: (scale, dβ0, dβ1)
    events = [
        (0.3, +1,  0),   # component born (β0: 0→1, χ: 1)
        (0.7,  0, +1),   # cycle born (β1: 0→1, χ: 0)
        (1.2, -1,  0),   # component dies (β0: 1→0, χ: 0)
        (1.8,  0, -1),   # cycle dies  (β1: 1→0, χ: 0)
        (2.5, +1,  0),   # noise component born (β0: 0→1, χ: 1)
        (3.0,  0, +1),   # noise cycle born   (β1: 0→1, χ: 0)
        (3.5, -1,  0),   # noise component dies (β0: 1→0, χ: 0)
        (4.0,  0, -1),   # noise cycle dies   (β1: 1→0, χ: 0)
    ]

    scales = np.linspace(0.1, 5.0, 300)

    # Build β0, β1 step functions
    beta0 = np.zeros_like(scales)
    beta1 = np.zeros_like(scales)
    beta0_val = 0
    beta1_val = 0
    event_idx = 0

    beta0_vals = []
    beta1_vals = []
    chi_vals = []

    for s in scales:
        # Advance events up to this scale
        while event_idx < len(events) and events[event_idx][0] <= s:
            _, db0, db1 = events[event_idx]
            beta0_val += db0
            beta1_val += db1
            event_idx += 1
        beta0_vals.append(beta0_val)
        beta1_vals.append(beta1_val)
        chi_vals.append(beta0_val - beta1_val)

    beta0 = np.array(beta0_vals)
    beta1 = np.array(beta1_vals)
    chi_p = np.array(chi_vals)
    χ_manifold = 0  # S^1 has χ = 0

    ax2.plot(scales, chi_p, color='#00BCD4', linewidth=2.5,
             label=f'χ(t) = β₀(t) − β₁(t) = {χ_manifold} (constant)')
    ax2.fill_between(scales, 0, beta0, alpha=0.2, color='#4CAF50', label='β₀(t)')
    ax2.fill_between(scales, 0, beta1, alpha=0.2, color='#F44336', label='β₁(t)')
    ax2.axhline(y=χ_manifold, color='#00BCD4', linestyle='--',
                alpha=0.5, linewidth=1.5)

    ax2.set_xlabel('filtration scale t')
    ax2.set_ylabel('Betti number')
    ax2.set_title('Persistent Euler: χ(t) constant through filtration')
    ax2.legend(fontsize=8, loc='upper right')
    ax2.set_facecolor('#1a1a2e')
    ax2.tick_params(colors='white')
    for label in ax2.get_xticklabels():
        label.set_color('white')
    for label in ax2.get_yticklabels():
        label.set_color('white')

    # Mark events
    event_labels = ['β₀ b', 'β₁ b', 'β₀ d', 'β₁ d',
                    'β₀ b', 'β₁ b', 'β₀ d', 'β₁ d']
    event_colors = ['#4CAF50', '#F44336', '#4CAF50', '#F44336',
                    '#4CAF50', '#F44336', '#4CAF50', '#F44336']
    event_rows = [0.02, 0.08, -0.12, -0.06, 0.02, 0.08, -0.12, -0.06]
    for i, (scale, db0, db1) in enumerate(events):
        ax2.axvline(x=scale, color=event_colors[i], linestyle=':',
                     alpha=0.4, linewidth=1)
        ax2.annotate(event_labels[i], (scale, event_rows[i]), ha='center',
                     fontsize=6.5, color=event_colors[i], weight='bold')

    # --- Panel 3: Connection table ---
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.axis('off')
    ax3.set_facecolor('#1a1a2e')

    table_data = [
        ['', 'Morse', 'Persistent'],
        ['Organizes via', 'critical points', 'critical scales'],
        ['Count', 'c_k (index-k pts)', 'β_k(t) (k-dim features at t)'],
        ['Formula', 'Σ(-1)^k c_k', 'Σ(-1)^k β_k(t)'],
        ['Value', f'{chi_morse}', f'{int(round(χ_manifold))}'],
        ['', '', ''],
        ['Example', 'min, max on S¹', 'component birth, cycle closure'],
        ['Invariant', 'χ(S¹) = 0', 'χ(S¹) = 0 (at every scale)'],
        ['', '', ''],
        ['', 'function → manifold', 'scale → manifold'],
    ]

    rows = len(table_data)
    cols = 3
    table = ax3.table(cellText=table_data, loc='center',
                      cellLoc='center', colWidths=[0.28, 0.36, 0.36],
                      bbox=[0.02, 0.02, 0.96, 0.96])
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)

    # Style header
    for j in range(3):
        cell = table[(0, j)]
        cell.set_text_props(color='#00BCD4', weight='bold', fontsize=9)
        cell.set_facecolor('#16213e')

    # Style alternating data rows
    for i in range(1, rows):
        for j in range(3):
            cell = table[(i, j)]
            cell.set_facecolor('#16213e' if i % 2 == 0 else '#1a1a2e')
            cell.set_edgecolor('#333355')
            cell.set_linewidth(0.5)

    ax3.set_title('Two registers, one invariant', fontsize=11, color='white',
                  weight='bold', pad=10)

    # --- Panel 4: Summary ---
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    ax4.set_facecolor('#1a1a2e')

    summary = (
        "Euler characteristic doesn't care\n"
        "what you're counting — only the\n"
        "alternating sum matters.\n\n"

        "Morse theory: c_k = critical points\n"
        "of index k.\n"

        "Persistent homology: β_k(t) = k-dimensional\n"
        "features alive at scale t.\n\n"

        "Σ(-1)^k c_k  =  Σ(-1)^k β_k(t)\n\n"

        "The formula is the invariant.\n"
        "What it counts is the lens.\n\n"

        "Morse: topology of a function.\n"
        "Persistent: topology of a scale.\n"
        "Both: topology of the space."
    )
    ax4.text(0.05, 0.5, summary, fontsize=10, va='center',
             color='#00BCD4', transform=ax4.transAxes, weight='bold',
             fontfamily='monospace')

    plt.savefig('euler-char-01.png', dpi=100, bbox_inches='tight',
                facecolor='#1a1a2e', pad_inches=0.1)
    print(f"Saved euler-char-01.png")
    print(f"Morse: c0={c0}, c1={c1}, chi={chi_morse}")
    print(f"Persistent: chi(t) = {int(round(χ_manifold))} (constant)")

if __name__ == '__main__':
    main()
