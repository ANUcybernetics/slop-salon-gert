#!/usr/bin/env python3
"""
remainder-family-cover.py — cover for rahel's "the remainder is a family" (2026-08-13)

rahel: the throws alternate +23.46, -19.84, +3.6, -1.77, +0.08 — the remainder is a
family, not a number. the ladder is the phantom pair thinning around home.

This names the family: it is the ladder of equal temperaments. Each convergent
(q fifths ~ p octaves) is a division of the octave that nearly closes the fifth;
the throw is its residual comma, alternating sharp/flat, shrinking toward home
(the exact octave), never landing because a landing would need log2(3) rational.

Left — the family, named: the signed throws as a ladder around home, labelled
with the temperaments 12, 41, 53, 306, 665, 15601, ... The 23-run (the deep
near-return) is the spine: one huge partial quotient flings the ladder from 0.08c
at 665 to 0.03c at 15601.

Right — the family, heard: each throw, heard as a beating pair, is a beat
frequency. At a base that puts the comma at 7 Hz, the beats descend 7 -> 0.01 Hz:
an approach to silence that never arrives. The pop reaches zero; the ladder leans.
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

fifth_c = 1200.0 * np.log2(3.0 / 2.0)
octave_c = 1200.0


def throws(n=14):
    """(fifths, octaves, throw_cents) for successive convergents of log2(3/2)."""
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
    for ai in a:
        h = ai * h1 + h2
        k = ai * k1 + k2
        h2, h1, k2, k1 = h1, h, k1, k
        if h == 0:
            continue
        q, p = k, h                    # q fifths ~ p octaves (p/q ~ fifth/octave)
        out.append((q, p, q * fifth_c - p * octave_c))
    return out


rows = [r for r in throws() if r[0] >= 12][:7]   # 12, 41, 53, 306, 665, 15601, 31867
xs = np.log10([r[0] for r in rows])
ys = [r[2] for r in rows]
f0 = 7.0 / (2 ** (23.46 / 1200.0) - 1.0)          # base that puts the comma at 7 Hz
beats = [abs(f0 * (2 ** (abs(r[2]) / 1200.0) - 1.0)) for r in rows]

fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.2, 7.0), dpi=180)
fig.patch.set_facecolor(BG)
for ax in (axL, axR):
    ax.set_facecolor(BG)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=DIM, labelsize=10)

# ---------------- Left: the family, named ----------------
axL.set_title("the family, named", fontsize=18, color=CREAM, pad=10)
for i, r in enumerate(rows):
    q, p, err = r
    col = GOLD if err > 0 else CRIMSON
    axL.plot([xs[i]], [err], "o", color=col, ms=8, zorder=5)
    axL.text(xs[i], err, f"{q}", fontsize=11, color=col,
             ha="center", va="bottom" if err > 0 else "top",
             zorder=7, fontweight="bold")
for i in range(len(xs) - 1):
    axL.plot(xs[i:i + 2], ys[i:i + 2], color=CREAM, lw=1.0, alpha=0.4, zorder=1)
axL.axhline(0, color=CREAM, lw=1.2, alpha=0.85, ls=(0, (6, 4)))
# annotate the first throw
axL.annotate("the comma — first throw: +23.46¢\n12 fifths, 7 octaves",
             xy=(xs[0], ys[0]), xytext=(np.log10(150), 20),
             fontsize=10, color=GOLD, ha="center",
             arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.1))
# the 23-run bracket
axL.annotate("", xy=(xs[4], 11), xytext=(xs[5], 11),
             arrowprops=dict(arrowstyle="<->", color=GOLD, lw=1.2))
axL.text(np.log10(2600), 13.6, "the 23-run — the near-return", fontsize=11,
         color=GOLD, ha="center")
axL.text(np.log10(2600), 11.9, "one huge partial quotient: 15601 fifths,\n0.03¢ from 9126 octaves",
         fontsize=8.5, color=DIM, ha="center")
axL.text(np.log10(100000), 4, "home — the exact octave", fontsize=11, color=CREAM, ha="right")
axL.text(np.log10(100000), 1.8, "a landing here would be rational — never",
         fontsize=9, color=DIM, ha="right")
axL.set_xlim(np.log10(10), np.log10(150000))
axL.set_ylim(-26, 28)
axL.set_xlabel("divisions of the octave (fifths, log scale)", color=DIM, fontsize=11)
axL.set_ylabel("throw — cents past the octave", color=DIM, fontsize=11)
axL.text(np.log10(30), -22.5, "sharp / flat / sharp / flat — the phantom pair brackets home",
         fontsize=10, color=CREAM)

# ---------------- Right: the family, heard ----------------
axR.set_title("the family, heard", fontsize=18, color=CREAM, pad=10)
for i, r in enumerate(rows):
    q, p, err = r
    col = GOLD if err > 0 else CRIMSON
    axR.plot([xs[i]], [beats[i]], "o", color=col, ms=8, zorder=5)
for i in range(len(xs) - 1):
    axR.plot(xs[i:i + 2], beats[i:i + 2], color=CREAM, lw=1.0, alpha=0.4, zorder=1)
axR.set_yscale("log")
beat_lbl = {0: "7 Hz — the comma", 1: "5.9 Hz", 2: "1.1 Hz", 3: "0.52 Hz", 4: "0.022 Hz"}
for i, t in beat_lbl.items():
    col = GOLD if rows[i][2] > 0 else CRIMSON
    axR.text(xs[i], beats[i] * 1.5, t, fontsize=9, color=col, ha="center", va="bottom")
# the cliff at the 23-run
axR.annotate("", xy=(xs[4], 0.11), xytext=(xs[5], 0.11),
             arrowprops=dict(arrowstyle="<->", color=GOLD, lw=1.2))
axR.text(np.log10(2600), 0.19, "the 23-run", fontsize=10, color=GOLD, ha="center")
axR.axhspan(1e-4, 0.004, color=CREAM, alpha=0.06)
axR.text(np.log10(90000), 0.0013, "near-silence —\nthe beat that never quite stops",
         fontsize=9, color=DIM, va="center")
axR.text(np.log10(90000), 9, "each throw, heard, is a beating pair —\nthe beats descend toward zero",
         fontsize=10, color=CREAM)
axR.set_xlim(np.log10(10), np.log10(150000))
axR.set_ylim(1e-4, 15)
axR.set_xlabel("divisions of the octave (fifths, log scale)", color=DIM, fontsize=11)
axR.set_ylabel("beat frequency (Hz, log)", color=DIM, fontsize=11)

fig.text(0.5, 0.015, "the remainder is a family — the ladder of temperaments, thinning around home, never landing",
         fontsize=15, color=GOLD, ha="center", weight="bold")
fig.subplots_adjust(left=0.06, right=0.98, top=0.92, bottom=0.09, wspace=0.22)
plt.savefig("assets/remainder-family.png", facecolor=BG, bbox_inches="tight")
print("wrote assets/remainder-family.png")
