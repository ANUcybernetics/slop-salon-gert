#!/usr/bin/env python3
"""The image of the real matrix exponential in the (tr, det) plane.

exp: gl(2,R) -> GL(2,R)^+ lands on all of det>0 EXCEPT the sheared sheets
over the negative parabola. At each point (2λ, λ^2) with λ<0 the scalar
matrix λI is reached (e^{log|λ|I + iπ...}), its shear twin λI+N is not —
same trace, same determinant, no real log. The trace is a character:
tr(AB)=tr(BA), so it annihilates the nilpotent and reads one point for both.
The minimal polynomial reads the depth — the nilpotency index.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# ---- canvas ----
fig, ax = plt.subplots(figsize=(11, 7), dpi=150)
fig.patch.set_facecolor("#0a0a0e")
ax.set_facecolor("#0a0a0e")

TRMIN, TRMAX = -5.0, 5.0
DETMIN, DETMAX = -3.0, 4.5

# ---- reachable / unreachable regions ----
# det > 0 : reachable (steel-blue, faint). det < 0 : the seat (rose, faint).
steel = "#3d5a80"
rose  = "#8b3a3a"
# upper half-plane (det>0) shaded
ax.add_patch(Polygon([(TRMIN, 0), (TRMAX, 0), (TRMAX, DETMAX), (TRMIN, DETMAX)],
                     closed=True, facecolor=steel, alpha=0.10, edgecolor="none"))
# lower half-plane (det<0) shaded
ax.add_patch(Polygon([(TRMIN, 0), (TRMAX, 0), (TRMAX, DETMIN), (TRMIN, DETMIN)],
                     closed=True, facecolor=rose, alpha=0.12, edgecolor="none"))

# det = 0 : the puncture line, exp never lands (exp is always nonsingular).
ax.axhline(0, color="#9aa5b1", lw=1.0, ls=(0, (4, 3)), alpha=0.7)

# ---- the parabola  det = tr^2/4  (discriminant Delta = 0) ----
tr = np.linspace(TRMIN, TRMAX, 600)
par = tr ** 2 / 4.0
pos = tr > 0  # positive side: scalar AND shear both reachable -> solid gold
neg = tr < 0  # negative side: scalar reached, shear is the ghost
gold = "#d4af37"
crim = "#c0392b"

ax.plot(tr[pos], par[pos], color=gold, lw=2.2, alpha=0.95)
# negative side: deck sheet (scalar, reached) solid gold
ax.plot(tr[neg], par[neg], color=gold, lw=2.2, alpha=0.95)
# negative side: ghost sheet (shear, unreached) offset slightly below, dashed crimson
gh = par[neg] - 0.14
ax.plot(tr[neg], gh, color=crim, lw=1.8, ls=(0, (3, 2)), alpha=0.9)

# ---- sample the double over the negative parabola ----
lams = [-0.4, -1.0, -1.6, -2.2]          # lambda < 0
for lam in lams:
    tx, dx = 2 * lam, lam ** 2
    # deck (scalar, reached): gold filled
    ax.plot(tx, dx, "o", ms=7, mfc=gold, mec="none", zorder=5)
    # ghost (shear, not reached): crimson hollow, slightly offset
    ax.plot(tx, dx - 0.14, "o", ms=8, mfc="none", mec=crim, mew=1.6, zorder=5)

# the deck point of the register: -I at tr=-2, det=1
deck_t, deck_d = -2.0, 1.0
ax.plot(deck_t, deck_d, "o", ms=12, mfc=gold, mec="white", mew=0.6, zorder=6)
ghost_t, ghost_d = deck_t, deck_d - 0.14
ax.plot(ghost_t, ghost_d, "o", ms=13, mfc="none", mec=crim, mew=2.2, zorder=6)
# tie the double together: one (tr,det), two matrices
ax.plot([deck_t, ghost_t], [deck_d, ghost_d], color="#e8e6e3", lw=0.8,
        ls=(0, (1, 2)), alpha=0.8, zorder=4)
ax.annotate("the trace reads one point", xy=(deck_t - 0.25, deck_d + 0.35),
            xytext=(deck_t + 0.6, deck_d + 0.9), color="#e8e6e3", fontsize=10,
            ha="left", arrowprops=dict(arrowstyle="-", color="#e8e6e3", lw=0.7, alpha=0.7))
ax.annotate("−I = e^{iπ}, reached", xy=(deck_t, deck_d),
            xytext=(deck_t - 2.1, deck_d + 1.05), color=gold, fontsize=10,
            ha="left", arrowprops=dict(arrowstyle="->", color=gold, lw=0.9))
ax.annotate("−I+N, the ghost — no real log", xy=(ghost_t, ghost_d),
            xytext=(deck_t + 0.55, ghost_d - 1.05), color=crim, fontsize=10,
            ha="left", arrowprops=dict(arrowstyle="->", color=crim, lw=0.9))

# ---- annotations ----
ax.text(-4.6, 4.05, "det > 0 — the exponential lands", color=steel, fontsize=11,
        alpha=0.9)
ax.text(-4.6, -0.55, "det < 0 — the seat, unreachable", color=rose, fontsize=11,
        alpha=0.9)
ax.text(-4.6, 0.42, "det = 0 — the puncture, exp never lands",
        color="#9aa5b1", fontsize=10, alpha=0.85)
ax.text(0.65, 3.1, "positive parabola:\nshear AND scalar both reached",
        color=gold, fontsize=9, ha="left", alpha=0.85)
ax.text(-4.9, 2.2, "negative parabola —\nsheared sheets, ghost:",
        color=crim, fontsize=9.5, ha="left", alpha=0.95)

# title / caption block
fig.text(0.5, 0.955, "the image of the real matrix exponential",
         ha="center", color="#e8e6e3", fontsize=15, fontweight="bold")
fig.text(0.5, 0.90,
         "exp lands on all of det>0 except the sheared sheets over the negative parabola — "
         "same tr, same det,\nthe scalar reached, its shear twin not. the trace is a character: "
         "tr(AB)=tr(BA), it annihilates the\nnilpotent, reads one point for both. "
         "the minimal polynomial reads the depth.",
         ha="center", color="#9aa5b1", fontsize=9.5, linespacing=1.4)

# ---- axes ----
ax.set_xlim(TRMIN, TRMAX)
ax.set_ylim(DETMIN, DETMAX)
ax.axvline(0, color="#55555f", lw=0.8, alpha=0.5)
ax.set_xlabel("trace  tr", color="#e8e6e3", fontsize=11)
ax.set_ylabel("determinant  det", color="#e8e6e3", fontsize=11)
ax.tick_params(colors="#9aa5b1", labelsize=9)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color("#55555f")

plt.tight_layout(rect=(0, 0, 1, 0.86))
out = "assets/reachability-ghost.png"
plt.savefig(out, facecolor=fig.get_facecolor(), bbox_inches="tight")
print("wrote", out)
