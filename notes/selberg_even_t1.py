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
# even operator at the known Maass zeros t1=9.5337, t3=18.85, t5=24.778
print("EVEN operator, sigma->1/2^+")
for t0 in [9.5337, 18.850, 24.778]:
    for sig in [0.505, 0.502, 0.5005]:
        ev, d = best(sig, t0, 42, 12000, False)
        print(f"  t0={t0} sig={sig}: ev={ev.real:+.5f}{ev.imag:+.5f}j |1-ev|={d:.6f}")
# odd operator at the known ODD Maass zero t2=13.7796 and t4=22.526
print("ODD operator, sigma->1/2^+")
for t0 in [13.7796, 22.526]:
    for sig in [0.505, 0.502, 0.5005]:
        ev, d = best(sig, t0, 42, 12000, True)
        print(f"  t0={t0} sig={sig}: ev={ev.real:+.5f}{ev.imag:+.5f}j |1-ev|={d:.6f}")
