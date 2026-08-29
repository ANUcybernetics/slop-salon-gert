#!/usr/bin/env python3
"""Find zeros of det(1 - L_s) on the critical line via eigenvalue tracking.

det(1 - L_s) = 0  <=>  L_s has an eigenvalue 1.
So scan t and track the leading eigenvalue(s) of L_{1/2 + it}.
Known: lambda_0 = 0 -> zero at s = 1 (t = i/2).
lambda_1 ~ 91.14134 -> t ~ 9.5337.  lambda_2 ~ 190.13334 -> t ~ 13.7796.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, 'notes')
from selberg_mayer import L_matrix

def leading_eigs(s, K=30, n=6):
    M = L_matrix(s, K)
    ev = np.linalg.eigvals(M)
    idx = np.argsort(np.abs(ev - 1.0))
    return ev[idx[:n]]

# 1) Convergence check at a few s
for s, name in [(1.0, "s=1"), (0.5+9.5337j, "t=9.5337"), (0.5+0.5j, "t=0.5")]:
    print(f"--- {name} ---")
    for K in [10, 20, 30, 40]:
        ev = np.linalg.eigvals(L_matrix(s, K))
        near = ev[np.argsort(np.abs(ev-1))][:3]
        print(f"  K={K:2d}  eigs near 1: {np.round(near, 5)}")
