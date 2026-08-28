#!/usr/bin/env python3
"""GKW operator full spectrum — beyond the two voices.

The salon read the first two eigenvalues (count λ₁=+1, sign λ₂=−0.30366).
This tick: the rest of the spectrum, and the continued fraction of |λ₂|
(the Wirsing constant) — pattern or patternless?
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


def cf(x, terms):
    """Continued fraction of x in [0,1)."""
    out = []
    for _ in range(terms):
        if x <= 0:
            out.append(0)
            break
        a = int(x)
        out.append(a)
        x = 1.0 / (x - a)
    return out


def main():
    xs = np.linspace(0.03, 0.97, 96)
    K, N = 48, 20000

    A, B = ruelle_matrix(1.0, xs, K, N)
    evals, evecs = np.linalg.eig(A)
    order = np.argsort(-np.abs(evals))[:10]
    print("GKW eigenvalues, |.| sorted:")
    for i in order:
        e = evals[i]
        print(f"  {e.real:+.10f} {e.imag:+.10f}i")

    lam2 = evals[order[1]].real
    w = abs(lam2)
    print(f"\n|lambda_2| = {w:.16f}")
    print(f"CF of |lambda_2| (40 terms): {cf(w, 40)}")
    print(f"CF of |lambda_3| (30 terms): {cf(abs(evals[order[2]].real), 30)}")
    print(f"CF of |lambda_4| (30 terms): {cf(abs(evals[order[3]].real), 30)}")


if __name__ == "__main__":
    main()
