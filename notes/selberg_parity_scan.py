#!/usr/bin/env python3
"""Fine scan near suspected resonances, even & odd operators, sigma -> 1/2."""
import numpy as np
import sys
sys.path.insert(0, 'notes')
from numpy.polynomial.legendre import legval

def shift_leg(j, t):
    c = np.zeros(j + 1); c[j] = 1.0
    return legval(2.0 * np.asarray(t) - 1.0, c)

def Ls_matrix(s, xs, K, odd=False, N=6000):
    n = np.arange(1, N + 1, dtype=float)
    M = np.zeros((len(xs), K), dtype=complex)
    B = np.zeros((len(xs), K))
    w = 2 * s
    sign = (-1.0) ** n if odd else np.ones(N)
    for j in range(K):
        xrow = xs[None, :] + n[:, None]
        vals = sign[:, None] * shift_leg(j, 1.0 / xrow) * xrow ** (-w)
        M[:, j] = vals.sum(axis=0) + sign[-1] * (-1.0) ** j * (xs + N) ** (1 - w) / (w - 1)
        B[:, j] = shift_leg(j, xs)
    return np.linalg.pinv(B) @ M

def nearest(s, xs, K, odd):
    A = Ls_matrix(s, xs, K, odd)
    ev = np.linalg.eigvals(A)
    d = np.abs(ev - 1.0)
    i = np.argmin(d)
    return ev[i], d[i]

xs = 0.5 * (1 + np.cos(np.pi * (np.arange(56) + 0.5) / 56))
K = 30
for odd, name, tlo, thi in [(False, "EVEN", 13.5, 14.1), (True, "ODD ", 9.2, 9.9)]:
    print(f"--- {name} operator ---")
    ts = np.arange(tlo, thi, 0.02)
    for sig in [0.52, 0.505, 0.501]:
        best = (1e9, None)
        for t in ts:
            ev, d = nearest(sig + 1j*t, xs, K, odd)
            if d < best[0]:
                best = (d, (t, ev))
        d, (t, ev) = best
        print(f"  sigma={sig}: best at t={t:.3f}  ev={ev.real:+.4f}{ev.imag:+.4f}j  |1-ev|={d:.4f}")
