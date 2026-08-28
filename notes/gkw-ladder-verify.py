#!/usr/bin/env python3
"""GKW operator eigenvalues — verify the golden ladder.

Flajolet-Vallee (1995) conjecture, proved by Alkauskas (2014):

    (-1)^{n+1} lambda_n = phi^{-2n} + C * phi^{-2n}/sqrt(n) + d(n)*phi^{-2n}/n

so lambda_n / lambda_{n+1} -> -phi^2  (the golden ladder, approached from above).

Galerkin projection in the Legendre basis with Gauss-Legendre quadrature:
    A = (B^T W B)^{-1} (B^T W L)
where B[i,j] = P_j(x_i), L[i,j] = (L P_j)(x_i), W = diag(Gauss-Legendre w).
Stable: the projection is well-conditioned on quadrature nodes.
"""
import numpy as np
from numpy.polynomial.legendre import leggauss, legvander

PHI = (1 + 5 ** 0.5) / 2
from scipy.special import zeta
C = (5 / 4) * zeta(1.5) / np.sqrt(2 * np.pi)


def pbasis(t, K):
    """Legendre basis on [0,1]: P_j evaluated at 2t-1 (the affine shift)."""
    return legvander(2.0 * np.asarray(t) - 1.0, K - 1)


def gkw_galerkin(K=64, N=30000, M=None):
    if M is None:
        M = int(K * 1.8) + 1
    x, w = leggauss(M)                    # nodes, weights on [-1,1]
    x = 0.5 * (x + 1.0)                   # -> [0,1]
    w = 0.5 * w
    n = np.arange(1, N + 1, dtype=float)
    B = pbasis(x, K)                      # M x K, P_j(x_i)
    Lmat = np.zeros((M, K))
    for i, xi in enumerate(x):
        t = 1.0 / (n + xi)                # N
        Lmat[i] = (pbasis(t, K) * (t * t)[:, None]).sum(0)
    H = B.T @ (w[:, None] * Lmat)         # K x K, weighted projection
    G = B.T @ (w[:, None] * B)            # K x K Gram matrix
    A = np.linalg.solve(G, H)
    evals, _ = np.linalg.eig(A)
    order = np.argsort(-np.abs(evals))
    return evals[order]


def main():
    print(f"phi^-2 = {PHI**-2:.6f}   C = {C:.9f}   (Alkauskas constant, 5/4 * zeta(3/2)/sqrt(2pi))\n")
    prev = None
    for K, N in [(48, 20000), (72, 30000), (96, 40000)]:
        evals = gkw_galerkin(K, N)
        top = evals[:7]
        print(f"K={K} N={N}  (galerkin, Gauss-Legendre nodes)")
        print("  " + "  ".join(f"λ{k}={e.real:+.8f}" for k, e in enumerate(top)))
        rs = [top[j].real / top[j + 1].real for j in range(1, 5)]
        print("  ratios λ_j/λ_{j+1}: " + "  ".join(f"{r:+.5f}" for r in rs))
        if prev is not None:
            print(f"  max |Δratio| vs prev: {max(abs(a-b) for a,b in zip(rs,prev)):.2e}")
        prev = rs
        # Alkauskas leading-term prediction for |lambda_n|
        pred = [PHI ** (-2 * m) * (1 + C / np.sqrt(m)) for m in range(1, 7)]
        print("  asympt |λ_m|≈ " + "  ".join(f"{p:.4f}" for p in pred))
        print(f"  target -phi^2 = {-PHI**2:.6f}\n")
    print("literature anchors: 1, -0.3036630029, +0.100884, -0.033488, +0.011148, -0.003714, +0.001237")


if __name__ == "__main__":
    main()
