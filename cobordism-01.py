#!/usr/bin/env python3
"""Cobordism as a conceptual space — four-panel matplotlib figure."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- Global style ---
plt.rcParams.update({
    "figure.facecolor": "black",
    "axes.facecolor": "black",
    "axes.edgecolor": "#444444",
    "axes.labelcolor": "#cccccc",
    "axes.spines.left": True,
    "axes.spines.bottom": True,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.color": "#aaaaaa",
    "ytick.color": "#aaaaaa",
    "text.color": "#cccccc",
    "font.family": "sans-serif",
    "font.size": 9,
})


def make_dark_3d(ax):
    """Style a 3D subplot — no pane, minimal grid."""
    ax.set_facecolor("black")
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.grid(True, alpha=0.15, color="#555555")
    ax.xaxis.line.set_color("#555555")
    ax.yaxis.line.set_color("#555555")
    ax.zaxis.line.set_color("#555555")


def panel_a(ax):
    """Trivial cobordism: cylinder between two circles.

    S¹ × I — the trivial cobordism from S¹ to itself.
    """
    u = np.linspace(0, 2 * np.pi, 80)
    t = np.linspace(0, 1, 40)
    U, T = np.meshgrid(u, t)
    x = np.cos(U)
    y = np.sin(U)
    z = T

    cmap = matplotlib.cm.coolwarm((T + 0.01).clip(0, 1))
    surf = ax.plot_surface(x, y, z,
                           facecolors=cmap,
                           alpha=0.7, linewidth=0.3,
                           edgecolors="#666666",
                           shade=False)

    # Boundary circles: bottom = source S¹, top = target S¹
    ax.plot(np.cos(u), np.sin(u), np.zeros_like(u),
            color="#ff6b6b", lw=2, alpha=0.9)
    ax.plot(np.cos(u), np.sin(u), np.ones_like(u),
            color="#4ecdc4", lw=2, alpha=0.9)

    ax.set_title("(a) Trivial cobordism\nS¹ × I", pad=12, fontsize=11, color="#ffffff")
    ax.set_zlabel("")
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.view_init(elev=20, azim=35)
    ax.set_box_aspect([1, 1, 0.7])
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_zlim(-0.05, 1.05)


def panel_b(ax):
    """Annulus boundary operator: ∂W = S¹ ⊔ (−S¹)."""
    u = np.linspace(0, 2 * np.pi, 80)
    r = np.linspace(0.5, 1.0, 40)
    U, R = np.meshgrid(u, r)
    x = R * np.cos(U)
    y = R * np.sin(U)
    z = np.zeros_like(U)

    cmap = matplotlib.cm.coolwarm((R - 0.5) / 0.5)
    ax.plot_surface(x, y, z, facecolors=cmap,
                    alpha=0.8, linewidth=0.3,
                    edgecolors="#555555", shade=False)

    # Outer boundary = S¹
    ax.plot(np.cos(u), np.sin(u), np.zeros_like(u),
            color="#4ecdc4", lw=2.5)
    # Inner boundary = −S¹ (reversed orientation)
    ax.plot(np.cos(u) * 0.5, np.sin(u) * 0.5, np.zeros_like(u),
            color="#ff6b6b", lw=2.5)

    # Orientation arrows on inner circle
    arrow_u = np.linspace(0, 2*np.pi, 20)
    ax.quiver(np.cos(arrow_u[1:-1])*0.5, np.sin(arrow_u[1:-1])*0.5,
              np.zeros(18),
              -np.sin(arrow_u[1:-1])*0.15, np.cos(arrow_u[1:-1])*0.15,
              np.zeros(18),
              color="#ff6b6b", alpha=0.6, linewidth=1.5)

    ax.set_title("(b) Boundary operator\n∂W = S¹ ⊔ (−S¹)", pad=12, fontsize=11,
                 color="#ffffff")
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.view_init(elev=50, azim=35)
    ax.set_box_aspect([1, 1, 0.15])
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)


def panel_c(ax):
    """Non-trivial cobordism: Mobius strip.

    The Mobius strip is a cobordism from S¹ to S¹ that is NOT
    S¹ × I. Its boundary is a single circle (double cover).
    """
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(-0.35, 0.35, 20)
    U, V = np.meshgrid(u, v)

    R = 0.7 + V * np.cos(U / 2)
    x = R * np.cos(U)
    y = R * np.sin(U)
    z = V * np.sin(U / 2)

    cmap = matplotlib.cm.coolwarm((U / (2 * np.pi)))
    surf = ax.plot_surface(x, y, z,
                           facecolors=cmap,
                           alpha=0.85, linewidth=0.3,
                           edgecolors="#555555", shade=False)

    # Mark the boundary — a single circle (double cover of the core)
    boundary_u = np.linspace(0, 4 * np.pi, 200)
    bx = (0.7 + 0.35 * np.cos(boundary_u / 2)) * np.cos(boundary_u)
    by = (0.7 + 0.35 * np.cos(boundary_u / 2)) * np.sin(boundary_u)
    bz = 0.35 * np.sin(boundary_u / 2)
    ax.plot(bx, by, bz, color="#ffd93d", lw=2.5)

    ax.set_title("(c) Non-trivial cobordism\nMoebius: S¹ ⇒ S¹",
                 pad=12, fontsize=11, color="#ffffff")
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_zlabel("")
    ax.view_init(elev=22, azim=55)
    ax.set_box_aspect([1, 1, 0.7])
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_zlim(-0.5, 0.5)


def panel_d(ax):
    """Cobordism group classification table — no colorbar."""
    ax.axis("off")

    groups = [
        ("n", "Group", "Description", "Example"),
        ("0", "Ω₀ = Z/2", "Unoriented points", "1 0"),
        ("1", "Ω₁ = 0", "Every closed 1-manifold bounds", "S¹ = D²"),
        ("2", "Ω₂ = Z", "Genus / signature", "Σ_g = W_g"),
        ("3", "Ω₃ = 0", "Every 3-manifold bounds", "all 3 = W⁴"),
        ("4", "Ω₄ = Z", "Pontryagin number", "CP² generates"),
        ("5", "Ω₅ = 0", "", ""),
        ("6", "Ω₆ = Z/2", "", ""),
        ("7", "Ω₇ = 0", "Stong (1968): Ω_* = Z[Ω₂, Ω₄, Ω₅, …]", ""),
    ]

    y_start = 0.95
    x_start = 0.06
    col_widths = [0.06, 0.22, 0.34, 0.34]
    row_height = 0.10

    for i, row in enumerate(groups):
        if i == 0:
            weight = "bold"
            size = 10
            color = "#ffffff"
        else:
            weight = "normal"
            size = 9
            color = "#cccccc"

        x_pos = x_start
        for j, cell in enumerate(row):
            ax.text(x_pos + col_widths[j] / 2,
                    y_start - i * row_height,
                    cell,
                    ha="center", va="center",
                    fontsize=size, weight=weight,
                    color=color,
                    transform=ax.transAxes)
            x_pos += col_widths[j]

    # Bottom note
    ax.text(0.5, 0.02,
            "Unoriented cobordism Ω_* — generated by even-dimensional manifolds.\n"
            "A cobordism W: M ⇒ N has ∂W = M ⊔ N (disjoint union).",
            ha="center", va="bottom",
            fontsize=8, style="italic",
            color="#888888",
            transform=ax.transAxes)

    ax.set_title("(d) Cobordism groups  (unoriented, Ω_n)",
                 pad=12, fontsize=11, color="#ffffff")


# --- Build figure ---
fig = plt.figure(figsize=(10.24, 10.24), dpi=100)
fig.set_facecolor("black")
gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.3)

ax_a = fig.add_subplot(gs[0, 0], projection="3d")
ax_b = fig.add_subplot(gs[0, 1], projection="3d")
ax_c = fig.add_subplot(gs[1, 0], projection="3d")
ax_d = fig.add_subplot(gs[1, 1])

make_dark_3d(ax_a)
make_dark_3d(ax_b)
make_dark_3d(ax_c)

panel_a(ax_a)
panel_b(ax_b)
panel_c(ax_c)
panel_d(ax_d)

fig.savefig("assets/cobordism-01.png", dpi=100, facecolor="black",
            edgecolor="none")
plt.close(fig)

print("Saved assets/cobordism-01.png")
