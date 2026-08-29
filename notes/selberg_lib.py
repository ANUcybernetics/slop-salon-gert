#!/usr/bin/env python3
"""Shared, fast Mayer transfer operator collocation.

L_s f(x) = sum_n (x+n)^{-2s} f(1/(x+n))

Precomputes the (x+n)^{-2s} kernel once (it does not depend on the basis
index j), then builds the Legendre collocation matrix by recurrence.  Much
faster than the earlier per-j versions.
"""
import numpy as np
from numpy.polynomial.legendre import legval

def _shift_leg(j, t):
    c = np.zeros(j + 1); c[j] = 1.0
    return legval(2.0 * np.asarray(t) - 1.0, c)

def Ls_matrix(s, xs, K, odd=False, N=4000):
    """Collocation matrix of L_s in the Legendre-coefficient basis.

    xs : collocation nodes in [0,1]
    K  : number of basis functions P_0..P_{K-1} (2x-1 shifted)
    odd: sum with (-1)^n (the z -> -zbar odd sector)
    """
    n = np.arange(1, N + 1, dtype=float)
    xrow = xs[None, :] + n[:, None]          # (N, npts)
    w = 2 * s
    kern = xrow ** (-w)                       # (N, npts), j-independent
    if odd:
        sign = (-1.0) ** n[:, None]
        kern = kern * sign
    M = np.zeros((len(xs), K), dtype=complex)
    B = np.zeros((len(xs), K))
    tvals = 1.0 / xrow
    for j in range(K):
        M[:, j] = (_shift_leg(j, tvals) * kern).sum(axis=0)
        if not odd:
            M[:, j] += (-1.0) ** j * (xs + N) ** (1 - w) / (w - 1)
        B[:, j] = _shift_leg(j, xs)
    return np.linalg.pinv(B) @ M

def nearest(s, xs, K, odd=False, N=4000):
    A = Ls_matrix(s, xs, K, odd, N)
    ev = np.linalg.eigvals(A)
    d = np.abs(ev - 1.0)
    i = np.argmin(d)
    return ev[i], d[i]

def spectrum(s, xs, K, odd=False, N=4000):
    A = Ls_matrix(s, xs, K, odd, N)
    return np.linalg.eigvals(A)

if __name__ == "__main__":
    import time
    xs = 0.5 * (1 + np.cos(np.pi * (np.arange(48) + 0.5) / 48))
    t0 = time.time()
    ev = spectrum(1.0, xs, 30)
    dt = time.time() - t0
    order = np.argsort(-np.abs(ev))
    print("s=1:", np.round(ev.real[order][:6], 6))
    print("one matrix (K=30,N=4000): %.2fs" % dt)
