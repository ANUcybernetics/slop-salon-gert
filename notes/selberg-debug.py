import numpy as np
from math import factorial
import sys
sys.path.insert(0, 'notes')
from selberg_mayer import L_matrix, zeta_em

np.set_printoptions(precision=2, suppress=True, linewidth=200)
for s in [1.0, 0.5+9.5337j]:
    print(f"=== s={s} ===")
    for K in [2,3,5,8,10,15,20,30]:
        M = L_matrix(s, K)
        # entries scale
        mx = np.max(np.abs(M))
        d = np.linalg.det(np.eye(K)-M)
        print(f"  K={K:2d}  max|M|={mx:.3e}  det={d:.3e}  |det|={abs(d):.3e}")
    if s==1.0:
        M5 = L_matrix(s, 5)
        print("M(5x5) at s=1:\n", M5)
