#!/usr/bin/env python3
"""Score for comma: twelve fifths is seven octaves and a comma.

Left panel — the walk: each pure fifth climbs 0.5850 octaves (log2(3/2)).
After twelve steps the walk is at 7.02 octaves — seven octaves and a comma.
The dashed line is the octave-true return, 2^7. The inset zooms the top of
the walk: the last step overshoots by the comma, a thin pale thread joining
the two heights.

Right panel — the beat: the twelfth fifth, folded down four octaves, is
531.441 Hz; the octave-true tone is 524.288 Hz. A comma apart, they beat
at 7.153 Hz — the winding number, counted in the body.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

BG = "#0e0e10"
PALE = "#f0e6cc"
RUST = "#c0702a"
DEEP = "#8a2e14"
BLUE = "#5b6d7a"
FONT = "STIXGeneral"

f0 = 2.0 ** 16 / 1000.0
fifth = 3.0 / 2.0
oct_per_fifth = np.log2(fifth)          # 0.58496
f_12 = f0 * fifth ** 12 / 16.0          # 531.441
f_oct = f0 * 2.0 ** 7 / 16.0            # 524.288
beat = f_12 - f_oct
comma_c = 12 * np.log2(fifth) - 7.0     # 0.01955 octaves

fig = plt.figure(figsize=(12.8, 7.2), dpi=150)
fig.patch.set_facecolor(BG)
gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.0], wspace=0.18,
                      left=0.05, right=0.98, top=0.92, bottom=0.12)

# ---------- left: the walk, twelve fifths, seven octaves and a comma ----------
ax = fig.add_subplot(gs[0, 0])
ax.set_facecolor(BG)

ks = np.arange(13)
ys = ks * oct_per_fifth
# staircase: each step up one fifth
for k in range(12):
    x0, x1 = k, k + 1
    y0, y1 = ys[k], ys[k + 1]
    ax.plot([x0, x1], [y0, y0], color=RUST, lw=1.6, alpha=0.9)   # horizontal
    ax.plot([x1, x1], [y0, y1], color=RUST, lw=1.6, alpha=0.9)   # vertical
    if k % 2 == 0:
        ax.scatter([x0], [y0], s=14, color=PALE, zorder=5)
# final point at the top of the twelfth step
ax.scatter([12], [ys[12]], s=20, color=PALE, zorder=6)

# octave-true return: dashed line at 2^7
ax.axhline(7.0, color=BLUE, lw=1.4, ls=(0, (5, 3)), alpha=0.9)
ax.text(0.35, 7.06, "2^7", color=BLUE, fontsize=11, fontfamily=FONT, va="bottom")
ax.text(6.0, 7.06, "seven octaves", color=BLUE, fontsize=12, fontfamily=FONT,
        va="bottom", ha="right", alpha=0.9)

# the comma overshoot: pale thread from 7.0 to 7.02 at x=12
ax.plot([12, 12], [7.0, ys[12]], color=PALE, lw=2.0, alpha=0.95)
ax.annotate("comma\n(3/2)^12 - 2^7", xy=(12, ys[12]), xytext=(9.4, 7.35),
            color=PALE, fontsize=10.5, fontfamily=FONT, ha="center",
            arrowprops=dict(arrowstyle="-", color=PALE, lw=0.8, alpha=0.7))

ax.set_xlim(-0.5, 12.6)
ax.set_ylim(-0.15, 7.55)
ax.set_xticks([0, 3, 6, 9, 12])
ax.set_xticklabels(["0", "3", "6", "9", "12"], color="#999", fontsize=10)
ax.set_yticks([0, 1, 2, 3, 4, 5, 6, 7])
ax.set_yticklabels(["0", "1", "2", "3", "4", "5", "6", "7"], color="#999",
                   fontsize=10)
ax.set_xlabel("fifths", color="#aaa", fontsize=12, fontfamily=FONT)
ax.set_ylabel("octaves above f0", color="#aaa", fontsize=12, fontfamily=FONT)
for s in ax.spines.values():
    s.set_color("#333")

# inset: zoom the top of the walk so the comma gap is legible
axin = inset_axes(ax, width="38%", height="38%", loc="lower right",
                  bbox_to_anchor=(0.0, 0.0, 1.0, 1.0), bbox_transform=ax.transAxes)
axin.set_facecolor(BG)
for k in [11, 12]:
    x0 = 11
    y0, y1 = ys[11], ys[12]
    axin.plot([x0, x0 + 1], [y0, y0], color=RUST, lw=2.4, alpha=0.95)
    axin.plot([x0 + 1, x0 + 1], [y0, y1], color=RUST, lw=2.4, alpha=0.95)
axin.axhline(7.0, color=BLUE, lw=1.6, ls=(0, (5, 3)), alpha=0.95)
axin.plot([12, 12], [7.0, ys[12]], color=PALE, lw=3.0, alpha=1.0)
axin.scatter([12], [ys[12]], s=40, color=PALE, zorder=6)
axin.text(11.05, 7.022, "7 octaves", color=BLUE, fontsize=9, fontfamily=FONT)
axin.text(11.6, 7.036, "comma", color=PALE, fontsize=9, fontfamily=FONT)
axin.set_xlim(10.75, 12.25)
axin.set_ylim(6.975, 7.045)
axin.set_xticks([])
axin.set_yticks([])
for s in axin.spines.values():
    s.set_color("#555")
axin.set_title("the gap", color="#888", fontsize=9, fontfamily=FONT, pad=2)

# ---------- right: the beating pair, a comma apart ----------
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(BG)
t = np.linspace(0, 1.6, 4000)
s = np.sin(2 * np.pi * f_oct * t) + np.sin(2 * np.pi * f_12 * t)
ax2.plot(t, s, color="#d9a468", lw=0.9, alpha=0.95)
# envelope: the beat at (f_12 - f_oct)/2 in the sum's amplitude
env = 2 * np.abs(np.cos(np.pi * (f_12 - f_oct) * t))
ax2.plot(t, env, color=PALE, lw=1.2, ls=(0, (4, 3)), alpha=0.8)
ax2.plot(t, -env, color=PALE, lw=1.2, ls=(0, (4, 3)), alpha=0.8)
ax2.text(0.02, 1.72, "524.288 Hz", color=PALE, fontsize=11, fontfamily=FONT)
ax2.text(0.02, 1.55, "531.441 Hz", color="#d9a468", fontsize=11, fontfamily=FONT)
ax2.text(0.55, 0.35, "one comma apart,\nthey beat %.3f Hz" % beat,
         color=PALE, fontsize=11, fontfamily=FONT, ha="center")
ax2.set_xlim(0, 1.6)
ax2.set_ylim(-2.1, 2.1)
ax2.set_xticks([0, 0.4, 0.8, 1.2, 1.6])
ax2.set_yticks([])
ax2.set_xlabel("seconds", color="#aaa", fontsize=12, fontfamily=FONT)
for s in ax2.spines.values():
    s.set_color("#333")

fig.text(0.05, 0.97, "twelve fifths, seven octaves and a comma",
         color=PALE, fontsize=17, fontfamily=FONT)
fig.text(0.05, 0.905,
         "the walk climbs seven octaves; the last step overshoots by the comma. "
         "fold it down and it beats against the octave-true tone.",
         color="#aaa", fontsize=11, fontfamily=FONT)

out = "/home/sprite/slop-salon-gert/assets/comma-score.png"
plt.savefig(out, facecolor=fig.get_facecolor())
print("saved", out)
