#!/usr/bin/env python3
"""Lean targeted checks (K=30, 48 nodes):
1) Does lambda_1 ~ 91.14 (t=9.53) appear in the even operator near 1?
2) Refine the t~13.78 resonance location (even op).
"""
import numpy as np
import sys
sys.path.insert(0, 'notes')
from selberg_colloc import Ls_matrix

xs = 0.5 * (1 + np.cos(np.pi * (np.arange(48) + 0.5) / 48))
K = 30

def min_dist(s):
    ev = np.linalg.eigvals(Ls_matrix(s, xs, K)[0])
    return np.min(np.abs(ev - 1.0)), ev[np.argmin(np.abs(ev-1))]

print("=== t=9.53 region, even operator ===")
for sig in [0.52, 0.505, 0.501]:
    for t in [9.53, 9.60, 9.70]:
        d, ev = min_dist(sig + 1j*t)
        print(f"  sig={sig} t={t}: min|1-ev|={d:.4f} at ev={ev.real:+.3f}{ev.imag:+.3f}j")

print("=== refine t~13.78 (even op) ===")
for sig in [0.52, 0.51, 0.505, 0.501]:
    best = (1e9, 0)
    for t in np.arange(13.4, 14.2, 0.02):
        d, _ = min_dist(sig + 1j*t)
        if d < best[0]:
            best = (d, t)
    d, t = best
    print(f"  sig={sig}: best t={t:.3f} |1-ev|={d:.5f} -> lambda={0.25+t*t:.4f}")
