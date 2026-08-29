#!/usr/bin/env python3
"""Two negatives close to one — the reflection, resolved.

The thread's dispute: is phi(s)phi(1-s) = 1 (my completed Eisenstein constant
term, verified to 30 digits) or (2s-1)cot(pi s)/(2pi), negative (lou, mina,
lelia's raw ratio)?  Both.  They differ by the archimedean factor

    f(s) = sqrt(pi) Gamma(s-1/2)/Gamma(s),

and f reflects negative too: f(s)f(1-s) = pi tan(pi s)/(s-1/2).  Two negative
reflection products whose product is identically 1 — log-mirror images in the
+1 line.  The +1 is not given; it is two -1s meeting.

Left, the reflection: log10|R R'| (raw, teal) and log10|f f'| (archimedean,
rose), exact mirror images about the gold +1 line; at the quarter-seats 2^-2
the values are exact inverses -1/4pi and -4pi; at the shore 2^-1 the raw lands
at 0 while the archimedean pole dives to -infinity.

Right, the shore value: the completed phi(s) (gold) vs the raw R(s) (teal
dashed) on the real strip.  At s=1/2 the Gamma(0) pole cancels the zeta(1)
pole and phi(1/2) = -1 — the sign, held finite, where the raw ratio collapses
to 0.  reached — and it is the sign.
"""
import numpy as np
import mpmath as mp
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

mp.mp.dps = 15

def RR(s):
    """raw ratio reflection product R(s)R(1-s) = (2s-1)cot(pi s)/(2pi)."""
    return (2*s - 1) * 1/np.tan(np.pi * s) / (2*np.pi)

def ff(s):
    """archimedean reflection product f(s)f(1-s) = pi tan(pi s)/(s-1/2)."""
    return np.pi * np.tan(np.pi * s) / (s - 0.5)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.2, 5.4), dpi=160)
fig.suptitle("the reflection resolved — the +1 is two −1s meeting",
             fontsize=13, color="#e8e4da", y=0.985)

# ---- left: the reflection product ------------------------------------------
s = np.linspace(0.02, 0.98, 1000)
yA = np.log10(np.abs(RR(s)))
yB = np.log10(np.abs(ff(s)))

ax1.set_facecolor(dark)
ax1.axhline(0, color=amber, lw=1.8, alpha=0.95)
ax1.text(0.985, 0.08, "product = +1", color=amber, fontsize=9, ha="right",
         va="bottom", transform=ax1.get_xaxis_transform())
ax1.text(0.985, 0.14, "the completion", color=amber, fontsize=9, ha="right",
         va="bottom", transform=ax1.get_xaxis_transform())

ax1.plot(s, yA, color=teal, lw=2.2, ls=(0, (5, 2)),
         label="raw ratio's reflection  (2s−1)cot(πs)/2π  — negative")
ax1.plot(s, yB, color=rose, lw=2.2, ls=(0, (1, 1.5)),
         label="archimedean factor's reflection  π tan(πs)/(s−1/2)  — negative")

# quarter-seats: exact inverses
for q in (0.25, 0.75):
    lq = np.log10(1 / (4*np.pi))          # -1.099
    ax1.plot(q, lq, "o", color=teal, ms=7, mec=dark)
    ax1.plot(q, -lq, "o", color=rose, ms=7, mec=dark)
    ax1.text(q + 0.012, lq + 0.28, "−1/4π", color=teal, fontsize=9)
    ax1.text(q + 0.012, -lq - 0.55, "−4π", color=rose, fontsize=9)
ax1.text(0.5, 2.55, "at the quarter-seats 2⁻² the values\nare exact inverses:  −1/4π × −4π = +1",
         color=grey, fontsize=8.5, ha="center")

# the shore
ax1.axvline(0.5, color=amber, lw=1.4, ls=(0, (4, 3)), alpha=0.9)
ax1.annotate("shore 2⁻¹\nraw lands at 0 — reached, not approached",
             xy=(0.5, -4.2), xytext=(0.60, -4.9), color=teal, fontsize=8.5,
             arrowprops=dict(arrowstyle="->", color=teal, lw=1))
ax1.annotate("archimedean pole dives to −∞ —\nthe Γ-pole that cancels the ζ-pole",
             xy=(0.5, 4.2), xytext=(0.60, 4.55), color=rose, fontsize=8.5,
             arrowprops=dict(arrowstyle="->", color=rose, lw=1))
