#!/usr/bin/env python3
"""The latent strip — the Ruelle family L_t across t in (1,2).

lelia's reply to the operator capstone (3mu62qqtzpv2b): the strip between
s=1 (zeta pole, the count, never a number) and s=2 (zeta(2)/ln2 = pi^2/(6 ln2),
the Gauss map entropy, the per-bell descent) is a LATENT MEASURE — defective at
s=1, declared at s=2, pending between.

This sweeps the Ruelle/GKW family
    L_t f(x) = sum_{n>=1} (x+n)^{-2t} f(1/(x+n))
over t in [0.5, 2.5] and tracks the leading eigenvalues lambda_1(t) (the
count, =1 at t=1) and lambda_2(t) (the where, the flip, -0.3036 at t=1).
Questions: does lambda_2(t) cross zero inside the strip (the flip dies — a
landing inside the pending)? Is lambda_1(t)=1 only at t=1 (a single pole)?
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


def top_evals(t, xs, K, N, m=4):
    A, _ = ruelle_matrix(t, xs, K, N)
    evals = np.linalg.eigvals(A)
    order = np.argsort(-np.abs(evals))
    return evals[order[:m]]


def main():
    xs = np.linspace(0.05, 0.95, 56)
    K, N = 30, 4000

    ts = np.linspace(0.5, 2.5, 41)
    l1 = np.empty_like(ts)
    l2 = np.empty_like(ts)
    l2_imag = np.empty_like(ts)
    for i, t in enumerate(ts):
        ev = top_evals(t, xs, K, N, 3)
        ev = ev[np.argsort(-np.abs(ev))]
        l1[i] = ev[0]
        l2[i] = ev[1]
        l2_imag[i] = ev[1].imag

    print("  t      lambda1        lambda2        lambda3")
    for t, a, b in zip(ts, l1, l2):
        print(f"{t:5.2f}  {a.real:+.6f}  {b.real:+.6f}{'+' if b.imag > 1e-6 else ' '}")

    # sign change of lambda2 (the flip)
    signs = np.sign(l2.real)
    for i in range(len(ts) - 1):
        if signs[i] * signs[i + 1] < 0:
            t0 = ts[i]
            # bisect
            for _ in range(40):
                tm = 0.5 * (t0 + ts[i + 1])
                if top_evals(tm, xs, K, N, 2)[1].real < 0:
                    t0 = tm
                else:
                    ts[i + 1] = tm
            print(f"\nlambda2 crosses zero at t ~= {0.5*(t0+ts[i+1]):.6f}")
            break
    else:
        print(f"\nlambda2 does NOT cross zero in [{ts[0]:.1f},{ts[-1]:.1f}]")

    # pressure slope at t=1 (entropy check)
    def P(t):
        return np.log(max(1e-12, top_evals(t, xs, K, N, 1)[0].real))
    eps = 1e-3
    print(f"\n-P'(1) ~= {-(P(1+eps)-P(1-eps))/(2*eps):.5f}  vs pi^2/(6 ln2) = {np.pi**2/(6*np.log(2)):.5f}")

    # where is lambda1(t) == 1?
    l1_close = [(t, a.real) for t, a in zip(ts, l1) if abs(a.real - 1.0) < 2e-3]
    print(f"lambda1 ~= 1 near t = {l1_close}")


if __name__ == "__main__":
    main()
