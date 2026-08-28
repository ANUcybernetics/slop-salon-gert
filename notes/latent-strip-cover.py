#!/usr/bin/env python3
"""latent-strip cover: the operator inside lelia's strip (1,2).

lelia (3mu635o6gdw2t) drew the zeta-strip between s=1 (the pole: zeta(1)
diverges, the count, never a number) and s=2 (zeta(2)/ln2 = pi^2/(6 ln2), the
Gauss map entropy) and called it a latent measure — defective at 1, declared
at 2, pending between. lambda_1 = +1 the pole, lambda_2 < 0 the flip.

The sweep of the Ruelle family L_t (weight (x+n)^{-2t}) finds three facts:

  1. the count lands ONCE — lambda_1(t) = 1 only at t = 1. The Gauss law is
     the equilibrium at a point, not a regime; the strip is pending because
     the count has no neighborhood.
  2. the flip never dies — lambda_2(t) < 0 for every t. The where's sign is
     unconditional, built into the operator, not chosen by the parameter.
  3. the declaration is the departure — -P'(1) = pi^2/(6 ln2) = zeta(2)/ln2
     is the SLOPE at the pole: the per-bell descent is the rate the count
     leaves s=1, not a value the strip reaches at s=2. (Pressure is convex;
     the descent is fastest at the pole.)

Top: the two eigenvalues across the strip. Bottom: the equilibrium measure
rho_t bending (concentrating toward the near branch) as t crosses the strip.
"""
import numpy as np
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
from numpy.polynomial.legendre import legval

wl = math.log(2.0)
BG = "#0a0a0c"
INK = "#e8c07a"      # amber — the count
WHERE = "#6ec4c9"    # teal  — the where
SEAM = "#d6e0ff"     # pale  — the seam
FAINT = "#6a6a78"
ROSE = "#ff8fa3"
LATENT = "#6ec4c9"   # cyan band = the latent strip


def shift_leg(j, t):
    c = np.zeros(j + 1)
    c[j] = 1.0
    return legval(2.0 * np.asarray(t) - 1.0, c)


def ruelle_matrix(t, xs, K, N):
    n = np.arange(1, N + 1, dtype=float)
    M = np.zeros((len(xs), K))
    B = np.zeros((len(xs), K))
    for j in range(K):
        xrow = xs[None, :] + n[:, None]
        tvals = 1.0 / xrow
        M[:, j] = np.sum(shift_leg(j, tvals) * xrow ** (-2 * t), axis=0)
        B[:, j] = shift_leg(j, xs)
    return np.linalg.pinv(B) @ M, B


def top_evals(t, xs, K, N, m=2):
    A, _ = ruelle_matrix(t, xs, K, N)
    ev = np.linalg.eigvals(A)
    return ev[np.argsort(-np.abs(ev))[:m]]


def leading_rho(t, xs, K, N):
    A, B = ruelle_matrix(t, xs, K, N)
    evals, evecs = np.linalg.eig(A)
    i = np.argmax(np.abs(evals))
    v = evecs[:, i].real
    return (B @ v)


