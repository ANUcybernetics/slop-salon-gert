#!/usr/bin/env python3
import numpy as np, sys
sys.path.insert(0, 'notes')
from selberg_lib import Ls_matrix
xs = 0.5 * (1 + np.cos(np.pi * (np.arange(48) + 0.5) / 48))
def best(sig, t, K, N, odd):
    A = Ls_matrix(sig + 1j*t, xs, K, odd, N)
    ev = np.linalg.eigvals(A)
    d = np.abs(ev - 1.0); i = np.argmin(d)
    return ev[i], d[i]
print("EVEN operator at t2=13.7796 (the known Maass zero my notes matched):")
for sig in [0.505, 0.502, 0.5005, 0.5002]:
    ev, d = best(sig, 13.7796, 42, 12000, False)
    print(f"  sig={sig}: ev={ev.real:+.5f}{ev.imag:+.5f}j |1-ev|={d:.6f}")
# refine t around 13.78 for the even operator
print("EVEN operator, t scan 13.5..14.0 at sigma=0.5005:")
for t in np.arange(13.55, 14.0, 0.025):
    ev, d = best(0.5005, t, 42, 12000, False)
    if d < 0.1:
        print(f"  t={t:.3f}: ev={ev.real:+.5f}{ev.imag:+.5f}j |1-ev|={d:.6f}")
