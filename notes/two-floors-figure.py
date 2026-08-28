import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def convergents(x, n):
    p_prev, q_prev = 1, 0
    p_cur, q_cur = int(x), 1
    a = int(x); rem = x - a
    yield (a, (p_cur, q_cur))
    for _ in range(n):
        if rem == 0: break
        r = 1/rem
        a = int(r)
        p_cur, q_cur, p_prev, q_prev = a*p_cur+p_prev, a*q_cur+q_prev, p_cur, q_cur
        rem = r - a
        yield (a, (p_cur, q_cur))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), sharey=True)

# phi: all quotients 1 -> width settles at 1/sqrt5
phi = (1+5**0.5)/2
cfs = list(convergents(phi, 18))
qs = [q for a,(p,q) in cfs]
ws = [q*q*abs(phi - p/q) for a,(p,q) in cfs]
ax1.semilogx(qs, ws, "o-", color="#d4af37", lw=1.5, ms=5)
ax1.axhline(1/5**0.5, color="#d4af37", ls="--", lw=1, alpha=0.7)
ax1.text(qs[1], 1/5**0.5*1.06, "1/√5  the floor", color="#d4af37", fontsize=9)
ax1.set_title("φ = (1+√5)/2 — all quotients 1", fontsize=11)
ax1.set_xlabel("q (convergent denominator)")
ax1.set_ylabel("width  q²|x − p/q|")
ax1.set_ylim(0.05, 0.7)

# log2(3/2): records descend, no floor
x = math.log2(1.5)
cfs = list(convergents(x, 30))
qs = [q for a,(p,q) in cfs]
ws = [q*q*abs(x - p/q) for a,(p,q) in cfs]
best = float('inf')
rec_q, rec_w = [], []
for q,w in zip(qs, ws):
    if w < best - 1e-12:
        best = w
        rec_q.append(q); rec_w.append(w)
ax2.semilogx(qs, ws, "o", color="#b87333", ms=3.5, alpha=0.55)
ax2.plot(rec_q, rec_w, "o-", color="#b87333", lw=2, ms=6)
for q,w,lab in [(665, 0.0419, "665→23"), (190537, 0.0177, "190537→55"), (171928773, 1e-6, "→114")]:
    ax2.annotate(lab, (q,w), textcoords="offset points", xytext=(4,-14),
                 fontsize=8.5, color="#b87333")
ax2.set_title("log₂(3/2) — rungs 23, 55, 114… no floor", fontsize=11)
ax2.set_xlabel("q (convergent denominator)")
ax2.set_ylim(0.05, 0.7)

fig.suptitle("the two arithmetics — a floor settles, a descent asks", fontsize=12)
fig.tight_layout(rect=[0,0,1,0.95])
fig.savefig("assets/two-floors.png", dpi=150)
print("saved assets/two-floors.png")
