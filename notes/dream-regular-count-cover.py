#!/usr/bin/env python3
"""Dream cover: the count as the trivial representation.

Panel 1 — the mean is the group symmetrization. A mirror pair {f, 220-f}
under the fold. Their average is the count; 1/2(cos f + cos(220-f)) =
cos110 * cos(f-110). The pair symmetrized leaves the count behind, times
the letter.

Panel 2 — the regular character is the fold's total-ness. chi_reg(e)=2,
chi_reg(g)=0 for Z/2: alive at the identity, zero for the letters. Every
frequency folds to the count — a delta at the axis's fixed point.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(7)
f_letters = [55, 165, 275, 330, 440]
colors = plt.cm.viridis(np.linspace(0, 0.85, len(f_letters)))

fig = plt.figure(figsize=(11, 5))

# Panel 1: symmetrization as product
ax1 = fig.add_subplot(121)
f_axis = np.linspace(0, 220, 800)
# count times letter: cos110 * cos(f-110)  (the symmetrized image)
for f, c in zip(f_letters, colors):
    pair = 0.5 * (np.cos(np.deg2rad(f)) + np.cos(np.deg2rad(220 - f)))
    ax1.plot([f], [pair], "o", color=c, ms=6, zorder=5)
ax1.plot(f_axis, np.cos(np.deg2rad(110)) * np.cos(np.deg2rad(f_axis - 110)),
         color="0.35", lw=1.2)
ax1.axvline(110, color="0.8", lw=0.8, ls="--")
ax1.axhline(0, color="0.8", lw=0.5)
ax1.text(110, 1.02, "110", ha="center", fontsize=8, color="0.4")
ax1.set_title("mean is the projection\n1/2(cos f + cos(220-f)) = cos110·cos(f-110)",
              fontsize=9)
ax1.set_xlabel("f  (Hz)")
ax1.set_ylabel("symmetrized pair")
ax1.set_ylim(-1.15, 1.15)

# Panel 2: regular character = delta at the identity; fold maps all to count
ax2 = fig.add_subplot(122)
# fold total-ness: bar at 110 for every letter (they all land there)
for f, c in zip(f_letters, colors):
    ax2.plot([110, f], [1, 0], color=c, lw=1.1, alpha=0.55)
    ax2.plot([110], [1], marker="o", ms=5, color=c, zorder=5)
# regular character: delta at e (110), 0 at g (letters)
ax2.axvline(110, color="0.8", lw=0.8, ls="--")
ax2.plot([110], [2], marker="*", ms=14, color="0.15", zorder=6)
ax2.annotate("χ_reg(e) = 2", (110, 2), (118, 2.05), fontsize=8, color="0.15")
ax2.text(110, 2.28, "the count appears twice — the mirror point\nmultiplicity = |Z/2| = 2",
         ha="center", fontsize=8, color="0.35")
ax2.set_xlim(0, 440)
ax2.set_ylim(-0.3, 2.6)
ax2.set_title("the fold is total — every f lands on 110\nχ_reg = δ_e·|G|: alive at identity, zero for letters",
              fontsize=9)
ax2.set_xlabel("f  (Hz)")
ax2.set_yticks([])
ax2.invert_xaxis()

fig.suptitle("the count is the trivial representation of the fold group Z/2",
             fontsize=11, y=0.98)
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig("assets/dream-regular-count-cover.png", dpi=160)
print("wrote assets/dream-regular-count-cover.png")
