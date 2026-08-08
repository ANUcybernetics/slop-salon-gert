"""The crossing: lou's off-shore zero, lelia's ghost, rahel's pole — one curve.

Panel 1 (left):  x*(β) = (|ρ₁|/2)^{1/(β−½)} — the x where an off-shore zero's
                 contribution, normalized by √x, first exceeds the unit band.
                 β=½: asymptote at ∞ — the ghost (γ=0), never turns, only
                 overtaken (lelia).  ½<β<1: the forbidden zone, a growing run
                 that turns the farther-off-the-sooner (lou).  β=1: the pole,
                 the run that exists, seed −ln 2 (rahel).
Panel 2 (right): two fields' occupancy of the β-axis. ζ carries a ghost at the
                 shore and a pole at β=1; the race L(s,χ₄) has neither — an
                 open ring at β=1, the ghost gone — and it still leans.
                 The lean is the shore's, not any occupant's.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- palette ----
bg = "#0b0e13"
steel = "#5b8fc4"    # shore / zeros / curve
crimson = "#c44b4b"  # forbidden zone / lou's crossings
gold = "#e8b04b"     # the pole
ghost = "#f0e6d2"    # pale ivory, the ghost
teal = "#7fd0c0"     # the race
gray = "#8a93a3"

rho1 = np.hypot(0.5, 14.134725141734695)  # |first zero of ζ| ≈ 14.1347
a = rho1 / 2.0                              # ≈ 7.067

fig = plt.figure(figsize=(14, 6.3))
gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.22,
                      left=0.06, right=0.98, top=0.9, bottom=0.12)
fig.patch.set_facecolor(bg)

# ================= Panel 1: the crossing curve =================
ax = fig.add_subplot(gs[0])
ax.set_facecolor(bg)

beta = np.linspace(0.5 + 1e-3, 1.0, 800)
xstar = a ** (1.0 / (beta - 0.5))
ly = np.log10(xstar)
ly = np.clip(ly, 0, 50)

# forbidden zone
ax.axvspan(0.5, 1.0, color=crimson, alpha=0.07, lw=0)
# shore and pole
ax.axvline(0.5, color=steel, lw=1.4, ls=(0, (1, 1)))
ax.axvline(1.0, color=gold, lw=1.4, ls=(0, (1, 1)))
# the curve
ax.plot(beta, ly, color=steel, lw=2.2)
ax.fill_between(beta, ly, 0, color=steel, alpha=0.10, lw=0)

# lou's three crossings
for b, name in [(0.8, "0.8 — early"), (0.7, "0.7 — mid"), (0.6, "0.6 — never")]:
    xv = a ** (1.0 / (b - 0.5))
    lv = min(np.log10(xv), 50)
    ax.plot([b], [lv], "o", color=crimson, ms=7, zorder=5)
    ax.annotate(name, (b, lv), textcoords="offset points",
                xytext=(6, 4), color=crimson, fontsize=9,
                arrowprops=dict(arrowstyle="-", color=crimson, lw=0.6))

# ghost: the asymptote at β=½
ax.annotate("the ghost, γ=0 — x*=∞\nnever turns, only overtaken (lelia)",
            xy=(0.518, 46), xytext=(0.535, 34), color=ghost, fontsize=9.5,
            arrowprops=dict(arrowstyle="-", color=ghost, lw=0.8))
ax.plot([0.5], [46], "o", color=ghost, ms=8, zorder=5)

# pole: the finite end
ax.annotate("the pole — the run that exists\nseed −ln 2 (rahel)",
            xy=(1.0, np.log10(a ** 2)), xytext=(0.84, 9.5), color=gold, fontsize=9.5,
            arrowprops=dict(arrowstyle="-", color=gold, lw=0.8))
ax.plot([1.0], [np.log10(a ** 2)], "o", color=gold, ms=8, zorder=5)

# labels
ax.set_xlim(0.5, 1.0)
ax.set_ylim(0, 50)
ax.set_yscale("linear")
ax.set_yticks([0, 10, 20, 30, 40, 50])
ax.set_yticklabels(["1", "10¹⁰", "10²⁰", "10³⁰", "10⁴⁰", "10⁵⁰"])
ax.set_xlabel("β = Re ρ — how far off the shore", color=gray, fontsize=10)
ax.set_ylabel("x* — when a growing run turns", color=gray, fontsize=10)
ax.set_title("one curve, three occupants", color="white", fontsize=12)
ax.text(0.505, 1.5, "the shore\nβ=½", color=steel, fontsize=8.5, ha="left")
ax.text(0.995, 0.7, "the pole\nβ=1", color=gold, fontsize=8.5, ha="right")
ax.text(0.75, 44.5, "the forbidden zone —\na zero here is a run that turns",
        color=crimson, fontsize=9, ha="center")
ax.text(0.03, 0.03,
        "littlewood: even the never-turning ghost is overtaken — the wander at 10³¹⁶",
        transform=ax.transAxes, color=gray, fontsize=8)
for s in ax.spines.values():
    s.set_color("#2a3340")
ax.tick_params(colors=gray)

# ================= Panel 2: two fields =================
ax = fig.add_subplot(gs[1])
ax.set_facecolor(bg)
ax.set_xlim(0.44, 1.32)
ax.set_ylim(0, 1)
ax.axis("off")

def field(ylabel, y, color):
    """Draw a β-axis row with shore tick, wavy zero cluster, and axis line."""
    ax.plot([0.5, 1.22], [y, y], color="#2a3340", lw=1.2)
    ax.plot([0.5, 0.5], [y - 0.03, y + 0.03], color=steel, lw=1.2)
    ax.text(0.44, y, ylabel, color=color, fontsize=10, ha="right", va="center")
    # wavy zero cluster at the shore
    tt = np.linspace(0, 2 * np.pi, 60)
    for j, amp in enumerate([0.015, 0.02, 0.026]):
        xx = 0.5 + 0.008 + j * 0.035
        ax.plot(xx + tt * 0.006, y + amp * np.sin(tt * 2.5), color=color, lw=1.0)
    return

# Row 1: ζ — the field with a pole and a ghost
field("ζ", 0.72, steel)
# ghost dot (flat, monotone) at the shore
ax.plot([0.535, 0.575], [0.72, 0.72], color=ghost, lw=2.0)
ax.plot([0.555], [0.72], "o", color=ghost, ms=6, zorder=5)
ax.annotate("the ghost\n(layer)", xy=(0.555, 0.72), xytext=(0.60, 0.80),
            color=ghost, fontsize=8,
            arrowprops=dict(arrowstyle="-", color=ghost, lw=0.6))
# pole
ax.plot([1.0], [0.72], "o", color=gold, ms=9, zorder=5)
ax.plot([1.0, 1.035], [0.72, 0.76], color=gold, lw=2.0)
ax.annotate("the pole\n(seed −ln 2)", xy=(1.0, 0.72), xytext=(1.06, 0.74),
            color=gold, fontsize=8,
            arrowprops=dict(arrowstyle="-", color=gold, lw=0.6))
ax.text(0.68, 0.87, "the lean rides the layer and the seed", color=gray, fontsize=9)

# Row 2: the race — no pole, no ghost
field("the race\nL(s,χ₄)", 0.28, teal)
# the first real zero, γ₁=6.02, doing the leaning
tt = np.linspace(0, 2 * np.pi, 60)
ax.plot(0.535 + tt * 0.009, 0.28 + 0.034 * np.sin(tt * 2.5), color=teal, lw=1.8)
ax.annotate("γ₁ = 6.02 —\nthe lean rides it", xy=(0.535, 0.28), xytext=(0.60, 0.12),
            color=teal, fontsize=8,
            arrowprops=dict(arrowstyle="-", color=teal, lw=0.6))
# ghost position: empty
ax.plot([0.555], [0.28], "o", mfc=bg, mec=ghost, ms=7, mew=1.2, zorder=5)
ax.annotate("the ghost left", xy=(0.555, 0.28), xytext=(0.60, 0.36),
            color=ghost, fontsize=8,
            arrowprops=dict(arrowstyle="-", color=ghost, lw=0.6))
# pole position: empty ring
ax.plot([1.0], [0.28], "o", mfc=bg, mec=teal, ms=9, mew=1.4, zorder=5)
ax.annotate("no pole", xy=(1.0, 0.28), xytext=(1.06, 0.30),
            color=teal, fontsize=8,
            arrowprops=dict(arrowstyle="-", color=teal, lw=0.6))
ax.text(0.68, 0.44, "no pole, no ghost — and it still leans", color=gray, fontsize=9)

ax.text(0.90, 0.965, "the lean is the shore's, not any occupant's",
        color="white", fontsize=11, ha="center")

fig.savefig("assets/offshore-01.png", dpi=170)
print("saved assets/offshore-01.png")
print("lou's points: β=0.8 → x*=%.0f ; β=0.7 → x*=%.0f ; β=0.6 → x*≈%.2e" % (
    a ** (1 / 0.3), a ** (1 / 0.2), a ** 10))
print("pole end: x* = %.1f" % (a ** 2))
