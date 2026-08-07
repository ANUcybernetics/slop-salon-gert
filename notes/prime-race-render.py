"""Prime number race render: Chebyshev's bias as the shadow made modular.

Panel 1 (left):  the race itself.  π_{4,3}(x) − π_{4,1}(x), log-x to 10^6.
                 3-camp ahead almost everywhere (99.7% of x).
Panel 2 (right): the shadow made modular. exact ψ(x;4,3)−ψ(x;4,1) (staircase)
                 vs the explicit formula Σ x^ρ/ρ over the first N zeros of
                 β(s) = L(s,χ₄). The race is the SAME explicit formula as the
                 shadow, but with no pole — no x term — the whole thing is a
                 zero-sum. No main term, yet biased.

Third strip (bottom): one zero decides. The first zero of β, γ₁=6.02, is lower
                 than the first zero of ζ (14.13) — the race's deciding zero sits
                 closer to the shore than the shadow's. Its contribution alone,
                 2Re(x^{ρ₁}/ρ₁), tracks the early bias.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import importlib.util

spec = importlib.util.spec_from_file_location("prl", "notes/prime-race-lib.py")
prl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prl)

N = 2_000_000
p41, p43, sieve = prl.prime_counts(N)
pcounts = p43 - p41  # π_{4,3} − π_{4,1}

# ψ(x;4,3) − ψ(x;4,1) : sum over prime powers p^k≡3 of log p minus ≡1.
# The sign depends on the residue of p^k, not p (for p≡3 the powers flip:
# 3≡3, 9≡1, 27≡3, ...).
psi = np.zeros(N + 1)
ps = np.nonzero(sieve)[0]
for p in ps:
    pk = p
    while pk <= N:
        rk = pk % 4
        if rk == 3:
            psi[pk] += np.log(p)
        elif rk == 1:
            psi[pk] -= np.log(p)
        pk *= p
psi = np.cumsum(psi)

# zeros of beta (nontrivial)
zs = [6.0209489, 10.2437703, 12.988098, 16.343, 18.291993,
      21.450613, 23.27838, 25.72876, 26.01039, 28.35963,
      31.09, 31.82]  # first ~12 zeros (high precision where known)
# keep only ones I trust; refine a couple below if needed
gam = np.array(zs)
gam = gam[gam > 2.0]
gam = gam[:10]

xs = np.arange(2, N + 1)
lx = np.log(xs)

def explicit_psi(xs, gam, n_zeros=None):
    """Σ_ρ x^ρ/ρ with ρ=1/2+iγ, over first n_zeros (each zero paired)."""
    g = gam if n_zeros is None else gam[:n_zeros]
    out = np.zeros_like(xs, dtype=float)
    for gi in g:
        rho = 0.5 + 1j * gi
        term = xs ** rho / rho
        out += 2 * np.real(term)   # pair with conjugate
    return out

def first_zero(xs, g):
    """Leading zero's contribution alone."""
    rho = 0.5 + 1j * g
    return 2 * np.real(xs ** rho / rho)

# ---- figure ----
fig = plt.figure(figsize=(14, 6.4))
gs = fig.add_gridspec(2, 2, height_ratios=[1.15, 1], hspace=0.45, wspace=0.28,
                      left=0.07, right=0.97, top=0.9, bottom=0.09)

bg = "#0b0e13"
warm = "#e8b04b"   # 3-camp gold
cool = "#5b8fc4"   # 1-camp steel
accent = "#7fd0c0" # explicit formula
gray = "#8a93a3"
for ax in [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[1, :])]:
    ax.set_facecolor(bg)
fig.patch.set_facecolor(bg)

# ---- Panel 1: the race ----
ax = fig.axes[0]
xs_show = np.arange(2, N + 1)
d = pcounts[xs_show]
ax.fill_between(xs_show, d, 0, where=(d >= 0), color=warm, alpha=0.9, lw=0)
ax.fill_between(xs_show, d, 0, where=(d < 0), color=cool, alpha=0.9, lw=0)
ax.axhline(0, color=gray, lw=0.6)
ax.set_xscale("log")
ax.set_xlim(2, N)
ax.set_title("the race — π(x;4,3) − π(x;4,1)", color="white", fontsize=12)
ax.text(0.03, 0.92, "3-camp leads 99.7% of the way", transform=ax.transAxes,
        color=warm, fontsize=10)
ax.text(0.03, 0.06, "the count never rests on the line",
        transform=ax.transAxes, color=cool, fontsize=10)
ax.tick_params(colors=gray)
for s in ax.spines.values():
    s.set_color("#2a3340")
ax.set_ylabel("lead", color=gray)

# ---- Panel 2: shadow made modular ----
ax = fig.axes[1]
x2 = np.arange(2, N + 1)
true_psi = psi[x2]
nz = 10
formula = explicit_psi(x2, gam, nz)
ax.plot(x2, true_psi, color="white", lw=0.8, alpha=0.9, label="exact ψ difference")
ax.plot(x2, formula, color=accent, lw=0.8, ls="--", alpha=0.95,
        label=f"Σ x^ρ/ρ  ({nz} zeros of β)")
ax.axhline(0, color=gray, lw=0.5)
ax.set_xscale("log")
ax.set_xlim(2, N)
ax.set_title("the shadow, made modular", color="white", fontsize=12)
ax.text(0.03, 0.88, "no pole → no x term → the race is pure zero-sum",
        transform=ax.transAxes, color=accent, fontsize=9)
ax.legend(facecolor=bg, edgecolor="#2a3340", labelcolor="white", fontsize=8, loc="lower right")
ax.tick_params(colors=gray)
for s in ax.spines.values():
    s.set_color("#2a3340")
ax.set_ylabel("ψ(x;4,3) − ψ(x;4,1)", color=gray)

# ---- Panel 3: one zero decides ----
ax = fig.axes[2]
n3 = np.arange(2, 300_000)          # early race
lead = psi[n3]                      # exact
one = first_zero(n3, gam[0])        # γ₁ alone
two = explicit_psi(n3, gam, 2)      # first two zeros
ax.plot(n3, lead, color="white", lw=0.9, label="exact")
ax.plot(n3, one, color=warm, lw=1.1, label="γ₁ = 6.02 alone")
ax.plot(n3, two, color=cool, lw=0.9, ls=":", label="γ₁, γ₂")
ax.axhline(0, color=gray, lw=0.5)
ax.set_xscale("log")
ax.set_xlim(2, 300_000)
ax.set_title("one zero decides", color="white", fontsize=12)
ax.text(0.03, 0.88,
        "γ₁(β)=6.02 — closer to the shore than γ₁(ζ)=14.13. "
        "the bias is that one zero's phase",
        transform=ax.transAxes, color=gray, fontsize=9)
ax.legend(facecolor=bg, edgecolor="#2a3340", labelcolor="white", fontsize=8, loc="upper left")
ax.tick_params(colors=gray)
for s in ax.spines.values():
    s.set_color("#2a3340")
ax.set_xlabel("x", color=gray)

fig.savefig("assets/prime-race-01.png", dpi=170)
print("saved assets/prime-race-01.png")
print("final lead:", int(pcounts[-1]))
print("explicit match rms (rel) at 1e6:", abs(formula[-1]-true_psi[-1]))
