#!/usr/bin/env python3
"""Pause table for the log2(3/2) record descent.

Extends the integer-Euclidean CF run and tabulates each record's
hold length against its expected value under the Gauss-Kuzmin
distribution: the mean wait for a quotient >= q is 1/log2(1+1/q) ~ q*ln2.
"""
import sys, time, math
import mpmath as mp

def compute(N, D):
    mp.mp.dps = D + 20
    alpha = mp.log(mp.mpf(3) / 2) / mp.log(2)
    tenD = 10 ** D
    A = int(alpha * tenD)
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
        if n % 100000 == 99999:
            print(f"  ... rung {n+1}, max {max_a}, {time.time()-t0:.0f}s", file=sys.stderr)
    return records

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 500000
    D = int(sys.argv[2]) if len(sys.argv) > 2 else int(N * 1.04) + 40
    records = compute(N, D)
    print(f"{N} rungs; {len(records)} records; trusted prefix ~{int(0.97*D)} digits", flush=True)
    print(f"{'rung':>8} {'q':>8} {'hold':>8} {'exp':>10} {'obs/exp':>8}", flush=True)
    prev_rung = None
    prev_q = None
    for (n, a) in records:
        if prev_rung is None:
            hold = float("nan")
        else:
            hold = n - prev_rung
        # mean wait for a quotient > prev record (the one to beat) = 1/log2(1+1/prev_q)
        if prev_q is None:
            exp = float("nan")
            ratio = float("nan")
        else:
            exp = 1.0 / math.log2(1 + 1.0 / prev_q)
            ratio = hold / exp
        print(f"{n:>8} {a:>8} {hold:>8.0f} {exp:>10.0f} {ratio:>8.2f}", flush=True)
        prev_rung, prev_q = n, a
    # open hold
    last_rung, last_q = records[-1]
    exp_open = 1.0 / math.log2(1 + 1.0 / last_q)
    hold_open = N - last_rung
    print(f"\ncurrent record q={last_q} at rung {last_rung}: held {hold_open} rungs, "
          f"expected next ~{exp_open:.0f} (ratio {hold_open/exp_open:.2f})", flush=True)
