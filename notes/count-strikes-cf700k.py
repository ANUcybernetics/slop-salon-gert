#!/usr/bin/env python3
"""Exact CF of log2(3/2) to 700k rungs.

Records (strict new maxima) and positions where quotient == 110 (the count).
Output: notes/count-strikes-700k.txt
"""
import time
from mpmath import mp

D = int(700000 / 0.97) + 20
mp.dps = D + 10
t0 = time.time()
x = mp.log(3, 2) - 1          # log2(3/2)
A = int(x * mp.mpf(10) ** D)
B = 10 ** D
t1 = time.time()

records = []                    # (rung, quotient)
strikes110 = []                 # rungs where quotient == 110
rec = 0
for r in range(700000):
    a, A, B = A // B, B, A % B
    if a == 110:
        strikes110.append(r)
    if a > rec:
        rec = a
        records.append((r, a))
    if B == 0:
        break
t2 = time.time()

with open("notes/count-strikes-700k.txt", "w") as f:
    f.write(f"log2(3/2) mpmath: {t1-t0:.1f}s, euclid: {t2-t1:.1f}s, rungs: {r+1}\n")
    f.write(f"records ({len(records)}):\n")
    for r, a in records:
        f.write(f"  q={a} @ rung {r}\n")
    f.write(f"110 strikes ({len(strikes110)}):\n")
    f.write("  " + " ".join(map(str, strikes110)) + "\n")
print("done in %.1fs, %d rungs, %d records, %d strikes" %
      (t2 - t0, r + 1, len(records), len(strikes110)))
