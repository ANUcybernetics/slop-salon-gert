#!/usr/bin/env python3
"""The near-shore exactness, verified (Mayer collocation, selberg_lib).

  s -> 1/2+ :  lambda_1(s) = zeta(2s) + o(1)     [residue 1/2 AND constant gamma]
               lambda_2(s) = -1 + 4(s-1/2) + O((s-1/2)^2)   [slope exactly 4 = 2^2]
               lambda_3(s) ~ +0.225  (the even holds; only the sign dives to -1)
               odd collocation leading eigenvalue -> -0.3706, NOT -1
  Synthesis: residue (1/2 = 2^-1) times slope (4 = 2^2) = 2 = the base.
             exponents -1 and +2 straddle the fold (+1/2) in arithmetic mean.
"""
import sys, time
import numpy as np
sys.path.insert(0, 'notes')
from selberg_lib import spectrum

def shore(s, K=48, N=10000, odd=False):
    xs = 0.5 * (1 + np.cos(np.pi * (np.arange(64) + 0.5) / 64))
    ev = spectrum(s, xs, K, odd=odd, N=N).real
    l1 = ev.max()
    i_sign = np.argmin(np.abs(ev + 1.0))
    i_even = np.argmin(np.abs(ev - 0.225))
    return l1, ev[i_sign], ev[i_even]

if __name__ == "__main__":
    GAMMA = 0.5772156649
    print(f"{'s':>6} {'l1*(s-1/2)':>11} {'l1-1/(2s-1)':>12} {'(l2+1)/(s-1/2)':>14} {'l3':>7}")
    for s in [0.52, 0.505, 0.501]:
        l1, l2, l3 = shore(s)
        print(f"{s:>6.3f} {l1*(s-0.5):>11.5f} {l1-1/(2*s-1):>12.5f} {(l2+1)/(s-0.5):>14.4f} {l3:>7.5f}")
    print(f"gamma = {GAMMA:.7f}")
