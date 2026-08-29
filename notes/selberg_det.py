#!/usr/bin/env python3
"""det(I - A) from collocation for L_s, vs t. Look for sharp dips (resonances).
Zeros of det(1 - L_s) on Re s = 1/2. Known t: 9.534 (91.14), 13.780 (190.13),
18.85 (355.6), 22.53 (507.8), 24.78 (614.4).
"""
import numpy as np
import sys
sys.path.insert(0, 'notes')
from numpy.polynomial.legendre import legval

def shift_leg(j, t):
    c = np.zeros(j + 1); c[j] = 1.0
    return legval(2.0 * np.asarray(t) - 1.0, c)

def Ls_matrix(s, xs, K, N=6000):
    n = np.arange(1, N + 1, dtype=float)
    M = np.zeros((len(xs), K), dtype=complex)
    B = np.zeros((len(xs), K))
    w = 2 * s
    for j in range(K):
        xrow = xs[None, :] + n[:, None]
        vals = shift_leg(j, 1.0 / xrow) * xrow ** (-w)
        M[:, j] = vals.sum(axis=0) + (-1.0) ** j * (xs + N) ** (1 - w) / (w - 1)
        B[:, j] = shift_leg(j, xs)
    return np.linalg.pinv(B) @ M

def logdet_one_minus(s, xs, K):
    A = Ls_matrix(s, xs, K)
    ev = np.linalg.eigvals(np.eye(K) - A)
    return np.sum(np.log(np.abs(ev))), np.sum(np.angle(ev))

xs = 0.5 * (1 + np.cos(np.pi * (np.arange(56) + 0.5) / 56))
K = 34
sigma = 0.505
ts = np.arange(0.0, 26.0, 0.1)
ld = []
for t in ts:
    v, ph = logdet_one_minus(sigma + 1j*t, xs, K)
    ld.append(v)
ld = np.array(ld)
np.save('notes/detlog_t.npy', ld)

# find local minima of log|det| (sharp dips)
dips = []
for i in range(1, len(ts)-1):
    if ld[i] < ld[i-1] and ld[i] < ld[i+1]:
        dips.append((ts[i], ld[i]))
# report the deepest dips, relative to the local baseline
for t, v in dips:
    if v < 2.0:   # log|det| < 2 means |det| < 7.4
        print(f"  t={t:5.2f}  log|det|={v:8.3f}")
