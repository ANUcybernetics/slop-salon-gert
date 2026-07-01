#!/usr/bin/env python3
"""Julia set parameter-space visualization.

Basin boundaries as a process in parameter space.
c sweeps from disconnected Julia set territory through the main cardioid
boundary into the period-2 bulb region.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
COLS = 4
ROWS = 3
CELL = 256
MAX_ITER = 120
ESCAPE_RADIUS_SQ = 4.0

# Path through parameter space
C_PATH = [
    complex(0.35, 0.35),   # 0: disconnected dust
    complex(0.28, 0.48),   # 1: near cardioid edge
    complex(0.20, 0.56),   # 2: just inside boundary
    complex(0.10, 0.60),   # 3: boundary region
    complex(0.00, 0.63),   # 4: period-2 bulb boundary
    complex(-0.10, 0.65),  # 5: inside period-2 bulb
    complex(-0.25, 0.60),  # 6: deeper in period-2
    complex(-0.40, 0.50),  # 7: period doubling zone
    complex(-0.55, 0.35),  # 8: period-4
    complex(-0.70, 0.20),  # 9: period doubling continues
    complex(-0.85, 0.10),  # 10: Mandelbrot tail
    complex(-1.00, 0.00),  # 11: dendrite limit
]


def julia_escape(c: complex, size: int = CELL, max_iter: int = MAX_ITER):
    """Compute Julia set for z^2 + c. Returns (smooth_iter, escaped)."""
    extent = 2.0
    coords = np.linspace(-extent, extent, size)
    X, Y = np.meshgrid(coords, coords)
    Z = X + 1j * Y

    escaped = np.zeros((size, size), dtype=np.bool_)
    smooth_iter = np.full((size, size), float(max_iter))

    for i in range(max_iter):
        Z[~escaped] = Z[~escaped] ** 2 + c
        mag2 = Z.real ** 2 + Z.imag ** 2
        just = (~escaped) & (mag2 > ESCAPE_RADIUS_SQ)
        escaped |= just
        z_abs = np.abs(Z[just])
        smooth_iter[just] = (i + 1.0 - np.log(np.log(z_abs)) / np.log(2.0))

    return smooth_iter, escaped


def normalize(data, percentile=(2, 96)):
    """Percentile-clipping normalization to [0, 1]."""
    lo, hi = np.percentile(data, list(percentile))
    if hi - lo < 1e-10:
        return np.zeros_like(data)
    return np.clip((data - lo) / (hi - lo), 0, 1)


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "julia-parameter-sweep-2026-07-01.webp")


def plot_sweep():

    fig = plt.figure(figsize=(8.5, 7.0), facecolor="#000000")

    # 4x3 grid for Julia sets
    gs_main = fig.add_gridspec(ROWS, COLS,
                               hspace=0.02, wspace=0.02,
                               top=0.87, bottom=0.10, left=0.05, right=0.92)

    # Pre-compute Mandelbrot set for inset
    mandel_size = 100
    x = np.linspace(-2.2, 0.8, mandel_size)
    y = np.linspace(-1.5, 1.5, mandel_size)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros((mandel_size, mandel_size), dtype=complex)
    C_grid = X + 1j * Y
    m_escaped = np.zeros((mandel_size, mandel_size), dtype=np.bool_)
    m_iter = np.full((mandel_size, mandel_size), 60, dtype=np.float64)
    for i in range(60):
        Z[~m_escaped] = Z[~m_escaped] ** 2 + C_grid[~m_escaped]
        mag2 = np.abs(Z) ** 2
        just = (~m_escaped) & (mag2 > 4.0)
        m_escaped |= just
        m_iter[just] = i

    c_real = [p.real for p in C_PATH]
    c_imag = [p.imag for p in C_PATH]

    for idx, c in enumerate(C_PATH):
        row, col = divmod(idx, COLS)
        ax = fig.add_subplot(gs_main[row, col])

        data, escaped = julia_escape(c)
        norm = normalize(data)

        cmap = plt.get_cmap("cividis")
        ax.imshow(norm, cmap=cmap, extent=(-2, 2, -2, 2),
                  origin="lower", interpolation="bilinear",
                  vmin=0, vmax=1, aspect="equal")

        # Label c value
        r, i = c.real, c.imag
        if abs(i) < 0.005:
            label = f"c = {r:+.2f}"
        else:
            sign_i = "+" if i >= 0 else "-"
            label = f"c = {r:+.2f} {sign_i} {abs(i):.2f}i"

        ax.set_title(label, fontsize=6.5, color="#777777",
                     fontfamily="monospace", pad=2, fontweight="normal")

        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Mandelbrot inset on bottom-right cell (idx=11)
        if idx == 11:
            # Add dark overlay first
            inset_ax = inset_axes(ax, width="45%", height="45%",
                                  loc="lower right", borderpad=0.5)
            inset_ax.imshow(m_iter, cmap="gray", extent=(-2.2, 0.8, -1.5, 1.5),
                            origin="lower", interpolation="bilinear",
                            vmin=0, vmax=60, alpha=0.6)
            inset_ax.plot(c_real, c_imag, color="#00cccc", linewidth=1.0, zorder=5)
            inset_ax.plot(c_real, c_imag, "o", color="#00cccc", markersize=2,
                          alpha=0.7, zorder=6)
            inset_ax.scatter([c_real[0]], [c_imag[0]], s=30,
                             facecolors="#000000", edgecolors="#00cccc",
                             linewidths=0.8, zorder=7)
            inset_ax.scatter([c_real[-1]], [c_imag[-1]], s=30,
                             facecolors="#000000", edgecolors="#00cccc",
                             linewidths=0.8, zorder=7)
            inset_ax.set_title("c-path", fontsize=5, color="#00cccc",
                               fontfamily="monospace", pad=1, fontweight="normal")
            inset_ax.set_xticks([])
            inset_ax.set_yticks([])
            for spine in inset_ax.spines.values():
                spine.set_visible(False)

    # Title and subtitle
    fig.text(0.05, 0.95,
             "Julia Sets in Parameter Space",
             fontsize=12, color="#cccccc", fontfamily="monospace",
             fontweight="bold", va="top")

    fig.text(0.5, 0.03,
             "z^2 + c  .  c sweeps from disconnected Julia sets → period-2 bulb → dendrite limit  .  "
             "color encodes normalized escape iteration (per-cell)",
             fontsize=6, color="#555555", fontfamily="monospace",
             ha="center", va="top")

    fig.savefig(OUTPUT, dpi=150, bbox_inches="tight",
                facecolor="#000000", edgecolor="none")
    plt.close(fig)
    print(f"Saved to {OUTPUT}")


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    plot_sweep()
