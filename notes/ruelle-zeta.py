#!/usr/bin/env python3
"""Ruelle zeta of the Gauss map — the latent strip's analytic shadow.

Mayer's theorem: the Selberg zeta of the modular group is
    Z_Sel(s) = prod_{n>=0} det(1 - L_{s+n})
with L_t the Gauss-map transfer operator. The classical factorization for
PGL(2,Z) is Z_Sel(s) = zeta(s) zeta(s-1) / zeta(2s) x (elliptic factors).

Here we compute the truncated product to see its pole/zero structure:
  - pole at s=1 (zeta(s): the count, never a number)
  - zero where zeta(2s) diverges -> s = 1/2 (the critical-line shadow)
  - the factor zeta(s-1) -> pole at s=2, unless elliptic factors cancel

We ask what the latent strip (1,2) actually contains.
"""
import numpy as np
from numpy.polynomial.legendre import legval


def shift_leg(j, t):
    c = np.zeros(j + 1)
    c[j] = 1.0
    return legval(2.0 * np.asarray(t) - 1.0, c)


def ruelle_matrix(t, xs, K, N):
    n = np.arange(1, N + 1, dtype=float)
    M = np.zeros((len(xs), K))
    B = np.zeros((len(xs), K))
    for j in range(K):
        xrow = xs[None, :] + n[:, None]
        tvals = 1.0 / xrow
        M[:, j] = np.sum(shift_leg(j, tvals) * xrow ** (-2 * t), axis=0)
        B[:, j] = shift_leg(j, xs)
    return np.linalg.pinv(B) @ M, B


def det_one_minus(t, xs, K, N):
    A, _ = ruelle_matrix(t, xs, K, N)
    return np.linalg.det(np.eye(K) - A)


def log_det_one_minus(t, xs, K, N):
    A, _ = ruelle_matrix(t, xs, K, N)
    # sum log(1 - ev) is more stable than det
    ev = np.linalg.eigvals(A)
    return np.sum(np.log(1.0 - ev)).real


def main():
    xs = np.linspace(0.05, 0.95, 56)
    K, N = 26, 3000

    # product Z_R(s) = prod_{n=0}^{M} det(1 - L_{s+n})
    M = 4
    ss = np.linspace(0.2, 2.0, 19)
    print("  s    log|Z_R(s)|   sign  (M=4)")
    for s in ss:
        tot = 0.0
        for n in range(M + 1):
            tot += log_det_one_minus(s + n, xs, K, N)
        print(f"{s:5.2f}   {tot:+8.3f}   {'+' if tot >= 0 else '-'}")

    # individual factors near the interesting points
    for s in [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]:
        line = " ".join(f"det(1-L_{{{s+n:.1f}}})={log_det_one_minus(s+n, xs, K, N):+.2f}"
                        for n in range(M + 1))
        print(f"s={s:4.2f}: {line}")


if __name__ == "__main__":
    main()
