#!/usr/bin/env python3
"""The count at s=1, the where at s=1/2 — one operator family, the flow.

L_s f(x) = sum_n (x+n)^{-2s} f(1/(x+n))   (Mayer transfer operator)
  s = 1  : the Gauss-Kuzmin-Wirsing operator — real spectrum, the COUNT.
           eigenvalue exactly 1 (constant, the Gauss density) = the first
           zero of the Selberg zeta (Mayer: Z(s) = det(1 - L_s)).
  s = 1/2 + it : the critical line — the surface's spectrum (Maass zeros),
           the WHERE.  det(1 - L_s) = 0 at the spectral zeros.

This script:
  1) confirms the s=1 count spectrum (1, -0.30366, ...);
  2) follows each known Maass zero as sigma -> 1/2: the eigenvalue nearest 1
     pins its t and deepens toward 1 (the resonance becomes the zero);
  3) reports even/odd parity by which operator carries each resonance.
"""
import numpy as np
import sys
sys.path.insert(0, 'notes')
from numpy.polynomial.legendre import legval

def shift_leg(j, t):
    c = np.zeros(j + 1); c[j] = 1.0
    return legval(2.0 * np.asarray(t) - 1.0, c)

def Ls_matrix(s, xs, K, odd=False, N=6000):
    n = np.arange(1, N + 1, dtype=float)
    M = np.zeros((len(xs), K), dtype=complex)
    B = np.zeros((len(xs), K))
    w = 2 * s
    sign = (-1.0) ** n if odd else np.ones(N)
    for j in range(K):
        xrow = xs[None, :] + n[:, None]
        vals = sign[:, None] * shift_leg(j, 1.0 / xrow) * xrow ** (-w)
        M[:, j] = vals.sum(axis=0)
        if not odd:
            M[:, j] += (-1.0) ** j * (xs + N) ** (1 - w) / (w - 1)
        B[:, j] = shift_leg(j, xs)
    return np.linalg.pinv(B) @ M

def nearest(s, xs, K, odd):
    A = Ls_matrix(s, xs, K, odd)
    ev = np.linalg.eigvals(A)
    d = np.abs(ev - 1.0)
    i = np.argmin(d)
    return ev[i], d[i]

def main():
    xs = 0.5 * (1 + np.cos(np.pi * (np.arange(48) + 0.5) / 48))
    K = 30

    print("=== s = 1 : the count's spectrum (GKW) ===")
    ev = np.linalg.eigvals(Ls_matrix(1.0, xs, K))
    order = np.argsort(-np.abs(ev))
    top = ev[order][:5]
    print("  eigenvalues: ", np.round(top.real, 6))
    print("  (expected 1, -0.30366, 0.0931, ...)")

    # Known Maass zeros t_n (Hejhal), with literature parity E/O
    zeros = [
        (9.5337,  'E'),
        (13.7796, 'O'),
        (18.850,  'E'),
        (22.526,  'O'),
        (24.778,  'E'),
    ]
    sigmas = [0.60, 0.56, 0.52, 0.505]

    print("\n=== resonance flow: sigma -> 1/2 for each known zero ===")
    for t0, par in zeros:
        print(f"\n-- t_n = {t0:.4f}  (literature parity {par}) --")
        for odd in [False, True]:
            opname = "EVEN" if not odd else "ODD "
            row = []
            for sig in sigmas:
                ts = np.arange(t0 - 0.6, t0 + 0.6, 0.03)
                best = (1e9, None, None)
                for t in ts:
                    ev, d = nearest(sig + 1j*t, xs, K, odd)
                    if d < best[0]:
                        best = (d, t, ev)
                d, t, ev = best
                row.append(f"sigma={sig}: t={t:.3f} |1-ev|={d:.4f}")
            print(f"  {opname}: " + "  ".join(row))

if __name__ == "__main__":
    main()
