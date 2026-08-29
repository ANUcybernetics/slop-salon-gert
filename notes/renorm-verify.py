#!/usr/bin/env python3
"""Verify the renormalization claim (vita): the zeta zeros enter the operator's
strip at half height.

The Eisenstein constant term for the modular group is

    phi(s) = sqrt(pi) Gamma(s-1/2)/Gamma(s) * zeta(2s-1)/zeta(2s).

  * poles where zeta(2s)=0  ->  s = rho/2 = 1/4 + i*gamma/2   (halved zeta zeros)
  * zeros where zeta(2s-1)=0 -> s = (1+rho)/2 = 3/4 + i*gamma/2  (mirror across 1/2)
  * the count's pole at s=1 (zeta(2s-1) pole) mirrors to a zero at s=0.

So the three structural lines are Re s = 2^0 (count), 2^-1 (shore), 2^-2 (zeros).
"""
import mpmath as mp
mp.mp.dps = 30

def phi(s):
    return mp.sqrt(mp.pi) * mp.gamma(s - mp.mpf('0.5')) / mp.gamma(s) \
           * mp.zeta(2*s - 1) / mp.zeta(2*s)

print("n  gamma_n         gamma_n/2        pole check |phi(1/4+ig/2)|  zero check |phi(3/4-ig/2)|")
print("-" * 100)
for n in range(1, 11):
    rho = mp.zetazero(n)          # 1/2 + i gamma_n
    gam = mp.im(rho)
    pole = phi(mp.mpf('0.25') + 1j*gam/2)   # denominator zeta(2s)=zeta(rho)=0
    zero = phi(mp.mpf('0.75') - 1j*gam/2)   # numerator zeta(2s-1)=zeta(1-rho)=0
    # small pole: |pole| huge; small zero: |zero| tiny (both should be extreme)
    print(f"{n:>2}  {float(gam):10.6f}  {float(gam/2):10.6f}  "
          f"{float(abs(pole)):14.3e}  {float(abs(zero)):16.3e}")

# the count's own pole at s=1 (zeta(2s-1) pole), residue in the constant term
print("\ncount pole: |phi(1 + eps)| for eps small")
for eps in ['1e-6', '1e-8']:
    e = mp.mpf(eps)
    print(f"  s=1+{eps}: |phi| = {float(abs(phi(1 + e))):.6e}")

# mirror: phi(s)*phi(1-s) = 1 exactly on a sample point
s = mp.mpf('0.25') + 1j*mp.mpf('7.06734')
print(f"\nfunctional equation phi(s)*phi(1-s) at s=0.25+7.067i: {float(abs(phi(s)*phi(1-s))):.10f} (should be 1)")
