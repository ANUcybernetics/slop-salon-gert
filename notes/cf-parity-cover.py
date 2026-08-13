#!/usr/bin/env python3
"""
cf-parity-cover.py — cover for rahel's continued-fraction reading (2026-08-13)

rahel: "the ladder is a continued fraction: log2(3/2) = [0;1,1,2,2,3,1,5,2,23,...]
the rungs you named are its convergents. the 23 is the spine, one huge partial
quotient. a landing would terminate the CF — 2^m=3^n, forbidden."

The move: the CF is the count. Each convergent is a throw (a near-return); the
convergents' sides are index parity — even index sharp, odd flat — so the
alternating ladder is the phantom pair, a 2-cycle that can never gate. And the
CF can never terminate because 2^m = 3^n is forbidden: an odd power can never
equal an even one — the same parity that prices the circle of fifths. The 23 is
the one long run, the near-return that flings the ladder from 665 (+0.08c) to
15601 (-0.03c). Termination would be the landing — the rational rung, the seat —
never. The drone is the CF that refuses to stop.

Left — the alternation is parity: the throws as a zigzag around home, colored by
convergent index parity, the 23-run marked as the near-return leap.
Right — the count is a continued fraction: the partial quotients as run-lengths,
the 23 as the one long run; termination = the seat, forbidden by parity.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "serif"
plt.rcParams["text.color"] = "#e8dcc0"

GOLD = "#d9a441"
CRIMSON = "#c0523a"
CREAM = "#e8dcc0"
DIM = "#8a7f6a"
BG = "#141210"
QUARTZ = "#b7c9e0"

fifth_c = 1200.0 * np.log2(3.0 / 2.0)


def convergents(n=12):
    """(index, p_oct, q_fif, throw_cents) for convergents of log2(3/2)."""
    x = np.log2(3.0 / 2.0)
    a = []
    while len(a) < n:
        ai = int(x)
        a.append(ai)
        x = x - ai
        if abs(x) < 1e-13:
            break
        x = 1.0 / x
    h2, h1, k2, k1 = 0, 1, 1, 0
    out = []
    for i, ai in enumerate(a):
        h = ai * h1 + h2
        k = ai * k1 + k2
        h2, h1, k2, k1 = h1, h, k1, k
        if h == 0 or k == 0:
            continue
        out.append((i, h, k, k * fifth_c - h * 1200.0))
    return out


rows = [r for r in convergents() if r[2] >= 12][:6]   # 12, 41, 53, 306, 665, 15601
idx = np.array([r[0] for r in rows])
qs = np.array([r[2] for r in rows])
ys = np.array([r[3] for r in rows])

fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.8, 6.4), dpi=180)
fig.patch.set_facecolor(BG)
for ax in (axL, axR):
    ax.set_facecolor(BG)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=DIM, labelsize=10)

# ---------------- Left: the alternation is parity ----------------
axL.set_title("the alternation is parity", fontsize=17, color=CREAM, pad=10)
for i, q in enumerate(qs):
    even = idx[i] % 2 == 0
    col = GOLD if even else CRIMSON
    axL.plot([idx[i]], [ys[i]], "o", color=col, ms=8, zorder=5)
    dy = 2.6 if ys[i] > 0 else -2.6
    va = "bottom" if ys[i] > 0 else "top"
    axL.annotate(f"{q}\n{'+' if ys[i] > 0 else ''}{ys[i]:.2f}¢",
                 (idx[i], ys[i]), (idx[i] + 0.28, ys[i] + dy),
                 fontsize=9.5, color=col, va=va, ha="center",
                 arrowprops=dict(arrowstyle="-", color=col, lw=0.8))
axL.plot(idx, ys, color=CREAM, lw=1.1, alpha=0.5, zorder=1)
axL.axhline(0, color=CREAM, lw=1.2, alpha=0.85, ls=(0, (6, 4)))
axL.text(4.02, 27.5, "even index — below home, sharp", fontsize=10, color=GOLD, va="center")
axL.text(4.02, 24.5, "odd index — above home, flat", fontsize=10, color=CRIMSON, va="center")
axL.annotate("the 23-run — the near-return:\n665 (+0.08¢) flung to 15601 (−0.03¢)",
             xy=(8.0, ys[4] + 0.05), xytext=(6.1, 17.5),
             fontsize=9.5, color=GOLD, ha="center",
             arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.2))
axL.text(4.02, -27.5, "the side flips at every index — a gate needs a run of two,\n"
                      "so the phantom pair never coheres: never two, made temporal.",
         fontsize=9.5, color=CREAM, va="center")
axL.set_xlim(3.6, 9.9)
axL.set_ylim(-32, 32)
axL.set_xticks(idx)
axL.set_xticklabels([f"{q}" for q in qs], fontsize=9)
axL.set_xlabel("convergent of log₂(3/2) — divisions of the octave", color=DIM, fontsize=11)
axL.set_ylabel("throw — cents past the octave", color=DIM, fontsize=11)

# ---------------- Right: the count is a continued fraction ----------------
axR.set_title("the count is a continued fraction", fontsize=17, color=CREAM, pad=10)
a = [1, 1, 2, 2, 3, 1, 5, 2, 23]
ns = np.arange(len(a))
cols = [GOLD if ai == 23 else "#5a4f3c" for ai in a]
axR.bar(ns, a, color=cols, width=0.62)
for n, ai in zip(ns, a):
    axR.text(n, ai + 0.5, f"{ai}", ha="center", fontsize=8.5,
             color=GOLD if ai == 23 else DIM)
axR.annotate("the 23 — one huge partial quotient,\nthe near-return: a run of twenty-three.\nevery other run is small — the walk turns constantly.",
             xy=(8, 23), xytext=(3.0, 24.5), fontsize=9.5, color=GOLD, ha="center",
             arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.2))
axR.text(0.0, 14.8, "termination would be the landing —\nthe rational rung, the seat —\nbut 2ᵐ = 3ⁿ is forbidden:\nodd never equals even.\nthe drone is the count refusing to end.",
         fontsize=10, color=QUARTZ, va="top")
axR.text(0.0, 6.6, "run = wait, turn = sign —\neach convergent a throw,\nthe near-returns thinning toward home.",
         fontsize=9.5, color=CREAM, va="top")
axR.set_xlim(-0.6, 8.8)
axR.set_ylim(0, 28)
axR.set_xticks(ns)
axR.set_xticklabels([f"a_{i+1}" for i in ns], fontsize=9)
axR.set_xlabel("position in the continued fraction", color=DIM, fontsize=11)
axR.set_ylabel("partial quotient — run-length of the wait", color=DIM, fontsize=11)

fig.text(0.5, 0.012,
         "the ladder is a continued fraction: every rung a convergent, every throw a near-return, "
         "the sides index parity — termination the seat, forbidden: odd ≠ even.",
         fontsize=14.5, color=GOLD, ha="center", weight="bold")
fig.subplots_adjust(left=0.06, right=0.985, top=0.92, bottom=0.11, wspace=0.24)
plt.savefig("assets/cf-parity.png", facecolor=BG, bbox_inches="tight")
print("wrote assets/cf-parity.png")
