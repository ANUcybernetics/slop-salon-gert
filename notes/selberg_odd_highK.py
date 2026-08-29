#!/usr/bin/env python3
import numpy as np, sys
sys.path.insert(0, 'notes')
from selberg_lib import Ls_matrix
xs = 0.5 * (1 + np.cos(np.pi * (np.arange(48) + 0.5) / 48))
def best(sig, t, K, N):
    A = Ls_matrix(sig + 1j*t, xs, K, True, N)
    ev = np.linalg.eigvals(A)
    d = np.abs(ev - 1.0); i = np.argmin(d)
    return ev[i], d[i]
for K, N in [(48, 16000), (56, 18000)]:
    ts = np.arange(9.90, 9.98, 0.001)
    bestd = (1e9, None)
    for t in ts:
        ev, d = best(0.5005, t, K, N)
        if d < bestd[0]:
            bestd = (d, (t, ev))
    d, (t, ev) = bestd
    print(f"K={K} N={N}: t={t:.4f} ev={ev.real:+.5f}{ev.imag:+.5f}j |1-ev|={d:.6f}", flush=True)
