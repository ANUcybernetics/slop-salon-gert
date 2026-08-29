#!/usr/bin/env python3
"""Scan the critical line: find t where L_{sigma+it} has an eigenvalue ~ 1.

As sigma -> 1/2+, these are the zeros of det(1 - L_s) on Re s = 1/2.
Known resonances: t ~ 9.5337 (lambda_1 ~ 91.14), t ~ 13.7796 (lambda_2 ~ 190.13).
"""
import numpy as np
import sys
sys.path.insert(0, 'notes')
from selberg_colloc import Ls_matrix

def nearest_one(s, xs, K):
    A, _ = Ls_matrix(s, xs, K)
    ev = np.linalg.eigvals(A)
    d = np.abs(ev - 1.0)
    i = np.argmin(d)
    return ev[i], d[i]

def main():
    xs = 0.5 * (1 + np.cos(np.pi * (np.arange(40) + 0.5) / 40))
    K = 24
    ts = np.arange(0.0, 16.0, 0.05)
    out = {}
    for sigma in [0.6, 0.55, 0.52]:
        print(f"scanning sigma={sigma} ...", file=sys.stderr)
        rows = []
        for t in ts:
            ev, d = nearest_one(1j * t + sigma, xs, K)
            rows.append((t, ev.real, ev.imag, d))
        out[sigma] = np.array(rows)
    for sigma, r in out.items():
        np.save(f'notes/scan_s{sigma}.npy', r)
        # report local minima of d
        d = r[:, 3]
        mins = []
        for i in range(1, len(ts) - 1):
            if d[i] < d[i-1] and d[i] < d[i+1] and d[i] < 0.3:
                mins.append((ts[i], r[i,1], r[i,2], d[i]))
        print(f"sigma={sigma}: dips (t, re, im, min|1-lam|):")
        for m in mins[:20]:
            print(f"   t={m[0]:6.2f}  ev={m[1]:+.3f}{m[2]:+.3f}j  |1-ev|={m[3]:.3f}")

if __name__ == "__main__":
    main()
