#!/usr/bin/env python3
"""Targeted: all eigenvalues of L_s near 1, even operator, high K.
1) t=9.53 (lambda_1 ~ 91.14): does ANY eigenvalue approach 1 as sigma->1/2?
2) refine t=13.78 resonance location.
"""
import numpy as np
import sys
sys.path.insert(0, 'notes')
from numpy.polynomial.legendre import legval

def shift_leg(j, t):
    c = np.zeros(j + 1); c[j] = 1.0
    return legval(2.0 * np.asarray(t) - 1.0, c)

def Ls_matrix(s, xs, K, N=8000):
    n = np.arange(1, N + 1, dtype=float)
    M = np.zeros((len(xs), K), dtype=complex)
    B = np.zeros((len(xs), K))
    w = 2 * s
    for j in range(K):
        xrow = xs[None, :] + n[:, None]
        vals = shift_leg(j, 1.0 / xrow) * xrow ** (-w)
        M[:, j] = vals.sum(axis=0) + (-1.0) ** j * (xs + N) ** (1 - w) / (w - 1)
        B[:, j] = shift_leg(j, xs)
    return np.linalg.pinv(B) @ M

def near_one(s, xs, K, thresh=0.10):
    A = Ls_matrix(s, xs, K)
    ev = np.linalg.eigvals(A)
    d = np.abs(ev - 1.0)
    idx = np.where(d < thresh)[0]
    o = idx[np.argsort(d[idx])]
    return [(ev[i], d[i]) for i in o]

xs = 0.5 * (1 + np.cos(np.pi * (np.arange(64) + 0.5) / 64))
K = 45

print("=== t=9.53, even operator, does lambda_1 appear? ===")
for sig in [0.52, 0.505, 0.501]:
    near = near_one(sig + 1j*9.53, xs, K, thresh=0.5)
    print(f"  sigma={sig}: eigenvalues near 1: {[(f'{e.real:.3f}{e.imag:+.3f}j', f'{d:.3f}') for e,d in near][:5]}")

print("=== refine t~13.78 resonance ===")
for sig in [0.52, 0.51, 0.505, 0.501]:
    best = (1e9, None, None)
    for t in np.arange(13.0, 14.6, 0.01):
        A = Ls_matrix(sig + 1j*t, xs, K)
        ev = np.linalg.eigvals(A)
        d = np.min(np.abs(ev - 1.0))
        if d < best[0]:
            best = (d, t, ev[np.argmin(np.abs(ev-1))])
    d, t, ev = best
    print(f"  sigma={sig}: best t={t:.3f}  ev={ev.real:.5f}{ev.imag:+.5f}j  |1-ev|={d:.5f}  -> lambda={0.25+t*t:.4f}")

print("=== t region 9.0-10.5, even operator, any clean approach? ===")
for sig in [0.505, 0.501]:
    best = (1e9, None, None)
    for t in np.arange(9.0, 10.5, 0.02):
        A = Ls_matrix(sig + 1j*t, xs, K)
        ev = np.linalg.eigvals(A)
        d = np.min(np.abs(ev - 1.0))
        if d < best[0]:
            best = (d, t, ev[np.argmin(np.abs(ev-1))])
    d, t, ev = best
    print(f"  sigma={sig}: best t={t:.3f}  ev={ev.real:.5f}{ev.imag:+.5f}j  |1-ev|={d:.5f}  -> lambda={0.25+t*t:.4f}")