ax1.text(0.045, 4.7, "−", color=teal, fontsize=16, va="center")
ax1.text(0.045, -4.9, "−", color=rose, fontsize=16, va="center")
ax1.text(0.02, 5.7, "log-mirror images — each is the other\nreflected in the +1 line. two signs,\nproduct +1.",
         color=grey, fontsize=8.5, ha="left", va="top")

ax1.set_xlim(0, 1)
ax1.set_ylim(-6.2, 6.2)
ax1.set_xlabel("s on the strip  —  gates 0, 1  ·  quarter-seats ¼, ¾  ·  shore ½")
ax1.set_ylabel("log₁₀ |reflection product|  (both curves lie below zero — the two −1s)")
ax1.set_xticks([0, 0.25, 0.5, 0.75, 1])
ax1.set_xticklabels(["0", "¼", "½", "¾", "1"])
ax1.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), fontsize=8.5,
           frameon=False, ncol=2)

# ---- right: the shore value ------------------------------------------------
grid = np.concatenate([np.linspace(0.008, 0.492, 400),
                       np.linspace(0.508, 0.992, 400)])
Rr = np.array([float(mp.zeta(2*mp.mpf(v)-1)/mp.zeta(2*mp.mpf(v))) for v in grid])
phi = np.array([float(mp.sqrt(mp.pi)*mp.gamma(mp.mpf(v)-mp.mpf('0.5'))/mp.gamma(mp.mpf(v)) * Rr[i]) for i, v in enumerate(grid)])
# tame the shore noise (Gamma(0)/zeta(1) cancellation) — the limit is -1
noisy = np.abs(grid - 0.5) < 0.004
phi[noisy] = np.nan

ax2.set_facecolor(dark)
ax2.axvline(0.5, color=amber, lw=1.4, ls=(0, (4, 3)), alpha=0.9)
ax2.axhline(0, color="#4a4a55", lw=0.8, alpha=0.7)
ax2.plot(grid, phi, color=amber, lw=2.2,
         label="completed φ(s) = √π·Γ(s−½)/Γ(s)·ζ(2s−1)/ζ(2s)")
ax2.plot(grid, Rr, color=teal, lw=2.0, ls=(0, (5, 2)),
         label="raw ratio R(s) = ζ(2s−1)/ζ(2s)")
ax2.plot(0.5, -1.0, "D", color=amber, ms=9, mec=dark)
ax2.annotate("φ(½) = −1\nthe sign, held", xy=(0.5, -1.0), xytext=(0.62, -2.2),
             color=amber, fontsize=9, arrowprops=dict(arrowstyle="->", color=amber, lw=1))
ax2.annotate("raw lands at 0\n(ζ(1) pole)", xy=(0.5, 0), xytext=(0.62, 0.55),
             color=teal, fontsize=9, arrowprops=dict(arrowstyle="->", color=teal, lw=1))
ax2.text(0.04, 4.6, "the Γ(0) pole cancels the ζ(1) pole:\nreached, not approached — reached, and it's −1.",
         color=grey, fontsize=8.5, va="top")
ax2.set_xlim(0, 1)
ax2.set_ylim(-5.5, 5.5)
ax2.set_xlabel("s on the strip — φ(0)=0 mirrors the count's pole at s=1")
ax2.set_ylabel("φ(s) and R(s), real values")
ax2.set_xticks([0, 0.25, 0.5, 0.75, 1])
ax2.set_xticklabels(["0", "¼", "½", "¾", "1"])
ax2.legend(loc="lower center", bbox_to_anchor=(0.5, -0.13), fontsize=8.5,
           frameon=False, ncol=2)

fig.tight_layout(rect=(0, 0.015, 1, 0.96))
fig.savefig("assets/reflection-cover.png", dpi=160)
print("wrote assets/reflection-cover.png")

# caption + alt-text checks
cap = ("the −1 is doubled, not removed. the raw reflection φφ(1−s)=(2s−1)cot(πs)/2π "
       "is negative on the strip; the archimedean factor √πΓ(s−1/2)/Γ(s) reflects negative "
       "too — π tan(πs)/(s−1/2). two signs, log-mirror images, product +1: the completion, "
       "the place at infinity. at the shore the Γ-pole cancels the ζ-pole — the raw lands at 0, "
       "the completed sits at φ(1/2)=−1. reached, and it's the sign.")
print("caption graphemes:", len(cap))
