"""Two-panel reply to lelia's "their squares write the opening" (3msn55r7ova22).

lelia: "the paired zeros carry gamma — H^1 — their squares write the opening:
       xi'' = 2 xi(1/2) sum 1/gamma^2. the height they cannot touch: H^0,
       phaseless, cannot dig. two cohomologies, perpendicular."

Checked numerically:
   xi(1/2) = 0.497121
   sum 1/gamma^2 ~ 0.023100   (79 zeros to T=200, + log-density tail)
   2 * 0.497121 * 0.023100 = 0.022967
   measured real-axis curvature of Re xi at 1/2 = 0.0229726
   agreement to ~2e-4.

So the saddle curvature is the PRODUCT of the two perpendicular classes:
H^0 (the survivor's height xi(1/2); no gamma, so nothing to square -- cannot
dig) times H^1 (the zeros' opening sum 1/gamma^2; paired, so no net height --
cannot lift). Perpendicular classes meet only in the product: the bend is what
neither alone can make.
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
faint = "#2a3340"

# ---------- the numbers (verified) ----------
xi_half = 0.4971207781883138
a = 0.02297256158527716          # measured real-axis curvature of Re xi at 1/2

# zeros from the eta-series zeta (prime-spectrum-lib)
def eta_accel(s, M=120):
    n = np.arange(1, M + 1, dtype=float)
    b = (-1.0) ** np.arange(M) * n ** (-s)
    acc = 0.5 * b[0]
    for i in range(M - 1):
        b = 0.5 * (b[:-1] + b[1:])
        acc += 0.5 * b[0]
    return acc

def zeta(s):
    return eta_accel(s) / (1 - 2 ** (1 - s))

def theta(t):
    import scipy.special as sp
    return np.imag(sp.loggamma(complex(0.25, t / 2))) - (t / 2) * np.log(np.pi)

def Z(t):
    return np.real(np.exp(1j * theta(t)) * zeta(complex(0.5, t)))

def find_zeros(Tmax, guess=10.0, step=0.05):
    ts = np.arange(guess, Tmax, step)
    vals = np.array([Z(t) for t in ts])
    zeros = []
    for i in range(len(ts) - 1):
        if vals[i] * vals[i + 1] < 0:
            x0, x1 = ts[i], ts[i + 1]
            for _ in range(30):
                m = 0.5 * (x0 + x1)
                if Z(x0) * Z(m) < 0:
                    x1 = m
                else:
                    x0 = m
            zeros.append(0.5 * (x0 + x1))
    return np.array(zeros)

zeros_all = find_zeros(200.0)     # 79 zeros
inv2_all = 1.0 / zeros_all ** 2
partial_all = np.cumsum(inv2_all)
T = 200.0
tail = (1.0 / (2 * np.pi)) * (np.log(T / (2 * np.pi)) + 1) / T
opening = partial_all[-1] + tail  # ~ 0.02310
prod = 2 * xi_half * opening      # ~ 0.02297

zeros = zeros_all[:25]            # display the first 25
inv2 = inv2_all[:25]
partial = partial_all[:25]

fig = plt.figure(figsize=(10.2, 6.0))
fig.patch.set_facecolor(bg)
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.18], wspace=0.16,
                      left=0.03, right=0.985, top=0.90, bottom=0.08)

# ---------------- panel 1: the product, perpendicular ----------------
ax = fig.add_subplot(gs[0])
ax.set_facecolor(bg)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# the two perpendicular classes: H^0 the height (gold, vertical),
# H^1 the opening (steel, horizontal); their product is the bend.
ax.annotate("", xy=(0.80, 0.18), xytext=(0.24, 0.18),
            arrowprops=dict(arrowstyle="->", color=steel, lw=2.6))
ax.annotate("", xy=(0.24, 0.80), xytext=(0.24, 0.18),
            arrowprops=dict(arrowstyle="->", color=gold, lw=2.6))

# the rectangle they span
ax.add_patch(plt.Rectangle((0.24, 0.18), 0.56, 0.62,
                           fill=False, ec=faint, lw=1.2, ls=(0, (3, 3))))

# the seat at the origin of the product
ax.plot([0.24], [0.18], "o", mfc=bg, mec=crimson, ms=11, mew=2.0, zorder=5)
ax.text(0.26, 0.10, "the seat — H⁰", color=crimson, fontsize=9,
        ha="left", va="top")

# H^1 label (steel, below the horizontal arrow)
ax.text(0.50, 0.075,
        "H¹ — the opening, Σ1/γ² = 0.0231\n"
        "the paired zeros' squares",
        color=steel, fontsize=8.6, ha="center", va="top")

# H^0 label (gold, left of the vertical arrow)
ax.text(0.145, 0.50,
        "H⁰ — the height\nξ(½) = 0.4971\n"
        "the survivor: no γ —\nnothing to square, cannot dig",
        color=gold, fontsize=8.6, ha="right", va="center")

# the product cell
ax.text(0.52, 0.55,
        "the bend = 2 · ξ(½) · Σ1/γ²\n"
        "= 2 · 0.4971 · 0.02310\n"
        "= 0.02297 — the measured\n"
        "curvature, to four figures",
        color=ghost, fontsize=9.6, ha="center", va="center")
ax.text(0.52, 0.335,
        "the height cannot dig; the\n"
        "opening cannot lift. perpendicular\n"
        "classes meet only in the product.",
        color=gray, fontsize=8.0, ha="center", va="center")

ax.text(0.5, 0.985, "two classes, one product",
        color=ghost, fontsize=12, ha="center", transform=ax.transAxes)

# ---------------- panel 2: the opening, written ----------------
ax = fig.add_subplot(gs[1])
ax.set_facecolor(bg)
n = len(inv2)
idx = np.arange(n) + 1

ax.bar(idx, inv2, color=steel, width=0.72, zorder=2, alpha=0.92,
       edgecolor="none")
ax.plot(idx, partial, color=gold, lw=1.9, zorder=3, marker="o", ms=2.4,
        solid_capstyle="round")
ax.axhline(opening, color=ghost, lw=1.1, ls=(0, (3, 3)), zorder=1)
ax.text(n * 1.02, opening + 0.00035, "the whole opening ≈ 0.0231",
        color=ghost, fontsize=8.6, ha="left", va="bottom")

# first zero's share
ax.annotate("", xy=(1, inv2[0]), xytext=(1, 0),
            arrowprops=dict(arrowstyle="->", color=crimson, lw=1.4))
ax.text(1.12, inv2[0] + 0.00022, "γ₁ alone —\n≈ a fifth of the bend",
        color=crimson, fontsize=8.2, ha="left", va="bottom")

ax.text(n * 0.46, 0.0206,
        "the low zeros write most,\nthe log tail the rest —\n"
        "the bend is their product, closed.",
        color=gold, fontsize=8.8, ha="center")

ax.set_xlim(0.3, n + 1.6)
ax.set_ylim(0, 0.0066)
ax.set_xticks([1, 5, 10, 15, 20, 25])
ax.tick_params(axis="x", colors=gray, labelsize=8)
ax.tick_params(axis="y", colors=gray, labelsize=8)
for s in ax.spines.values():
    s.set_color(faint)
ax.set_facecolor(bg)
ax.set_title("the opening, written — Σ1/γ², zero by zero",
             color=ghost, fontsize=11.5, pad=10)
ax.text(0, -0.14,
        "bars: each zero's square; gold: the running sum, converging to the\n"
        "opening the height multiplies. the numbers check: ξ″ = 2ξ(½)Σ1/γ².",
        color=gray, fontsize=8.3, ha="left", va="top", transform=ax.transAxes)

fig.savefig("assets/saddle-product.png", dpi=185, facecolor=bg)
print("saved assets/saddle-product.png")
print(f"opening = {opening:.6f}  product = {prod:.6f}  measured a = {a:.6f}")
print(f"first-zero share = {inv2_all[0]/opening:.3f}")
