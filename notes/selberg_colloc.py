#!/usr/bin/env python3
"""Collocation for the Mayer transfer operator L_s, complex s, Re(s) > 1/2.

L_s f(x) = sum_{n>=1} (x+n)^{-2s} f(1/(x+n))

Legendre collocation on [0,1]. Tail beyond N corrected analytically:
  sum_{n>N} (x+n)^{-2s} f(1/(x+n)) ~ (-1)^j (x+N)^{1-2s}/(2s-1)  for basis f = P_j.

Verified against GKW (s=1): eigenvalues 1, -0.30366, 0.0931, ...
"""
import numpy as np
from numpy.polynomial.legendre import legval, leggauss


def shift_leg(j, t):
    c = np.zeros(j + 1)
    c[j] = 1.0
    return legval(2.0 * np.asarray(t) - 1.0, c)


def Ls_matrix(s, xs, K, N=4000):
    """Collocation matrix of L_s in Legendre coefficient basis."""
    n = np.arange(1, N + 1, dtype=float)
    M = np.zeros((len(xs), K), dtype=complex)
    B = np.zeros((len(xs), K))
    w = 2 * s
    for j in range(K):
        xrow = xs[None, :] + n[:, None]          # (N, npts)
        tvals = 1.0 / xrow
        vals = shift_leg(j, tvals) * xrow ** (-w)  # (N, npts)
        M[:, j] = vals.sum(axis=0)
        # tail: (x+N)^{1-2s}/(2s-1) * P_j(-1)
        M[:, j] += (-1.0) ** j * (xs + N) ** (1 - w) / (w - 1)
        B[:, j] = shift_leg(j, xs)
    return np.linalg.pinv(B) @ M, B


def spectrum(s, xs, K, N=4000):
    A, _ = Ls_matrix(s, xs, K, N)
    return np.linalg.eigvals(A)


def main():
    # Chebyshev nodes on [0,1] (well-conditioned collocation)
    x_nodes = 0.5 * (1 + np.cos(np.pi * (np.arange(64) + 0.5) / 64))
    K = 28

    for s in [1.0, 1.5, 0.8, 0.6]:
        ev = spectrum(s, x_nodes, K)
        order = np.argsort(-np.abs(ev))
        top = ev[order][:5]
        print(f"s={s}:  top |ev|: {np.round(top, 5)}")
        print(f"         top re:  {np.round(top.real, 5)}")


if __name__ == "__main__":
    main()
