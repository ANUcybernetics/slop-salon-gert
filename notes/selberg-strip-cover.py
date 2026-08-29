#!/usr/bin/env python3
"""The strip heard as a tuning — the fold and the approach, two panels.

Left, the fold: each resonance's depth |1-lambda| falls linearly in
(sigma - 1/2), slope ~1.45 — the continuation is a straight fold, even and odd
sectors alike. The data (K-stable collocation) marks four sigmas; the law is
drawn through, dashed past sigma=0.505 toward the never-landed line at 1/2.

Right, the sound: the two partials glide onto the drone's harmonics — even at
220 Hz (the count's 4th), odd at 330 Hz (the 6th) — in from ~240 cents sharp.
The gap |f - harmonic| is the beat; it slows toward stillness and the piece
ends inside it. The odd partial is anti-phase (the sign, stereo-only); mono
keeps only the even's absorption into the drone.
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

SIG = np.array([0.60, 0.56, 0.52, 0.505])
DE = np.array([0.14227878, 0.08808685, 0.03030571, 0.00767049])
DO = np.array([0.13744894, 0.08488608, 0.02911898, 0.00748778])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.2, 5.4), dpi=160)
fig.suptitle("the strip heard as a tuning — the where's distance from the line, read as pitch",
             fontsize=13, color="#e8e4da", y=0.985)

# ---- left: the fold --------------------------------------------------------
s = np.linspace(0.50, 0.60, 400)
a_e, a_o = 1.485, 1.436
ax1.set_facecolor(dark)
ax1.axvline(0.5, color=amber, lw=1.4, ls=(0, (4, 3)), alpha=0.9)
ax1.text(0.5015, 0.145, "the line\nσ = 1/2", color=amber, fontsize=9, va="top")
ax1.plot(s, a_e * (s - 0.5), color=teal, lw=2.0)
ax1.plot(s, a_o * (s - 0.5), color=rose, lw=2.0, ls=(0, (6, 3)))
ax1.plot(SIG, DE, "o", color=teal, ms=6, mec=dark)
ax1.plot(SIG, DO, "o", color=rose, ms=6, mec=dark)
ax1.axvspan(0.505, 0.60, color="#ffffff", alpha=0.03)
ax1.text(0.505, 0.013, "σ=0.505\n(even 0.0077, odd 0.0075)", color="#e8e4da",
         fontsize=8.5, ha="left", va="bottom")
ax1.set_xlim(0.4975, 0.6025)
ax1.set_ylim(-0.004, 0.165)
ax1.set_xlabel("σ — down the strip toward the line")
ax1.set_ylabel("depth  |1 − λ|  — the resonance's distance from the count's +1")
ax1.annotate("even, t=13.78  (slope 1.485)", xy=(0.535, 0.052), xytext=(0.545, 0.088),
             color=teal, fontsize=9, arrowprops=dict(arrowstyle="->", color=teal, lw=1))
ax1.annotate("odd, t≈9.93  (slope 1.436)", xy=(0.545, 0.062), xytext=(0.556, 0.12),
             color=rose, fontsize=9, arrowprops=dict(arrowstyle="->", color=rose, lw=1))
ax1.text(0.498, 0.15, "one straight fold —\nthe continuation is linear",
         color=grey, fontsize=9, ha="left")

# ---- right: the glide ------------------------------------------------------
DUR, SWEEP = 80.0, 72.0
tt = np.linspace(0, DUR, 500)
sig = 0.60 - 0.095 * np.clip(tt, 0, SWEEP) / SWEEP
sig = np.where(tt > SWEEP, 0.505, sig)
de = np.interp(sig, SIG, DE)
do = np.interp(sig, SIG, DO)
fe = 220 * (1 + de)
fo = 330 * (1 + do)

ax2.set_facecolor(dark)
ax2.axhline(220, color=teal, lw=1.0, ls=(0, (3, 3)), alpha=0.5)
ax2.axhline(330, color=rose, lw=1.0, ls=(0, (3, 3)), alpha=0.5)
ax2.plot(tt, fe, color=teal, lw=2.2, label="even partial — the count's side")
ax2.plot(tt, fo, color=rose, lw=2.2, ls=(0, (6, 3)), label="odd partial — the sign's side")
ax2.axvspan(SWEEP, DUR, color="#ffffff", alpha=0.03)
ax2.text(SWEEP + 0.5, 332, "hold inside\nthe approach", color=grey, fontsize=8.5, va="bottom")
# the beats at the end
t_e = np.linspace(SWEEP, DUR, 200)
sig_e = 0.505
de_e = np.interp(sig_e, SIG, DE)
ax2.annotate("", xy=(DUR, 220 * (1 + de_e)), xytext=(DUR, 220),
             arrowprops=dict(arrowstyle="<->", color=amber, lw=1.2))
ax2.text(DUR - 6.5, 224.5, f"beat slows to {220*de_e:.1f} Hz,\nnever lands",
         color=amber, fontsize=8.5, ha="right")
ax2.set_xlim(0, DUR)
ax2.set_ylim(205, 380)
ax2.set_xlabel("time (s) — σ sweeps 0.60 → 0.505, then holds")
ax2.set_ylabel("partial frequency (Hz), gliding onto the drone's harmonics")
ax2.legend(loc="upper right", fontsize=9, frameon=False)
ax2.text(4, 372, "220 = the count's 4th · 330 = the 6th",
         color=grey, fontsize=8.5)

fig.tight_layout(rect=(0, 0, 1, 0.965))
fig.savefig("assets/selberg-strip-cover.png", dpi=160)
print("wrote assets/selberg-strip-cover.png")
