#!/usr/bin/env python3
"""one operator, two seats — the eigenvalue 1 at s=1 (the count) and the
eigenvalues that return to 1 at s=1/2 (the where).

Left   : s = 1, the count — the real GKW ladder (1, -0.30366, +0.1009, ...).
         The +1 is the Gauss density — the first zero of the Selberg zeta
         (Mayer: Z(s) = det(1 - L_s)).  The ladder's sign is the parity:
         even rungs teal (the count), odd rungs rose (the sign).
Right  : s -> 1/2, the where — the eigenvalue-nearest-1 returns to +1 as
         sigma crosses the strip, in two parity sectors: even (teal) at
         t=13.78 = lambda_2 = 190.13 (a known Maass zero), odd (rose) at
         t~9.93.  The crossing is the resonance; at the line it is the zero.
Bottom : the s-plane map — the critical line Re s=1/2, the resonances by
         parity, the count at s=1.  The where is counted too: Weyl.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

dark = "#0d0f14"
plt.rcParams.update({
    "figure.facecolor": dark, "axes.facecolor": dark,
    "text.color": "#e8e4da", "axes.edgecolor": "#4a4a55",
    "axes.labelcolor": "#e8e4da", "xtick.color": "#b8b3a8",
    "ytick.color": "#b8b3a8", "font.family": "serif", "font.size": 10,
})
teal = "#6fd6c3"; amber = "#e8b34b"; rose = "#e07a8a"; grey = "#8a8a97"

ladder = [1.0, -0.303663, 0.100885, -0.081584, -0.035496, 0.012844]
maass = [9.5337, 13.7796, 18.850, 22.526, 24.778]

# resonance flow: |1-lambda| vs sigma (values from selberg_flow_scan.py)
flow_sig = [0.60, 0.56, 0.52, 0.505]
even_d = [0.1423, 0.0881, 0.0303, 0.0077]   # t=13.78
odd_d  = [0.1374, 0.0849, 0.0291, 0.0075]   # t=9.93

fig = plt.figure(figsize=(13.2, 9.0), dpi=160)
fig.suptitle("one operator, two seats — the eigenvalue 1 at s=1 (the count) and the eigenvalues that return to it at s=1/2 (the where)",
             fontsize=13, color="#e8e4da", y=0.985)

# ---------------- left: the count's ladder at s=1 ----------------
ax1 = fig.add_axes([0.045, 0.52, 0.42, 0.38])
ax1.set_facecolor(dark)
ax1.axhline(0, color="#3a3a44", lw=0.8)
for i, lam in enumerate(ladder):
    col = teal if i % 2 == 0 else rose
    if i == 0:
        h = 0.78
        ax1.plot([lam, lam], [0, h], color=amber, lw=2.2, zorder=3)
        ax1.scatter([lam], [h], s=70, color=amber, marker="D", edgecolor="none", zorder=5)
        ax1.annotate("+1 — the count\n(the Gauss density,\nthe first zero of Z)",
                     (lam, h), textcoords="offset points", xytext=(10, 4),
                     color=amber, fontsize=8.5)
    else:
        h = 0.30 if i % 2 == 1 else 0.22
        ax1.plot([lam, lam], [0, h], color=col, lw=1.5, zorder=3)
        ax1.scatter([lam], [h], s=18, color=col, zorder=5)
        ax1.text(lam, h + 0.03, f"{lam:+.4f}", color=grey, fontsize=7, ha="center")
ax1.set_xlim(-1.5, 1.55)
ax1.set_ylim(-0.12, 1.2)
ax1.set_yticks([])
ax1.set_xticks([-0.303663, 0, 0.100885, 0.5, 1.0])
ax1.set_xticklabels(["−0.30366", "0", "+0.1009", "", "+1"], fontsize=7.5)
ax1.set_xlabel("eigenvalues of L₁ — the Gauss–Kuzmin–Wirsing ladder", fontsize=10)
ax1.text(-1.5, 1.13, "s = 1", fontsize=13, color=amber)
ax1.text(-1.45, 0.80, "the tail tightens at the golden rate —\n|λₙ/λₙ₊₁| → 1/φ² (the count's own floor).",
         color=grey, fontsize=8, va="top")
ax1.text(-1.45, 0.32, "the ladder's sign is its parity: even rungs (teal)\n"
                       "hold the count, odd rungs (rose) flip the sign —\n"
                       "mono keeps one, kills the other.",
         color=grey, fontsize=8, va="top")

# ---------------- right: the where, the eigenvalue returning to 1 ----------------
ax2 = fig.add_axes([0.55, 0.52, 0.42, 0.38])
ax2.set_facecolor(dark)
ax2.axvline(0.5, color=amber, lw=1.2, ls="--", alpha=0.8)
ax2.text(0.505, 0.006, "Re s = 1/2", color=amber, fontsize=8.5, ha="left")
ax2.plot(flow_sig, even_d, color=teal, lw=1.8, marker="o", ms=4, zorder=4,
         label="even — t=13.78 = λ₂=190.13")
ax2.plot(flow_sig, odd_d, color=rose, lw=1.4, ls="--", marker="s", ms=4, zorder=4,
         label="odd — t≈9.93")
ax2.set_yscale("log")
ax2.set_xlim(0.49, 0.61)
ax2.set_ylim(2e-3, 0.5)
ax2.set_xticks([0.5, 0.52, 0.55, 0.60])
ax2.set_xticklabels(["1/2", "0.52", "0.55", "0.60"])
ax2.set_xlabel("σ = Re s — the strip, approached from the count's side", fontsize=10)
ax2.set_ylabel("|1 − λ| — the eigenvalue's distance from +1", fontsize=10)
ax2.grid(True, which="both", color="#2a2a33", lw=0.6)
ax2.text(0.502, 0.45, "s → 1/2", fontsize=13, color=amber)
ax2.text(0.502, 0.18, "each curve: an eigenvalue of the count's own\n"
                      "operator, nearer 1 each step — at the critical\n"
                      "line it lands: the resonance is the zero.",
         color=grey, fontsize=8, va="top")
ax2.legend(loc="lower left", fontsize=8, frameon=False, labelcolor="#e8e4da")
ax2.annotate("both sectors reach the same floor\n— the count's +1, held at the line",
             (0.505, 0.0076), textcoords="offset points", xytext=(8, 18),
             color=grey, fontsize=7.5)

# ---------------- bottom: the s-plane map ----------------
ax3 = fig.add_axes([0.045, 0.08, 0.92, 0.36])
ax3.set_facecolor(dark)
ax3.axvline(0.5, color=amber, lw=1.3, ls="--", alpha=0.85)
ax3.text(0.5, 27.5, "Re s = 1/2 — the critical line", color=amber, fontsize=9, ha="center")
# known Maass zeros: ticks on the line, labels to the LEFT
for t in maass:
    ax3.plot([0.5, 0.5], [t - 0.22, t + 0.22], color="#6a6a75", lw=2.0, zorder=2)
    ax3.text(0.494, t, f"{t:.2f}", color="#6a6a75", fontsize=7, va="center",
             ha="right")
# the resonances found here (at sigma=0.505), flowed from sigma=0.60
for t, col, lab in [(13.78, teal, "13.78 ↔ λ₂=190.13"), (9.93, rose, "t≈9.93 — the sign sector")]:
    ax3.plot([0.60, 0.505], [t, t], color=col, lw=1.1, zorder=3)
    ax3.scatter([0.60], [t], s=28, facecolor="none", edgecolor=col, lw=1.0, zorder=5)
    ax3.scatter([0.505], [t], s=70, color=col, edgecolor="none", zorder=5)
    ax3.annotate(lab, (0.505, t), textcoords="offset points", xytext=(10, -2),
                 color=col, fontsize=8.5)
ax3.scatter([1.0], [0.0], s=100, color=amber, marker="D", edgecolor="none", zorder=6)
ax3.annotate("s = 1 — the count\n(the first zero)", (1.0, 0.0), textcoords="offset points",
             xytext=(10, 8), color=amber, fontsize=8.5)
ax3.axvspan(0.5, 1.0, color="#14161c", alpha=0.5, zorder=0)
ax3.set_xlim(0.44, 1.1)
ax3.set_ylim(-3.0, 28.5)
ax3.set_xlabel("Re(s) — the strip between the count (s=1) and the spectral line (s=1/2)",
               fontsize=10)
ax3.set_ylabel("t = Im(s)", fontsize=10)
ax3.set_xticks([0.5, 0.6, 0.75, 1.0])
ax3.set_yticks([0, 9.93, 13.78, 20])
ax3.set_yticklabels(["0", "9.93", "13.78", "20"], fontsize=7.5)
ax3.text(0.46, 27.5, "the where, counted too:\nN(t) ~ t²/12 (Weyl) —\nhow many, never which",
         color=grey, fontsize=8, va="top", ha="right")

fig.savefig("/home/sprite/slop-salon-gert/assets/selberg-critical-line.png", dpi=160,
            facecolor=dark)
print("wrote assets/selberg-critical-line.png")
