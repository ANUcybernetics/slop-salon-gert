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

# fine t scan: where does the odd eigenvalue's imag cross 0, and what is the real part there?
for sig in [0.505, 0.502, 0.501, 0.5005]:
    ts = np.arange(9.90, 9.99, 0.002)
    prev = None
    cross = None
    bestd = (1e9, None)
    for t in ts:
        ev, d = best(sig, t, 36, 9000)
        if d < bestd[0]:
            bestd = (d, (t, ev))
        im = ev.imag
        if prev is not None and prev[1] * im < 0:
            cross = (prev[0], t)
        prev = (t, im)
    d, (t, ev) = bestd
    c = f"imag crosses in ({cross[0]:.3f},{cross[1]:.3f})" if cross else "no imag crossing"
    print(f"sigma={sig}: best t={t:.3f} ev={ev.real:+.5f}{ev.imag:+.5f}j |1-ev|={d:.5f} | {c}", flush=True)
