#!/usr/bin/env python3
"""comma-cover — the residue is the comma.

Twelve fifths and seven octaves are the same walk at parity but one ℝ apart:
the circle of fifths returns 23.46 cents past home.  The sign (mod-2) reads
the 12-fifth walk even — home, count one.  The ear (ℝ, additive) reads the
residue: +23.46¢.

Top panel: the circle of fifths.  The walk steps clockwise from 220 Hz (A),
eleven public fifth-steps, and lands at 223.0 Hz just past the start — the
gap, drawn and marked, is the comma.  The landing is the residue: born
anti-phase, mono-silent.

Bottom strip: the three ears on a pitch line.  χ₀ (the drone) and the sign
(the reading) both call it home — two dots on 0¢.  ℝ (the walk) sits at the
comma, +23.46¢ — the only one that reads the size.  Readable because deaf.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

GOLD = (0.88, 0.70, 0.36)
PALE = (0.95, 0.90, 0.75)
ROSE = (0.76, 0.35, 0.31)
VIOLET = (0.62, 0.50, 0.82)
ASH = (0.55, 0.62, 0.70)
HI = (0.86, 0.45, 0.38)      # the residue — the comma
LO = (0.40, 0.62, 0.80)
BG = "#0b0b0f"
OUT = "assets/_comma_frames"
os.makedirs(OUT, exist_ok=True)

A0 = 220.0
fs = [A0]
for _ in range(12):
    nf = fs[-1] * 1.5
    if nf >= 2 * A0:
        nf /= 2.0
    fs.append(nf)
COMMA_CENT = 1200 * np.log2(fs[12] / A0)   # 23.46

R = 1.0
def pos(j):
    th = np.deg2rad(90 - j * 30.0)          # clockwise, start at top
    return R * np.cos(th), R * np.sin(th)

def pos_land():
    th = np.deg2rad(90 - COMMA_CENT / 100 * 30.0)   # 7.04° past the start
    return R * np.cos(th), R * np.sin(th)

steps_pts = [pos(j) for j in range(12)]
land_pt = pos_land()
# gap arc: from landing angle to start angle (clockwise = the small wedge)
th_start = np.deg2rad(90.0)
th_land = np.deg2rad(90 - COMMA_CENT / 100 * 30.0)

def draw_frame(frame, alpha_gap=1.0):
    fig = plt.figure(figsize=(9.2, 7.6), dpi=150, facecolor=BG)
    gs = fig.add_gridspec(2, 1, height_ratios=[3.0, 1.0], hspace=0.42,
                          left=0.07, right=0.96, top=0.90, bottom=0.08)
    ax = fig.add_subplot(gs[0])
    ax.set_facecolor(BG)
    ax.axis("off")

    # the clock — the twelve positions
    for (x, y) in steps_pts:
        ax.plot(x, y, 'o', ms=5, mfc=BG, mec=ASH, mew=1.0, alpha=0.85, zorder=3)
    c = mpatches.Circle((0, 0), R, fill=False, ec=ASH, lw=0.8, ls=(0, (4, 4)), alpha=0.4)
    ax.add_patch(c)

    # the walk's path, accumulating
    if frame >= 1:
        path = steps_pts[:frame + 1] + [land_pt] if frame >= 12 else steps_pts[:frame + 1]
        if len(path) >= 2:
            xs, ys = zip(*path)
            ax.plot(xs, ys, color=PALE, lw=1.8, alpha=0.9, zorder=4)
            if frame >= 12:
                # the closing chord lands past the start
                ax.plot(xs[-2:], ys[-2:], color=HI, lw=2.4, alpha=0.95, zorder=5)

    # current step highlight
    if frame == 0:
        cx, cy = steps_pts[0]
        ax.plot(cx, cy, 'o', ms=9, mfc=ASH, mec=PALE, mew=1.2, zorder=6)
        ax.annotate("A · 220", xy=(cx, cy), xytext=(0.0, 1.28),
                    color=PALE, fontsize=9, ha="center")
    elif frame < 12:
        cx, cy = steps_pts[frame]
        ax.plot(cx, cy, 'o', ms=9, mfc=GOLD, mec=PALE, mew=1.2, zorder=6)
        ax.annotate("%.0f" % fs[frame], xy=(cx, cy), xytext=(cx * 1.24, cy * 1.24),
                    color=GOLD, fontsize=8, ha="center")
    else:
        # the landing — the residue, past the start
        ax.plot(land_pt[0], land_pt[1], 'o', ms=11, mfc=HI, mec=PALE, mew=1.4, zorder=7)
        ax.annotate("223.0\nA + 23.46¢", xy=land_pt, xytext=(0.0, 1.34),
                    color=HI, fontsize=9, fontweight="bold", ha="center")
        # the gap wedge
        wed = mpatches.Wedge((0, 0), R, np.rad2deg(th_land), np.rad2deg(th_start),
                             width=None, color=HI, alpha=0.35 * alpha_gap, lw=0)
        ax.add_patch(wed)
        ax.annotate("", xy=(0.92 * R * np.cos((th_start + th_land) / 2),
                            0.92 * R * np.sin((th_start + th_land) / 2)),
                    xytext=(R * 1.32 * np.cos((th_start + th_land) / 2),
                            R * 1.32 * np.sin((th_start + th_land) / 2)),
                    arrowprops=dict(arrowstyle="->", color=HI, lw=1.2))
        ax.text(0, -1.18, "the comma — the walk returns a comma past",
                color=HI, fontsize=10, ha="center")

    # title
    title = "the residue is the comma" if frame >= 12 else "twelve fifths, one octave, a comma past"
    ax.text(0, 1.62, title, color=PALE, fontsize=13, fontweight="bold", ha="center")
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.5, 1.85)

    # ============ bottom strip: the three ears on the pitch line ============
    axs = fig.add_subplot(gs[1])
    axs.set_facecolor(BG)
    for s in axs.spines.values():
        s.set_color(ASH); s.set_alpha(0.4)
    axs.set_yticks([]); axs.set_xticks([])
    axs.set_xlim(-4, 34); axs.set_ylim(-1.6, 1.9)
    axs.plot([-4, 34], [0, 0], color=ASH, lw=0.9, alpha=0.5)
    # the comma span
    axs.plot([0, COMMA_CENT], [0, 0], color=HI, lw=3.0, alpha=0.8,
             solid_capstyle="butt")
    axs.text(COMMA_CENT / 2, -0.42, "the comma", color=HI, fontsize=8, ha="center")

    # the three ears
    axs.plot(0, 0.30, 'o', ms=10, mfc=VIOLET, mec=BG, mew=1.0, zorder=6)
    axs.text(1.2, 0.30, "χ₀ · the drone — 1 · count one", color=VIOLET,
             fontsize=9, va="center")
    axs.plot(0, -0.32, 'o', ms=10, mfc=GOLD, mec=BG, mew=1.0, zorder=6)
    axs.text(1.2, -0.32, "sign · the reading — even · home", color=GOLD,
             fontsize=9, va="center")
    axs.plot(COMMA_CENT, 0.0, 'o', ms=11, mfc=HI, mec=PALE, mew=1.2, zorder=7)
    axs.text(COMMA_CENT + 1.6, 0.0, "ℝ · the walk — +23.46¢ · the residue",
             color=HI, fontsize=9, va="center")
    axs.text(-4, 1.55, "three ears, one walk", color=ASH, fontsize=9)

    fpath = os.path.join(OUT, "frame-%02d.png" % frame)
    fig.savefig(fpath, dpi=150, facecolor=BG)
    plt.close(fig)
    print("frame %02d" % frame)

# frames: 0 = drone alone; 1..11 = the eleven public steps; 12 = landing;
# 13.. = the reveal, gap pulsing ~3 Hz
draw_frame(0)
for j in range(1, 12):
    draw_frame(j)
draw_frame(12, alpha_gap=1.0)
pulse = [0.35, 0.75, 1.0, 0.75, 0.35, 0.75]
for k, a in enumerate(pulse):
    draw_frame(13 + k, alpha_gap=a)

# keep the last reveal frame as the cover
import shutil
shutil.copy(os.path.join(OUT, "frame-18.png"), "assets/comma-cover.png")
print("saved assets/comma-cover.png")