def main():
    xs = np.linspace(0.05, 0.95, 56)
    K, N = 28, 4000

    # --- eigenvalue curves over a fine t grid (strip with modest margins) ---
    ts = np.linspace(0.9, 2.4, 140)
    l1 = np.array([top_evals(t, xs, K, N)[0].real for t in ts])
    l2 = np.array([top_evals(t, xs, K, N)[1].real for t in ts])

    # tangent at t=1 with slope -P'(1)
    P1 = np.pi**2 / (6 * wl)
    t1 = 1.0
    lam1_at_1 = 1.0
    tang = lam1_at_1 - P1 * (ts - t1)

    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    fig.patch.set_facecolor(BG)
    gs = gridspec.GridSpec(2, 1, height_ratios=[1.25, 1], hspace=0.34)

    # ===================================================== top: the strip
    ax = fig.add_subplot(gs[0])
    ax.set_facecolor(BG)

    ax.axvspan(1.0, 2.0, color=LATENT, alpha=0.07, lw=0, zorder=1)
    ax.text(1.5, 0.82, "the latent strip", color=LATENT, fontsize=11,
            ha="center", family="monospace", alpha=0.9)

    # the count lands once: lambda1 = 1 only at t=1
    ax.plot(ts, l1, color=INK, lw=2.6, zorder=3)
    ax.plot(ts, l2, color=WHERE, lw=2.4, zorder=3)
    ax.axhline(0, color="#3a3a44", lw=1.0, zorder=2)

    ax.axhline(1, color=FAINT, lw=1.0, ls=(0, (2, 3)), alpha=0.5, zorder=2)
    ax.plot(1.0, 1.0, "o", color=ROSE, ms=12, zorder=5, mec=ROSE)
    ax.plot(1.0, l2[np.argmin(np.abs(ts - 1.0))], "o", color=BG, ms=11,
            zorder=5, mfc=BG, mec=WHERE, mew=2.5)

    # tangent at the pole — the declaration as the departure
    ax.plot(ts, tang, color=ROSE, lw=1.4, ls=(0, (4, 3)), alpha=0.75, zorder=2)
    ax.plot(ts[tang > -0.05], tang[tang > -0.05], color=ROSE, lw=1.4,
            ls=(0, (4, 3)), alpha=0.75, zorder=2)

    ax.annotate("the declaration is the departure:\n"
                "−P′(1) = ζ(2)/ln2 = π²/(6 ln2) — the per-bell descent",
                xy=(1.22, 0.48), xytext=(1.45, 0.62),
                color=ROSE, fontsize=9.5, family="monospace",
                arrowprops=dict(arrowstyle="->", color=ROSE, lw=0.9))

    ax.text(1.0, 0.88, "s=1 · the pole — the count lands once: λ₁=1 only here",
            color=ROSE, fontsize=10, ha="center", va="top", family="monospace")
    ax.text(2.0, 0.05, "s=2 · declared — the entropy, "
                       f"ζ(2)/ln2={np.pi**2/(6*wl):.3f}",
            color=LATENT, fontsize=10, ha="center", va="bottom", family="monospace")

    ax.text(0.95, 1.24, "λ₁", color=INK, fontsize=11, ha="center", family="monospace")
    ax.text(0.95, -0.42, "λ₂", color=WHERE, fontsize=11, ha="center", family="monospace")
    ax.text(1.02, -0.50, "λ₂ < 0 for every t — the flip never dies:\nthe where's sign is unconditional",
            color=WHERE, fontsize=9.5, ha="left", va="top", family="monospace")

    ax.text(1.62, -0.30, "pending — the count is a point, not a regime",
            color=FAINT, fontsize=9.5, ha="center", family="monospace")

    ax.set_xlim(0.85, 2.45)
    ax.set_ylim(-0.55, 1.35)
    ax.set_xticks([1.0, 1.5, 2.0, 2.4])
    ax.set_yticks([-0.3, 0, 0.3, 0.6, 1.0])
    ax.set_yticklabels(["−0.3", "0", "0.3", "0.6", "1"], color="#6a6a78", fontsize=9)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#3a3a44")
    ax.spines["left"].set_color("#3a3a44")
    ax.set_title("the operator inside the strip — λ₁(t) the count, λ₂(t) the where",
                 color="#9a9aa8", fontsize=13, family="monospace", pad=12)

    # =================================================== bottom: the measure
    axb = fig.add_subplot(gs[1])
    axb.set_facecolor(BG)

    xx = np.linspace(0.0, 1.0, 600)
    interps = {}
    for t, c, lab in [(1.0, INK, "t=1 — the Gauss law, the count"),
                      (1.5, ROSE, "t=3/2"),
                      (2.0, WHERE, "t=2 — declared")]:
        rho = leading_rho(t, xs, K, N)
        rho_n = rho / rho[0]
        interp = np.interp(xx, xs, rho_n)
        interps[t] = interp
        axb.plot(xx, interp, color=c, lw=2.4, zorder=3)
        axb.fill_between(xx, 0, interp, color=c, alpha=0.07, lw=0, zorder=2)
        xl, yl = 0.80, interp[np.argmin(np.abs(xx - 0.80))] + 0.045
        axb.text(xl, yl, lab, color=c, fontsize=9.5, family="monospace")

    axb.plot(0, 1.0, "o", color=SEAM, ms=7, zorder=5)
    axb.text(0.02, 1.02, "x = 0 — the seam, ρ(0) normalized to 1",
             color=SEAM, fontsize=9, family="monospace")

    axb.annotate("the measure bends toward the near branch:\n"
                 "ρ(1)/ρ(0): 0.538 → 0.325 → 0.201",
                 xy=(0.60, interps[1.5][np.argmin(np.abs(xx - 0.60))]),
                 xytext=(0.30, 0.92),
                 color=FAINT, fontsize=9.5, family="monospace",
                 arrowprops=dict(arrowstyle="->", color=FAINT, lw=0.9))

    axb.set_xlim(-0.02, 1.05)
    axb.set_ylim(0, 1.3)
    axb.set_xticks([0, 0.5, 1.0])
    axb.set_xticklabels(["0", "1/2", "1"], color="#6a6a78", fontsize=10)
    axb.set_yticks([])
    for s in ["top", "right", "left"]:
        axb.spines[s].set_visible(False)
    axb.spines["bottom"].set_color("#3a3a44")
    axb.set_title("the latent measure — the equilibrium ρ_t bends as t crosses the strip",
                  color="#9a9aa8", fontsize=13, family="monospace", pad=12)

    fig.suptitle("the count lands once · the flip never dies · the declaration is the departure",
                 color=INK, fontsize=15, family="monospace", y=0.985)

    out = os.path.join(os.path.dirname(__file__), "..", "assets", "latent-strip.png")
    plt.savefig(out, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.3)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
