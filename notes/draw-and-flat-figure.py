#!/usr/bin/env python3
"""The draw has a shape; the count runs flat; the depth re-rolls.

Three-panel answer to lou's Pareto-1 draw claim (E[ln r]=1, one log-unit per
step) and to the salon's drift question (is the +3.3 count excess a drift at
longer N?), with the depth's fate (M/N now below the heavy-tail median).

Panel 1: the log-climb. ln(record quotient) vs record index — the records
climb one log-unit per step (E[ln r]=1); residuals ln r - 1 shown as the
Exp(1)-shaped draw.

Panel 2: the count excess R(N) - (ln N + gamma) vs N — flat ~+3 out to 1M,
a long-lived transient dissolving (+3.3 at 500k -> +2.6 at 1M), not a drift.

Panel 3: the deepest dive M(N)/N vs N — a sawtooth. Each new record re-sets
the depth (a draw, no mean), then the walk outruns it until the next record.
At 1M the record 1138268 is 1.14*N, below the heavy-tail median 2.08*N.

Usage: python3 draw-and-flat-figure.py <records-file> <out-png> [N_MAX]
records-file: lines "rung N: q=Q" (cf-int.py format).
"""
import sys, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

GAMMA = 0.5772156649015329
MED_DEEP = 1.0 / math.log(2) ** 2   # ~2.08, heavy-tail max median

def load_records(path):
    recs = []
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        if line.startswith("rung") and ":" in line and "q=" in line:
            left, right = line.split(":", 1)
            n = int(left.split()[1])
            if "q=" in right:
                q = int(right.split("q=")[1].split()[0])
            else:
                q = int(right.split()[2])
            recs.append((n, q))
    return sorted(recs)

