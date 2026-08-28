#!/usr/bin/env python3
"""Longer CF run for log2(3/2). Finds record partial quotients and their pauses.
dps is set so the guaranteed-correct prefix is ~0.97*dps rungs.
"""
import sys, time
import mpmath as mp

def run(N, dps):
    mp.mp.dps = dps
    alpha = mp.log(mp.mpf(3) / 2) / mp.log(2)
    x = alpha
    max_a = 0
    records = []
    t0 = time.time()
    for n in range(N):
        a = int(x)
        x = 1 / (x - a)
        if a > max_a:
            max_a = a
            records.append((n, a))
        if n % 20000 == 19999:
            print(f"  ... rung {n+1}, max {max_a}, {time.time()-t0:.0f}s", file=sys.stderr)
    return alpha, records

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 60000
    dps = int(N * 1.04) + 40
    alpha, records = run(N, dps)
    print(f"alpha log2(3/2) ~ {mp.nstr(alpha, 20)}; computed {N} rungs at dps={dps} "
          f"(guaranteed prefix ~{int(0.97*dps)})")
    print(f"{len(records)} record-max events:\n")
    prev = None
    for (n, a) in records:
        pause = "" if prev is None else f"  |  held {n-prev} rungs"
        print(f"  rung {n:>7}: quotient {a:>7}   width ~1/{a:<7} = {1/a:.6g}{pause}")
        prev = n
    # current open pause
    print(f"\n  current max {records[-1][1]} at rung {records[-1][0]}: "
          f"still held at rung {N} ({N-records[-1][0]} rungs, open)")
    # growth samples
    mp.mp.dps = dps
    x = mp.log(mp.mpf(3) / 2) / mp.log(2)
    max_a = 0
    step = max(1, N // 12)
    out = []
    for n in range(N):
        a = int(x)
        x = 1 / (x - a)
        if a > max_a:
            max_a = a
        if (n + 1) % step == 0:
            out.append((n + 1, max_a, max_a / (n + 1)))
    print("\nmax-quotient growth (rung, running max, max/rung):")
    for t in out:
        print(f"  {t[0]:>8}  {t[1]:>8}   {t[2]:.4f}")
