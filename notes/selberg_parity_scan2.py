#!/usr/bin/env python3
"""Fixed odd-operator tail. Alternating sum needs NO positive-tail correction
(the alternating tail after N is ~ (-1)^N N^{-w}/2, tiny at N=6000).
"""
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
        M[:, j] = vals.sum(axis=0)
        if not odd:
            M[:, j] += (-1.0) ** j * (xs + N) ** (1 - w) / (w - 1)
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

# ODD operator, scan t around 9.2-10.0 (first Maass eigenvalue ~91.14 -> t~9.53)
print("--- ODD operator (fixed tail) ---")
for sig in [0.52, 0.505, 0.501]:
    ts = np.arange(9.2, 10.0, 0.02)
    best = (1e9, None)
    for t in ts:
        ev, d = nearest(sig + 1j*t, xs, K, odd=True)
        if d < best[0]:
            best = (d, (t, ev))
    d, (t, ev) = best
    print(f"  sigma={sig}: best at t={t:.3f}  ev={ev.real:+.4f}{ev.imag:+.4f}j  |1-ev|={d:.5f}")

# sanity: EVEN operator, t=13.78 should still be clean
print("--- EVEN operator check ---")
for sig in [0.505]:
    ev, d = nearest(sig + 1j*13.78, xs, K, odd=False)
    print(f"  sigma={sig}: t=13.78  ev={ev.real:+.4f}{ev.imag:+.4f}j  |1-ev|={d:.5f}")
