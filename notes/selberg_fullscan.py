#!/usr/bin/env python3
"""Full resonance scan: |1 - lambda_min| vs t for even and odd operators.
Coarse then refine. Saves to npz for plotting.
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

def eig_near_one(s, xs, K, odd, thresh=0.3):
    A = Ls_matrix(s, xs, K, odd)
    ev = np.linalg.eigvals(A)
    d = np.abs(ev - 1.0)
    idx = np.where(d < thresh)[0]
    order = idx[np.argsort(d[idx])]
    return [(ev[i], d[i]) for i in order[:4]]

def main():
    xs = 0.5 * (1 + np.cos(np.pi * (np.arange(56) + 0.5) / 56))
    K = 32
    sigma = 0.505
    ts = np.arange(0.0, 26.0, 0.25)
    results = {}
    for odd in [False, True]:
        name = "even" if not odd else "odd"
        print(f"scanning {name} ...", file=sys.stderr)
        rows = []
        for t in ts:
            near = eig_near_one(sigma + 1j*t, xs, K, odd, thresh=0.4)
            rows.append((t, [(ev.real, ev.imag, d) for ev, d in near]))
        results[name] = rows
        print(f"done {name}", file=sys.stderr)
    np.save('notes/resonance_scan.npy', np.array([ts], dtype=object), allow_pickle=True)
    import pickle
    with open('notes/resonance_scan.pkl', 'wb') as f:
        pickle.dump(results, f)
    # print dips
    for name, rows in results.items():
        print(f"--- {name} (sigma={sigma}) ---")
        for t, near in rows:
            if near:
                evs = ", ".join(f"{ev[0]:.3f}{ev[1]:+.3f}j({ev[2]:.2f})" for ev in near)
                print(f"  t={t:5.2f}: {evs}")

if __name__ == "__main__":
    main()
