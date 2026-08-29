#!/usr/bin/env python3
"""The renormalization, verified: the Riemann zeros enter the operator's strip at
half height, mirrored across the shore.

  phi(s) = sqrt(pi) Gamma(s-1/2)/Gamma(s) * zeta(2s-1)/zeta(2s)
    poles at s = rho/2 = 1/4 + i gamma/2      (the halved Riemann zeros)
    zeros at s = (1+rho)/2 = 3/4 + i gamma/2  (the mirror, across Re s = 1/2)
    the count's pole at s = 1, mirror zero at s = 0

Three structural seats, descending by octaves: 2^0 (count), 2^-1 (shore),
2^-2 (the zeros). The continuation halves both coordinates.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import mpmath as mp
mp.mp.dps = 25

GOLD  = '#e3b341'
AMBER = '#d08c60'
TEAL  = '#4ec9b0'
ROSE  = '#d25f7f'
INK   = '#0d1117'
GRID  = '#2a3140'
TXT   = '#d6dae0'

def phi(s):
    return mp.sqrt(mp.pi) * mp.gamma(s - mp.mpf('0.5')) / mp.gamma(s) \
           * mp.zeta(2*s - 1) / mp.zeta(2*s)

# ---- data -------------------------------------------------------------
gams = [mp.im(mp.zetazero(n)) for n in range(1, 11)]
half = [float(g / 2) for g in gams]          # t = gamma/2
maass = [9.5337, 13.7796, 18.850, 22.526, 24.778]   # literature PSL(2,Z) zeros

ts = np.linspace(5.0, 27.0, 400)
logphi_pole  = np.array([float(mp.log10(abs(phi(mp.mpf('0.25') + 1j*t)))) for t in ts])
logphi_mirr  = np.array([float(mp.log10(abs(phi(mp.mpf('0.75') + 1j*t)))) for t in ts])
# exact pole/zero heights, evaluated epsilon off the pole (so log10 stays finite)
EPS = mp.mpf('1e-7')
pole_heights = [float(mp.log10(abs(phi(mp.mpf('0.25') + 1j*(g/2 + EPS))))) for g in gams]
zero_heights = [float(mp.log10(abs(phi(mp.mpf('0.75') + 1j*g/2)))) for g in gams]

# even-operator resonance depth near the shore (distance of the leading eig to 1)
import sys
sys.path.insert(0, 'notes')
from selberg_lib import nearest
xs = 0.5 * (1 + np.cos(np.pi * (np.arange(44) + 0.5) / 44))
K, N = 30, 6000
sigt = 0.505
dts = np.arange(5.0, 26.5, 0.15)
depth_even = np.array([nearest(sigt + 1j*t, xs, K, False, N)[1] for t in dts])

# ---- figure -----------------------------------------------------------
fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.2, 5.2), dpi=200,
                               gridspec_kw={'width_ratios': [1.08, 1.0]})
fig.patch.set_facecolor(INK)
for ax in (axL, axR):
    ax.set_facecolor(INK)
    ax.tick_params(colors=TXT, labelsize=8)
    for sp in ax.spines.values():
        sp.set_color(GRID)

# ---- left: the s-plane ------------------------------------------------
ax = axL
ax.set_xlim(-0.15, 1.15); ax.set_ylim(0, 29)
ax.set_xlabel(r'Re $s$', color=TXT, fontsize=10)
ax.set_ylabel(r'Im $s = t$', color=TXT, fontsize=10)
ax.set_title('three seats, halving', color=TXT, fontsize=11)

# structural lines
ax.axvline(1.0,   color=GOLD, lw=2.2, zorder=2)
ax.axvline(0.5,   color=AMBER, lw=1.8, zorder=2)
ax.axvline(0.25,  color=TEAL, lw=2.2, zorder=2)
ax.axvline(0.75,  color=ROSE, lw=1.4, ls='--', zorder=2)

# labels
ax.text(1.0, 27.6, 'count\n2$^0$ · ζ pole · Z zero', color=GOLD, fontsize=8, ha='center', va='top')
ax.text(0.5, 27.6, 'shore\n2$^{-1}$ · Maass', color=AMBER, fontsize=8, ha='center', va='top')
ax.text(0.25, 25.0, 'ρ/2 · poles of φ\n2$^{-2}$', color=TEAL, fontsize=8, ha='center', va='top')
ax.text(0.75, 25.0, '(1+ρ)/2\nzeros, mirrored', color=ROSE, fontsize=8, ha='center', va='top')

# count diamond and its mirror zero
ax.plot([1.0], [0.0], marker='D', ms=8, color=GOLD, mec='white', mew=0.4, zorder=5)
ax.plot([0.0], [0.0], marker='o', ms=7, mfc=INK, mec=GOLD, mew=1.2, zorder=5)
ax.annotate('', xy=(1.0, 0.2), xytext=(0.0, 0.2),
            arrowprops=dict(arrowstyle='-|>', color=GOLD, lw=0.9, ls=':'))

# zeta-zero ticks at half height on Re=1/4, and mirrors on Re=3/4
for t in half:
    ax.plot(0.25, t, marker='_', ms=9, color=TEAL, lw=2, zorder=4)
    ax.plot(0.75, t, marker='_', ms=9, color=ROSE, lw=2, zorder=4)
# one mirror arrow
ax.annotate('', xy=(0.73, half[0]), xytext=(0.27, half[0]),
            arrowprops=dict(arrowstyle='<|-|>', color=ROSE, lw=0.9, ls=':'))

# Maass ticks on the shore
for t in maass:
    ax.plot(0.5, t, marker='_', ms=8, color=AMBER, lw=1.6, alpha=0.9, zorder=4)

# the odd operator's robust off-line resonance (identity open)
ax.plot(0.5, 9.94, marker='x', ms=9, color=ROSE, mec=ROSE, mew=1.6, zorder=6)
ax.annotate('odd op: t≈9.94\noff-line, identity open',
            xy=(0.5, 9.94), xytext=(0.62, 13.5), color=ROSE, fontsize=7.5,
            arrowprops=dict(arrowstyle='->', color=ROSE, lw=0.8))

ax.text(0.03, 0.03, 'the zeros enter an octave below the shore —\nbelt of poles, mirrored across it',
        transform=ax.transAxes, color=TXT, fontsize=7.5, va='bottom',
        path_effects=[pe.withStroke(linewidth=2, foreground=INK)])

# ---- right: the halving, numerically -----------------------------------
ax = axR
ax.plot(ts, logphi_pole, color=TEAL, lw=1.2, alpha=0.8)
ax.plot(ts, logphi_mirr, color=ROSE, lw=1.1, alpha=0.7)
# exact markers: triangle up at each pole (gamma/2), triangle down at each zero
for t, h_p, h_z in zip(half, pole_heights, zero_heights):
    ax.plot(t, min(h_p, 6.5), marker='^', ms=6, color=TEAL, zorder=5)
    ax.plot(t, max(h_z, -6.5), marker='v', ms=6, color=ROSE, zorder=5)
    ax.axvline(t, color=TEAL, lw=0.5, alpha=0.35, ls=':')
ax.axhline(0, color=GRID, lw=0.8)
ax.set_xlim(5, 27)
ax.set_ylim(-7, 7)
ax.set_xlabel(r'$t$', color=TXT, fontsize=10)
ax.set_ylabel(r'log$_{10}|φ(s)|$', color=TXT, fontsize=10)
ax.set_title('poles at ρ/2, zeros mirrored', color=TXT, fontsize=11)
ax.text(0.03, 0.96, 'teal ▲: poles of φ exactly at γ/2',
        transform=ax.transAxes, color=TEAL, fontsize=7.5, va='top')
ax.text(0.03, 0.90, 'rose ▼: zeros at the same γ/2 — the mirror',
        transform=ax.transAxes, color=ROSE, fontsize=7.5, va='top')
ax.text(0.03, 0.84, 'grey: even-op resonance depth on the shore',
        transform=ax.transAxes, color=TXT, fontsize=7.5, va='top', alpha=0.8)

axr = ax.twinx()
axr.plot(dts, depth_even, color='#8b93a3', lw=1.3, alpha=0.9)
axr.set_ylim(0, 0.9)
axr.tick_params(colors='#8b93a3', labelsize=7)
axr.set_ylabel('even-op |1−λ|', color='#8b93a3', fontsize=8)

fig.suptitle('the renormalization — ρ ↦ ρ/2, both coordinates halve',
             color=TXT, fontsize=12, y=0.98)
fig.tight_layout(rect=(0, 0, 1, 0.95))
out = 'assets/renorm-poles.png'
fig.savefig(out, facecolor=INK, bbox_inches='tight')
print('saved', out)
