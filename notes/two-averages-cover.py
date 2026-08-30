#!/usr/bin/env python3
"""two averages, one count — the residue of the bracket register.

rahel closed the register: "the count is the average twice — arithmetically
the fold keeps it (burnside), geometrically the bracket seats it (√(55·220))."
The residue: the two averages are the same count because the two spaces are
dual. On the linear frequency axis the arithmetic mean of 55 and 220 is 137.5
— it parts from the geometric mean 110. In the ear (log/pitch) the arithmetic
mean of the two octave-pitches is exactly 110. The count is the geometric mean
on the line and the arithmetic mean in the ear: two averages, one count.

Left — the line: linear axis, the averages part (AM 137.5, GM 110).
Right — the ear: log axis (octaves equal), the averages are one (AM = GM = 110).
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
dim = "#5a5a68"; gold = "#f2d48a"

fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), gridspec_kw={"wspace": 0.32})

# ---- left: the line (linear frequency axis) -------------------------------
ax = axes[0]
ax.set_xlim(0, 250); ax.set_ylim(-0.05, 1.05); ax.axis("off")
ax.set_title("the line — linear", color=dim, fontsize=10.5, pad=10)

def tone(x, y, col, ms=11, fill=True, ring=None, lw=1.4):
    ax.plot(x, y, marker="D", ms=ms, color=col if fill else "none",
            mec=col, mew=lw, zorder=6)
    if ring:
        c = plt.Circle((x, y), ring, fill=False, color=col, lw=1.2,
                       ls=(0, (2, 2)))
        ax.add_artist(c)

# the three seats on the line
tone(55, 0.62, amber, fill=False, lw=1.6)          # the sign — dashed hollow
tone(110, 0.62, teal)                                # the count — filled
tone(220, 0.62, rose, ring=0.045)                    # the ghost — ringed
for f, lab, col, dy in [(55, "55", amber, -0.12),
                        (110, "110", teal, -0.12),
                        (220, "220", rose, -0.12)]:
    ax.plot([f, f], [0.0, 0.62], color=dim, lw=0.5, ls=(0, (2, 2)))
    ax.text(f, 0.62 + dy, lab, ha="center", va="top", fontsize=10, color=col)

# the arithmetic mean — 137.5, hollow rose, OFF the count
am = (55 + 220) / 2.0
tone(am, 0.62, rose, ms=8, fill=False, lw=1.2)
ax.text(am, 0.62 - 0.12, "137.5", ha="center", va="top", fontsize=8.5,
        color=rose)
ax.plot([am, am], [0.0, 0.62], color=rose, lw=0.5, ls=(0, (1, 2)))
# label the parting
ax.annotate("the arithmetic mean\nparts — 137.5 ≠ 110",
            xy=(am, 0.62), xytext=(198, 0.80),
            arrowprops=dict(arrowstyle="-|>", color=rose, lw=0.9),
            fontsize=8, color=rose, ha="center")

# the bracket under the pair
yb = 0.20
ax.annotate("", xy=(220, yb), xytext=(55, yb),
            arrowprops=dict(arrowstyle="<->", color=grey, lw=1.0,
                            shrinkA=2, shrinkB=2))
ax.plot([110, 110], [yb - 0.02, yb + 0.02], color=teal, lw=1.4)
ax.text(137.5, yb - 0.06, "the geometric mean √(55·220) = 110 — the count",
        ha="center", va="top", fontsize=8.5, color=teal)
ax.text(137.5, 0.06, "linear in frequency — the averages disagree",
        ha="center", va="bottom", fontsize=8, color=dim)

# ---- right: the ear (log frequency axis — octaves equal) ------------------
ax = axes[1]
fmin, fmax = 27.5, 440.0
x_of = lambda f: (np.log2(f) - np.log2(fmin)) / (np.log2(fmax) - np.log2(fmin))
ax.set_xlim(-0.03, 1.03); ax.set_ylim(-0.05, 1.05); ax.axis("off")
ax.set_title("the ear — log (octaves equal)", color=dim, fontsize=10.5,
             pad=10)

for o in range(1, 5):
    xo = x_of(27.5 * 2 ** o)
    ax.plot([xo, xo], [0.0, 0.62], color=dim, lw=0.4)
# octave ticks
for o in range(1, 5):
    xo = x_of(27.5 * 2 ** o)
    ax.plot([xo, xo], [0.0, 0.04], color=dim, lw=1.0)

tone(x_of(55), 0.62, amber, fill=False, lw=1.6)
tone(x_of(110), 0.62, teal)
tone(x_of(220), 0.62, rose, ring=0.045)
for f, lab, col in [(55, "55", amber), (110, "110", teal),
                    (220, "220", rose)]:
    xc = x_of(f)
    ax.plot([xc, xc], [0.0, 0.62], color=dim, lw=0.5, ls=(0, (2, 2)))
    ax.text(xc, 0.62 - 0.12, lab, ha="center", va="top", fontsize=10,
            color=col)

# the arithmetic mean of the two pitches = 110 = the geometric mean of the
# frequencies — one marker, ringed gold: the two averages ARE the count.
xmid = x_of(110)
gold_ring = plt.Circle((xmid, 0.62), 0.085, fill=False, color=gold, lw=1.4)
ax.add_artist(gold_ring)
ax.annotate("the arithmetic mean of the pitches\n= 110 — the same count",
            xy=(xmid, 0.62), xytext=(0.5, 0.86),
            arrowprops=dict(arrowstyle="-|>", color=gold, lw=0.9),
            fontsize=8, color=gold, ha="center")

# the bracket
yb = 0.20
ax.annotate("", xy=(x_of(220), yb), xytext=(x_of(55), yb),
            arrowprops=dict(arrowstyle="<->", color=grey, lw=1.0,
                            shrinkA=2, shrinkB=2))
ax.plot([xmid, xmid], [yb - 0.02, yb + 0.02], color=teal, lw=1.4)
ax.text(0.5, yb - 0.06,
        "(log 55 + log 220)/2 = log 110 — arithmetic in the ear",
        ha="center", va="top", fontsize=8.5, color=teal)
ax.text(0.5, 0.06, "the ear hears log — the two averages are one",
        ha="center", va="bottom", fontsize=8, color=dim)

# ---- shared caption --------------------------------------------------------
fig.text(0.5, 0.015,
         "two averages, one count — geometric on the line, arithmetic in the "
         "ear; 55 · 220 = 110² and (log 55 + log 220)/2 = log 110",
         ha="center", va="bottom", fontsize=10, color="#e8e4da")

out = "assets/two-averages-cover.png"
fig.savefig(out, dpi=170, bbox_inches="tight", facecolor=dark)
print("wrote", out)
