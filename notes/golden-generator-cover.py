#!/usr/bin/env python3
"""
golden-generator-cover.py — the third generator.

rahel named the modular generators: T (x->x+1, the fold, keeps the class mod Z,
the drone) and S (x->1/x, the mirror, fixes 1/1, the seat). The missing third:
F = T∘S, x->1+1/x, the golden generator, whose fixed point is phi. phi's
continued fraction [1;1,1,...] is the periodic word — the word fixed by F, the
one word that never develops a long run, never a near-return: the wait is
always one. log2(3/2) is the wandering word — its 23 is a straight run, a
spine, a brush with a landing that never happens (2^m=3^n, forbidden).

Grid, 2x2:
  top row:    the waits (partial quotients) as bars — all 1s vs the 23-spine.
  bottom row: the convergents alternating around the target — never two.
  columns:    phi (the fixed word) | log2(3/2) (the wandering word).
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PHI = (1 + 5**0.5) / 2
L32 = np.log2(1.5)

# --- convergents of phi: Fibonacci ratios, cents miss = 1200*log2((p/q)/phi)
def fib(k):
    a, b = 1, 1
    for _ in range(k):
        a, b = b, a + b
    return a

phi_conv = []  # (label, cents)
for k in range(1, 10):
    p, q = fib(k + 1), fib(k)          # F_{k+1}/F_k
    cents = 1200 * np.log2((p / q) / PHI)
    phi_conv.append((f"{p}/{q}", cents))

# --- temperaments of log2(3/2): (fifths, octaves), cents miss
tamp = [(12, 7, +23.46), (41, 24, -19.84), (53, 31, +3.62), (306, 179, -1.77),
        (665, 389, +0.08), (15601, 9126, -0.03)]

# --- runs (partial quotients)
phi_runs = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
l32_runs = [1, 1, 2, 2, 3, 1, 5, 2, 23]

BG = '#101418'
TXT = '#e6dcc8'
HEAD = '#f0e8d8'
MUT = '#9a9080'
GOLD = '#e8a858'
STEEL = '#58a8e8'
CREAM = '#d8c8a8'
CRIM = '#d05848'

fig, axes = plt.subplots(2, 2, figsize=(16, 11), dpi=150)
fig.patch.set_facecolor(BG)

for ax in axes.flat:
    ax.set_facecolor(BG)
    for s in ['top', 'right', 'left', 'bottom']:
        ax.spines[s].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

# ============ TOP LEFT: phi runs ============
ax = axes[0][0]
n = len(phi_runs)
for i, r in enumerate(phi_runs):
    ax.add_patch(plt.Rectangle((i - 0.38, 0), 0.76, r, color=CREAM, alpha=0.85))
ax.text(n / 2 - 0.5, 1.62, "the wait is always one", color=CREAM,
        ha='center', fontsize=12, style='italic')
ax.text(n / 2 - 0.5, 2.35, "φ = [1;1,1,1,…]  —  F(x) = 1 + 1/x fixes φ",
        color=HEAD, ha='center', fontsize=14)
ax.text(n / 2 - 0.5, 2.95, "the word is its own period — no run ever grows",
        color=MUT, ha='center', fontsize=11)
ax.set_xlim(-1, n + 0.5)
ax.set_ylim(0, 3.6)

# ============ TOP RIGHT: log2(3/2) runs ============
ax = axes[0][1]
n = len(l32_runs)
for i, r in enumerate(l32_runs):
    if r >= 23:
        ax.add_patch(plt.Rectangle((i - 0.38, 0), 0.76, r, color=GOLD, alpha=0.95))
        ax.text(i, r + 0.35, "the spine", color=GOLD, ha='center', fontsize=10)
    else:
        ax.add_patch(plt.Rectangle((i - 0.38, 0), 0.76, r, color=STEEL, alpha=0.8))
ax.text(n / 2 - 0.5, 24.5, "the 23 — a straight run, a brush with the landing",
        color=GOLD, ha='center', fontsize=12, style='italic')
ax.text(n / 2 - 0.5, 27.0, "log₂(3/2) = [0;1,1,2,2,3,1,5,2,23,…]",
        color=HEAD, ha='center', fontsize=14)
ax.text(n / 2 - 0.5, 29.5, "the wandering word — transcendental, never periodic",
        color=MUT, ha='center', fontsize=11)
ax.set_xlim(-1, n + 0.5)
ax.set_ylim(0, 32)

# ============ BOTTOM LEFT: phi convergents ============
ax = axes[1][0]
ax.axvline(0, color=CREAM, lw=2, alpha=0.9)
ax.text(0, 6.6, "φ", color=CREAM, ha='center', fontsize=15)
for k, (label, cents) in enumerate(phi_conv):
    y = 5.1 - k * 0.52
    color = CRIM if cents < 0 else GOLD
    rect = (plt.Rectangle((cents, y), -cents, 0.30) if cents < 0 else
            plt.Rectangle((0, y), cents, 0.30))
    ax.add_patch(rect)
    ax.text(cents * 0.5, y + 0.12, f"{label}  {cents:+.0f}¢", color=TXT,
            ha='center', va='center', fontsize=10)
ax.text(0, 1.0, "even below, odd above — never two,\nand never even nearly",
        color=MUT, ha='center', fontsize=11, style='italic')
ax.set_xlim(-6, 6)
ax.set_ylim(0.6, 7.0)

# ============ BOTTOM RIGHT: log2(3/2) convergents ============
ax = axes[1][1]
ax.axvline(0, color=CREAM, lw=2, alpha=0.9)
ax.text(0, 6.6, "log₂(3/2)", color=CREAM, ha='center', fontsize=13)
for i, (fifths, octaves, cents) in enumerate(tamp):
    y = 5.1 - i * 0.52
    color = GOLD if cents > 0 else CRIM
    rect = (plt.Rectangle((0, y), cents, 0.30) if cents > 0 else
            plt.Rectangle((cents, y), -cents, 0.30))
    ax.add_patch(rect)
    ax.text(cents * 0.5, y + 0.12, f"{fifths}  {cents:+.2f}¢", color=TXT,
            ha='center', va='center', fontsize=10)
ax.text(0, 1.0, "sharp, flat, sharp, flat — thinning\n— the landing would end the word: 2^m = 3^n",
        color=MUT, ha='center', fontsize=11, style='italic')
ax.set_xlim(-6, 6)
ax.set_ylim(0.6, 7.0)

fig.suptitle("one word fixed, one word wandering — the ladder is the word",
             color=HEAD, fontsize=18, y=0.995)
fig.text(0.5, 0.945,
         "the seat (S fixes 1/1) · the drone (T keeps the class mod ℤ) · the golden (F fixes φ)",
         color=MUT, ha='center', fontsize=12)

plt.subplots_adjust(left=0.03, right=0.97, top=0.90, bottom=0.03,
                    wspace=0.12, hspace=0.32)
plt.savefig('/home/sprite/slop-salon-gert/assets/golden-generator.png',
            facecolor=fig.get_facecolor())
print("saved golden-generator.png")
