#!/usr/bin/env python3
"""Equilibrium measure rho_t across the latent strip, plus pressure details.

rho_t = leading eigenfunction of L_t (weight (x+n)^{-2t}), the Gauss map's
equilibrium measure at inverse temperature t. At t=1 it is the Gauss density
1/(1+x) (the count's law). We track its shape as t crosses the latent strip
(1,2), and verify -P'(1) = pi^2/(6 ln2) (the declaration as departure rate).
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


def leading(t, xs, K, N):
    A, B = ruelle_matrix(t, xs, K, N)
    evals, evecs = np.linalg.eig(A)
    i = np.argmax(np.abs(evals))
    v = evecs[:, i].real
    approx = (B @ v)
    approx /= approx[0]
    return evals[i].real, approx


def main():
    xs = np.linspace(0.05, 0.95, 56)
    K, N = 30, 6000
    for t in [1.0, 1.25, 1.5, 1.75, 2.0]:
        lam, rho = leading(t, xs, K, N)
        target = 1.0 / (1.0 + xs)
        target /= target[0]
        diff = np.max(np.abs(rho - target))
        # concentration: value at x=0 vs x=1
        conc = rho[-1] / rho[0]
        print(f"t={t:4.2f}  lam1={lam:+.6f}  max|rho-gauss|={diff:.4f}  rho(1)/rho(0)={conc:.4f}")

    # pressure convexity: slope of log lambda1 across the strip
    def P(t):
        return np.log(max(1e-12, leading(t, xs, K, N)[0]))
    print("\npressure slope -P'(t) across the strip:")
    for t in [1.0, 1.3, 1.6, 1.9]:
        eps = 2e-3
        s = -(P(t + eps) - P(t - eps)) / (2 * eps)
        print(f"  t={t:4.2f}: -P'={s:+.4f}   (pi^2/6ln2={np.pi**2/(6*np.log(2)):.4f})")


if __name__ == "__main__":
    main()
