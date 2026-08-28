#!/usr/bin/env python3
"""Continued fraction records of log2(3/2): verify/extend lou's "the floor was a pause".

lou computed to rung 4000 and found record partial quotients
23, 55, 100, 964, 2436, 3308, 4878; 1/55 held 204 rungs; 1/4878 held 1236 rungs
and "an unbounded fifth breaks it by ~3400". This recomputes further and
tracks every record-max event, its rung, its pause (rungs held), and the
width q^2 * ||q*alpha|| of the convergent that set it.
"""
import sys
import mpmath as mp

mp.mp.dps = 6000  # plenty for N=20k; ~0.3 digits/rung needed, use 0.4 as margin

def cf_of_log2_3over2(N, dps=6000):
    mp.mp.dps = dps
    alpha = mp.log(mp.mpf(3) / 2) / mp.log(2)
    x = alpha
    # convergents p/q
    p_prev2, q_prev2 = 0, 1   # p_{-2}, q_{-2}
    p_prev1, q_prev1 = 1, 0   # p_{-1}, q_{-1}
    max_a = 0
    records = []   # (rung_index_of_newmax, quotient_value)
    # for widths: track q_n and p_n
    for n in range(N):
        a = int(x)          # partial quotient
        x = 1 / (x - a)
        p = a * p_prev1 + p_prev2
        q = a * q_prev1 + q_prev2
        p_prev2, q_prev2 = p_prev1, q_prev1
        p_prev1, q_prev1 = p, q
        if a > max_a:
            max_a = a
            # width of this convergent: q^2 * |alpha - p/q| = q * |q*alpha - p|
            w = q * abs(q * alpha - p)
            records.append((n, a, float(w), q))
    return alpha, records

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    dps = int(N * 0.35) + 60
    alpha, records = cf_of_log2_3over2(N, dps)
    print(f"alpha = log2(3/2) ~ {mp.nstr(alpha, 25)}")
    print(f"computed {N} rungs at dps={dps}; {len(records)} record-max events")
    print(f"\n{'newmax @rung':>14} {'quotient':>9} {'width w=q||qa||':>20} {'1/qm approx':>12} {'log10 denom':>12}")
    prev_rung = None
    for (n, a, w, q) in records:
        pause = "" if prev_rung is None else f"pause {n - prev_rung} rungs"
        import math
        print(f"{n:>14} {a:>9} {w:>20.6g} {1.0/a:>12.6g} {math.log10(q):>12.2f}  {pause}")
        prev_rung = n
    # growth check: max quotient at the end
    # recompute tracking running max at sampled rungs for growth law
    print("\ngrowth of running max of partial quotients (sampled):")
    mp.mp.dps = dps
    x = mp.log(mp.mpf(3) / 2) / mp.log(2)
    max_a = 0
    samples = []
    step = max(1, N // 20)
    for n in range(N):
        a = int(x)
        x = 1 / (x - a)
        if a > max_a:
            max_a = a
        if (n + 1) % step == 0:
            samples.append((n + 1, max_a, float(max_a) / (n + 1)))
    for (n, m, ratio) in samples:
        print(f"  rung {n:>6}: running max {m:>7}  (max/rung {ratio:.4f})")
