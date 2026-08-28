#!/usr/bin/env python3
"""Integer Euclidean CF of log2(3/2). A = round(alpha*10^D), B = 10^D.
The first ~0.97*D quotients of A/B match alpha's true CF. Tracks records.
Fast: pure big-int divmod. Usage: cf-int.py <N_rungs> [D_digits]
"""
import sys, time
import mpmath as mp

def compute(N, D):
    mp.mp.dps = D + 20
    alpha = mp.log(mp.mpf(3) / 2) / mp.log(2)
    tenD = 10 ** D
    A = int(alpha * tenD)          # floor(alpha*10^D)
    B = tenD
    max_a = 0
    records = []
    t0 = time.time()
    for n in range(N):
        if B == 0:
            break
        a, r = divmod(A, B)
        A, B = B, r
        if a > max_a:
            max_a = a
            records.append((n, a))
        if n % 10000 == 9999:
            print(f"  ... rung {n+1}, max {max_a}, {time.time()-t0:.0f}s", file=sys.stderr)
    return alpha, records

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 40000
    D = int(sys.argv[2]) if len(sys.argv) > 2 else int(N * 1.04) + 40
    alpha, records = compute(N, D)
    print(f"alpha ~ {mp.nstr(alpha, 20)}; {N} rungs from rational with {D} digits "
          f"(trust prefix ~{int(0.97*D)})")
    print(f"{len(records)} records:")
    prev = None
    for (n, a) in records:
        pause = "" if prev is None else f"  |  held {n-prev} rungs"
        print(f"  rung {n:>7}: quotient {a:>7}  width ~1/{a:<6} = {1/a:.6g}{pause}")
        prev = n
    print(f"\n  current max {records[-1][1]} at rung {records[-1][0]}: "
          f"open at rung {N} ({N-records[-1][0]} rungs held)")
