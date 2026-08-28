#!/usr/bin/env python3
"""Check lou's draw shape claim (Aug 28, 3mu54s3pxxh2v):

    the next record is q·r — a Pareto-1 step, no mean, median ×2, E[ln r]=1.
    the record climbs one log-unit per step.

For a record q_k with q_{k+1} = q_k · r_k, if r is Pareto-1 (P(r>x)=1/x on [1,∞))
then ln r ~ Exp(1): mean 1, median ln2 ≈ 0.693, no mean for r itself.

Reads a record list (rung, quotient) from a file, or uses built-in known records.
"""
import sys, math

KNOWN = [(0, 2), (1, 3), (2, 5), (3, 23), (4, 55), (5, 100), (6, 964),
         (7, 2436), (8, 3308), (9, 4878), (10, 8228), (11, 24477),
         (12, 59599), (13, 104733), (14, 698813), (15, 1138268)]

def load(path):
    recs = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("rung"):
                parts = line.split()
                # "rung 12345: q=678"
                try:
                    n = int(parts[1].rstrip(":"))
                    q = int(parts[3].split("=")[1])
                    recs.append((n, q))
                except (IndexError, ValueError):
                    pass
    return recs

def analyze(recs, label):
    print(f"=== {label}: {len(recs)} records ===")
    if len(recs) < 3:
        print("  too few")
        return
    qs = [q for (_, q) in recs]
    ratios = [qs[i+1] / qs[i] for i in range(len(qs)-1)]
    lnr = [math.log(r) for r in ratios]
    mean_lnr = sum(lnr) / len(lnr)
    sorted_lnr = sorted(lnr)
    med_lnr = (sorted_lnr[len(sorted_lnr)//2]
               if len(sorted_lnr) % 2 else
               (sorted_lnr[len(sorted_lnr)//2 - 1] + sorted_lnr[len(sorted_lnr)//2]) / 2)
    med_r = math.exp(med_lnr)
    print(f"  n ratios = {len(ratios)}")
    print(f"  E[ln r]  = {mean_lnr:.3f}   (lou: 1)")
    print(f"  median ln r = {med_lnr:.3f}  -> median r = {med_r:.2f}   (lou: ×2)")
    print(f"  min/max r = {min(ratios):.2f} / {max(ratios):.2f}")
    # Pareto-1 tail check: P(r > x) ≈ 1/x  ->  x·(1-F(x)) ≈ 1
    xs = sorted(ratios, reverse=True)
    print("  tail check  x * (rank/n):")
    for i, x in enumerate(xs[:6]):
        F = (i + 0.5) / len(xs)     # mid-rank empirical CDF
        print(f"    r={x:>6.2f}  x·(1-F)={x*(1-F):.2f}")
    # log-unit climb: total ln advance = sum lnr = ln(last/first)
    total = math.log(qs[-1] / qs[0])
    print(f"  total log-climb = {total:.2f} over {len(ratios)} steps -> {total/len(ratios):.3f} per step")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    if path:
        recs = load(path)
        analyze(recs, path)
    else:
        analyze(KNOWN, "known 500k records")
