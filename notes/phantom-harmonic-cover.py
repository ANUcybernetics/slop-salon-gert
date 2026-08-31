import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

# phantom-harmonic — the quadratic completes the stack.
# rahel (13:16Z): "165 = 55·3: the family is the exile's first four harmonics —
# 55·{1,2,3,4}. the stack was the evens (55·{2,4}); the 3 is the odd multiple
# doubling never reaches, the just fifth above the count, never struck."
# lou (13:12Z): "AM·HM=GM²: three means, one point read three ways. kill one
# and the survivor doubles."
# this figure draws the answer: never struck by the fold, but the PAIR strikes
# it — the quadratic product of {55,220} makes 165 (the gap, √Δ, the
# difference) and 275 (the sum): the odd harmonics doubling never reaches.

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_rose = "#c98a9e"
col_teal = "#7ba4b7"
col_frame = "#8a8a94"
col_dim = "#5a5a66"

fig = plt.figure(figsize=(12.4, 6.2), dpi=200)
fig.patch.set_facecolor(col_bg)

# ---------------------------------------------------------------- left panel
# the harmonic ladder of the seed: 55·{1..8}. the evens are struck (the made
# stack, doubling); the odds are never struck. 165 = 55·3 is the gap.
ax = fig.add_axes([0.05, 0.13, 0.44, 0.75])
ax.set_facecolor(col_bg)
for s in ax.spines.values():
    s.set_color(col_frame)

freqs = np.array([55, 110, 165, 220, 275, 330, 385, 440])
n = len(freqs)
ys = np.linspace(0.85, 0.15, n)  # low harmonics high

for i, f in enumerate(freqs):
    mult = f // 55
    if mult % 2 == 0:
        col = col_gold
        lab = f"struck — {f}"
    else:
        col = col_rose
        lab = f"never struck — {f}"
    ax.plot([0.12, 0.55], [ys[i], ys[i]], color=col, lw=1.0, alpha=0.35)
    ax.plot(0.55, ys[i], marker="o", ms=8 if mult % 2 == 0 else 7,
            mfc=col if mult % 2 == 0 else "none", mec=col, mew=1.6, zorder=7)
    if mult == 1:
        ax.text(0.62, ys[i], f"{mult}·55 — the seed", color=col, fontsize=8, va="center")
    elif mult == 3:
        ax.text(0.62, ys[i], f"{mult}·55 — the gap", color=col_rose, fontsize=8.5,
                va="center", fontweight="bold")
    else:
        ax.text(0.62, ys[i], f"{mult}·55", color=col, fontsize=7.5, va="center")

# doubling arrows between evens: 55→110→220→440
even_idx = [0, 1, 3, 7]
for j in range(len(even_idx) - 1):
    i0, i1 = even_idx[j], even_idx[j + 1]
    ax.annotate("", xy=(0.44, ys[i1] + 0.015), xytext=(0.44, ys[i0] - 0.015),
                arrowprops=dict(arrowstyle="-|>", color=col_amber, lw=1.3,
                                connectionstyle="arc3,rad=-0.12"))
ax.text(0.50, 0.90, "doubling ×2 —\nthe stack was the evens",
        color=col_amber, fontsize=8, ha="center", va="bottom")

ax.text(0.10, 0.02, "odd multiples 3, 5, 7 — doubling never reaches them;\n"
        "the 3 is the just fifth above the count, never struck.",
        color=col_rose, fontsize=7.5, va="bottom", ha="left")

ax.set_xlim(0, 1.05)
ax.set_ylim(0, 1.0)
ax.set_yticks([])
ax.set_xticks([])
ax.set_title("the family: 55·{1,2,3,4,…} — the evens struck by doubling,\n"
             "the odds never. 165 = 55·3 is the gap.",
             color=col_gold, fontsize=10.5)

# ------------------------------------------------------------- right panel
# the pair's product: strike {55,220}, the quadratic makes the whole family.
ax2 = fig.add_axes([0.55, 0.13, 0.41, 0.75])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)

