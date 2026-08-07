"""The lean — the counting shadow carries a sign.

π(x) < Li(x) for every reachable x: the primes are shy. The additive shadow
ψ(x)−x pairs to zero (the two hands fold even); the counting shadow π(x)−Li(x)
carries a constant −ln 2 from its explicit formula, and the low zeros lean
with it, so the count lands low. Littlewood: the lean is not forever.

Panels:
  A  the shy count — π(x) steps just below Li(x); the gap is the lean.
  B  Li(x)−π(x) — positive everywhere, growing like √x/ln x, ln 2 dashed.
  C  normalized — (Li−π)·ln x/√x (gold) leans positive; (ψ−x)/√x (teal)
     oscillates about zero, paired. The two shadows: one carries a sign.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import expi

BG = '#0a0a12'; TXT = '#e8eef2'; SUB = '#8899aa'
TEAL = '#5fd4c7'; GOLD = '#ffd257'; ORANGE = '#e0765a'

N = 5_000_000

# ---- sieve primes ----
sieve = np.ones(N + 1, bool); sieve[:2] = False
for i in range(2, int(N ** 0.5) + 1):
    if sieve[i]:
        sieve[i * i::i] = False
primes = np.nonzero(sieve)[0]

# ---- von Mangoldt Lambda for psi ----
L = np.zeros(N + 1)
for p in primes:
    pk = p
    while pk <= N:
        L[pk] += np.log(p)
        pk *= p
psi = np.cumsum(L)                      # psi[x] for integer x

def pi_count(x):
    return np.searchsorted(primes, x)

# ---- grid ----
xg = np.geomspace(1e3, N, 900)
lnx = np.log(xg)
sqrtx = np.sqrt(xg)
Li = expi(lnx)                          # Li(x) = Ei(ln x)
pix = np.array([pi_count(v) for v in xg], dtype=float)
psix = psi[np.minimum(xg.astype(int), N)]

# ---- the two shadows, normalized ----
lean = (Li - pix) * lnx / sqrtx         # counting shadow, ~O(1), biased +
shadow = (psix - xg) / sqrtx            # additive shadow, ~O(1), paired
zero_line = np.full_like(xg, np.log(2.0) * lnx / sqrtx)

# =====================================================================
fig = plt.figure(figsize=(13, 8.2), dpi=130, facecolor=BG)

# ---------- A: the shy count ----------
ax = fig.add_subplot(2, 2, 1)
ax.set_facecolor(BG)
for s in ax.spines.values(): s.set_visible(False)
ax.set_title('the shy count — \u03c0(x) < Li(x)', color=TXT, fontsize=15, pad=10)
ax.plot(xg, pix, color='#f2f5f7', lw=1.4, label='\u03c0(x)', zorder=4)
ax.plot(xg, Li, color=GOLD, lw=1.8, label='Li(x)', zorder=3)
ax.fill_between(xg, pix, Li, color=GOLD, alpha=0.16, lw=0, zorder=2)
ax.plot(xg, xg / lnx, color=TEAL, lw=1.0, ls=(0, (4, 3)), label='x/log x', zorder=3)
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlim(1e3, N); ax.set_ylim(1e2, 5e6)
ax.tick_params(colors=SUB, labelsize=8)
ax.legend(loc='upper left', facecolor=BG, edgecolor='none', labelcolor=TXT, fontsize=9)
ax.text(0.03, 0.08, 'the gap is the lean', transform=ax.transAxes,
        color=GOLD, fontsize=10, va='bottom')

# ---------- B: the lean itself ----------
ax = fig.add_subplot(2, 2, 2)
ax.set_facecolor(BG)
for s in ax.spines.values(): s.set_visible(False)
ax.set_title('Li(x) \u2212 \u03c0(x) \u2014 positive everywhere we reach',
             color=TXT, fontsize=15, pad=10)
ax.fill_between(xg, 0, Li - pix, color=GOLD, alpha=0.5, lw=0, zorder=2)
ax.plot(xg, Li - pix, color=GOLD, lw=1.6, zorder=3)
env = lnx / sqrtx                       # ~√x/ln x up to log factors
ax.plot(xg, env, color=SUB, lw=1.0, ls=(0, (2, 3)), zorder=3)
ax.axhline(np.log(2.0), color='#ffffff', lw=1.1, ls=(0, (6, 3)), zorder=4)
ax.text(N ** 0.2, np.log(2.0) + 0.15, 'ln 2 \u2014 the constant in the explicit formula',
        color='#ffffff', fontsize=9, ha='left')
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlim(1e3, N); ax.set_ylim(1e-1, 2e4)
ax.tick_params(colors=SUB, labelsize=8)
ax.text(0.03, 0.92, 'the lean', transform=ax.transAxes,
        color=GOLD, fontsize=11, va='top', fontweight='bold')

# ---------- C: the normalized contrast ----------
ax = fig.add_subplot(2, 1, 2)
ax.set_facecolor(BG)
for s in ax.spines.values(): s.set_visible(False)
ax.set_title('the two shadows, at their own scale \u2014 one leans, one pairs to zero',
             color=TXT, fontsize=15, pad=10)
ax.axhline(0, color='#555a66', lw=1.0, zorder=2)
ax.plot(xg, shadow, color=TEAL, lw=1.3, zorder=4,
        label='(\u03c8(x)\u2212x)/\u221ax \u2014 paired, no sign')
ax.plot(xg, lean, color=GOLD, lw=1.6, zorder=5,
        label='(Li(x)\u2212\u03c0(x))·ln x/\u221ax \u2014 the lean')
ax.fill_between(xg, 0, lean, where=lean > 0, color=GOLD, alpha=0.18, lw=0, zorder=3)
ax.set_xscale('log')
ax.set_xlim(1e3, N)
ax.set_ylim(-2.6, 4.2)
ax.tick_params(colors=SUB, labelsize=8)
ax.legend(loc='lower right', facecolor=BG, edgecolor='none', labelcolor=TXT, fontsize=10)
ax.text(0.03, 0.06, 'teal: \u03c8(x)\u2212x folds its mirrors to a real sum \u2014 zero mean.',
        transform=ax.transAxes, color=TEAL, fontsize=10, va='bottom')
ax.text(0.03, 0.24, 'gold: \u03c0(x) carries a \u2212ln 2 and the low zeros lean with it.',
        transform=ax.transAxes, color=GOLD, fontsize=10, va='bottom')

fig.text(0.5, 0.012,
         '\u03c0(x) = Li(x) \u2212 \u03a3 Li(x^\u03c1) \u2212 ln 2 + \u222b \u2014 the \u2212ln 2 is a lean the pairing cannot cancel. '
         'littlewood: the lean is not forever.',
         ha='center', color=SUB, fontsize=11)

plt.tight_layout(rect=(0, 0.04, 1, 1))
plt.savefig('assets/the-lean.png', dpi=130, facecolor=fig.get_facecolor())
print('wrote assets/the-lean.png')
