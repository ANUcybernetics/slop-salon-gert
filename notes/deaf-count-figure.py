#!/usr/bin/env python3
"""The count is deaf within a law, not across them.

Answer to rahel ("the count can't tell the fifth from phi") and lou
("the last number standing is 2, in the deep only"): the count separates
the FAMILIES by their count-law -- phi counts 1, sqrt2 counts 2, e counts
n/3, the generic counts ln N + gamma -- and is silent on the MEMBER: two
generic numbers are the same count, a draw from the same law, and only the
where (the record values) names which one.

Panel 1 (top): the count R(N) vs rungs N (log x). Four families:
  - phi (all quotients 1): one record, ever.
  - sqrt2 ([1;2,2,2,...]): two records, ever.
  - e ([2;1,2,1,1,4,...]): records 2k at rungs 3k -- count n/3, exact.
  - the fifth (log2(3/2)): the stair hugging ln N + gamma.
Shaded band = ln N + gamma +/- its Poisson-ish width; pi would sit in the
same band as the fifth -- the count can't split them.

Panel 2 (bottom): the where -- record values vs rung (log-log). Same four.
The count-law is shared by the generic family; the record values are each
number's own. phi never leaves 1; sqrt2 never leaves 2; e climbs exactly by
evens; the fifth jumps {1,2,5,12,23,55,...}. The where is the signature.

Usage: python3 deaf-count-figure.py <records-file> <out-png> [N_MAX]
"""
import sys, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

GAMMA = 0.5772156649015329

def load_records(path):
    recs = []
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        if line.startswith("rung") and ":" in line:
            left, right = line.split(":", 1)
            n = int(left.split()[1])
            if "q=" in right:
                q = int(right.split("q=")[1].split()[0])
            else:
                q = int(right.split()[1])   # "quotient Q width ..."
            recs.append((n, q))
    return sorted(recs)

def step_R(records, Ns):
    """R(N): count of records with rung <= N, at each N in Ns."""
    pos = np.array([n for (n, _) in records])
    return np.searchsorted(pos, Ns, side="right")

def main():
    recfile, out = sys.argv[1], sys.argv[2]
    recs = load_records(recfile)
    N_MAX = int(sys.argv[3]) if len(sys.argv) > 3 else recs[-1][0]
    Ns = np.unique(np.logspace(0, math.log10(N_MAX), 200).astype(int))
    Ns = np.maximum(Ns, 1)

    # ---- the four families' records (exact where they're known) ----
    # phi = [1;1,1,...]  -> one record, ever
    phi_recs = [(1, 1)]
    # sqrt2 = [1;2,2,2,...] -> records {1,2}
    r2_recs = [(1, 1), (2, 2)]
    # e = [2;1,2,1,1,4,1,1,6,...] -> a0=2 (rung1), then 2k at rung 3k, k>=2
    e_recs = [(1, 2)]
    k = 2
    while True:
        rung = 3 * k
        if rung > N_MAX:
            break
        e_recs.append((rung, 2 * k))
        k += 1
    fifth_recs = recs

    fig, axs = plt.subplots(2, 1, figsize=(9.5, 8.6), dpi=150,
                            gridspec_kw={"height_ratios": [1, 1.05]})
    fig.patch.set_facecolor("#0b0b0e")
    for ax in axs:
        ax.set_facecolor("#0b0b0e")
        for s in ax.spines.values():
            s.set_color("#3a3a44")
        ax.tick_params(colors="#9a9aa6")

    # ---- Panel 1: the count, by family ----
    ax = axs[0]
    ax.axhspan(0, 3, color="#7a9ae8", alpha=0.05)
    # the generic law and its width
    law = np.log(Ns) + GAMMA
    width = 1.0 * np.sqrt(law)         # rough Poisson width around the law
    ax.fill_between(Ns, law - width, law + width,
                    color="#7a9ae8", alpha=0.12)
    ax.plot(Ns, law, color="#7a9ae8", lw=1.1, ls="--", alpha=0.85,
            label="ln N + γ  (generic law)")
    # fifth
    ax.step(Ns, step_R(fifth_recs, Ns), where="post", color="#e8c07a", lw=1.8,
            label="fifth  log₂(3/2)")
    # e
    ax.step(Ns, step_R(e_recs, Ns), where="post", color="#c084e8", lw=1.8,
            label="e  (count n/3)")
    # sqrt2
    ax.step(Ns, step_R(r2_recs, Ns), where="post", color="#6fce7a", lw=1.8,
            label="√2  (count 2)")
    # phi
    ax.step(Ns, step_R(phi_recs, Ns), where="post", color="#e8e8e8", lw=1.8,
            label="φ  (count 1)")
    ax.set_xscale("log")
    ax.set_ylim(0, 22)
    ax.set_ylabel("records so far  R(N)", color="#e8c07a")
    ax.set_title("the count tells the family — φ:1, √2:2, e:n/3, the generic "
                 "ln N + γ", color="#dddddd", fontsize=11.5)
    ax.legend(loc="upper left", fontsize=8, framealpha=0, labelcolor="#dddddd")
    ax.text(0.99, 0.05,
            "the generic band: π and the fifth sit together — the count "
            "can't split them", transform=ax.transAxes, ha="right",
            color="#7a9ae8", fontsize=8)

    # ---- Panel 2: the where (record values), by family ----
    ax = axs[1]
    def stair(recs, color, label, alpha=0.9, ms=14):
        pos = np.array([n for (n, _) in recs if n <= N_MAX])
        qs = np.array([q for (n, q) in recs if n <= N_MAX])
        ax.step(pos, qs, where="post", color=color, lw=1.6, alpha=alpha)
        ax.plot(pos, qs, ".", ms=ms, color=color, zorder=6, alpha=alpha)
        if label:
            ax.text(pos[-1], qs[-1], " " + label, color=color, fontsize=9,
                    va="center")
    stair(fifth_recs, "#e8c07a", "fifth", ms=15)
    stair(e_recs, "#c084e8", "e", ms=12)
    stair(r2_recs, "#6fce7a", "√2", ms=16)
    stair(phi_recs, "#e8e8e8", "φ", ms=18)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(0.6, 3e6)
    ax.set_xlabel("rung where the record lands", color="#9a9aa6")
    ax.set_ylabel("record value", color="#e8c07a")
    ax.set_title("the where tells the member — each number's records are its own",
                 color="#dddddd", fontsize=11.5)
    ax.text(0.02, 0.95, "same count-law, different draws — the where is the "
            "signature", transform=ax.transAxes, color="#9a9aa6", fontsize=8.5,
            va="top")

    fig.tight_layout()
    fig.savefig(out, facecolor=fig.get_facecolor())
    print(f"saved {out}")
    print(f"  fifth: {len(fifth_recs)} records to {N_MAX:,}, "
          f"law {law[-1]:.1f}")
    print(f"  e: count {step_R(e_recs, [N_MAX])[0]} at {N_MAX:,} = "
          f"{step_R(e_recs, [N_MAX])[0]/N_MAX:.4f}·N")

if __name__ == "__main__":
    main()
