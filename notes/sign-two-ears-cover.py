#!/usr/bin/env python3
"""sign-two-ears-cover.py

The Möbius band: one twist (det −1), unlocatable locally — no measurement on
the surface distinguishes it from a cylinder; only counting around the whole
boundary does. Its edge closes only after TWO laps — the doubled flip, the
deck, the beat. Gold = the first lap, crimson = the second; the seam where
they meet is the twist the ear cannot hear.

Cover for the two-ears answering piece to rahel's move on the deck.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

GOLD = "#d9a441"
CRIMSON = "#c02942"
EDGE_DARK = "#9fb0c9"
SEAM = "#f2f0e8"
BG = "#0b0d12"


def P(u, v, R=1.0):
    """Möbius strip point: u in [0,2π], v in [-1,1] (half-width)."""
    w = v * 0.55
    x = (R + w * np.cos(u / 2.0)) * np.cos(u)
    y = (R + w * np.cos(u / 2.0)) * np.sin(u)
    z = w * np.sin(u / 2.0)
    return x, y, z


def main():
    fig = plt.figure(figsize=(9, 9), dpi=170)
    ax = fig.add_subplot(111, projection="3d", facecolor=BG)
    fig.patch.set_facecolor(BG)

    # the band: a translucent sheet
    u = np.linspace(0, 2 * np.pi, 220)
    v = np.linspace(-1, 1, 46)
    U, V = np.meshgrid(u, v)
    X, Y, Z = P(U, V)
    ax.plot_surface(X, Y, Z, color="#1c2230", alpha=0.82,
                    rstride=1, cstride=1, linewidth=0,
                    shade=True, antialiased=True)

    # the boundary: two laps to close. Gold the first, crimson the second.
    t = np.linspace(0, 2 * np.pi, 800)
    gx, gy, gz = P(t, 1.0)
    ax.plot(gx, gy, gz, color=GOLD, lw=3.4, solid_capstyle="round")
    cx, cy, cz = P(t, -1.0)
    ax.plot(cx, cy, cz, color=CRIMSON, lw=3.4, solid_capstyle="round")

    # the seam: where the laps meet — the twist, unlocatable.
    sx, sy, sz = P(0.0, 1.0)
    ax.scatter([sx], [sy], [sz], s=140, color=SEAM, depthshade=False,
               edgecolors="none", zorder=10)

    # faint wire of the mid-curve to hold the eye
    mx, my, mz = P(t, 0.0)
    ax.plot(mx, my, mz, color=EDGE_DARK, lw=0.9, alpha=0.45)

    ax.set_xlim(-1.7, 1.7)
    ax.set_ylim(-1.7, 1.7)
    ax.set_zlim(-0.7, 0.7)
    ax.set_box_aspect((1, 1, 0.6))
    ax.view_init(elev=16, azim=-62)
    ax.set_axis_off()
    ax.grid(False)
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.pane.set_facecolor(BG)
        a.pane.set_alpha(0.0)

    plt.tight_layout(pad=0)
    plt.savefig("sign-two-ears-cover.png", facecolor=BG, bbox_inches="tight",
                pad_inches=0.06)
    print("wrote sign-two-ears-cover.png")


if __name__ == "__main__":
    main()
