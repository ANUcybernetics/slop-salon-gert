#!/usr/bin/env python3
"""Even vs odd Mayer operator. The Maass spectrum splits by parity under z -> -zbar.
Even operator:  L^+ f(x) = sum_n (x+n)^{-2s} f(1/(x+n))   [what I've been using]
Odd operator:   L^- f(x) = sum_n (-1)^n (x+n)^{-2s} f(1/(x+n))
If lambda_1 ~ 91.14 (t ~ 9.53) is odd and lambda_2 ~ 190.13 (t ~ 13.78) is even,
each operator should show its own resonance.
"""
import numpy as np
import sys
sys.path.insert(0, 'notes')
from numpy.polynomial.legendre import legval

def shift_leg(j, t):
    c = np.zeros(j + 1); c[j] = 1.0
    return legval(2.0 * np.asarray(t) - 1.0, c)

def Ls_matrix(s, xs, K, odd=False, N=4000):
    n = np.arange(1, N + 1, dtype=float)
    M = np.zeros((len(xs), K), dtype=complex)
    B = np.zeros((len(xs), K))
    w = 2 * s
    sign = np.ones(N)
    if odd:
        sign = (-1.0) ** n
    for j in range(K):
        xrow = xs[None, :] + n[:, None]
        tvals = 1.0 / xrow
        vals = sign[:, None] * shift_leg(j, tvals) * xrow ** (-w)
        M[:, j] = vals.sum(axis=0)
        M[:, j] += sign[-1] * (-1.0) ** j * (xs + N) ** (1 - w) / (w - 1)
        B[:, j] = shift_leg(j, xs)
    return np.linalg.pinv(B) @ M

def top_near(s, xs, K, odd=False):
    A = Ls_matrix(s, xs, K, odd)
    ev = np.linalg.eigvals(A)
    d = np.abs(ev - 1.0)
    i = np.argmin(d)
    return ev[i], d[i]

xs = 0.5 * (1 + np.cos(np.pi * (np.arange(48) + 0.5) / 48))
K = 28
for odd in [False, True]:
    name = "EVEN" if not odd else "ODD "
    print(f"--- {name} operator ---")
    for t in [9.53, 12.5, 13.78, 18.86]:
        for sig in [0.55, 0.52]:
            ev, d = top_near(sig + 1j*t, xs, K, odd)
            print(f"   t={t:6.2f} sigma={sig}: nearest-1 ev={ev:+.4f}{ev.imag:+.4f}j  |1-ev|={d:.4f}")
