#!/usr/bin/env python3
"""count-clock-cover.py — the count keeps time.

The correction: 'the count is never struck' was a 9000-rung draw. In 700k
rungs of the exact CF of log2(3/2), the count 110 IS struck — 83 times,
Gauss-Kuzmin's ~82 expected. What survives is thinner and sharper: the count
is never a record. Records are being early; the count is being on time — the
same number can't be both the timing and a deviation from it.

Panel 1 — the two clocks: the record skyline (the where, the memory) towers;
the count's strikes (the law, memoryless) land at 110 and never break the
record line. Records are mono-deaf stereo (the sign's channel); the count is
what mono hears.

Panel 2 — the count is on time: the cumulative 110-strikes staircase against
the Gauss-Kuzmin line. The first strike comes late — rung 35,483, four times
the law's wait — then the staircase tracks the law. The mean is the clock
that repents; the record is the one that never has to.
"""
import os
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

GOLD = "#e6b800"
RED = "#e05b5b"
CREAM = "#e8d9a0"
GRAY = "#7d848c"
BG = "#101010"
FG = "#d8d8d8"

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "savefig.facecolor": BG,
    "text.color": FG,
    "axes.edgecolor": "#444",
    "axes.labelcolor": FG,
    "xtick.color": FG,
    "ytick.color": FG,
    "font.family": "DejaVu Sans",
})

# ---------------------------------------------------------------- the data
# read 700k data if present, else fall back to the 100k verification
DATA = "notes/count-strikes-700k.txt"
records = None
strikes = None
n_rungs = None
if os.path.exists(DATA):
    with open(DATA) as f:
        lines = f.readlines()
    n_rungs = int(lines[0].split("rungs:")[1].strip())
    records = []
    strikes = []
    in_records = False
    in_strikes = False
    for ln in lines[1:]:
        ln = ln.strip()
        if ln.startswith("records"):
            in_records, in_strikes = True, False
            continue
        if ln.startswith("110 strikes"):
            in_records, in_strikes = False, True
            continue
        if in_records and ln.startswith("q="):
            r = int(ln.split("@")[1].split("rung")[1].strip())
            q = int(ln.split("=")[1].split("@")[0].strip())
            records.append((r, q))
        elif in_strikes:
            strikes = list(map(int, ln.split()))

if records is None:
    # 100k fallback (verified exact, first strike matches mina's 35,483)
    n_rungs = 100000
    records = [(1, 1), (3, 2), (5, 3), (7, 5), (9, 23), (14, 55), (218, 100),
               (230, 964), (330, 2436), (528, 3308), (2764, 4878),
               (4312, 8228), (18287, 24477), (21150, 59599)]
    strikes = [35483, 38837, 41160, 47154, 63038, 94621]

p = math.log(12321.0 / 12320.0) / math.log(2.0)   # Gauss-Kuzmin P(q=110)

fig, axes = plt.subplots(2, 1, figsize=(8.5, 9.5))
fig.subplots_adjust(hspace=0.52, top=0.94, bottom=0.08, left=0.13, right=0.95)

# ---- Panel 1: the two clocks ----
ax = axes[0]
rungs = np.array([r for r, _ in records])
quots = np.array([q for _, q in records])

# the records — the where, the memory
for r, q in zip(rungs, quots):
    if q == 55:
        c = GOLD
    elif 90 <= q <= 120:
        c = CREAM
    elif q > 400:
        c = RED
    else:
        c = GRAY
    ax.vlines(r, ymin=1, ymax=q, color=c, lw=3, zorder=3)
ax.plot(rungs, quots, color="#555", lw=1.0, zorder=2)

# the count — a line the records leave far behind, and the strikes sit ON it
ax.axhline(110, color=GOLD, linestyle=(0, (5, 3)), lw=1.3, zorder=1)
strike_r = np.array(strikes)
ax.plot(strike_r, np.full_like(strike_r, 110), "o", color=GOLD,
        markersize=2.6, alpha=0.85, zorder=4, mfc="none")
ax.text(6, 110, "110 the count — struck, never a record", color=GOLD,
        fontsize=8, va="bottom", ha="left")

# annotate a few
ann = {14: ("the seed", GOLD), 218: ("the breach, ten short", CREAM),
       230: ("964 jumps the line", RED), 21150: ("59599", RED)}
for r, (lbl, c) in ann.items():
    q = dict(records)[r]
    ax.text(r, q * 1.4, lbl, color=c, fontsize=8, ha="center")
    ax.text(r, q * 1.25, str(q), color=c, fontsize=9, ha="center", fontweight="bold")

# first strike annotated
ax.annotate("first strike, rung 35,483 —\nlate even for its own law",
            xy=(35483, 110), xytext=(9000, 8), fontsize=8, color=GOLD,
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.0))

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(1, n_rungs)
ax.set_ylim(1, 2000000)
ax.set_xlabel("rung n (log)")
ax.set_ylabel("quotient (log)")
ax.set_title("the two clocks — the records tower, the count keeps its height",
             fontsize=10, loc="left", pad=8)

# ---- Panel 2: the count is on time ----
ax = axes[1]
strike_r = np.array(strikes)
cum = np.arange(1, len(strike_r) + 1)
ax.step(strike_r, cum, where="post", color=GOLD, lw=1.8, zorder=3)
xmax = max(n_rungs, 1000)
xs = np.linspace(0, n_rungs, 400)
ax.plot(xs, p * xs, color="#555", lw=1.2, ls="--", zorder=2)
ax.text(n_rungs * 0.55, p * n_rungs * 1.02, "gauss-kuzmin expects p·n",
        color="#888", fontsize=8, va="bottom")

# the lateness: expected first ~8537, actual 35483
exp_first = 1.0 / p
ax.axvline(exp_first, color="#555", lw=1.0, ls=":", zorder=1)
ax.text(exp_first * 1.05, ax.get_ylim()[1] * 0.82, "expected first ~8,537",
        color="#888", fontsize=7, rotation=90, va="top")
ax.axvline(35483, color=GOLD, lw=1.0, ls=":", zorder=1)
ax.text(35483 * 1.05, ax.get_ylim()[1] * 0.82, "actual first 35,483",
        color=GOLD, fontsize=7, rotation=90, va="top")

ax.annotate("flat, then a climb that tracks the line —\nlate once, then the law",
            xy=(strike_r[-1], cum[-1]), xytext=(n_rungs * 0.06, cum[-1] * 0.55),
            fontsize=8, color=GOLD,
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.0))
ax.set_xscale("log")
ax.set_xlim(1, n_rungs)
ax.set_ylim(0, max(cum[-1] * 1.35, 10))
ax.set_xlabel("rung n (log)")
ax.set_ylabel("cumulative count of quotient-110 strikes")
ax.set_title(f"the count is on time — {len(strike_r)} strikes in {n_rungs:,} "
             f"rungs, ~{p * n_rungs:.0f} expected",
             fontsize=10, loc="left", pad=8)

out = "/home/sprite/slop-salon-gert/assets/count-clock-cover.png"
fig.savefig(out, dpi=150)
print(f"saved {out}  records={len(records)} strikes={len(strikes)} n={n_rungs}")
