#!/usr/bin/env python3
"""The primes are a spectrum.

Animated two-panel piece: the explicit formula assembles the von Mangoldt
staircase psi(e^u) from the smooth term x plus one zeta-zero mode at a time.
Right panel: the zero spectrum, lit as modes are added. Soundtrack: additive
synthesis, one partial per zero, frequencies f_n = 55 * (t_n / t_1) Hz,
amplitudes ~ 1/sqrt(t_n), each swelling in as it is added.
"""
import sys, os
sys.path.insert(0, '/tmp')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from prime_spectrum_lib import find_zeros, psi, partial_sums

OUT = '/tmp/prime_frames'
os.makedirs(OUT, exist_ok=True)

# ---------------- geometry / data ----------------
TMAX = 300.0
zeros = find_zeros(TMAX)               # 108 zeros up to t=300
NMAX = 100                             # modes swept in the animation
zeros = zeros[:NMAX]
t1 = zeros[0]

u = np.linspace(np.log(2.0), np.log(50.0), 400)
x = np.exp(u)
P = partial_sums(u, zeros)             # (NMAX+1, 400)
psi_vals = np.array([psi(xv) for xv in x])

# staircase as a proper step function (for crisp rendering)
u_step = np.concatenate([[u[0]-0.01], u, [u[-1]+0.01]])
psi_step = np.concatenate([[psi_vals[0]], psi_vals, [psi_vals[-1]]])

# ---------------- figure ----------------
FPS = 30
DUR = 40.0
NFRAMES = int(FPS * DUR)
W, H = 1280, 720
fig = plt.figure(figsize=(W/100, H/100), dpi=100, facecolor='#101216')
gs = fig.add_gridspec(1, 2, width_ratios=[2.6, 1.0], wspace=0.06,
                       left=0.07, right=0.98, top=0.86, bottom=0.12)
axL = fig.add_subplot(gs[0, 0])
axR = fig.add_subplot(gs[0, 1])

BG = '#101216'
FG = '#e8e4da'
RED = '#ff6b4a'
ACC = '#7fd4ff'
DIM = '#3a3f46'

# left panel: static context
axL.set_facecolor(BG)
axL.plot(u, x, ':', color='#6a6f76', lw=1.2, zorder=2, alpha=0.8)
axL.plot(u_step, psi_step, color=FG, lw=1.8, alpha=0.9, zorder=4)
axL.plot(u, np.full_like(u, np.nan), color=RED, lw=2.4, zorder=5)  # live series (reuse)
axL.set_xlim(u[0], u[-1])
ylim = (0, psi_vals.max()*1.06)
axL.set_ylim(*ylim)
axL.set_xlabel(r'$u = \log x$', color=FG, fontsize=11)
axL.set_ylabel(r'$\psi(e^u)$', color=FG, fontsize=11)
axL.tick_params(colors=FG, labelsize=9)
for s in axL.spines.values():
    s.set_color('#2a2e34')
# secondary x ticks as x = e^u
xt = np.log([2, 5, 10, 20, 50])
axL.set_xticks(xt)
axL.set_xticklabels(['2', '5', '10', '20', '50'])
axL.set_xlabel(r'$x$   ($u=\log x$)', color=FG, fontsize=11)

# right panel: the spectrum ladder
axR.set_facecolor(BG)
yrs = np.arange(1, NMAX+1)
axR.set_ylim(NMAX+0.5, 0.5)
axR.set_xlim(-0.9, 1.5)
# faint all-zeros ladder
axR.scatter(np.zeros(NMAX), yrs, s=8, color=DIM, zorder=2)
live_dots, = axR.plot([], [], 'o', color=RED, ms=6, zorder=4)
add_dot, = axR.plot([], [], 'o', color=ACC, ms=11, mfc='none', mew=2.5, zorder=5)
for i in range(1, NMAX+1):
    axR.annotate(f'{zeros[i-1]:.0f}', xy=(0.1, i), color='#8a8f96', fontsize=7, va='center')
axR.set_yticks([])
axR.set_xticks([])
for s in axR.spines.values():
    s.set_color('#2a2e34')
axR.set_title('the spectrum', color=ACC, fontsize=12, pad=8)

# title text
title = fig.text(0.07, 0.93, 'the primes are a spectrum', color=FG, fontsize=19, fontweight='bold')
mode_text = fig.text(0.07, 0.88, '', color=RED, fontsize=12)
mode_text.set_text('')

live_line = axL.lines[2]

# ---------------- render ----------------
for i in range(NFRAMES):
    frac = i / (NFRAMES - 1)
    N = int(round(frac * NMAX))
    # left: explicit sum for current N
    live_line.set_data(u, P[N])
    # faint band of all the correction terms individually? keep clean, skip.
    # right: lit dots
    live_dots.set_data(np.zeros(N), yrs[:N])
    if N > 0:
        add_dot.set_data([0.0], [N])
    else:
        add_dot.set_data([], [])
    mode_text.set_text(f'{N} zero-modes')
    fig.savefig(f'{OUT}/f{i:04d}.png', facecolor=BG)
    if i % 200 == 0:
        print(f'frame {i}/{NFRAMES}  N={N}', flush=True)

print('done rendering', NFRAMES, 'frames')
