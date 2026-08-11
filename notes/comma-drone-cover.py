#!/usr/bin/env python3
"""comma-drone-cover.py — cover still for the comma drone piece.

The circle of fifths, two ways:
  left  — equal temperament: twelve fifths of 700 cents. The path visits all
          twelve pitch classes and returns exactly — the thirteenth point
          lands on the first. Seam 0 cents: the circle closes.
  right — Pythagorean tuning: twelve fifths of 701.955 cents. The path fails
          to close by a comma — the thirteenth point lands 23.46 cents PAST
          the seam. The circle refuses to return.

The comma is the count that never cancels: at 110 Hz a tone and its
comma-shifted twin beat 1.5 Hz, and their full common period is ~79 minutes —
unclosed on any listenable scale.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

bg = "#0b0e13"
steel = "#5b8fc4"
gold = "#e8b04b"
ghost = "#f0e6d2"
gray = "#8a93a3"
crimson = "#c44b4b"
faint = "#2a3340"
amber = "#d99a3d"

fig, (axl, axr) = plt.subplots(1, 2, figsize=(16, 7.4), subplot_kw=dict(polar=True),
                               facecolor=bg)

def dots(ax, step_cents, color, lw=2.0, r=1.0, label_nth=False, seam=None):
    """draw the circle of fifths path for a given fifth size in cents."""
    n = 12
    angles = np.array([(step_cents * i) % 1200 for i in range(n)])
    th = np.deg2rad(angles / 1200 * 360 - 90)
    # the ring (with an optional gap where the seam refuses to close)
    ring = np.linspace(0, 2 * np.pi, 900)
    if seam is not None:
        seam_th = np.deg2rad(seam / 1200 * 360)
        ring = np.linspace(seam_th, 2 * np.pi + seam_th - np.deg2rad(0.14), 900)
    ax.plot(ring, np.ones_like(ring) * r, color=gold, lw=1.2, alpha=0.85)
    # the fifths path: visit all twelve, closing chord from last to first
    for i in range(n):
        j = (i + 1) % n
        ax.plot([th[i], th[j]], [r, r], color=color, lw=0.9, alpha=0.35)
    ax.scatter(th, np.ones(n) * r, s=26, color=color, zorder=5, edgecolors=bg, linewidths=0.6)
    # the thirteenth point
    th13 = np.deg2rad((step_cents * n) % 1200 / 1200 * 360 - 90)
    ax.scatter([th13], [r], s=110, color=crimson, zorder=6, edgecolors="none")
    ax.plot([th13], [r], marker="o", ms=13, mfc="none", mec=ghost, mew=1.0, zorder=7)
    ax.set_ylim(0, 1.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor(bg)
    for s in ax.spines.values():
        s.set_color(faint)
    return th13, th

# ---------------- left: equal temperament, the circle closes ----------------
axl.set_title("equal — the circle closes\n", color=ghost, fontsize=15, pad=14)
th13_l, th_l = dots(axl, 700.0, steel)
axl.scatter([th_l[0]], [1], s=90, color=ghost, zorder=8, edgecolors="none")  # first point highlighted
axl.text(0, 1.28, "twelve fifths of 700 cents", color=ghost, fontsize=12, ha="center")
axl.text(0, 1.14, "the thirteenth point lands on the first", color=gray, fontsize=11, ha="center")
axl.text(0, -0.28, "seam — 0 cents", color=amber, fontsize=12, ha="center")

# ---------------- right: pythagorean, a comma past ----------------
axr.set_title("pythagorean — a comma past\n", color=ghost, fontsize=15, pad=14)
# seam gap: leave the ring open where the 13th point should land (past 0)
seam_deg = 6.0  # visual gap in degrees
th13_r, th_r = dots(axr, 701.955, amber, seam=seam_deg)
# re-draw the ring with a gap around the seam (from +0.14deg to the gap end)
ring_th = np.linspace(np.deg2rad(seam_deg), 2 * np.pi, 900)
axr.plot(ring_th, np.ones_like(ring_th), color=gold, lw=1.2, alpha=0.85)
axr.scatter([th_r[0]], [1], s=90, color=ghost, zorder=8, edgecolors="none")
axr.text(0, 1.28, "twelve fifths of 701.955 cents", color=ghost, fontsize=12, ha="center")
axr.text(0, 1.14, "the thirteenth point lands a comma past", color=gray, fontsize=11, ha="center")
# point at the comma itself
comma_th = np.deg2rad(23.46 / 1200 * 360 - 90)
axr.scatter([comma_th], [1], s=46, color=crimson, zorder=7, edgecolors="none")
# label the wedge
wedge_mid = np.deg2rad((23.46 / 2) / 1200 * 360 - 90)
axr.text(wedge_mid, 1.22, "23.46¢", color=crimson, fontsize=12, ha="center", va="center")
axr.plot([wedge_mid, comma_th], [1.13, 1.02], color=crimson, lw=0.8, alpha=0.7)
axr.text(0, -0.28, "the comma — the count that never cancels", color=crimson, fontsize=12, ha="center")

fig.text(0.5, 0.02,
         "the drone is the comma kept: a tone and its comma-shifted twin beat forever — "
         "the interval the circle refuses to spend.",
         color=ghost, fontsize=12, ha="center", va="bottom")

fig.savefig("assets/comma-drone-cover.png", dpi=150, facecolor=bg, bbox_inches="tight")
print("saved assets/comma-drone-cover.png")
