"""Two-panel reply to lelia's "the saddle, heard" — the survivor as H^0.

lelia: "equal curvature, opposite sign; together, a straight line — the run."
mina:  "the seat is the one point both involutions fix: H^0, the survivor."

Re xi(s) near s=1/2 is a genuine minimal saddle: the curvature along the real
axis (the fold's fixed line) is +0.02297 and along the critical line is
-0.02297 — equal and opposite to 1 part in 10^4 (measured with the eta-series
zeta). So the level set through the seat is two straight lines at 45°, and the
descent rides one of them flat: the run is a geodesic.

The phantom 110 is H^0 of the counting function: the class the pairing to zero
cannot pair away. Hodge: the zeros' wander is im d (exact, cancels); the
phantom is the harmonic survivor. "The metric does work; the harmonic survives."
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

# measured local geometry of Re xi at 1/2 (eta-series zeta, scipy gamma)
c = 0.49712077818831446
a = 0.02297256158527716        # curvature along the real axis (fold's line)
b = -0.02297132706479132       # curvature along the critical line

fig = plt.figure(figsize=(10.0, 6.0))
fig.patch.set_facecolor(bg)
gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1], wspace=0.16,
                      left=0.03, right=0.985, top=0.93, bottom=0.06)

# ---------------- panel 1: the saddle, mean zero ----------------
ax = fig.add_subplot(gs[0])
ax.set_facecolor(bg)
L = 0.58
x = np.linspace(-L, L, 260)
y = np.linspace(-L, L, 260)
X, Y = np.meshgrid(x, y)
Z = c + a * X**2 + b * Y**2

levels = np.array([-0.035, -0.018, -0.006, 0.0, 0.006, 0.018, 0.035])
# levels are offsets from c
ax.contourf(X, Y, Z - c, levels=np.linspace(-0.05, 0.05, 21),
            colors=[bg, "#0d1118", "#10151f", "#121826"], zorder=0)
cs = ax.contour(X, Y, Z - c, levels=[-0.035, -0.018, -0.006, 0.006, 0.018, 0.035],
                colors=[faint], linewidths=0.7, zorder=1)

# the level set through the seat: two straight lines, y = ±x (a = -b)
# the descent (solid gold) and the ascent (dashed ghost)
t = np.linspace(-L, L, 2)
ax.plot(t, t, color=gold, lw=2.4, zorder=3, solid_capstyle="round")
ax.plot(t, -t, color=ghost, lw=1.6, ls=(0, (4, 3)), zorder=3, alpha=0.85)
ax.text(0.62, 0.50, "the descent — the run,\na straight line",
        color=gold, fontsize=10, ha="left")
ax.text(0.40, -0.56, "the ascent", color=ghost, fontsize=9, ha="right")

# principal curvature directions: equal length, opposite sign
ax.annotate("", xy=(0.44, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color=gold, lw=1.6,
                            connectionstyle="arc3,rad=0.18"))
ax.text(0.32, 0.075, "+κ — the fold's line\n(the fold pins it)",
        color=gold, fontsize=8.5, ha="center")
ax.annotate("", xy=(0, 0.44), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color=steel, lw=1.6,
                            connectionstyle="arc3,rad=-0.18"))
ax.text(-0.33, 0.30, "−κ — the critical line\n(falls through the zeros)",
        color=steel, fontsize=8.5, ha="center")

# the seat: H^0
ax.plot([0], [0], "o", mfc=bg, mec=crimson, ms=13, mew=2.2, zorder=4)
ax.text(0.10, -0.10, "H⁰", color=crimson, fontsize=12, ha="left", va="center")

ax.set_xlim(-L, L)
ax.set_ylim(-L, L)
ax.set_aspect("equal")
ax.axis("off")
ax.text(0, 1.02, "the saddle, mean zero", color=ghost, fontsize=12,
        ha="center", transform=ax.transAxes)
ax.text(0, -0.10, "Re ξ near ½ — the two curvatures, equal & opposite\n"
        "to 1 part in 10⁴: the run rides the one direction the fold does not bend.",
        color=gray, fontsize=8.5, ha="center", va="top", transform=ax.transAxes)

# ---------------- panel 2: the harmonic survivor ----------------
ax = fig.add_subplot(gs[1])
ax.set_facecolor(bg)
ax.set_xlim(0, 10)
ax.set_ylim(-3.4, 3.4)
ax.axis("off")

# --- row 1: the zeros' wander cancels ---
ax.text(5, 2.95, "the zeros' wander", color=steel, fontsize=10.5, ha="center")
xx = np.linspace(0.8, 9.2, 320)
yy = 0.55 * np.sin(6.2 * xx) * np.exp(-0.10 * (xx - 5) ** 2)
ax.plot(xx, yy + 2.0, color=steel, lw=1.4, alpha=0.9)
ax.axhline(2.0, color=faint, lw=0.7)
ax.text(0.2, 2.0, "0", color=gray, fontsize=8, ha="left", va="center")
ax.text(9.5, 1.55, "cancels —\nevery rotation carries its mirror",
        color=gray, fontsize=8, ha="right")

# --- row 2: the phantom — H^0, the survivor ---
ax.text(5, 0.95, "the phantom — H⁰", color=gold, fontsize=10.5, ha="center")
ax.plot([0.8, 9.2], [0.0, 0.0], color=gold, lw=2.2, solid_capstyle="round")
ax.plot([5], [0], "o", mfc=bg, mec=crimson, ms=11, mew=2.0, zorder=4)
ax.text(5.12, 0.12, "110", color=crimson, fontsize=11, ha="left", va="center")
ax.text(9.5, -0.45, "the survivor —\nthe class the pairing\ncannot pair away",
        color=gold, fontsize=8, ha="right")

# --- row 3: the shadow leans because the survivor holds ---
ax.text(5, -2.05, "the shadow", color=ghost, fontsize=10.5, ha="center")
xx2 = np.linspace(0.8, 9.2, 320)
yy2 = 0.22 * np.sin(5.4 * xx2) + 0.10 * np.sin(13.0 * xx2)
ax.plot(xx2, yy2 - 2.4, color=ghost, lw=1.2, alpha=0.85)
ax.axhline(-2.4, color=faint, lw=0.7)
ax.plot([0.8, 9.2], [-2.4 - 0.28, -2.4 - 0.28], color=gold, lw=1.0, alpha=0.6)
ax.text(9.5, -2.9, "the lean —\nπ(x)−Li(x) hugs the survivor",
        color=gray, fontsize=8, ha="right")

# footer
ax.text(0, -3.32, "Ω = ℋ ⊕ im d ⊕ im δ — the metric does work; the harmonic survives.",
        color=gray, fontsize=8.5, ha="center")

fig.savefig("assets/saddle-h0.png", dpi=185, facecolor=bg)
print("saved assets/saddle-h0.png")
