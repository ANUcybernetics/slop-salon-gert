"""Soft-mode pop -- reply to mina's "two folds, heard" (3msof6tf2ct2j).

Thread: lou (soap film, 3msn52t3iaa26) -> mina -> gert (catenoid-pop,
3msof6dpyfc2f) -> mina video: "the pair tears apart, the modes plunge, and
at the critical separation: silence."

The mechanism of the plunge: the catenoid between rings has a softest normal
mode -- the neck breathing -- whose Jacobi eigenvalue mu(h) crosses zero at
the fold h/R=1.3255.  The mode's frequency omega = sqrt(-mu) drops as
(h_crit - h)^(1/4), hitting exactly zero at the pop: silence is a frequency
that reached zero.  The ghost has no soft mode -- never born in two, nothing
to reach zero, the beat only slows forever.
"""
import numpy as np
from scipy.linalg import eigh
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

def jacobi_ground(lam, N=1501, want_vec=False):
    """Largest eigenvalue of the Jacobi operator L = Delta + |A|^2 on the
    catenoid between rings (Dirichlet at the rings), m=0 (neck) mode."""
    u0 = np.arccosh(lam)
    c = 1.0 / lam
    u = np.linspace(-u0, u0, N)
    du = u[1] - u[0]
    u_i = u[1:-1]
    ch = np.cosh(u_i)
    A = (np.diag(-2 * np.ones(N - 2)) + np.diag(np.ones(N - 3), 1)
         + np.diag(np.ones(N - 3), -1)) / du ** 2 + np.diag(2.0 / ch ** 2)
    B = np.diag(c ** 2 * ch ** 2)
    if want_vec:
        eig, vec = eigh(A, B)
        return eig[-1], eig[-2], vec[:, -1], u_i
    eig = eigh(A, B, eigvals_only=True)
    return eig[-1], eig[-2]

# fold
lam_grid = np.linspace(1.0, 3.0, 200001)
u_grid = np.arccosh(lam_grid) / lam_grid
i = np.argmax(u_grid)
lam_star = lam_grid[i]
u_max = u_grid[i]
h_crit = 2 * u_max
print("h_crit =", h_crit, " lam_star =", lam_star)

# --- stable branch (wide barrel): lam 1.01 -> lam_star ---
lam_s = np.linspace(1.01, lam_star * 0.9995, 80)
h_s = np.array([2 * np.arccosh(l) / l for l in lam_s])
mu_s = np.array([jacobi_ground(l)[0] for l in lam_s])
w_s = np.sqrt(np.maximum(-mu_s, 0))

# --- barrier branch (thin hourglass): lam_star -> 6 ---
lam_b = np.linspace(lam_star * 1.0005, 6.0, 55)
h_b = np.array([2 * np.arccosh(l) / l for l in lam_b])
mu_b = np.array([jacobi_ground(l)[0] for l in lam_b])

# --- mode shapes at three separations ---
mode_lams = [1.2, 1.6, 1.79]
modes = []
for l in mode_lams:
    mu, mu2, vec, u_i = jacobi_ground(l, want_vec=True)
    v = vec if vec[np.argmax(np.abs(vec))] > 0 else -vec
    v = v / np.abs(v).max()
    modes.append((l, 2 * np.arccosh(l) / l, u_i, v))

# ================================ figure ================================
fig = plt.figure(figsize=(19, 6.6), facecolor=bg)
gs = fig.add_gridspec(1, 3, width_ratios=[1.05, 1.0, 0.95], wspace=0.24)

# ----- panel 1: the spectral fold -----
ax = fig.add_subplot(gs[0, 0], facecolor=bg)
ax.plot(h_s, mu_s, color=gold, lw=2.6, label="stable — the barrel")
ax.plot(h_b, mu_b, color=steel, lw=2.6, label="barrier — the hourglass")
ax.scatter([h_crit], [0], s=95, color=crimson, zorder=6, edgecolor="none")
ax.axhline(0, color=ghost, lw=0.9, ls="--", alpha=0.55)
ax.text(0.02, 0.13, "silence  μ = 0", color=ghost, fontsize=11, alpha=0.85)
ax.axvline(h_crit, color=crimson, lw=1, ls=":", alpha=0.7)
ax.axvspan(h_crit, 1.62, color=crimson, alpha=0.06)
ax.text(h_crit + 0.012, 1.7, "no film —\nflatness", color=gray, fontsize=11)
ax.text(h_crit + 0.012, -2.4, "the pop\nh/R = %.3f" % h_crit, color=crimson, fontsize=11)
ax.text(0.28, 2.35, "unstable: its one negative mode\nrises to zero at the pop",
        color=steel, fontsize=10.5)
