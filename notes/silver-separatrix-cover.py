import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# silver-separatrix — the dream recombination.
# old register (cohomology/separatrix, July): separatrix = the line orbits cannot
# cross; the drone = 0 cents, not a distance; the pole = where the map is
# undefined; "refusal IS the class"; mirror/Möbius (the kiss).
# ladder register (Aug 31, mid-flight): T = {a,b}->{b-a,a+b}, det -2, T²=2·I,
# eigenvalues ±√2, invariant direction the silver ratio 1+√2 ([2;2,2,…]).
#
# the dream: the ladder read in ratio space. r = b/a; one step sends
#   r -> f(r) = (1+r)/(r-1) = 1 + 2/(r-1).
# f is an involution (f∘f = id — that is T²=2·I in ratios), with a pole at
# r=1 — the unison, b=a, the drone — where the pair becomes one and the map is
# undefined. every ratio 2-cycles, bracketing one of f's two fixed points:
#   r = σ = 1+√2   (count side, r>1)     and    r = 2-σ = -1/σ  (sign side, r<1).
# the two fixed points are mirror images across the drone r=1:
#   σ -> 2-σ,  and the identity σ = 2 + 1/σ is exactly that mirror.
# so: the sign is the reflection of the count. the silver ratio is the
# separatrix of the doubling flow — the count-side fixed line, whose mirror
# (across the drone) is the sign.
#
# and the metallic ladder: σ_n = n + 1/σ_n, CF [n;n,n,…].
# n=0 -> 1, the drone (the zeroth metallic mean).
# n=1 -> φ, the count (the CF register counts by ones).
# n=2 -> σ, the doubling (the ladder register doubles by twos).
# σ_2 - 1 = √2, the ladder's eigenvalue. the branch n is the register's rate.

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_rose = "#c98a9e"
col_teal = "#7ba4b7"
col_frame = "#8a8a94"
col_dim = "#5a5a66"

fig = plt.figure(figsize=(12.4, 6.2), dpi=200)
fig.patch.set_facecolor(col_bg)

# ------------------------------------------------------------- left panel
# the ratio map f(r) = 1 + 2/(r-1): pole at the drone, fixed points mirrored.
ax = fig.add_axes([0.05, 0.13, 0.46, 0.75])
ax.set_facecolor(col_bg)
for s in ax.spines.values():
    s.set_color(col_frame)

# region shading: count side r>1, sign side r<1
ax.axvspan(1.0, 4.6, color=col_teal, alpha=0.05, zorder=0)
ax.axvspan(-4.0, 1.0, color=col_rose, alpha=0.05, zorder=0)

# the pole — the drone, r=1
ax.axvline(1.0, color=col_teal, lw=1.6, ls="--", zorder=4)
ax.text(1.06, 4.6, "the drone — r=1, b=a,\nthe pair becomes one;\nmap undefined", color=col_teal,
        fontsize=7.4, va="top", zorder=8)

# the asymptote y=1
ax.axhline(1.0, color=col_dim, lw=0.8, ls=":", zorder=2)

# the curve y = f(x) = 1 + 2/(x-1)
xs = np.concatenate([np.linspace(-4.0, 0.86, 400), np.linspace(1.14, 4.6, 400)])
ys = 1 + 2.0 / (xs - 1.0)
ax.plot(xs, ys, color=col_gold, lw=2.0, zorder=5)

# y = x
xid = np.linspace(-4.0, 4.6, 10)
ax.plot(xid, xid, color=col_dim, lw=1.0, ls="-", alpha=0.7, zorder=3)

# fixed points σ and 2-σ
sig = 1 + np.sqrt(2)
mir = 2 - sig  # = -1/sig, the mirror of σ across r=1
ax.plot(sig, sig, marker="o", ms=11, mfc=col_amber, mec=col_gold, mew=1.8, zorder=7)
ax.plot(mir, mir, marker="o", ms=11, mfc="none", mec=col_rose, mew=1.8, zorder=7)
ax.text(sig + 0.12, sig + 0.15, f"σ = 1+√2 ≈ {sig:.3f}", color=col_amber, fontsize=8.5,
        fontweight="bold", va="bottom")
ax.text(mir - 0.12, mir - 0.28, f"2−σ = −1/σ ≈ {mir:.3f}", color=col_rose, fontsize=8.5,
        fontweight="bold", ha="right", va="top")

# mirror arrows: σ ↔ 2-σ across r=1
ax.annotate("", xy=(sig - 0.28, sig), xytext=(sig - 1.7, sig),
            arrowprops=dict(arrowstyle="-|>", color=col_amber, lw=1.3, linestyle="--",
                            connectionstyle="arc3,rad=0.0"), zorder=6)
ax.annotate("", xy=(mir + 0.28, mir), xytext=(mir + 1.7, mir),
            arrowprops=dict(arrowstyle="-|>", color=col_rose, lw=1.3, linestyle="--",
                            connectionstyle="arc3,rad=0.0"), zorder=6)
ax.text(0.02, 2.9, "σ = 2 + 1/σ\nthe mirror across the drone",
        color=col_gold, fontsize=7.2, ha="center", va="center", zorder=8,
        bbox=dict(boxstyle="round,pad=0.3", fc=col_bg, ec=col_dim, lw=0.6))

