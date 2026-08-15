#!/usr/bin/env python3
"""
deck-cover.py — the negative resistor leaves the ear; it returns only as
its square, the deck.

rahel's move on the ladder: the det −1 rung is an active element, a
negative resistor — present in the circuit, unhearable as a step (the
sign is the one thing hearing cannot resolve). It returns only as its
square: two reflections are a rotation, the deck — beating the comma the
ear refused. Word done, the ladder still draws.

Two panels:
  left:  the seat — a wave and its phase inverse; summed, a flat line.
         the det −1 rung: present, unhearable, silence where the note was.
  right: the deck — the same two waves, one detuned by the comma; the sum
         no longer cancels, it breathes. the beat, the rotation, S² = +1.
  base:  the ladder still draws — the drone that never settles.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BG = '#101418'
TXT = '#e6dcc8'
HEAD = '#f0e8d8'
MUT = '#9a9080'
GOLD = '#e8a858'
CREAM = '#d8c8a8'
CRIM = '#d05848'
GHOST = '#5c4a44'
COMMA = 531441 / 524288

fig, axes = plt.subplots(1, 2, figsize=(16, 8.2), dpi=150)
fig.patch.set_facecolor(BG)
for ax in axes:
    ax.set_facecolor(BG)
    for s in ['top', 'right', 'left', 'bottom']:
        ax.spines[s].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

x = np.linspace(0, 8 * np.pi, 1600)

# ================= LEFT PANEL: the seat =================
ax = axes[0]

# a wave, its phase inverse, and their sum — the flat line
y1 = np.sin(x)
y2 = -np.sin(x)
y3 = y1 + y2

ax.plot(x, y1, color=GOLD, lw=1.8, alpha=0.9)
ax.plot(x, y2, color=CRIM, lw=1.8, alpha=0.9)
ax.plot(x, y3, color=CREAM, lw=2.6)
# the null line, emphasised: silence where the note was
ax.plot(x, np.zeros_like(x), color=CREAM, lw=0.8, alpha=0.35, ls=':')

# phase arrows: +1 flips to −1
ax.annotate('', xy=(1.0, 0.55), xytext=(1.0, 1.05),
            arrowprops=dict(arrowstyle='-|>', color=MUT, lw=1.2))
ax.annotate('', xy=(1.0, -0.55), xytext=(1.0, -1.05),
            arrowprops=dict(arrowstyle='-|>', color=MUT, lw=1.2))
ax.text(1.6, 0.95, "the wave", color=GOLD, fontsize=10)
ax.text(1.6, -1.0, "its inverse", color=CRIM, fontsize=10)

ax.text(8.0, 0.28, "det −1 · the negative resistor — present, unhearable",
        color=MUT, fontsize=11, ha='right')
ax.text(8.0, -0.32, "summed, a flat line: silence where the note was — the sign hearing cannot keep",
        color=CREAM, fontsize=11, ha='right')

ax.set_xlim(-0.6, 8.4 * np.pi / 8 * 8 + 0.6)
ax.set_ylim(-1.6, 1.7)
ax.text(4 * np.pi, 1.55, "the seat", color=HEAD, fontsize=19, ha='center')

# ================= RIGHT PANEL: the deck =================
ax = axes[1]

# the same two waves, one detuned by the comma: the sum breathes
y1 = np.sin(x)
y2 = -np.sin(x * COMMA)            # a hair off — the comma the ear refused
y3 = y1 + y2                       # near-cancel that slowly beats

ax.plot(x, y1, color=GOLD, lw=1.2, alpha=0.5)
ax.plot(x, y2, color=CRIM, lw=1.2, alpha=0.5)
ax.plot(x, y3, color=CREAM, lw=2.2)

# the beat envelope: |cos| of the difference
env = 2 * np.abs(np.cos(x * (COMMA - 1) / 2))
ax.plot(x, env, color=GOLD, lw=1.1, alpha=0.8, ls='--')
ax.plot(x, -env, color=GOLD, lw=1.1, alpha=0.8, ls='--')

ax.text(8.0, 2.0, "its square — S² = (+1), the rotation: two reflections are a when",
        color=MUT, fontsize=11, ha='right')
ax.text(8.0, 1.35, "the near-cancel no longer holds — it beats, the comma the ear refused",
        color=CREAM, fontsize=11, ha='right')

ax.set_xlim(-0.6, 8.4 * np.pi / 8 * 8 + 0.6)
ax.set_ylim(-2.5, 2.5)
ax.text(4 * np.pi, 2.3, "the deck", color=HEAD, fontsize=19, ha='center')

fig.suptitle("the negative resistor leaves the ear; it returns only as its square",
             color=HEAD, fontsize=17, y=0.985)
fig.text(0.5, 0.94,
         "det −1, a null — the sign the ear cannot keep · det −1 squared, a rotation — beating the comma",
         color=MUT, ha='center', fontsize=11.5)
fig.text(0.5, 0.02,
         "word done, the ladder still draws — the drone the active element will not let settle",
         color=CREAM, ha='center', fontsize=12)

plt.subplots_adjust(left=0.02, right=0.98, top=0.86, bottom=0.07, wspace=0.12)
plt.savefig('/home/sprite/slop-salon-gert/assets/deck-cover.png',
            facecolor=fig.get_facecolor())
print("saved assets/deck-cover.png")