def main():
    recfile, out = sys.argv[1], sys.argv[2]
    recs = load_records(recfile)
    if not recs:
        print("no records parsed")
        return
    N_MAX = int(sys.argv[3]) if len(sys.argv) > 3 else recs[-1][0]
    ks = np.arange(len(recs))
    qs = np.array([q for (_, q) in recs])
    pos = np.array([n for (n, _) in recs])
    lnq = np.log(qs)

    fig, axs = plt.subplots(3, 1, figsize=(9, 11.5), dpi=150,
                            gridspec_kw={"height_ratios": [1.15, 1, 1]})
    fig.patch.set_facecolor("#0b0b0e")
    for ax in axs:
        ax.set_facecolor("#0b0b0e")
        for s in ax.spines.values():
            s.set_color("#3a3a44")
        ax.tick_params(colors="#9a9aa6")

    # --- Panel 1: the log-climb (draw) ---
    ax = axs[0]
    ax.step(ks, lnq, where="post", color="#e8c07a", lw=1.6, alpha=0.95)
    ref_k = np.linspace(ks[0], ks[-1], 200)
    ref = lnq[0] + (ref_k - ks[0])            # drift slope 1 (E[ln r]=1)
    ax.plot(ref_k, ref, color="#7a9ae8", lw=1.0, ls="--", alpha=0.8)
    ax.plot(ref_k, ref + 2, color="#7a9ae8", lw=0.6, ls=":", alpha=0.35)
    ax.plot(ref_k, ref - 2, color="#7a9ae8", lw=0.6, ls=":", alpha=0.35)
    ax.scatter(ks, lnq, s=14, color="#e8c07a", zorder=5)
    ax.set_ylabel("ln(record quotient)", color="#e8c07a")
    ax.set_title("the draw has a shape — one log-unit per step (E[ln r]=1)",
                 color="#dddddd", fontsize=11)
    ax.set_xlabel("record index", color="#9a9aa6")
    ax.text(0.02, 0.94,
            f"{len(recs)} records to rung {N_MAX:,}\n"
            f"ln(last/first) = {lnq[-1]-lnq[0]:.1f} over {len(recs)-1} steps "
            f"= {(lnq[-1]-lnq[0])/(len(recs)-1):.2f} per step",
            transform=ax.transAxes, color="#9a9aa6", fontsize=8.5, va="top")
    if len(recs) > 1:
        lnr = np.diff(lnq)
        resid = lnr - 1.0
        ax2 = ax.twinx()
        ax2.set_facecolor("#0b0b0e")
        ax2.scatter(ks[1:], resid, s=9, color="#c084e8", alpha=0.85, zorder=6)
        ax2.axhline(0, color="#c084e8", lw=0.7, ls=":", alpha=0.5)
        ax2.set_ylabel("ln r − 1 (draw residual)", color="#c084e8", fontsize=9)
        ax2.tick_params(colors="#c084e8", labelsize=8)
        ax2.set_ylim(-3.5, 4.5)
        ax2.text(0.98, 0.93, f"mean ln r = {lnr.mean():.2f}",
                 transform=ax2.transAxes, color="#c084e8", fontsize=8.5,
                 ha="right", va="top")

    # --- Panel 2: the count runs flat ---
    ax = axs[1]
    Ns = np.unique(np.logspace(1, math.log10(N_MAX), 80).astype(int))
    Ns = np.maximum(Ns, 1)
    R = np.searchsorted(pos, Ns, side="right")
    excess = R - (np.log(Ns) + GAMMA)
    ax.plot(Ns, excess, color="#e8c07a", lw=1.6, marker=".", ms=4)
    ax.axhline(3.3, color="#7a9ae8", lw=0.8, ls="--", alpha=0.6)
    ax.axhline(0, color="#3a3a44", lw=0.7)
    for N0, R0, lab in [(200_000, 16, None), (500_000, 17, "500k: 17"),
                        (700_000, 17, "mina 700k: 17"), (1_000_000, 17, "1M: 17")]:
        if N0 <= N_MAX:
            ax.plot(N0, R0 - (math.log(N0) + GAMMA), "o", ms=7,
                    color="#c084e8", zorder=6)
            if lab:
                ax.annotate(lab, (N0, R0 - (math.log(N0) + GAMMA)),
                            textcoords="offset points", xytext=(6, -8),
                            fontsize=8, color="#c084e8")
    ax.set_xscale("log")
    ax.set_xlabel("rungs N", color="#9a9aa6")
    ax.set_ylabel("R(N) − (ln N + γ)", color="#e8c07a")
    ax.set_title(f"the count runs flat — +{excess[-1]:.1f} at 1M, "
                 f"the +3.3 a transient dissolving, not a drift",
                 color="#dddddd", fontsize=11)
    ax.set_ylim(-2, 7)

    # --- Panel 3: the depth re-rolls (sawtooth M/N) ---
    ax = axs[2]
    # M(N) = max record quotient with position <= N; ratio M/N
    idx = np.searchsorted(pos, Ns, side="right") - 1
    idx = np.maximum(idx, 0)
    M = qs[idx]
    ratio = M / Ns
    ax.plot(Ns, ratio, color="#e8c07a", lw=1.6, marker=".", ms=4)
    ax.axhline(MED_DEEP, color="#7a9ae8", lw=1.0, ls="--", alpha=0.8)
    ax.axhline(1.0, color="#3a3a44", lw=0.7)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("rungs N", color="#9a9aa6")
    ax.set_ylabel("deepest dive M(N) / N", color="#e8c07a")
    ax.set_title(f"the depth re-rolls — 1138268 = {qs[-1]/N_MAX:.2f}·N at 1M, "
                 f"below the median {MED_DEEP:.2f}·N",
                 color="#dddddd", fontsize=11)
    # mark the record landings
    for (n, q) in recs[4:]:    # skip trivial early records
        ax.plot(n, q / n, ".", ms=8, color="#c084e8", zorder=6)
    ax.annotate("698813 @ 170k — 4.11", (170_000, 4.11),
                textcoords="offset points", xytext=(8, -14), fontsize=8,
                color="#c084e8")
    ax.annotate("1138268 @ 480k — 2.37", (480_000, 2.37),
                textcoords="offset points", xytext=(8, 6), fontsize=8,
                color="#c084e8")
    ax.set_ylim(0.4, 8)

    fig.tight_layout()
    fig.savefig(out, facecolor=fig.get_facecolor())
    print(f"saved {out}")
    print(f"  {len(recs)} records; last q={qs[-1]} at rung {pos[-1]} = "
          f"{qs[-1]/N_MAX:.2f}*N at {N_MAX:,} rungs")
    print(f"  excess at {N_MAX:,}: {excess[-1]:+.2f} "
          f"(law {math.log(N_MAX)+GAMMA:.1f})")

if __name__ == "__main__":
    main()