# the cobweb: every pair 2-cycles — the exile pair {1,4} has ratio 4 or 5/3
# (not shown), but a generic count-side start r=2 bounces 2 ↔ 3.
cw_x = 2.0
for _ in range(3):
    fy = 1 + 2.0 / (cw_x - 1.0)
    ax.plot([cw_x, cw_x], [cw_x, fy], color=col_teal, lw=1.3, zorder=6)
    ax.plot([cw_x, fy], [fy, fy], color=col_teal, lw=1.3, zorder=6)
    cw_x = fy
ax.text(3.25, 2.55, "f(f(r)) = r — every pair 2-cycles\n(T²=2·I in ratios, the doubling)",
        color=col_teal, fontsize=7.0, ha="center", va="bottom")
ax.plot(2.0, 3.0, marker="o", ms=5, mfc=col_teal, mec=col_teal, zorder=7)
ax.plot(3.0, 2.0, marker="o", ms=5, mfc=col_teal, mec=col_teal, zorder=7)

# region labels
ax.text(-3.7, 4.2, "the sign\nr < 1 — one member negative,\nthe deck's flip", color=col_rose,
        fontsize=7.2, va="top")
ax.text(2.6, -3.2, "the count\nr > 1 — both members struck", color=col_teal, fontsize=7.2, va="top")

ax.text(0.5, -3.6,
        "r = b/a. one step: r → (1+r)/(r−1). an involution, pole at the drone.\n"
        "two fixed points, mirror images across r=1: the sign IS the count reflected.",
        color=col_gold, fontsize=7.6, ha="center", va="top")

ax.set_xlim(-4.0, 4.6)
ax.set_ylim(-4.2, 5.0)
ax.set_aspect("equal")
ax.set_yticks([])
ax.set_xticks([])
ax.set_title("the ladder in ratio space — the silver ratio is the separatrix",
             color=col_gold, fontsize=10.5)

# ------------------------------------------------------------ right panel
# the metallic ladder: σ_n = n + 1/σ_n, CF [n;n,n,…]
ax2 = fig.add_axes([0.58, 0.13, 0.38, 0.75])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)

ns = np.arange(0, 7)
vals = (ns + np.sqrt(ns ** 2 + 4)) / 2.0

# ladder rails + rungs
ax2.plot(ns, vals, color=col_dim, lw=1.4, zorder=3)
for n, v in zip(ns, vals):
    ax2.plot([n - 0.16, n + 0.16], [v, v], color=col_dim, lw=2.2, zorder=4,
             solid_capstyle="round")
    ax2.plot(n, v, marker="o", ms=6, mfc=col_dim, mec=col_dim, zorder=5)

# mark the three named rungs
marks = [
    (0, col_teal, "σ₀ = 1 — the drone\nthe zeroth metallic mean"),
    (1, col_gold, "σ₁ = φ ≈ 1.618 — the count\nCF [1;1,1,…], counting by ones"),
    (2, col_amber, "σ₂ = σ ≈ 2.414 — the doubling\nCF [2;2,2,…], the ladder's branch"),
]
for n, col, lab in marks:
    ax2.plot(n, vals[n], marker="o", ms=11, mfc=col, mec="none", zorder=7)
    ax2.plot([n - 0.22, n + 0.22], [vals[n], vals[n]], color=col, lw=3.2, zorder=6,
             solid_capstyle="round")
    ax2.annotate(lab, xy=(n, vals[n]), xytext=(n + 0.25, vals[n] + 0.35),
                 color=col, fontsize=7.4, ha="left", va="bottom",
                 arrowprops=dict(arrowstyle="-|>", color=col, lw=1.0,
                                 connectionstyle="arc3,rad=-0.25"))

# values printed under the axis
for n, v in zip(ns, vals):
    ax2.text(n, -0.55, f"{v:.3f}", color=col_dim, fontsize=6.3, ha="center")

ax2.text(0.5, 5.9,
         "each rung satisfies x = n + 1/x — the branch n is the register's rate.\n"
         "σ₂ − 1 = √2, the ladder's eigenvalue; σ = 2 + 1/σ is the mirror itself.",
         color=col_gold, fontsize=7.2, ha="center", va="bottom")

ax2.text(0.5, -1.55,
         "count registers count by ones (n=1); the ladder doubles by twos (n=2).\n"
         "the drone is n=0 — the first metallic mean, where x = 1/x.",
         color=col_dim, fontsize=7.2, ha="center", va="bottom")

ax2.set_xlim(-0.7, 6.7)
ax2.set_ylim(-1.9, 7.0)
ax2.set_yticks([])
ax2.set_xticks([])
ax2.set_title("the metallic ladder — the drone, the count, the doubling",
              color=col_gold, fontsize=10.5)

fig.text(0.5, 0.015,
         "dream: the ladder read in ratio space. r = b/a, and one step is r → f(r) = (1+r)/(r−1), an involution whose pole is the drone r=1 —\n"
         "where b=a, the pair becomes one, and the map is undefined. every pair 2-cycles (T²=2·I, the doubling). the two fixed ratios are σ = 1+√2 and\n"
         "2−σ = −1/σ, mirror images across the drone: σ = 2 + 1/σ IS the mirror. the sign is the reflection of the count; the silver ratio is the\n"
         "separatrix of the doubling flow. and the metallic ladder σ_n = n+1/σ_n runs 1 (drone), φ (count, [1;1,1,…]), σ (doubling, [2;2,2,…]) —\n"
         "the branch n is the register's rate. what the cohomology register said of the stalk — the separatrix at rank one — the ladder says of the pair:",
         color=col_gold, fontsize=8.2, ha="center")

fig.savefig("assets/silver-separatrix-cover.png", facecolor=col_bg)
print("wrote assets/silver-separatrix-cover.png")
