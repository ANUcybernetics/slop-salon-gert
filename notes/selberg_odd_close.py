#!/usr/bin/env python3
import numpy as np, sys
sys.path.insert(0, 'notes')
from selberg_lib import Ls_matrix

xs = 0.5 * (1 + np.cos(np.pi * (np.arange(48) + 0.5) / 48))

def best(sig, t, K, N):
    A = Ls_matrix(sig + 1j*t, xs, K, True, N)
    ev = np.linalg.eigvals(A)
    d = np.abs(ev - 1.0)
    i = np.argmin(d)
    return ev[i], d[i]

print("K-stability of the t~9.934 resonance + gap closure as sigma->1/2^+")
for sig in [0.503, 0.502, 0.501, 0.5005, 0.5002]:
    for K, N in [(30, 6000), (36, 9000), (42, 12000)]:
        ts = np.arange(9.90, 9.98, 0.0015)
        bestd = (1e9, None)
        for t in ts:
            ev, d = best(sig, t, K, N)
            if d < bestd[0]:
                bestd = (d, (t, ev))
        d, (t, ev) = bestd
        print(f"  sig={sig:.4f} K={K} N={N}: t={t:.4f} ev={ev.real:+.5f}{ev.imag:+.5f}j |1-ev|={d:.6f}")
    print(flush=True)
