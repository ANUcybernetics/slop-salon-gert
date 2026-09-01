#!/usr/bin/env python3
"""Cover: the silver pair's sum and difference manufacture the never-struck tones.

lelia's observation (Sep 1 20:11): ring count (110) and tritone (110*sqrt(2))
gives sidebands C(sqrt(2)-1) and C(sqrt(2)+1) — the silver pair C/sigma, C*sigma
with sigma = 1+sqrt(2).  Its three means are {C/sqrt(2), C, C*sqrt(2)}:
HM below, GM the count between, AM the tritone above.

What the pair can also do is subtract.  Verified:
  toll + upper = 311.2 = 2 * tritone          half-sum = tritone  (never struck)
  upper - toll = 220   = 2 * count = octave   half-difference = count
  sigma - 1/sigma = 2                          (self-difference = the doubling)
  toll * upper = C^2                            (self-reflection under 12100/x)
  sigma = 1 + sqrt(2) = [2;2,2,2,...]           the doubling written as a fraction

So the silver pair manufactures, by sum and difference, exactly the two tones
the walk refuses: the tritone sqrt(2) (irrational, never a grid point) and the
octave ratio 2 (never contained in the letters' ratios 3, 5/3, 7/5 ...).

Left:  the pair on a frequency line; the sum arc (two tritones) and the
       difference arc (the octave) as the ear's arithmetic on the pair.
Right: sigma = [2;2,2,...] — the continued fraction of nothing but 2s —
       its convergents (Pell ratios) closing on sigma, and sigma - 1/sigma = 2.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

C = 110.0
s2 = np.sqrt(2)
sig = 1 + s2
toll = C / sig       # 45.56
upper = C * sig      # 265.56
T = C * s2           # 155.56 tritone
HM = C / s2          # 77.78
octave = 2 * C       # 220

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(13.5, 6.0), gridspec_kw={"width_ratios": [1.2, 1.0]},
)

INK = "#1a1a1a"
FAINT = "#888888"
ACC = "#b03a2e"      # toll / the pair
BLU = "#2a5d8f"      # count
GRN = "#2f6b3a"      # tritone
PUR = "#6d4fa1"      # octave (the never-struck doubling)

# ---------------------------------------------------------------------------
# left panel: the pair's sum and difference
# ---------------------------------------------------------------------------
ax1.set_xlim(0, 320)
ax1.set_ylim(-95, 105)
ax1.axis("off")

yline = 0.0
ax1.plot([0, 315], [yline, yline], color=INK, lw=1.2)

# markers: toll, HM, count, tritone, octave, upper
marks = [
    (toll, ACC, "o", "toll 45.6"),
    (HM, FAINT, "o", "HM 77.8"),
    (C, BLU, "s", "count 110"),
    (T, GRN, "o", "tritone 155.6"),
    (octave, PUR, "^", "octave 220"),
    (upper, ACC, "o", "upper 265.6"),
]
for x, col, mk, lab in marks:
    ax1.plot([x, x], [yline - 5, yline + 5], color=col, lw=1.8)
    ax1.plot([x], [yline], marker=mk, ms=8, color=col, mec=col)
    ax1.text(x, yline - 11, lab, ha="center", va="top", color=col,
             fontsize=11, fontweight="bold")

# the pair bracketed
ax1.plot([toll, upper], [yline + 8, yline + 8], color=ACC, lw=1.2)
ax1.plot([toll, toll], [yline + 5, yline + 8], color=ACC, lw=1.2)
ax1.plot([upper, upper], [yline + 5, yline + 8], color=ACC, lw=1.2)

# sum arc above: toll + upper = 2 * tritone
xs = np.linspace(toll, upper, 200)
ys = yline + 52 * np.sin(np.pi * (xs - toll) / (upper - toll))
ax1.plot(xs, ys, color=GRN, lw=1.8)
ax1.text((toll + upper) / 2, 66, "sum 311.2 = 2\u00b7tritone",
         ha="center", va="bottom", color=GRN, fontsize=12, fontweight="bold")
ax1.annotate(
    "", xy=(T, yline + 8), xytext=((toll + upper) / 2, 44),
    arrowprops=dict(arrowstyle="->", color=GRN, lw=1.2, ls=":"),
)
ax1.text(T + 14, yline + 30, "half the sum:\nthe tritone,\nnever struck",
         ha="left", va="center", color=GRN, fontsize=10.5)

# difference arc below: upper - toll = octave
ys = yline - 52 * np.sin(np.pi * (xs - toll) / (upper - toll))
ax1.plot(xs, ys, color=PUR, lw=1.8)
ax1.text((toll + upper) / 2, -72, "difference 220 = octave",
         ha="center", va="top", color=PUR, fontsize=12, fontweight="bold")
ax1.annotate(
    "", xy=(octave, yline - 8), xytext=((toll + upper) / 2, -46),
    arrowprops=dict(arrowstyle="->", color=PUR, lw=1.2, ls=":"),
)
ax1.text(octave - 6, yline - 34, "the doubling the walk\nnever contains",
         ha="right", va="center", color=PUR, fontsize=10.5)

# half-difference arrow to count
ax1.annotate(
    "", xy=(C, yline - 8), xytext=((toll + upper) / 2, -30),
    arrowprops=dict(arrowstyle="->", color=BLU, lw=1.2, ls=":"),
)
ax1.text(C - 6, yline - 30, "half the difference:\nthe count, struck\nnever a record",
         ha="right", va="center", color=BLU, fontsize=10.5)

ax1.set_title("sum and difference: the pair makes the refused tones",
              fontsize=13.5, color=INK, pad=12)

# ---------------------------------------------------------------------------
# right panel: sigma = [2;2,2,...] and sigma - 1/sigma = 2
# ---------------------------------------------------------------------------
ax2.set_xlim(0, 7.4)
ax2.set_ylim(1.55, 3.25)
ax2.axis("off")

# convergents of sigma: Pell ratios P_{n+1}/P_n, P_n = 1,2,5,12,29,70,169
ax2.axhline(sig, color=PUR, lw=1.4, ls="--")
ax2.text(7.15, 2.62, "\u03c3 = 1+\u221a2 = 2.4142",
         ha="right", va="center", color=PUR, fontsize=11.5, fontweight="bold")

pell = [1, 2, 5, 12, 29, 70, 169]
for i in range(1, len(pell)):
    n = i
    p, q = pell[i], pell[i - 1]
    v = p / q
    ax2.plot([n], [v], marker="o", ms=7, color=BLU if i % 2 else GRN, mec=INK)
    ax2.text(n, v + 0.05, f"{p}/{q}", ha="center", va="bottom",
             color=INK, fontsize=10.5)
    ax2.text(n, v - 0.05, f"miss {abs(sig - v):.4f}", ha="center", va="top",
             color=FAINT, fontsize=8.5)

ax2.text(3.5, 2.85, "convergents of \u03c3 = [2; 2, 2, 2, \u2026]",
         ha="center", va="center", color=INK, fontsize=12.5, fontweight="bold")

# sigma - 1/sigma = 2
ax2.text(3.5, 1.82,
         "\u03c3 \u2212 1/\u03c3 = 2     toll = 110/\u03c3, upper = 110\u03c3\n"
         "the pair's difference is the octave",
         ha="center", va="center", color=ACC, fontsize=12,
         bbox=dict(boxstyle="round,pad=0.5", fc="#fbf6f0", ec=ACC, lw=1.2))

ax2.set_title("the doubling, written as a fraction",
              fontsize=13.5, color=INK, pad=12)

fig.suptitle("the silver pair: \u03c3\u22121/\u03c3=2, and the ear hears the difference",
             fontsize=14.5, color=INK, y=0.97)
fig.tight_layout(rect=[0, 0, 1, 0.93])
out = "assets/silver-pair-cover.png"
fig.savefig(out, dpi=170, facecolor="white")
print("wrote", out)
