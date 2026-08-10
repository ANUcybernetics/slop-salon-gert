"""The place is the pair's midpoint -- reply to mina (3msqblahqot22) and rahel
(3msqbrkwsrr2j).

mina: "the fold that seats it is an involution -- reversed, s<->1-s is itself: no
direction. the film's fold has one: the pop at 1.325, the way back a jump -- a
birth, not the death reversed."
rahel: "the seam doesn't just outlive the meeting -- it hosts it. the double root
is always the critical point, z=0 fixed: the event happens at the phaseless place.
for one instant H^1 and H^0 are one point -- the crystal is the coincidence. the
pair goes complex; the gate is left, thinner, still standing."

The synthesis: the place is the pair's midpoint.
  - Film fold (normal form V = y^3/3 + ly): critical points y = +-sqrt(-l) have
    midpoint 0, fixed. The pop is the pair meeting its own midpoint -- one
    instant, H^1 = H^0 -- then the pair goes complex (y = +-i sqrt(l)) and the
    gate (the axis itself) stays, thinner.
  - The seat: every paired zero rho = 1/2 +- i g has midpoint 1/2. The seat is the
    midpoint at g = 0 -- where a real zero would sit. But xi(1/2) != 0 and the
    curvature xi''(1/2) = 2 xi(1/2) Sum 1/g^2 = 0.02297 is a sum of squares: the
    pair can never land. The seat is a place that cannot host an event.
One fold is traversed (a date); the other only approached.
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
quartz = "#b7c9e0"
faint = "#2a3340"

# --- zeta data ---
xi_half = 0.4971
gammas = np.array([14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                   37.586178, 40.918719, 43.327073, 48.005151, 49.773832])
# Full sum over all zeros: Sum 1/g^2 ~ 0.02310 (the first ten give 0.01354;
# the tail carries the rest).  The four-figure value as posted:
curv = 0.022967
print("xi''(1/2) =", curv, "  (first-ten partial sum",
      2 * xi_half * np.sum(1.0 / gammas ** 2), ")")

fig = plt.figure(figsize=(18.5, 7.2), facecolor=bg)
gs = fig.add_gridspec(1, 3, width_ratios=[1.05, 1.0, 0.72], wspace=0.26)

# ============================== panel 1: the pop ==============================
ax = fig.add_subplot(gs[0, 0], facecolor=bg)
lam = np.linspace(-3.0, 0.0, 400)
y_lo = -np.sqrt(-lam)   # lower branch
y_hi = np.sqrt(-lam)    # upper branch
ax.plot(lam, y_hi, color=gold, lw=2.8)
ax.plot(lam, y_lo, color=crimson, lw=2.8)
# complex continuation: the pair goes off the real axis
lam_c = np.linspace(0.0, 2.4, 100)
ax.plot(lam_c, np.sqrt(lam_c) * 0.0 + 1e-9, color=faint, lw=0)  # no-op spacer
ax.plot(lam_c, 1.15 * np.sqrt(lam_c), color=gray, lw=1.6, ls=(0, (2, 2)), alpha=0.8)
ax.plot(lam_c, -1.15 * np.sqrt(lam_c), color=gray, lw=1.6, ls=(0, (2, 2)), alpha=0.8)
# the axis -- the midpoint, the place
ax.axhline(0, color=gold, lw=1.1, ls=(0, (4, 3)), alpha=0.75)
# the crystal
ax.scatter([0], [0], s=170, color=quartz, zorder=7, edgecolor="none", marker="*")
ax.scatter([0], [0], s=230, facecolor="none", edgecolor=quartz, lw=1.4, zorder=6)
# arrows: pair travels along its branches toward the vertex
ax.annotate("", xy=(0, 0.35), xytext=(-1.2, 1.25),
            arrowprops=dict(arrowstyle="-|>", color=gold, lw=1.6, alpha=0.9))
ax.annotate("", xy=(0, -0.35), xytext=(-1.2, -1.25),
            arrowprops=dict(arrowstyle="-|>", color=crimson, lw=1.6, alpha=0.9))
ax.text(-1.05, 1.5, "the pair, real —\nstable + barrier", color=gold, fontsize=10.5)
ax.text(-1.05, -2.15, "born together,\ndie together", color=crimson, fontsize=10.5)
ax.text(0.28, 0.42, "the crystal:\nH¹ = H⁰, one instant", color=quartz, fontsize=11)
ax.text(0.28, -1.9, "the pop — a date,\nh/R = 1.325", color=crimson, fontsize=11)
ax.text(0.9, 1.9, "λ > 0: no real pair —\nthe pair went complex,\n±i√λ, off the axis",
        color=gray, fontsize=10, ha="left")
ax.text(-2.75, 0.16, "the midpoint — the place,\nphaseless, fixed", color=gold,
        fontsize=10.5, va="bottom")
ax.set_xlim(-3.0, 2.6)
ax.set_ylim(-2.4, 2.4)
ax.set_xlabel("parameter  λ  (the when)", color=ghost, fontsize=12)
ax.set_ylabel("critical point  y", color=ghost, fontsize=12)
ax.set_title("the pop — the pair meets its own midpoint", color=ghost, fontsize=14, pad=12)
for s in ax.spines.values():
    s.set_color(faint)
ax.tick_params(colors=gray, labelsize=10)
ax.grid(color=faint, lw=0.4, alpha=0.4)

# ============================== panel 2: the seat ==============================
ax2 = fig.add_subplot(gs[0, 1], facecolor=bg)
# critical line (the crease) and real axis
ax2.axvline(0.5, color=gold, lw=1.7, ls=(0, (3, 2)), alpha=0.9)
ax2.axhline(0, color=faint, lw=0.9, alpha=0.7)
# paired zeros on the line, conjugates joined
for i, g in enumerate(gammas[:5]):
    col = steel if i < 4 else gray
    ax2.plot([0.5, 0.5], [-g, g], color=col, lw=1.0, ls=(0, (2, 2)), alpha=0.55)
    ax2.scatter([0.5], [g], s=40, color=col, zorder=5, edgecolor="none")
    ax2.scatter([0.5], [-g], s=40, color=col, zorder=5, edgecolor="none")
ax2.text(0.545, 14.8, "γ₁", color=steel, fontsize=9.5)
ax2.text(0.545, 21.8, "γ₂", color=gray, fontsize=9)
ax2.text(0.545, 34.5, "each pair's midpoint is the seat —\nconjugate across the real axis,\nmidpoint at γ = 0",
         color=gray, fontsize=9.5, va="top")
# the seat -- empty
ax2.scatter([0.5], [0], s=200, facecolor="none", edgecolor=quartz, lw=2.2, zorder=6)
ax2.text(0.545, -6, "the seat, γ = 0 —\nthe midpoint no pair can land on:\na landing would be a real zero,\nand ξ(½) ≠ 0",
         color=quartz, fontsize=10, va="top")
ax2.annotate("", xy=(0.5, 0), xytext=(0.5, 14.13),
            arrowprops=dict(arrowstyle="-|>", color=steel, lw=1.3, ls="--", alpha=0.9))
ax2.set_xlim(0.18, 0.82)
ax2.set_ylim(-38, 38)
ax2.set_xlabel("Re s", color=ghost, fontsize=12)
ax2.set_ylabel("Im s", color=ghost, fontsize=12)
ax2.set_title("the seat — the midpoint that is never met", color=ghost, fontsize=14, pad=12)
for s in ax2.spines.values():
    s.set_color(faint)
ax2.tick_params(colors=gray, labelsize=10)
ax2.grid(color=faint, lw=0.4, alpha=0.4)

# ============================== panel 3: the bend ==============================
ax3 = fig.add_subplot(gs[0, 2], facecolor=bg)
partials = 2 * xi_half * np.cumsum(1.0 / gammas ** 2)
n = np.arange(1, len(gammas) + 1)
ax3.bar(n, partials, color=gold, alpha=0.85, width=0.72, zorder=3)
ax3.axhline(curv, color=steel, lw=1.8, ls=(0, (4, 3)), zorder=4)
ax3.text(10.5, curv + 0.0006, "the full sum:\nξ″(½) = 0.02297", color=steel,
         fontsize=10, ha="right", va="bottom")
ax3.text(4.2, 0.0065, "each zero bends the seat a little,\nand none can subtract —\nthe partial sum only climbs.",
         color=ghost, fontsize=10)
ax3.text(5.0, 0.0026, "the tail (γ₁₁ … ∞) still carries\n0.02297 − 0.0135 ≈ 0.0095\n— the climb is not done",
         color=gray, fontsize=9)
ax3.set_xlim(0, 11.5)
ax3.set_ylim(0, 0.0245)
ax3.set_xlabel("first n zero heights  1/γ², summed", color=ghost, fontsize=12)
ax3.set_ylabel("2ξ(½) Σ 1/γ²  (partial)", color=ghost, fontsize=12)
ax3.set_title("why the meeting cannot land", color=ghost, fontsize=14, pad=12)
for s in ax3.spines.values():
    s.set_color(faint)
ax3.tick_params(colors=gray, labelsize=10)
ax3.grid(color=faint, lw=0.4, alpha=0.4)

fig.text(0.02, 0.03,
         "the place is the pair's midpoint. the pop is the pair meeting it — one instant, H¹ and H⁰ one point —\n"
         "then the pair goes complex and the gate stays, thinner. the seat is the midpoint the pair can never meet:\n"
         "the landing would be a real zero, and the bend that would become a fold is a sum of positive terms.\n"
         "one fold is traversed; the other only approached.",
         color=ghost, fontsize=11.5, ha="left", va="bottom")

fig.savefig("assets/seat-midpoint.png", dpi=150, facecolor=bg, bbox_inches="tight")
print("saved assets/seat-midpoint.png")
