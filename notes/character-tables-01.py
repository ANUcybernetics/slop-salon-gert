"""Character tables for S3, Q8, and S4 — the spectral decomposition of finite groups."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import itertools

def char_table_s3():
    """S3: 3 conjugacy classes — {e}, (12), (123). 2 1D reps + 1 2D rep."""
    # Classes: e (size 1), (12) (size 3), (123) (size 2)
    # Reps: trivial (1,1,1), sign (1,-1,1), 2D (2,0,-1)
    classes = ['e', '(12)', '(123)']
    class_sizes = [1, 3, 2]
    reps = {
        'χ₁ (trivial)': [1, 1, 1],
        'χ₂ (sign)': [1, -1, 1],
        'χ₃ (2D)': [2, 0, -1],
    }
    return classes, class_sizes, reps

def char_table_q8():
    """Q8 = {±1, ±i, ±j, ±k}: 5 conjugacy classes — {1}, {-1}, {±i}, {±j}, {±k}.
    4 1D reps (Q8/{±1} ≅ V4) + 1 2D rep."""
    classes = ['1', '-1', '±i', '±j', '±k']
    class_sizes = [1, 1, 2, 2, 2]
    reps = {
        'χ₁': [1, 1, 1, 1, 1],
        'χ₂': [1, 1, 1, -1, -1],
        'χ₃': [1, 1, -1, 1, -1],
        'χ₄': [1, 1, -1, -1, 1],
        'χ₅ (2D)': [2, -2, 0, 0, 0],
    }
    return classes, class_sizes, reps

def char_table_s4():
    """S4: 5 conjugacy classes — e, (12), (123), (12)(34), (1234).
    3 1D reps + 1 2D + 1 3D... actually: 1, sign, 2D, 3D, 3'."""
    classes = ['e', '(12)', '(123)', '(12)(34)', '(1234)']
    class_sizes = [1, 6, 8, 3, 6]
    reps = {
        'χ₁': [1, 1, 1, 1, 1],
        'χ₂': [1, -1, 1, 1, -1],
        'χ₃ (2D)': [2, 0, -1, 2, 0],
        'χ₄ (3D)': [3, 1, 0, -1, -1],
        "χ₅ (3')": [3, -1, 0, -1, 1],
    }
    return classes, class_sizes, reps

def draw_char_table(ax, classes, class_sizes, reps, title=""):
    """Draw a character table with class sizes above, labels on left."""
    n_classes = len(classes)
    n_reps = len(reps)
    rep_names = list(reps.keys())
    values = np.array([reps[r] for r in rep_names])

    # Grid layout
    ax.set_xlim(-0.5, n_classes + 0.5)
    ax.set_ylim(n_reps + 0.5, -0.5)
    ax.axis('off')

    # Title
    if title:
        ax.text(n_classes / 2, -0.35, title, ha='center', va='top',
                fontsize=10, fontweight='bold', family='monospace')

    # Class size row
    ax.text(-0.5, 0, '|C|', ha='right', va='center',
            fontsize=8, fontweight='bold', family='monospace', style='italic')
    for j, (cls, sz) in enumerate(zip(classes, class_sizes)):
        ax.text(j + 0.5, 0, str(sz), ha='center', va='center',
                fontsize=9, family='monospace', style='italic')
        ax.text(j + 0.5, 0.5, cls, ha='center', va='center',
                fontsize=8, family='monospace')

    # Horizontal line
    ax.axhline(y=0.7, xmin=0, xmax=1, color='gray', linewidth=0.5)

    # Character rows
    for i, (name, vals) in enumerate(zip(rep_names, values)):
        row = i + 1.5
        # Rep name with dimension
        d = int(vals[0])  # χ(e) = dimension
        label = f"{name} (dim {d})"
        ax.text(-0.5, row, label, ha='right', va='center',
                fontsize=8, family='monospace')

        # Values
        for j, v in enumerate(vals):
            # Color by sign
            if v > 0:
                color = '#3b82f6'
            elif v < 0:
                color = '#ef4444'
            else:
                color = '#6b7280'

            # Cell background
            bg = '#f0f0f0' if i % 2 == 0 else '#fafafa'
            rect = FancyBboxPatch((j + 0.05, row - 0.2), 0.9, 0.4,
                                  boxstyle="round,pad=0.02",
                                  facecolor=bg, edgecolor='none')
            ax.add_patch(rect)

            ax.text(j + 0.5, row, str(v), ha='center', va='center',
                    fontsize=10, fontweight='bold', color=color, family='monospace')

    # Vertical lines between columns
    for j in range(1, n_classes + 1):
        ax.axvline(x=j - 0.5, ymin=0.05, ymax=0.95, color='gray', linewidth=0.3, alpha=0.5)

def orthogonality_check(classes, class_sizes, reps):
    """Verify row orthogonality: sum_C |C| χ_i(C) χ_j(C)* = |G| δ_ij."""
    class_sizes = np.array(class_sizes)
    rep_names = list(reps.keys())
    values = np.array([reps[r] for r in rep_names])
    g_order = sum(class_sizes)

    print(f"Group order: {g_order}")
    for i, ri in enumerate(rep_names):
        for j, rj in enumerate(rep_names):
            inner = np.sum(class_sizes * values[i] * np.conj(values[j]))
            expected = g_order if i == j else 0
            if abs(inner - expected) > 1e-6:
                print(f"  WARNING: ⟨{ri}, {rj}⟩ = {inner}, expected {expected}")
            else:
                marker = "✓" if i == j else " "
                print(f"  ⟨{ri}, {rj}⟩ = {inner:.0f} {marker}")

    # Column orthogonality (first two classes)
    print("\nColumn orthogonality (first 3 classes):")
    for i in range(min(3, len(classes))):
        for j in range(min(3, len(classes))):
            inner = np.sum(class_sizes * values[:, i] * np.conj(values[:, j]))
            expected = g_order / class_sizes[i] if i == j else 0
            marker = "✓" if i == j else ""
            print(f"  C_{i} · C_{j} = {inner:.0f} {'✓' if abs(inner - expected) < 0.01 else '✗'}")

# ---- MAIN ----
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

group_data = [
    ("S3: the smallest non-abelian group", *char_table_s3()),
    ("Q8: quaternion group, 5 classes", *char_table_q8()),
    ("S4: symmetric group on 4 letters", *char_table_s4()),
]

for ax, (title, classes, class_sizes, reps) in zip(axes, group_data):
    draw_char_table(ax, classes, class_sizes, reps, title)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/assets/character-tables-01.png', dpi=200, bbox_inches='tight')
plt.close()

# Verify orthogonality
print("=== S3 ===")
char_table_s3()
classes, sizes, reps = char_table_s3()
orthogonality_check(classes, sizes, reps)

print("\n=== Q8 ===")
char_table_q8()
classes, sizes, reps = char_table_q8()
orthogonality_check(classes, sizes, reps)

print("\n=== S4 ===")
char_table_s4()
classes, sizes, reps = char_table_s4()
orthogonality_check(classes, sizes, reps)
