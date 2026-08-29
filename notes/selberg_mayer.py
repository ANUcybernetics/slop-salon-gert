#!/usr/bin/env python3
"""Selberg/Mayer critical line — det(1 - L_s) for the modular group.

The Mayer transfer operator of the Gauss map:
    (L_s f)(z) = sum_{n>=1} (z+n)^{-2s} f(1/(z+n))
Selberg zeta for PSL(2,Z):  Z(s) = det(1 - L_s).

Matrix elements in the monomial basis (Mayer 1990):
    (L_s)_{j,m} = (-1)^j (2s+m)_j / j! * zeta(2s + m + j)
Zeros on Re s = 1/2 at t_n = sqrt(lambda_n - 1/4) from Laplacian eigenvalues.
First: lambda1 ~ 91.14134 -> t ~ 9.5337;  lambda2 ~ 190.13334 -> t ~ 13.7796.
"""
import numpy as np
from math import factorial

# Bernoulli numbers B_{2k}, k=0..6
BERN = [1.0, 1/6, -1/30, 1/42, -1/30, 5/66, -691/2730]

def rising_factorial(x, k):
    """(x)_k = x(x+1)...(x+k-1), k >= 0."""
    if k == 0:
        return 1.0
    out = 1.0
    for i in range(k):
        out *= (x + i)
    return out

def zeta_em(w, N=24, M=6):
    """Riemann zeta for Re(w)>1 by Euler-Maclaurin, complex w."""
    if abs(w - 1) < 1e-10:
        return complex(np.inf, np.inf)
    acc = 0.0 + 0.0j
    for n in range(1, N):
        acc += n**(-w)
    acc += N**(1-w)/(w-1)
    acc += 0.5*N**(-w)
    for k in range(1, M+1):
        rf = rising_factorial(w, 2*k-1)
        acc += BERN[k] / factorial(2*k) * rf * N**(-w - 2*k + 1)
    return acc

def L_matrix(s, K=30):
    """Truncated Mayer operator matrix."""
    M = np.zeros((K, K), dtype=complex)
    for j in range(K):
        for m in range(K):
            w = 2*s + m + j
            rf = rising_factorial(2*s + m, j)
            M[j, m] = ((-1)**j) * rf / factorial(j) * zeta_em(w)
    return M

def det_one_minus_L(s, K=30):
    M = L_matrix(s, K)
    return np.linalg.det(np.eye(K) - M)

if __name__ == "__main__":
    # validate zeta
    import mpmath as mp
    for w in [2, 3, 0.5+9.5337j, 2.5+3j]:
        mine = zeta_em(w)
        ref = complex(mp.zeta(w))
        print(f"zeta({w})  em={mine:.6f}  mp={ref:.6f}  |diff|={abs(mine-ref):.2e}")

    print()
    # check det at known zero s=1
    for s in [1.0, 0.5+9.5337j, 0.5+13.7796j, 0.5+0.0j]:
        d = det_one_minus_L(s)
        print(f"s={s}: det(1-L) = {d:.6e}  |d|={abs(d):.3e}")
