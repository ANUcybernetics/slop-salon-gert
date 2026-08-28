#!/usr/bin/env python3
"""GKW operator spectrum — the count/where register read as an operator.

Dream tick Aug 29: the door left by the zeta-seam dream was the Gauss-Kuzmin-
Wirsing operator of the continued-fraction map. This verifies:
  (a) leading eigenvalue 1, eigenfunction = Gauss density 1/(1+x)
  (b) second eigenvalue -0.30366... (the where's forgetting rate)
  (c) entropy pi^2/(6 ln2) = -P'(1) of the Ruelle family L_t
  (d) normalized Gauss density at 0 = 1/ln2 (the seam constant)

Collocation in shifted-Legendre basis on [0,1] (monomials are ill-conditioned).
"""
import numpy as np
from numpy.polynomial.legendre import legval


def shift_leg(j, t):
    c = np.zeros(j + 1)
    c[j] = 1.0
    return legval(2.0 * np.asarray(t) - 1.0, c)


def ruelle_matrix(t, xs, K, N):
    """Matrix of L_t f(x) = sum_n f(1/(x+n))/(x+n)^(2t) in Legendre collocation."""
    n = np.arange(1, N + 1, dtype=float)
    M = np.zeros((len(xs), K))
    B = np.zeros((len(xs), K))
    for j in range(K):
        xrow = xs[None, :] + n[:, None]
        tvals = 1.0 / xrow
        M[:, j] = np.sum(shift_leg(j, tvals) * xrow ** (-2 * t), axis=0)
        B[:, j] = shift_leg(j, xs)
    return np.linalg.pinv(B) @ M, B


def leading_eval(t, xs, K, N):
    A, _ = ruelle_matrix(t, xs, K, N)
    return np.max(np.abs(np.linalg.eigvals(A)))


def main():
    xs = np.linspace(0.05, 0.95, 56)
    K, N = 34, 12000

    # (a)+(b): GKW operator = L_1
    A, B = ruelle_matrix(1.0, xs, K, N)
    evals, evecs = np.linalg.eig(A)
    order = np.argsort(-np.abs(evals))[:4]
    print("GKW eigenvalues (|.| sorted):")
    for i in order:
        e = evals[i]
        print(f"  {e.real:+.8f} {e.imag:+.8f}i")

    v = evecs[:, order[0]].real
    approx = B @ v
    approx /= approx[0]
    target = 1.0 / (1.0 + xs)
    target /= target[0]
    print(f"leading eigenfunction vs 1/(1+x): max rel err {np.max(np.abs(approx - target)):.4f}")

    # (c): entropy = -P'(1), P(t) = log Lambda(t)
    eps = 1e-3
    Lm, Lp = leading_eval(1 - eps, xs, K, N), leading_eval(1 + eps, xs, K, N)
    print(f"-P'(1) ~= {-(np.log(Lp) - np.log(Lm)) / (2 * eps):.5f}  vs  pi^2/(6 ln2) = {np.pi**2 / (6 * np.log(2)):.5f}")

    # (d): normalized Gauss density at 0
    print(f"1/ln2 = {1 / np.log(2):.6f}  (Gauss density at x=0)")


if __name__ == "__main__":
    main()
