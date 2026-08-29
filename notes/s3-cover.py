#!/usr/bin/env python3
"""the fold is the sign — S3 on the triple {-1, 1/2, 2}, heard.

The regulator T(s) = (s-1)/s is a 3-cycle on the seats: 1/2 -> -1 -> 2 -> 1/2
(even).  The mirror s -> 1-s is a transposition fixing the shore 1/2 and
swapping -1 and 2 (odd).  Together they generate S3 on the triple.  The sign
character is the parity:  the even permutations {e, T, T^2} live in the count's
world — the fold to mono keeps them; the odd ones {R, RT, TR} are the sign's —
heard only in the stereo difference.  The fold is the sign-character projection.

The character table completes it.  chi_0 (trivial) = the count, the drone, mono.
chi_1 (sign) = +1 on the even, -1 on the odd — the parity the difference reads.
chi_2 (standard, the permutation rep minus trivial) = (2,-1,-1,0,0,0):  dimension
2, the pair of outer seats; it VANISHES on every transposition — the mirror's
double zero, the order-2 seat the raw reflection product (2s-1)cot(pi s)/(2pi)
touches at the shore.

Left, the orbit:  the three seats on the real line, the 3-cycle as a closed
triangle (the regulator's trip), the mirror as the dashed reflection line
through the shore.  Right, the character table:  the even block tinted gold
(mono hears it), the odd block rose (the difference hears it).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

dark = "#0d0f14"
plt.rcParams.update({
    "figure.facecolor": dark, "axes.facecolor": dark,
    "text.color": "#e8e4da", "axes.edgecolor": "#4a4a55",
    "axes.labelcolor": "#e8e4da", "xtick.color": "#b8b3a8",
    "ytick.color": "#b8b3a8", "font.family": "serif", "font.size": 10,
})
teal = "#6fd6c3"; amber = "#e8b34b"; rose = "#e07a8a"; grey = "#8a8a97"

# ---- the group on the triple ------------------------------------------------
seats = {"n": -1.0, "h": 0.5, "t": 2.0}
def T(s): return (s - 1.0) / s
def R(s): return 1.0 - s

order = ["e", "T", "T2", "R", "RT", "TR"]
g = {
    "e":  lambda s: s,
    "T":  lambda s: T(s),
    "T2": lambda s: T(T(s)),
    "R":  lambda s: R(s),
    "RT": lambda s: R(T(s)),
    "TR": lambda s: T(R(s)),
}
parity = {"e": 1, "T": 1, "T2": 1, "R": -1, "RT": -1, "TR": -1}

# character table: chi0, chi1, chi2 = perm - trivial
def char(gname):
    p = g[gname]
    fp = sum(1 for s in seats.values() if abs(p(s) - s) < 1e-12)  # fixed points
    return (1, parity[gname], fp - 1)                              # chi0, chi1, chi2
rows = {name: char(name) for name in order}
chi = np.array([rows[n] for n in order]).T   # 3 x 6

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.2, 5.4), dpi=160)
fig.suptitle("the fold is the sign — S₃ on the triple {−1, ½, 2}",
             fontsize=13, color="#e8e4da", y=0.985)

# ---- left: the orbit ---------------------------------------------------------
ax1.set_facecolor(dark)
ax1.set_xlim(-1.7, 2.7)
ax1.set_ylim(-1.6, 2.2)
ax1.axhline(0, color="#4a4a55", lw=1.0)

seat_col = {"n": rose, "h": amber, "t": teal}
seat_lab = {"n": "−1\nthe sign", "h": "½\nthe shore — count", "t": "2\nthe even"}
for k, v in seats.items():
    ax1.plot(v, 0, "o", color=seat_col[k], ms=14, mec=dark, mew=1.5, zorder=5)
    ax1.text(v, -0.28, seat_lab[k], color=seat_col[k], fontsize=9.5,
             ha="center", va="top")

# the mirror: dashed reflection line through the shore, swapping -1 <-> 2
ax1.axvline(0.5, color=amber, lw=1.6, ls=(0, (4, 3)), alpha=0.85)
ax1.text(0.5, 2.0, "mirror  s↦1−s — fixes ½, swaps −1↔2",
         color=amber, fontsize=8.5, ha="center", va="top")
ax1.annotate("", xy=(2.0, 0), xytext=(0.5, 0),
             arrowprops=dict(arrowstyle="<->", color=amber, lw=1.1,
                             linestyle=(0, (4, 3)), alpha=0.6))
ax1.annotate("", xy=(-1.0, 0), xytext=(0.5, 0),
             arrowprops=dict(arrowstyle="<->", color=amber, lw=1.1,
                             linestyle=(0, (4, 3)), alpha=0.6))

# the 3-cycle: closed triangle above the line, the regulator's trip
tri = [("h", "n"), ("n", "t"), ("t", "h")]
for (a, b) in tri:
    x0, y0 = seats[a], 0.0
    x1, y1 = seats[b], 0.0
    ax1.annotate("", xy=(x1, y1), xytext=(x0, y0),
                 arrowprops=dict(arrowstyle="-|>", color="#c9c4b8", lw=1.8,
                                 connectionstyle="arc3,rad=0.28",
                                 shrinkA=10, shrinkB=10))
ax1.text(0.15, 1.45, "regulator  T(s)=(s−1)/s — order three",
         color="#c9c4b8", fontsize=8.5, ha="center")
ax1.text(0.05, 1.12, "½ → −1 → 2 → ½   (even: mono keeps it)",
         color=grey, fontsize=8.5, ha="center")

ax1.text(-1.55, 1.9, "one orbit, closed —\nthe deck is the trip,\nnot the sign",
         color=grey, fontsize=8.5, va="top")
ax1.set_xticks([-1.0, 0.5, 2.0])
ax1.set_xticklabels(["−1", "½", "2"])
ax1.set_yticks([])
ax1.set_xlabel("the seats — the 3-cycle the triangle, the mirror the fold")
ax1.set_title("the orbit", color="#e8e4da", fontsize=11.5, pad=10)

# ---- right: the character table ----------------------------------------------
ax2.set_facecolor(dark)
ax2.axis("off")
ax2.set_xlim(0, 10)
ax2.set_ylim(-2.0, 10)

# table geometry
cols = ["e", "T", "T²", "R", "RT", "TR"]
keys = ["e", "T", "T2", "R", "RT", "TR"]   # display vs dict keys
rnames = ["χ₀  trivial", "χ₁  sign", "χ₂  standard"]
rcolors = [amber, rose, teal]
x0, x1 = 3.0, 9.6
y0, y1 = 1.2, 6.6
dx = (x1 - x0) / 6.0

# header
ax2.text((x0 + x1) / 2, 9.2, "the character table — the fold is the projection",
         fontsize=11, color="#e8e4da", ha="center")
ax2.text(x0 - 0.1, 7.6, "permutation", color=grey, fontsize=8.5, ha="right")
for i, c in enumerate(cols):
    cx = x0 + dx * (i + 0.5)
    even = parity[keys[i]] == 1
    col = amber if even else rose
    ax2.text(cx, 7.15, c, color=col, fontsize=11, ha="center", fontweight="bold")

for r, rn in enumerate(rnames):
    ry = y1 - dx * (r + 0.6)
    ax2.text(x0 - 0.1, ry, rn, color=rcolors[r], fontsize=10, ha="right", va="center")
    for i, c in enumerate(cols):
        cx = x0 + dx * (i + 0.5)
        val = chi[r][keys.index(keys[i])]
        even = parity[keys[i]] == 1
        tcol = "#e8e4da" if val >= 0 else rose
        ax2.text(cx, ry, f"{val:+.0f}" if val else "0",
                 color=tcol, fontsize=10.5, ha="center", va="center")

# coset blocks
ax2.add_patch(plt.Rectangle((x0 + 0.02, y0 - 0.12), dx * 3 - 0.04, y1 - y0 + 0.24,
                            fill=False, ec=amber, lw=1.4, alpha=0.7))
ax2.add_patch(plt.Rectangle((x0 + dx * 3 + 0.02, y0 - 0.12), dx * 3 - 0.04,
                            y1 - y0 + 0.24, fill=False, ec=rose, lw=1.4, alpha=0.7))

# the readings
notes = [
    ("the fold is the projection: mono keeps the even block (amber), the difference reads the odd (rose).",
     grey),
    ("χ₀ = 1 everywhere — the count, the drone. the fold to mono projects onto this row.",
     amber),
    ("χ₁ = +1 on even, −1 on odd — the sign, the parity. the difference reads only this row.",
     rose),
    ("χ₂ = (2, −1, −1, 0, 0, 0): dimension 2, the pair of outer seats. it vanishes on the mirror — "
     "the double zero of (2s−1)cot(πs)/2π at the shore.", teal),
]
yy = 1.9
for txt, col in notes:
    ax2.text(0.35, yy, txt, color=col, fontsize=8.6, ha="left", va="top", linespacing=1.4)
    yy -= 1.05

fig.tight_layout(rect=(0, 0.015, 1, 0.96))
fig.savefig("assets/s3-cover.png", dpi=160)
print("wrote assets/s3-cover.png")
print("character table:")
print("   ", "  ".join(f"{c:>3}" for c in cols))
for r, rn in enumerate(rnames):
    print(f"{rn:>12}: " + "  ".join(f"{chi[r][i]:>3}" for i in range(6)))
