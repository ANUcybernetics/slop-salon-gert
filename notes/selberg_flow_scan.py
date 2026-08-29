#!/usr/bin/env python3
"""Scan the resonance flow for the first five Maass zeros as sigma -> 1/2.

For each known zero t_n and each operator (even/odd), find where an
eigenvalue of L_{sigma+it} is nearest 1, at several sigma.  Saves a npz for
plotting and prints a compact table.
"""
import numpy as np
import sys
sys.path.insert(0, 'notes')
from selberg_lib import Ls_matrix, nearest

xs = 0.5 * (1 + np.cos(np.pi * (np.arange(40) + 0.5) / 40))
K = 26
N = 4000

# (t0, literature parity, label)
zeros = [
    (9.5337,  'E', 't1'),
    (13.7796, 'O', 't2'),
    (18.850,  'E', 't3'),
    (22.526,  'O', 't4'),
    (24.778,  'E', 't5'),
]
sigmas = [0.60, 0.56, 0.52, 0.505]
results = {}   # key = zero label, value = {sigma: {'pos','depth','ev'}} for both operators

def scan_one(sig, t0, odd):
    ts = np.arange(t0 - 0.55, t0 + 0.55, 0.05)
    best = (1e9, None, None)
    for t in ts:
        ev, d = nearest(sig + 1j*t, xs, K, odd, N)
        if d < best[0]:
            best = (d, t, ev)
    return best  # (d, t, ev)

for t0, par, lab in zeros:
    print(f"=== {lab}: t0={t0:.4f} (literature {par}) ===", flush=True)
    results[lab] = {'t0': t0, 'par': par}
    for odd in [False, True]:
        op = 'even' if not odd else 'odd'
        results[lab][op] = {}
        for sig in sigmas:
            d, t, ev = scan_one(sig, t0, odd)
            results[lab][op][sig] = {'pos': t, 'depth': d, 're': ev.real, 'im': ev.imag}
            print(f"  {op:4s} sigma={sig:.3f}: t={t:.3f} |1-ev|={d:.4f}  ev={ev.real:+.4f}{ev.imag:+.4f}j", flush=True)

np.savez('notes/selberg_flow.npz', results=results)
print("\nsaved notes/selberg_flow.npz", flush=True)
