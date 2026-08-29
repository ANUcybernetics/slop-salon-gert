#!/usr/bin/env python3
import numpy as np, sys
sys.path.insert(0, 'notes')
from selberg_lib import Ls_matrix

# parity_scan2 settings: 56 nodes, K=30, N=6000
xs56 = 0.5 * (1 + np.cos(np.pi * (np.arange(56) + 0.5) / 56))
# selberg_lib settings: 48 nodes
xs48 = 0.5 * (1 + np.cos(np.pi * (np.arange(48) + 0.5) / 48))

def best(sig, t, xs, K, N):
    A = Ls_matrix(sig + 1j*t, xs, K, True, N)
    ev = np.linalg.eigvals(A)
    d = np.abs(ev - 1.0)
    i = np.argmin(d)
    return ev[i], d[i]

for label, xs, K, N in [("xs56 K30 N6000", xs56, 30, 6000),
                        ("xs48 K30 N6000", xs48, 30, 6000),
                        ("xs48 K30 N4000", xs48, 30, 4000)]:
    for sig in [0.502, 0.505]:
        for t in [9.925, 9.93, 9.94]:
            ev, d = best(sig, t, xs, K, N)
            print(f"{label} sig={sig} t={t}: ev={ev.real:+.4f}{ev.imag:+.4f}j |1-ev|={d:.5f}")
