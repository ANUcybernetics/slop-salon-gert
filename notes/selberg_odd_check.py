#!/usr/bin/env python3
"""Settle the odd gap-note t~9.94: is the resonance real, and is the -0.008
imag a resolution artifact? Scan odd operator, two K and two N, sigma -> 1/2."""
import numpy as np
import sys
sys.path.insert(0, 'notes')
from selberg_lib import Ls_matrix

xs = 0.5 * (1 + np.cos(np.pi * (np.arange(48) + 0.5) / 48))

def best_near(s, xs, K, odd, N):
    A = Ls_matrix(s, xs, K, odd, N)
    ev = np.linalg.eigvals(A)
    d = np.abs(ev - 1.0)
    i = np.argmin(d)
    return ev[i], d[i]

print("ODD operator, t scan 9.6..10.4, sigma -> 1/2^+")
for sig in [0.55, 0.52, 0.505, 0.501, 0.5005]:
    row = []
    for (K, N) in [(30, 6000), (36, 9000), (42, 12000)]:
        ts = np.arange(9.55, 10.35, 0.025)
        best = (1e9, None, None)
        for t in ts:
            ev, d = best_near(sig + 1j*t, xs, K, True, N)
            if d < best[0]:
                best = (d, t, ev)
        d, t, ev = best
        row.append(f"K{N//300}={K}: t={t:.3f} re={ev.real:+.4f} im={ev.imag:+.4f} |1-ev|={d:.5f}")
    print(f"  sigma={sig:.4f}  " + " | ".join(row), flush=True)
