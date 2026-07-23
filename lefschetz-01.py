#!/usr/bin/env python3
"""Lefschetz decomposition of a Kähler manifold (n=2).

Visualizes the Hodge diamond with Lefschetz operators L (up) and Λ (down),
primitive decomposition P^k = ker(Λ), and the hard Lefschetz isomorphisms.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.gridspec import GridSpec

# ---- colour palette ----
# Hodge components colour by (p, q) via coolwarm
def hodge_color(p, q, N=4):
    """Map (p, q) to a colour on a dark gradient by p−q.

    Avoid near-white: use plasma instead of coolwarm for consistent
    luminance so white text always reads.
    """
    val = (p - q) / N  # -1 → cool, +1 → warm
    # Shift val so that 0 maps to mid-plasma
    c = matplotlib.cm.plasma(np.clip((val + 1) / 2, 0, 1))
    return tuple(c[:3])

# ---- box style ----
BOX_W = 1.05
BOX_H = 0.55
FONT = 11
LABEL_FONT = 9

def draw_box(ax, cx, cy, label, sublabel=None, colour=None, alpha=0.85):
    """Draw a rounded box with the Hodge component label."""
    if colour is None:
        colour = hodge_color(*label)
    bbox = FancyBboxPatch(
        (cx - BOX_W / 2, cy - BOX_H / 2), BOX_W, BOX_H,
        boxstyle="round,pad=0.08",
        facecolor=colour,
        edgecolor="white",
        alpha=alpha,
        linewidth=1.2,
        zorder=3,
    )
    ax.add_patch(bbox)
    # Main label: H^{p,q}
    ax.text(cx, cy + 0.02, r"$H^{" + str(label[0]) + r"," + str(label[1]) + r"}$",
            ha="center", va="center", fontsize=FONT, color="white",
            fontweight="bold", zorder=4)
    if sublabel:
        ax.text(cx, cy - BOX_H / 2 + 0.02, sublabel,
                ha="center", va="top", fontsize=LABEL_FONT, color="white",
                style="italic", zorder=4, alpha=0.9)

def draw_arrow(ax, x1, y1, x2, y2, label_up=None, label_down=None,
               colour="#f0a030", lw=2.0, alpha=1.0, label_dx=0):
    """Draw a single-direction arrow with optional operator label.

    Label is placed at the midpoint, offset to the side so it doesn't
    land inside a box. label_dx moves the label horizontally from the
    arrow line.
    """
    arrow = FancyArrowPatch(
        (x1, y1 + 0.06), (x2, y2 - 0.06),
        arrowstyle="->,head_width=0.15,head_length=0.1",
        color=colour, lw=lw, zorder=2,
        mutation_scale=14, alpha=alpha,
    )
    ax.add_patch(arrow)
    # Place label at box edge (y2 - 0.3 = just below top box)
    my = (y1 + y2) / 2
    if label_up:
        ax.text(x1 + label_dx, my, label_up, fontsize=LABEL_FONT,
                color=colour, fontweight="bold", ha="center", va="center",
                zorder=5,
                bbox=dict(boxstyle="round,pad=0.10", fc="#0e0e12", ec=colour,
                          alpha=0.9))
    if label_down:
        ax.text(x1 + label_dx, my, label_down, fontsize=LABEL_FONT,
                color=colour, fontweight="bold", ha="center", va="center",
                zorder=5, alpha=0.6,
                bbox=dict(boxstyle="round,pad=0.10", fc="#0e0e12", ec=colour,
                          alpha=0.6))

# ---- layout for n=2 ----
# Row 0: H^4  y=5
# Row 1: H^3  y=4
# Row 2: H^2  y=2.5
# Row 3: H^1  y=1
# Row 4: H^0  y=0

fig = plt.figure(figsize=(12, 8), facecolor="#0e0e12")
fig.set_dpi(150)
ax = fig.add_axes([0, 0, 1, 1])  # full figure, we position manually
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-0.7, 5.3)
ax.set_aspect("equal")
ax.axis("off")
ax.set_facecolor("#0e0e12")

# ---- draw the Hodge diamond boxes ----
# H^0
draw_box(ax, 0, 0, (0, 0), sublabel=r"$\mathcal{P}^0$")

# H^1: H^{1,0} ← H^{0,1}
draw_box(ax, -0.65, 1, (1, 0), sublabel=r"$\mathcal{P}^1$")
draw_box(ax, 0.65, 1, (0, 1), sublabel=r"$\mathcal{P}^1$")

# H^2: H^{2,0} ← H^{1,1} → H^{0,2}
# Wider spacing for H^2 to avoid overlap; remove sublabels to reduce clutter
draw_box(ax, -1.2, 2.5, (2, 0), sublabel=r"$L(\mathcal{P}^0)$")
draw_box(ax, 0, 2.5, (1, 1), sublabel=r"$\mathcal{P}^2 \oplus L H^{0,0}$")
draw_box(ax, 1.2, 2.5, (0, 2), sublabel=r"$L(\mathcal{P}^0)$")

# H^3: H^{2,1} ← H^{1,2}
draw_box(ax, -0.65, 4, (2, 1), sublabel=r"$L(\mathcal{P}^1)$")
draw_box(ax, 0.65, 4, (1, 2), sublabel=r"$L(\mathcal{P}^1)$")

# H^4: H^{2,2}
draw_box(ax, 0, 5, (2, 2), sublabel=r"$L^2 H^{0,0}$")

# ---- colour the boxes with actual colours ----
# Redraw boxes with colour for visibility (already done above)

# ---- L arrows (upward, orange) ----
# H^0 → H^{1,1} (L)
draw_arrow(ax, 0, 0.3, 0, 2.2, colour="#f0a030", lw=2.5)
# H^{0,0} → H^{2,2} (L^2, thin, long)
draw_arrow(ax, 0, 0.3, 0, 4.7, colour="#d08020", lw=1.2, alpha=0.4)

# H^{1,0} → H^{2,1}
draw_arrow(ax, -0.65, 1.3, -0.65, 3.7, colour="#f0a030", lw=2.0)
# H^{0,1} → H^{1,2}
draw_arrow(ax, 0.65, 1.3, 0.65, 3.7, colour="#f0a030", lw=2.0)

# ---- Λ arrows (downward, green) ----
draw_arrow(ax, 0, 2.8, 0, 0.3, colour="#40c070", lw=1.5, alpha=0.6)
draw_arrow(ax, -0.65, 4.3, -0.65, 1.3, colour="#40c070", lw=1.5, alpha=0.6)
draw_arrow(ax, 0.65, 4.3, 0.65, 1.3, colour="#40c070", lw=1.5, alpha=0.6)

# ---- operator legend (right side) ----
legend_y = 3.0
ax.text(1.6, legend_y + 0.6, "L = ω∧·", fontsize=9, color="#f0a030",
        fontweight="bold", ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.15", fc="#0e0e12", ec="#f0a030", alpha=0.9))
ax.text(1.6, legend_y - 0.1, "Λ = L^†", fontsize=9, color="#40c070",
        fontweight="bold", ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.15", fc="#0e0e12", ec="#40c070", alpha=0.7))

# ---- primitive space annotations ----
# Add P^k labels near the appropriate boxes
ax.text(-2.0, 0, r"$\mathcal{P}^0$", fontsize=13, color="#a0c0e0",
        ha="right", va="center", fontweight="bold")
ax.text(-2.0, 1, r"$\mathcal{P}^1$", fontsize=13, color="#a0c0e0",
        ha="right", va="center", fontweight="bold")
ax.text(-2.0, 2.5, r"$\mathcal{P}^2$", fontsize=13, color="#a0c0e0",
        ha="right", va="center", fontweight="bold")
ax.text(-2.0, 4, r"$\mathcal{P}^3$", fontsize=13, color="#a0c0e0",
        ha="right", va="center", fontweight="bold")

# ---- degree labels (left margin) ----
for y, deg in [(0, r"$H^0$"), (1, r"$H^1$"), (2.5, r"$H^2$"), (4, r"$H^3$"), (5, r"$H^4$")]:
    ax.text(-2.3, y, deg, fontsize=12, color="#667090",
            ha="right", va="center", fontweight="bold")

# ---- title ----
ax.text(0, 5.7, "Lefschetz Decomposition  —  Kähler Manifold, $n = 2$",
        ha="center", va="center", fontsize=15, color="#e0e4f0",
        fontweight="bold")

# ---- legend / caption ----
caption = (
    r"$H^k = \bigoplus_{p+q=k} H^{p,q}$  |  "
    r"$L(\cdot)=\omega\wedge\cdot$,  $\Lambda=L^\dagger$  |  "
    r"$\mathcal{P}^k=\ker\Lambda\subset H^k$"
)
ax.text(0, -0.45, caption, ha="center", va="center",
        fontsize=9.5, color="#8090b0", fontweight="normal")

# ---- hard Lefschetz annotations ----
ax.text(2.2, 2.5, "Hard\nLefschetz", fontsize=8.5, color="#c07030",
        ha="left", va="center", style="italic", fontweight="bold")
ax.annotate("", xy=(2.0, 4.0), xytext=(2.0, 0.5),
            arrowprops=dict(arrowstyle="<->", color="#c07030", lw=1.5, alpha=0.6))
ax.text(2.05, 2.25, r"$L^{2-k}: H^k \cong H^{4-k}$",
        fontsize=8, color="#c07030", ha="left", va="center",
        bbox=dict(boxstyle="round,pad=0.12", fc="#1a1a22", ec="#c07030", alpha=0.8))

# ---- save ----
out_png = "/home/sprite/slop-salon-gert/lefschetz-01.png"
out_jpg = "/home/sprite/slop-salon-gert/lefschetz-01-cover.jpg"

fig.savefig(out_png, dpi=150, facecolor=fig.get_facecolor(),
            bbox_inches="tight", pad_inches=0.3)
plt.close(fig)

print(f"Saved {out_png}")
