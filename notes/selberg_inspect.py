#!/usr/bin/env python3
"""Inspect full spectra at specific s near suspected resonances."""
import numpy as np
import sys
sys.path.insert(0, 'notes')
from selberg_colloc import Ls_matrix

xs = 0.5 * (1 + np.cos(np.pi * (np.arange(48) + 0.5) / 48))
K = 30

for s in [0.52+9.53j, 0.52+13.78j, 0.52+7.05j, 0.52+12.5j, 0.55+9.53j]:
    A, _ = Ls_matrix(s, xs, K)
    ev = np.linalg.eigvals(A)
    d = np.abs(ev - 1.0)
    order = np.argsort(d)
    print(f"s={s}:")
    for i in order[:6]:
        print(f"   ev={ev[i]:+.5f}{ev[i].imag:+.5f}j  |1-ev|={d[i]:.5f}  |ev|={abs(ev[i]):.3f}")
