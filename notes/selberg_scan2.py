#!/usr/bin/env python3
"""Clean resonance scan at sigma=0.505, both parity sectors, for the figure."""
import numpy as np
import sys
sys.path.insert(0, 'notes')
from selberg_lib import Ls_matrix, nearest

xs = 0.5 * (1 + np.cos(np.pi * (np.arange(40) + 0.5) / 40))
K, N = 26, 4000
sig = 0.505
ts = np.arange(2.0, 26.0, 0.25)
out = {'ts': ts}
for odd, op in [(False, 'even'), (True, 'odd')]:
    depths, evre, evim = [], [], []
    for t in ts:
        ev, d = nearest(sig + 1j*t, xs, K, odd, N)
        depths.append(d); evre.append(ev.real); evim.append(ev.imag)
    out[op] = {'depth': np.array(depths), 're': np.array(evre), 'im': np.array(evim)}
    print(f"{op}: min depth {min(depths):.4f} at t={ts[np.argmin(depths)]}", flush=True)
np.savez('notes/selberg_scan2.npz', **out)
print("saved notes/selberg_scan2.npz", flush=True)