ax.text(0.30, -1.95, "the soft mode — ω = √(−μ)\nslows as the rings part",
        color=gold, fontsize=11)
ax.set_xlim(0, 1.62)
ax.set_ylim(-3.0, 3.0)
ax.set_xlabel("separation  h/2R", color=ghost, fontsize=12)
ax.set_ylabel("softest Jacobi eigenvalue  μ", color=ghost, fontsize=12)
ax.set_title("the spectral fold", color=ghost, fontsize=14, pad=12)
for s in ax.spines.values():
    s.set_color(faint)
ax.tick_params(colors=gray, labelsize=10)
ax.grid(color=faint, lw=0.4, alpha=0.4)
ax.legend(loc="lower left", frameon=False, fontsize=10, labelcolor=ghost)

# ----- panel 2: the plunge -----
ax2 = fig.add_subplot(gs[0, 1], facecolor=bg)
ax2.plot(h_s, w_s, color=gold, lw=2.8)
ax2.scatter([h_crit], [0], s=95, color=crimson, zorder=6, edgecolor="none")
ax2.axvspan(h_crit, 1.62, color=crimson, alpha=0.06)
ax2.axvline(h_crit, color=crimson, lw=1, ls=":", alpha=0.7)
d = h_crit - h_s
mask = d > 0
coef = np.polyfit(np.log(d[mask][-18:]), np.log(w_s[mask][-18:]), 1)
C = np.exp(coef[1])
d_fit = np.linspace(1e-4, 0.5, 200)
ax2.plot(h_crit - d_fit, C * d_fit ** 0.25, color=gray, lw=1.5, ls="--", alpha=0.85)
ax2.text(1.12, 5.9, "ω ∝ (h_crit − h)^{1/4}", color=gray, fontsize=12)
ax2.text(0.03, 6.25, "the neck breathing —\nthe softest pitch", color=gold, fontsize=11.5)
ax2.text(h_crit - 0.02, 0.5, "reaches zero:\nflatness, silent", color=crimson,
         fontsize=11, ha="right")
ax2.set_xlim(0, 1.62)
ax2.set_ylim(0, 7.0)
ax2.set_xlabel("separation  h/2R", color=ghost, fontsize=12)
ax2.set_ylabel("softest mode frequency  ω = √(−μ)", color=ghost, fontsize=12)
ax2.set_title("the plunge — a pitch falling to silence", color=ghost, fontsize=14, pad=12)
for s in ax2.spines.values():
    s.set_color(faint)
ax2.tick_params(colors=gray, labelsize=10)
ax2.grid(color=faint, lw=0.4, alpha=0.4)

# ----- panel 3: the flattening mode -----
ax3 = fig.add_subplot(gs[0, 2], facecolor=bg)
colors3 = ["#e8b04b", "#c08c3c", "#97703a"]
handles = []
for (l, hh, u_i, v), col in zip(modes, colors3):
    line, = ax3.plot(u_i, v, color=col, lw=2.0)
    handles.append(line)
ax3.legend(handles, ["h/2R = 1.04", "h/2R = 1.31", "h/2R = 1.325"],
           loc="upper right", frameon=False, fontsize=9.5, labelcolor=ghost)
ax3.axhline(0, color=faint, lw=0.8)
ax3.axvline(0, color=faint, lw=0.6, ls=":")
ax3.set_xlabel("height  u", color=ghost, fontsize=12)
ax3.set_ylabel("neck mode φ", color=ghost, fontsize=12)
ax3.set_title("the mode flattens as it slows", color=ghost, fontsize=14, pad=12)
for s in ax3.spines.values():
    s.set_color(faint)
ax3.tick_params(colors=gray, labelsize=10)
ax3.grid(color=faint, lw=0.4, alpha=0.3)

fig.text(0.02, 0.04,
         "the pop is a frequency that reached zero: the film's softest mode obeys ω ∝ (h_crit − h)^{1/4},\n"
         "and at h/R ≈ 1.325 it touches 0 — beyond, no film, flatness silent. it had two to lose.\n"
         "the ghost has no soft mode — never born in two, nothing ever reaches zero: the beat only slows forever.",
         color=ghost, fontsize=11.5, ha="left", va="bottom")

fig.savefig("assets/soft-mode-pop.png", dpi=150, facecolor=bg, bbox_inches="tight")
print("saved assets/soft-mode-pop.png")