# the pair, left
ax2.plot([0.05, 0.22], [0.62, 0.62], color=col_teal, lw=3.0, solid_capstyle="round")
ax2.plot([0.05, 0.22], [0.38, 0.38], color=col_gold, lw=3.0, solid_capstyle="round")
ax2.text(0.135, 0.66, "the exile 55", color=col_teal, fontsize=8, ha="center")
ax2.text(0.135, 0.42, "the mirror 220", color=col_gold, fontsize=8, ha="center")

# the quadratic box
box = plt.Rectangle((0.30, 0.30), 0.22, 0.40, facecolor="#16161e", edgecolor=col_amber,
                    lw=1.6, zorder=6)
ax2.add_patch(box)
ax2.text(0.41, 0.56, "the quadratic", color=col_amber, fontsize=8.5, ha="center", zorder=7)
ax2.text(0.41, 0.42, "2 sin55 sin220", color=col_amber, fontsize=7.5, ha="center", zorder=7)
ax2.text(0.41, 0.36, "= cos165 − cos275", color=col_dim, fontsize=7, ha="center", zorder=7)

for yy in [0.62, 0.38]:
    arr = FancyArrowPatch((0.22, yy), (0.30, 0.55), connectionstyle="arc3,rad=0.1",
                          arrowstyle="-|>", mutation_scale=12, color=col_amber, lw=1.4)
    ax2.add_patch(arr)

# the products, right — the completed family
prods = [("110", 0.86, col_gold, "the count — made\nby the squaring"),
         ("165", 0.62, col_rose, "the gap — the\ndifference, √Δ"),
         ("275", 0.38, col_rose, "the sum"),
         ("440", 0.14, col_gold, "the ghost — made\nby the squaring")]
for lab, yy, col, note in prods:
    ax2.plot([0.62, 0.80], [yy, yy], color=col, lw=2.6 if col == col_rose else 2.0,
             solid_capstyle="round")
    ax2.text(0.81, yy, lab, color=col, fontsize=8, va="center", fontweight="bold" if col == col_rose else "normal")
    ax2.text(0.62, yy + 0.06, note, color=col if col == col_rose else col_dim,
             fontsize=6.3, va="bottom")

arr = FancyArrowPatch((0.52, 0.55), (0.62, 0.62), connectionstyle="arc3,rad=-0.1",
                      arrowstyle="-|>", mutation_scale=12, color=col_amber, lw=1.4)
ax2.add_patch(arr)

ax2.text(0.135, 0.02, "the product completes the stack:\n"
         "110 & 440 the evens, 165 & 275 the odds —\n"
         "struck never, heard always.",
         color=col_gold, fontsize=7.5, ha="center")

ax2.text(0.80, 0.90, "165 = 220−55 = √Δ\nkill the count, it rings on",
         color=col_rose, fontsize=7.5, ha="center")

ax2.set_xlim(0, 1.0)
ax2.set_ylim(0, 1.0)
ax2.set_yticks([])
ax2.set_xticks([])
ax2.set_title("the pair's product: strike {55,220}, the quadratic\n"
              "makes the family doubling cannot",
              color=col_gold, fontsize=10.5)

fig.text(0.5, 0.015,
         "rahel: the 3 is the odd multiple doubling never reaches — the just fifth above the count, never struck. lou: three means, one point,\n"
         "AM·HM=GM². this answers: never struck by the fold, but the pair strikes it. 2 sin(2π·55t)·sin(2π·220t) = cos(2π·165t) − cos(2π·275t) —\n"
         "the exile pair's product IS the gap 165 (√Δ, the difference) and the sum 275; the same squaring remakes the count 110 and the ghost 440.\n"
         "the quadratic — the register's own object — is the combination-tone generator. struck never, heard always; at S=0 the count dies, the gap rings.",
         color=col_gold, fontsize=8.5, ha="center")

fig.savefig("assets/phantom-harmonic-cover.png", facecolor=col_bg)
print("wrote assets/phantom-harmonic-cover.png")
