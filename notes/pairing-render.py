"""The pairing — the primes' shadow is real because the zeros pair.

ψ(x) − x = −Σ x^ρ/ρ is lelia's conjugate sum. It is real and finite only
because each zero's term x^ρ/ρ is summed together with its functional-
equation partner x^{1−ρ}/(1−ρ); on the critical line 1−ρ = ρ̄ (the conjugate),
so the pair sum is 2·Re(·). Unpaired (upper half-plane zeros only) the sum
leans off the real axis and never settles.

Left panel: the two mirror walks. U_N = −Σ_{n≤N} x^{ρ_n}/ρ_n (γ>0, teal) and
L_N = conj(U_N) (γ<0, gold). Each leans; the parallelogram they span has its
far corner exactly on the real axis — the shadow. That corner lands on the
target ψ(47)−47 (gold ×).
Right panel: the paired partial sum p_N (teal) converges to the target (gold
dashed); the unpaired imaginary lean (orange) wanders and never cancels.
"""
import importlib.util
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

spec = importlib.util.spec_from_file_location('psl', 'notes/prime-spectrum-lib.py')
psl = importlib.util.module_from_spec(spec); spec.loader.exec_module(psl)

BG = '#0a0a12'; TXT = '#e8eef2'; SUB = '#8899aa'
TEAL = '#5fd4c7'; GOLD = '#ffd257'; ORANGE = '#e0765a'

z = psl.find_zeros(210.0)          # 73 zeros, t < 210
x = 47.0                            # a prime; psi(47)=47.5395
u = np.log(x)
rho = 0.5 + 1j * z
terms = np.exp(rho * u) / rho       # x^rho/rho
U = -np.cumsum(terms)               # unpaired upper-half partial sums (complex)
L = np.conj(U)                      # lower-half partners = mirror walk
pN = -np.cumsum(2 * np.real(terms)) # paired partial sums (real)
target = psl.psi(x) - x             # true shadow

N = len(z)
idx = np.arange(N) + 1

fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 6.2), dpi=130)
for ax in (axL, axR):
    ax.set_facecolor(BG)
    for s in ax.spines.values():
        s.set_visible(False)
fig.patch.set_facecolor(BG)

# ---------- LEFT: the two mirror walks + the parallelogram ----------
ax = axL
ax.set_title('unpaired \u2014 each zero leans', color=TXT, fontsize=17, pad=14)

cmapU = LinearSegmentedColormap.from_list('u', ['#123a44', TEAL])
cmapL = LinearSegmentedColormap.from_list('l', ['#4a3a12', GOLD])
for i in range(N - 1):
    ax.plot([U[i].real, U[i+1].real], [U[i].imag, U[i+1].imag],
            color=cmapU(i / N), lw=1.1, alpha=0.9)
    ax.plot([L[i].real, L[i+1].real], [L[i].imag, L[i+1].imag],
            color=cmapL(i / N), lw=1.1, alpha=0.9)

# axes
ax.axhline(0, color='#555a66', lw=0.9, ls=(0, (4, 4)))
ax.axvline(0, color='#555a66', lw=0.9, ls=(0, (4, 4)))

# the parallelogram of the final pair: O -> U -> U+L -> L -> O
O = 0.0 + 0.0j
S = U[-1] + L[-1]                   # the pair's sum = the shadow, real
ax.plot([O.real, U[-1].real], [O.imag, U[-1].imag], color=TEAL, lw=1.2, ls=(0, (2, 2)))
ax.plot([U[-1].real, S.real], [U[-1].imag, S.imag], color=GOLD, lw=1.2, ls=(0, (2, 2)))
ax.plot([S.real, L[-1].real], [S.imag, L[-1].imag], color=TEAL, lw=1.2, ls=(0, (2, 2)))
ax.plot([L[-1].real, O.real], [L[-1].imag, O.imag], color=GOLD, lw=1.2, ls=(0, (2, 2)))
# the diagonal: the shadow
ax.plot([O.real, S.real], [O.imag, S.imag], color='#ffffff', lw=1.8, alpha=0.95, zorder=5)

# endpoints and target
ax.plot([U[-1].real], [U[-1].imag], 'o', color=TEAL, ms=8, zorder=6)
ax.plot([L[-1].real], [L[-1].imag], 'o', color=GOLD, ms=8, zorder=6)
ax.plot([S.real], [S.imag], 'o', color='#ffffff', ms=7, zorder=7)
ax.plot([target], [0], marker='x', color=GOLD, ms=12, mew=2.6, zorder=8)

# endpoint labels
ax.text(U[-1].real - 0.12, U[-1].imag - 0.12, 'γ > 0', color=TEAL, fontsize=11, ha='right', va='top')
ax.text(L[-1].real - 0.12, L[-1].imag + 0.12, 'γ < 0', color=GOLD, fontsize=11, ha='right', va='bottom')

ax.set_xlabel('Re', color=SUB, fontsize=12)
ax.set_ylabel('Im', color=SUB, fontsize=12)
ax.tick_params(colors=SUB, labelsize=9)
ax.set_xlim(-1.35, 1.35)
ax.set_ylim(-1.15, 1.15)
ax.set_aspect('equal')
ax.text(0.02, 0.96, 'teal: zeros γ>0', color=TEAL, transform=ax.transAxes, fontsize=10, va='top')
ax.text(0.02, 0.90, 'gold: the mirrors γ<0', color=GOLD, transform=ax.transAxes, fontsize=10, va='top')

# ---------- RIGHT: the paired sum settles, the lean wanders ----------
ax = axR
ax.set_title('paired \u2014 the shadow is real', color=TXT, fontsize=17, pad=14)
ax.axhline(target, color=GOLD, lw=1.5, ls=(0, (5, 3)), zorder=3)
ax.plot(idx, pN, color=TEAL, lw=2.2, zorder=4)
ax.plot(idx, np.imag(U), color=ORANGE, lw=1.5, alpha=0.9, zorder=4)

ax.text(42, target + 0.16, 'ψ(47)\u221247', color=GOLD, fontsize=11)
ax.text(40, np.imag(U)[-1] - 0.3, 'the lean \u2014 the unpaired imaginary', color=ORANGE, fontsize=11)
ax.text(8, target + 0.3, 'paired: converges', color=TEAL, fontsize=11)

ax.set_xlabel('zero pairs added', color=SUB, fontsize=12)
ax.set_ylabel('shadow value', color=SUB, fontsize=12)
ax.tick_params(colors=SUB, labelsize=9)
ax.set_xlim(0, N + 2)
ax.set_ylim(-1.5, 1.5)

fig.text(0.5, 0.015,
         '\u03c8(x)\u2212x = \u2212\u03a3 x^\u03c1/\u03c1   \u2014   real because the partner of \u03c1 under s\u21921\u2212s is its conjugate: the pair is the shadow.',
         ha='center', color=SUB, fontsize=12)

plt.tight_layout(rect=(0, 0.05, 1, 1))
plt.savefig('assets/the-pairing.png', dpi=130, facecolor=fig.get_facecolor())
print('wrote assets/the-pairing.png')
