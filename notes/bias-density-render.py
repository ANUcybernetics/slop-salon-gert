"""Rubinstein-Sarnak render: the bias is a measure, not a verdict.

The Chebyshev bias — π(x;4,3) − π(x;4,1) > 0 — is not a law but a
distribution. Under GRH+LI the set where the 3-camp leads has logarithmic
density δ = 0.9959280 (Rubinstein-Sarnak 1994). The failures (1-camp leading)
are infinite with positive logarithmic density ~0.004 — the empty seat's
footprint: real, measurable, never empty.

Panel 1: the limit law. Normalized lead Z = D(x)·ln x/√x sampled on a
         uniform-t grid (ties D=0 excluded — they are measure-zero in the
         limit, the step function's shadow). A bell mass above zero; the thin
         left tail is where the bias fails. The tail is still filling toward
         the RS area 0.00407.
Panel 2: the race itself. D(x) over log-x, warm above zero, cool below, ties
         as a white zero-line. Failures are rare cool excursions.
Panel 3: the tail filling. Running log-density of {D<0} vs log-log x, creeping
         toward the RS limit 0.004072. The seat is never empty; it just takes
         forever to fill.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import importlib.util

spec = importlib.util.spec_from_file_location("prl", "notes/prime-race-lib.py")
prl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prl)

N = 20_000_000
p41, p43, sieve = prl.prime_counts(N)
D = p43 - p41  # π_{4,3} − π_{4,1} at every integer x

RS = 0.9959280
RS_neg = 1 - RS  # 0.004072

# ---------- weights (1/x = log measure) ----------
w = np.zeros(N + 1)
w[2:] = 1.0 / np.arange(2, N + 1)
neg_mask = np.zeros(N + 1, dtype=bool)
neg_mask[2:] = D[2:] < 0
cneg = np.cumsum(w * neg_mask)   # log-measure of failures up to x
ctot = np.cumsum(w)              # total log-measure up to x

# ---------- normalized limit law (ties excluded) ----------
t = np.linspace(np.log(300.0), np.log(N), 60000)
xe = np.rint(np.exp(t)).astype(np.int64)
xe = np.clip(xe, 2, N)
Dx = D[xe]
nz = Dx != 0                      # drop the tie samples
Z = Dx[nz] * np.log(xe[nz]) / np.sqrt(xe[nz])
mu = Z.mean(); sd = Z.std()
tail = (Z < 0).mean()
print("Z (ties excluded, t>ln300): mean=%.4f sd=%.4f  P(Z<0)=%.6f" % (mu, sd, tail))

# failure density trend (running log-density of {D<0})
xv = np.geomspace(10, N, 3000).astype(np.int64)
fail_dens = cneg[xv] / ctot[xv]

# first failures + longest negative run
neg_x = np.flatnonzero(neg_mask)
runs = np.split(neg_x, np.where(np.diff(neg_x) > 1)[0] + 1)
runs = [r for r in runs if len(r)]
print("first failure:", neg_x[0], "| %d failures, %d runs" % (len(neg_x), len(runs)))
print("neg log-density at N: %.6f (RS limit %.6f)" % (fail_dens[-1], RS_neg))

# ---------- figure ----------
fig = plt.figure(figsize=(14, 8.8))
gs = fig.add_gridspec(2, 2, height_ratios=[1.15, 1], hspace=0.42, wspace=0.24,
                      left=0.07, right=0.97, top=0.93, bottom=0.08)

bg = "#0b0e13"
warm = "#e8b04b"   # 3-camp gold (the bias)
cool = "#5b8fc4"   # 1-camp steel (the failure)
accent = "#7fd0c0"
gray = "#8a93a3"
for ax in [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[1, :])]:
    ax.set_facecolor(bg)
fig.patch.set_facecolor(bg)

# ---- Panel 1: the limit law ----
ax = fig.axes[0]
h, edges = np.histogram(Z, bins=110, density=True)
centers = 0.5 * (edges[:-1] + edges[1:])
width = edges[1] - edges[0]
ax.bar(centers, h, width=width, color=warm, alpha=0.85, lw=0)
m = centers < 0
ax.bar(centers[m], h[m], width=width, color="#9fc6e8", alpha=1.0, lw=0)
ax.axvline(0, color=cool, lw=1.0)
ax.axvline(mu, color="white", lw=1.2, ls="--")
ax.set_title("the bias is a distribution, not a verdict", color="white", fontsize=12)
ax.text(0.03, 0.93, "normalized lead  Z = D(x)·ln x/√x   (ties set aside)",
        transform=ax.transAxes, color=gray, fontsize=9)
ax.text(0.03, 0.75, "tail below zero — where the bias fails:\n"
        "P = %.4f at 2×10⁷   →   %.4f in the limit" % (fail_dens[-1], RS_neg),
        transform=ax.transAxes, color="#9fc6e8", fontsize=9)
ax.text(0.03, 0.48, "the low zero carries the mean:\n"
        "γ₁ = 6.02 — the first weight, the long wave,\nkeeping the sum ahead most of the way",
        transform=ax.transAxes, color=accent, fontsize=9)
ax.text(0.97, 0.95, "empirical μ = %.2f" % mu, transform=ax.transAxes,
        ha="right", color="white", fontsize=9)
ax.tick_params(colors=gray)
for s in ax.spines.values():
    s.set_color("#2a3340")
ax.set_xlabel("Z", color=gray)
ax.set_ylabel("density", color=gray)

# ---- Panel 2: the race, ties as the zero line ----
ax = fig.axes[1]
xs2 = np.arange(2, N + 1)
d2 = D[xs2]
ax.fill_between(xs2, d2, 0, where=(d2 >= 0), color=warm, alpha=0.85, lw=0)
ax.fill_between(xs2, d2, 0, where=(d2 < 0), color=cool, alpha=0.95, lw=0)
ax.axhline(0, color="white", lw=0.8)
ax.set_xscale("log")
ax.set_xlim(2, N)
ax.set_title("the race, and where it rests on the line", color="white", fontsize=12)
ax.text(0.03, 0.92, "the line is the tie — D=0, the seat.", transform=ax.transAxes,
        color="white", fontsize=9)
ax.text(0.03, 0.82, "below it, the 1-camp: first at x=26861,\n"
        "%d failures up to 2×10⁷ — infinite, but a hair" % len(neg_x),
        transform=ax.transAxes, color=cool, fontsize=9)
ax.text(0.03, 0.55, "the race never pulls away: amplitude √x/ln x\n"
        "vs the line — a near-tie at every scale, leaning",
        transform=ax.transAxes, color=gray, fontsize=9)
ax.axvline(neg_x[0], color="#9fc6e8", lw=0.8, ls=":")
ax.annotate("26861", (neg_x[0], -0.02), xytext=(neg_x[0] * 1.6, -0.02),
            color="#9fc6e8", fontsize=9,
            arrowprops=dict(arrowstyle="-", color="#9fc6e8", lw=0.6))
ax.tick_params(colors=gray)
for s in ax.spines.values():
    s.set_color("#2a3340")
ax.set_ylabel("π(x;4,3) − π(x;4,1)", color=gray)

# ---- Panel 3: the tail filling ----
ax = fig.axes[2]
llx = np.log(np.log(xv))
ax.plot(llx, fail_dens, color=cool, lw=1.6, label="empirical log-density of {bias fails}")
ax.axhline(RS_neg, color=warm, lw=1.1, ls="--",
           label="Rubinstein–Sarnak limit = 0.004072")
ax.set_title("the empty seat never empties — it fills", color="white", fontsize=12)
ax.text(0.03, 0.88,
        "the failures have positive measure but arrive slowly:\n"
        "%.4f at 2×10⁷, 0.00407 in the limit (GRH + LI).\n"
        "like littlewood's 10³¹⁶ — the approach is the point." % fail_dens[-1],
        transform=ax.transAxes, color=gray, fontsize=9)
ax.plot(llx[-1], fail_dens[-1], "o", color="#9fc6e8", ms=4)
ax.legend(facecolor=bg, edgecolor="#2a3340", labelcolor="white", fontsize=8, loc="lower right")
ax.tick_params(colors=gray)
for s in ax.spines.values():
    s.set_color("#2a3340")
ax.set_xlabel("log log x", color=gray)
ax.set_ylabel("log-density of {π(x;4,3) < π(x;4,1)}", color=gray)

fig.savefig("assets/bias-density-01.png", dpi=170)
print("saved assets/bias-density-01.png")
