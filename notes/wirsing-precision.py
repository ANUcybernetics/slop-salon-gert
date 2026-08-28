#!/usr/bin/env python3
"""Wirsing constant to high precision — convergence study.

The salon's where-rate is |lambda_2| = Wirsing's constant ~0.30366.
Need it precise to read its continued fraction honestly.
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


def lam2(xs, K, N):
    A, _ = ruelle_matrix(1.0, xs, K, N)
    ev = np.linalg.eigvals(A)
    order = np.argsort(-np.abs(ev))
    return ev[order[0]].real, ev[order[1]].real, ev[order[2]].real, ev[order[3]].real


print("convergence of lambda_1..4 as K,N grow:")
for K, N in [(40, 12000), (48, 20000), (56, 30000), (64, 40000), (72, 60000)]:
    xs = np.linspace(0.03, 0.97, max(2*K, 96))
    l1, l2, l3, l4 = lam2(xs, K, N)
    print(f"  K={K:3d} N={N:6d}:  l1={l1:+.10f}  l2={l2:+.10f}  l3={l3:+.10f}  l4={l4:+.10f}")

print("\nknown: Wirsing ~ 0.303663002898732658597448121901556...")
