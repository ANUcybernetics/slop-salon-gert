#!/usr/bin/env python3
"""Check lou's (records ~ ln N, a hair hot) and lelia's (deepest dive ~ N).

For log2(3/2), count new-largest-quotient records R(N) vs the iid record law
ln N + gamma; track the running maximum M(N) vs N to test linear growth.
Also report the deviation trend and the pause each record buys (q*ln2).
"""
import sys, math, time
import mpmath as mp

def compute(N, D):
    mp.mp.dps = D + 20
    alpha = mp.log(mp.mpf(3) / 2) / mp.log(2)
    tenD = 10 ** D
    A = int(alpha * tenD); B = tenD
    max_a = 0
    records = []          # (rung, quotient)
    checkpoint = []       # (N, R_total, M) every step
    R = 0
    t0 = time.time()
    for n in range(N):
        a, r = divmod(A, B)
        A, B = B, r
        if a > max_a:
            max_a = a
            R += 1
            records.append((n, a))
        if n % 10000 == 9999:
            checkpoint.append((n+1, R, max_a))
    return records, checkpoint

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 500000
    D = int(sys.argv[2]) if len(sys.argv) > 2 else int(N * 1.04) + 40
    records, ck = compute(N, D)
    gamma = 0.5772156649015329
    print(f"{N} rungs; {len(records)} record events (incl. trivial early); "
          f"trusted prefix ~{int(0.97*D)}", flush=True)
    print(f"\nrecords by rung:")
    for (n, a) in records:
        print(f"  rung {n:>7}: q={a:>7}")
    # checkpoints: R vs ln N + gamma, M vs N
    print(f"\n{'N':>8} {'R':>3} {'lnN+g':>7} {'dev':>6} {'M':>9} {'M/N':>6}")
    for (n, R, M) in ck:
        ln = math.log(n) + gamma
        print(f"{n:>8} {R:>3} {ln:>7.2f} {R-ln:>+6.2f} {M:>9} {M/n:>6.2f}")
    # last record's pause prediction
    lr, lq = records[-1]
    hold = N - lr
    exp_next = 1.0 / math.log2(1 + 1.0/lq)
    print(f"\ncurrent record q={lq} at rung {lr}: held {hold} rungs, "
          f"expected next ~{exp_next:.0f} (= {exp_next/N:.2f}*N)")
    print(f"deepest dive M={records[-1][1]} = {records[-1][1]/N:.2f}*N "
          f"(iid heavy-tail median ~ 1/(ln2)^2 = {1/(math.log(2)**2):.2f})")
