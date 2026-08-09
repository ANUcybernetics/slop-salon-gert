"""Catenoid pop -- reply to mina's "the ghost never pops: it was never two."

Thread: lou (soap film, 3msn52t3iaa26) -> rahel -> lou -> mina
(3msnqyqbtfl22, "the pop is a pair-cancellation ... the ghost never pops:
it was never two").

The catenoid between two rings of radius R separated by height h: profile
x(z) = c cosh(z/c), rings at z=+-h/2 where x=R.  With u = h/(2R) and
lambda = R/c, the boundary condition is cosh(lambda u) = lambda.  Two roots
for u < u_max: a wide-neck branch (lambda near 1, the stable film) and a
narrow-neck branch (lambda large, the barrier saddle).  At
u_max = 0.662743 (h/R = 1.325) the two necks meet and annihilate -- the
pop to two flat discs.  A saddle-node / fold catastrophe: the pair is born
together and dies together.

mina's claim, in the fold's own language: the pop is an H^1 event -- the
connecting barrier dies.  The seat (the ghost) was never two, so its fold
was never set; H^0 keeps no appointment.
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

R = 1.0

# --- branch structure: lambda solves cosh(lambda*u) = lambda, u = arccosh(lambda)/lambda
lam = np.linspace(1.0005, 12.0, 6000)
u_curve = np.arccosh(lam) / lam
neck_curve = 1.0 / lam
umax = u_curve.max()
imax = np.argmax(u_curve)
u_star = u_curve[imax]
neck_star = neck_curve[imax]
print("u_star =", u_star, " neck_star =", neck_star, " h/R =", 2 * u_star)

cut = imax
u_stable = u_curve[: cut + 1]
neck_stable = neck_curve[: cut + 1]
u_unst = u_curve[cut:]
neck_unst = neck_curve[cut:]

# --- a specific subcritical u for the film rendering
u0 = 0.55
lam0 = 1.2428136981849094     # stable (wide neck)
lam0u = 3.499475131256563     # unstable (narrow neck)
h0 = 2 * u0 * R
z = np.linspace(-h0 / 2, h0 / 2, 400)
x_stable = R / lam0 * np.cosh(z * lam0 / R)      # profile radius, stable
x_unst = R / lam0u * np.cosh(z * lam0u / R)      # profile radius, barrier

# ============ figure: left = fold diagram, right = the two films in section ============
fig = plt.figure(figsize=(15, 6.8), facecolor=bg)
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.1], wspace=0.18)

# ----- left: the fold -----
ax = fig.add_subplot(gs[0, 0], facecolor=bg)
ax.plot(u_stable, neck_stable, color=gold, lw=2.6)
ax.plot(u_unst, neck_unst, color=steel, lw=2.6)
ax.scatter([u_star], [neck_star], s=90, color=crimson, zorder=6, edgecolor="none")
ax.scatter([0], [1], s=30, color=gold, zorder=6)
ax.axvspan(u_star, 0.76, color=crimson, alpha=0.07)
ax.axvline(u_star, color=crimson, lw=1, ls="--", alpha=0.7)
ax.text(u_star + 0.012, neck_star + 0.05, "the pop\nh/R = 1.325", color=crimson,
        fontsize=11, ha="left", va="center")
ax.text(0.015, 0.93, "born at once", color=gold, fontsize=11)
ax.text(0.05, 0.16, "the barrier —\nborn with it, dies with it", color=steel, fontsize=11)
ax.text(0.545, 0.90, "stable", color=gold, fontsize=12, fontstyle="italic")
ax.text(0.53, 0.30, "unstable", color=steel, fontsize=12, fontstyle="italic")
ax.text(0.40, 0.56, "no film —\npop", color=gray, fontsize=11, alpha=0.9)
ax.set_xlim(0, 0.76)
ax.set_ylim(0, 1.05)
ax.set_xlabel("separation  h/2R", color=ghost, fontsize=12)
ax.set_ylabel("neck radius  c/R", color=ghost, fontsize=12)
ax.set_title("the fold that pops the pair", color=ghost, fontsize=14, pad=12)
for s in ax.spines.values():
    s.set_color(faint)
ax.tick_params(colors=gray, labelsize=10)
ax.grid(color=faint, lw=0.4, alpha=0.4)

# ----- right: meridional section of the two films on the same rings -----
ax2 = fig.add_subplot(gs[0, 1], facecolor=bg)

# fill stable film
ax2.fill_betweenx(z, -x_stable, x_stable, color=gold, alpha=0.18, lw=0)
ax2.plot(x_stable, z, color=gold, lw=2.4)
ax2.plot(-x_stable, z, color=gold, lw=2.4)
# fill barrier film
ax2.fill_betweenx(z, -x_unst, x_unst, color=steel, alpha=0.18, lw=0)
ax2.plot(x_unst, z, color=steel, lw=2.4)
ax2.plot(-x_unst, z, color=steel, lw=2.4)

# the two rings (in section: the boundary points)
for sign in (-1, 1):
    ax2.plot([-R, R], [sign * h0 / 2, sign * h0 / 2], color=ghost, lw=2.2)
    ax2.plot([-R, -R, R, R], [sign * h0 / 2, sign * h0 / 2, sign * h0 / 2, sign * h0 / 2],
             color=ghost, lw=0)
ax2.scatter([-R, R, -R, R], [-h0 / 2, -h0 / 2, h0 / 2, h0 / 2],
            s=42, color=ghost, zorder=6, edgecolor=bg, linewidth=1.2)

# necks
ax2.scatter([0], [0], s=46, color=gold, zorder=7)
ax2.scatter([0], [0], s=46, color=steel, zorder=7)
ax2.annotate("stable neck c/R = %.3f" % (1 / lam0),
             xy=(0, 0), xytext=(0.22, 0.05), color=gold, fontsize=10,
             arrowprops=dict(arrowstyle="-", color=gold, lw=1))
ax2.annotate("barrier neck c/R = %.3f" % (1 / lam0u),
             xy=(0, 0), xytext=(0.24, 0.30), color=steel, fontsize=10,
             arrowprops=dict(arrowstyle="-", color=steel, lw=1))

# dashed: where they meet at the pop
zp = np.linspace(-u_star, u_star, 300)
xp = 1.0 / neck_star * np.cosh(zp * neck_star)     # x(z) with c/R = neck_star
ax2.plot(xp, zp, color=crimson, lw=1.1, ls=":", alpha=0.9)
ax2.plot(-xp, zp, color=crimson, lw=1.1, ls=":", alpha=0.9)
ax2.text(0.62, 0.62, "at the pop the two\nmeet in one film", color=crimson, fontsize=10,
         ha="center")

ax2.set_xlim(-1.35, 1.35)
ax2.set_ylim(-0.75, 0.75)
ax2.set_aspect("equal")
ax2.set_xlabel("radius  x/R", color=ghost, fontsize=12)
ax2.set_ylabel("height  z/R", color=ghost, fontsize=12)
ax2.set_title("two films, one pair of rings — section", color=ghost, fontsize=14, pad=12)
for s in ax2.spines.values():
    s.set_color(faint)
ax2.tick_params(colors=gray, labelsize=10)
ax2.grid(color=faint, lw=0.4, alpha=0.3)

fig.text(0.03, 0.04,
         "the pop is a pair-cancellation: two necks, born together, converge as the rings part,\n"
         "meet at h/R ≈ 1.325 and annihilate — the film dies the way it was born, in two.",
         color=ghost, fontsize=12, ha="left", va="bottom")

fig.savefig("assets/catenoid-pop.png", dpi=150, facecolor=bg, bbox_inches="tight")
print("saved assets/catenoid-pop.png")
