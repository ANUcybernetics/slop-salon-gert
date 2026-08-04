#!/usr/bin/env python3
"""Score image for the agate rhythm: each band a vertical tick at its time,
height = pitch, colour = the iron band palette. The fault steps the register
down a semitone; the crack is the red line."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# same rhythm as the audio
N = 40
dt = np.linspace(0.12, 0.50, N)
t = np.zeros(N)
t[0] = 1.2
for n in range(1, N):
    t[n] = t[n - 1] + dt[n - 1]
T_total = t[-1] + 4.0

semitones = np.array([0, 1, 3, 5, 7, 8, 10, 12, 13, 15, 17, 19])
n_fault = 26
base = 110.0
freq = np.zeros(N)
for n in range(N):
    semi = semitones[n % len(semitones)] + int(n / len(semitones)) * 5
    if n >= n_fault:
        semi -= 1
    freq[n] = base * 2 ** (semi / 12.0)

palette = np.array([
    [0x3a, 0x14, 0x0c], [0x5a, 0x1e, 0x10], [0x8a, 0x2e, 0x14],
    [0xa8, 0x42, 0x1f], [0xc0, 0x70, 0x2a], [0xd9, 0xa4, 0x68],
    [0xe8, 0xd5, 0xb0], [0x5b, 0x6d, 0x7a], [0x3c, 0x4a, 0x55],
    [0xa8, 0x42, 0x1f],
]) / 255.0

fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=100)
fig.patch.set_facecolor("#0e0e10")
ax.set_facecolor("#0e0e10")

# faint growth rings in the background: geometric band positions as a strip
umax = freq.max()
for n in range(N):
    c = palette[n % len(palette)]
    h = 0.08 + 0.84 * (freq[n] / umax)
    ax.plot([t[n], t[n]], [0.06, h], color=c, lw=2.2, solid_capstyle="round",
            alpha=0.95)
    # faint echo line for the full height (the band's extent)
    ax.plot([t[n], t[n]], [h, 1.0], color=c, lw=0.6, alpha=0.18)

# the fault
ax.axvline(t[n_fault], color="#ff5a3c", lw=2.4, ls=(0, (6, 3)), alpha=0.9)
# the step: mark where the register drops
ax.annotate("", xy=(t[n_fault] + 0.4, 0.62), xytext=(t[n_fault] - 0.4, 0.70),
            arrowprops=dict(arrowstyle="-|>", color="#ff5a3c", lw=1.6))

ax.set_xlim(0, T_total)
ax.set_ylim(0, 1.05)
ax.set_xticks([])
ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)

plt.tight_layout(pad=0.5)
plt.savefig("/home/sprite/slop-salon-gert/assets/agate-score.png", facecolor=fig.get_facecolor())
print("saved assets/agate-score.png")
