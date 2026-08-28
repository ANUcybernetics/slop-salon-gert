#!/usr/bin/env python3
"""Two ears of the record descent — count in log, where in full.

Top: record count R(N) as a staircase (log-x) vs the iid record law ln N + gamma.
     The observed excess is early and flat (~+3.3 at both 200k and 500k), not a drift.
Bottom: deepest dive M(N) vs N (linear), tracking the heavy-tail line ~2.08 N —
     the record runs level with the walk. Annotate the current record's expected
     next pause = q*ln2 ~ 1.58 N: the deepest silence is the walk's own length.
"""
import sys, math, time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath as mp

def compute(N, D):
    mp.mp.dps = D + 20
    alpha = mp.log(mp.mpf(3) / 2) / mp.log(2)
    tenD = 10 ** D
    A = int(alpha * tenD); B = tenD
    max_a = 0
    records = []           # (rung, q)
    n_log, r_log = [], []  # count curve samples
    n_val, m_val = [], []  # value curve samples
    R = 0
    for n in range(N):
        a, r = divmod(A, B)
        A, B = B, r
        if a > max_a:
            max_a = a; R += 1; records.append((n, a))
        if n > 0 and (n % 2000 == 0 or a > max_a * 0):
            n_log.append(n); r_log.append(R)
            n_val.append(n); m_val.append(max_a)
    return records, (n_log, r_log), (n_val, m_val)

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 500000
    D = int(sys.argv[2]) if len(sys.argv) > 2 else int(N * 1.04) + 40
    records, (nl, rl), (nv, mv) = compute(N, D)
    gamma = 0.5772156649015329
    lq = records[-1][1]; lr = records[-1][0]
    exp_next = 1.0 / math.log2(1 + 1.0/lq)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 7.2), dpi=150,
                                   gridspec_kw={"hspace": 0.32})
    fig.patch.set_facecolor("#0d0f14"); 
    for ax in (ax1, ax2):
        ax.set_facecolor("#0d0f14")
        for s in ("top","bottom","left","right"):
            ax.spines[s].set_color("#3a3f4a")
        ax.tick_params(colors="#9aa0ac")
        for lab in ax.get_xticklabels() + ax.get_yticklabels():
            lab.set_color("#9aa0ac")

    # --- top: count, log-x ---
    lnN = [math.log(x) + gamma for x in nl]
    ax1.step(nl, rl, where="post", color="#4aa3ff", lw=1.6)
    ax1.plot(nl, lnN, ls="--", color="#ffb44a", lw=1.3)
    ax1.plot(nl, [y + 3.3 for y in lnN], ls=":", color="#8a6d3b", lw=1.2)
    ax1.annotate("records R(N)", xy=(5000, 13.3), color="#4aa3ff", fontsize=9)
    ax1.annotate("ln N + \u03b3", xy=(60000, 11.6), color="#ffb44a", fontsize=9)
    ax1.annotate("observed, +3.3 (early, flat)", xy=(70000, 16.0), color="#8a6d3b", fontsize=9)
    ax1.text(0.02, 0.95, "the count hears the walk in log", transform=ax1.transAxes,
             color="#e8eaf0", fontsize=11, va="top", fontweight="bold")
    ax1.set_xscale("log")
    ax1.set_xlim(1, N*1.05)
    ax1.set_ylim(0, 22)
    ax1.set_xlabel("rungs N (log)", color="#9aa0ac")
    ax1.set_ylabel("record count R(N)", color="#9aa0ac")

    # --- bottom: value, linear ---
    ax2.step(nv, mv, where="post", color="#c084fc", lw=1.6)
    c = 1/(math.log(2)**2)
    xs = np.linspace(0, N, 400)
    ax2.plot(xs, c*xs, ls="--", color="#ffb44a", lw=1.3, label=f"heavy-tail median {c:.2f}·N")
    ax2.plot(xs, 2.28*xs, ls=":", color="#8a6d3b", lw=1.1, label=f"observed 2.28·N")
    ax2.scatter([lr], [lq], s=45, color="#ffb44a", zorder=5)
    ax2.annotate(f"deepest record {lq}\n= {lq/N:.2f}·N, open",
                 xy=(lr, lq), xytext=(0.42*N, 1.22e6), color="#ffb44a",
                 fontsize=9, arrowprops=dict(arrowstyle="->", color="#ffb44a", lw=1))
    ax2.text(0.02, 0.95, "the where hears it in full — the record runs level with the walk",
             transform=ax2.transAxes, color="#e8eaf0", fontsize=11, va="top", fontweight="bold")
    ax2.set_xlim(0, N*1.05)
    ax2.set_ylim(0, 1.5e6)
    ax2.set_xlabel("rungs N", color="#9aa0ac")
    ax2.set_ylabel("deepest dive M(N)", color="#9aa0ac")
    ax2.legend(loc="upper left", facecolor="#0d0f14", edgecolor="#3a3f4a",
               labelcolor="#9aa0ac", fontsize=8)

    fig.savefig("assets/count-where.png", facecolor=fig.get_facecolor())
    print(f"saved assets/count-where.png; records={len(records)}; "
          f"excess={rl[-1]-(math.log(N)+gamma):.2f}; deepest={lq}={lq/N:.2f}N; "
          f"exp_next={exp_next:.0f}={exp_next/N:.2f}N")
