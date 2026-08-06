#!/usr/bin/env python3
"""The clocks — four tempi.

mina's three tempi (Lagrange/Khinchin): φ periodic (wait 1), e patterned
(wait grows), generic (wait -> 2.685). The fourth: the primes —
almost-periodic. Two hands: prime gaps wait ~log x and grow; zeta-zero
spacings wait ~2pi/log t and shrink; the two waits multiply toward 2pi.
The comma is the two-prime slice (19/12, the 23-run).
"""
import sys, importlib.util
spec = importlib.util.spec_from_file_location('psl', 'notes/prime-spectrum-lib.py')
psl = importlib.util.module_from_spec(spec); spec.loader.exec_module(psl)

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ---------------- data ----------------
# e's partial-quotient pattern (Euler): 2,1,2,1,1,4,1,1,6,1,1,8,...
e_pat = [1, 2]
k = 4
while len(e_pat) < 15:
    e_pat += [1, 1, k]
    k += 2

# generic: sample waits from the Gauss-Kuzmin law P(k)=log2(1+1/(k(k+2)))
rng = np.random.default_rng(7)
u = rng.random(26)
gk = np.cumsum(1.0/(np.arange(1, 30)**2 + np.arange(1, 30)))
gk /= gk[-1]  # approx CDF
gen = np.searchsorted(gk, u) + 1

# primes up to 300, and zeta zeros to t=120
def primes_upto(n):
    sieve = np.ones(n+1, bool); sieve[:2] = False
    for i in range(2, int(n**0.5)+1):
        if sieve[i]: sieve[i*i::i] = False
    return np.nonzero(sieve)[0]
pr = primes_upto(300)
zr = psl.find_zeros(120.0)

# ---------------- figure ----------------
BG  = '#101216'
FG  = '#e8e4da'
DIM = '#3a3f46'
GOLD = '#e8b84a'
SIL  = '#b9bec6'
BLU  = '#7d9fd4'
RED  = '#ff6b4a'
CYN  = '#7fd4ff'

fig = plt.figure(figsize=(12.8, 8.0), dpi=100, facecolor=BG)
gs = fig.add_gridspec(2, 2, hspace=0.42, wspace=0.16,
                      left=0.08, right=0.97, top=0.85, bottom=0.08)

def clock_strip(ax, pos, color, label, hi, bracket=None):
    """pos: sorted tick positions. Draw a baseline + vertical ticks."""
    ax.set_facecolor(BG)
    ax.set_xlim(-0.5, hi + 0.5)
    ax.set_ylim(-0.9, 1.6)
    ax.plot([-0.5, hi + 0.5], [0, 0], color=DIM, lw=1.2, zorder=1)
    ax.vlines(pos, 0, 0.9, color=color, lw=2.2, zorder=3)
    # ends
    ax.scatter([pos[0], pos[-1]], [0, 0], s=22, color=color, zorder=4)
    ax.set_yticks([]); ax.set_xticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.text(0.0, 1.32, label, color=FG, fontsize=12, va='center')
    if bracket is not None:
        ax.annotate('', xy=(bracket[0], -0.55), xytext=(bracket[1], -0.55),
                    arrowprops=dict(arrowstyle='|-|,widthA=0.6,widthB=0.6',
                                    color=SIL, lw=1.2))
        ax.text(0.5*(bracket[0]+bracket[1]), -0.85, bracket[2],
                color=SIL, fontsize=10, ha='center')

# --- Panel A: phi, periodic ---
axA = fig.add_subplot(gs[0, 0])
phi_pos = np.arange(0, 24)
clock_strip(axA, phi_pos, GOLD, 'periodic — wait 1.  φ (quadratic)', 24,
            bracket=(0, 4, 'runs 1,1,1,1'))

# --- Panel B: e, patterned ---
axB = fig.add_subplot(gs[0, 1])
e_pos = np.concatenate([[0], np.cumsum(e_pat)])
clock_strip(axB, e_pos, SIL, 'patterned — wait grows.  e (transcendental)',
            e_pos.max(), bracket=(0, e_pos.max(), '1,2,1,1,4,1,1,6'))

# --- Panel C: generic, Khinchin ---
axC = fig.add_subplot(gs[1, 0])
gen_pos = np.concatenate([[0], np.cumsum(gen)])
gen_label = ','.join(str(int(v)) for v in gen[:8])
clock_strip(axC, gen_pos, BLU, 'generic — wait → 2.685.  Khinchin',
            gen_pos.max(), bracket=(0, gen_pos.max(), f'runs {gen_label},...'))

# --- Panel D: primes, almost-periodic ---
axD = fig.add_subplot(gs[1, 1])
axD.set_facecolor(BG)
axD.set_xlim(0, 1.0)
axD.set_ylim(-1.9, 1.6)
axD.set_yticks([]); axD.set_xticks([])
for s in axD.spines.values():
    s.set_visible(False)

# top strip: prime events, gaps grow. x-scale: primes 2..300 -> [0,1]
axD.plot([0, 1], [0, 0], color=DIM, lw=1.2, zorder=1)
pr_n = (pr - 2) / (298.0)
axD.vlines(pr_n, 0, 0.9, color=RED, lw=1.4, zorder=3)
axD.text(0.0, 1.32, 'almost-periodic — the primes', color=FG, fontsize=12, va='center')
axD.text(1.0, 1.12, 'gaps wait ~ log x', color=RED, fontsize=10, ha='right', va='center')

# bottom strip: zeta zeros, spacing shrinks. t: 14..120 -> [0,1]
axD.plot([0, 1], [-1.0, -1.0], color=DIM, lw=1.2, zorder=1)
z_n = (zr - zr[0]) / (zr[-1] - zr[0])
axD.vlines(z_n, -1.0, -0.1, color=CYN, lw=2.4, zorder=3)
axD.text(1.0, -1.45, 'zero clock waits ~ 2π/log t', color=CYN, fontsize=10, ha='right', va='center')
axD.text(0.5, -0.5, 'gap · spacing → 2π', color=SIL, fontsize=12, ha='center', va='center')

fig.savefig('assets/the-clocks.png', facecolor=BG, bbox_inches='tight')
print('saved assets/the-clocks.png')
