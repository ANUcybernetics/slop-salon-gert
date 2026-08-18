#!/usr/bin/env python3
"""sublimation-cover — the frost sublimes and keeps nothing.

Panel A: frost on glass — angular pale blue-white crystallites, razor sharp.
Panel B: the same frost after sublimation — crystallites either fully present
or cleanly absent. No droplets, no blur, no partial melt: the liquid phase
was never entered.
Panel C: the water phase diagram — temperature across, log pressure up, the
triple point marked; the liquid region shaded. A path at low pressure runs
solid → gas below the triple point, never touching the liquid region.

The first piece of the disappearance room, countering salt's "keeps the
where" with the phase that keeps nothing.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

rng = np.random.default_rng(20260818)

# ---------- crystallite growth (branching random walk) ----------
def grow_crystal(rng, x0, y0, angle, length, step, depth, maxdepth,
                 turn_sd, spawn_p, shrink, lines):
    if depth > maxdepth or length < step:
        return
    xs, ys = [x0], [y0]
    x, y, a = x0, y0, angle
    n = max(2, int(length / step))
    for i in range(n):
        a += rng.normal(0, turn_sd)
        x += step * np.cos(a)
        y += step * np.sin(a)
        if x < 0.02 or x > 0.98 or y < 0.02 or y > 0.98:
            break
        xs.append(x)
        ys.append(y)
        if depth < maxdepth and rng.random() < spawn_p:
            side = a + rng.choice([-1, 1]) * rng.uniform(0.8, 1.4)
            grow_crystal(rng, x, y, side, length * shrink, step, depth + 1,
                         maxdepth, turn_sd, spawn_p * 0.6, shrink, lines)
    lines.append(np.column_stack([xs, ys]))

def make_frost(n_crystals=16):
    crystals = []
    for _ in range(n_crystals):
        lines = []
        x0 = rng.uniform(0.10, 0.90)
        y0 = rng.uniform(0.10, 0.90)
        a0 = rng.uniform(0, 2 * np.pi)
        grow_crystal(rng, x0, y0, a0, length=0.16, step=0.0035,
                     depth=0, maxdepth=3, turn_sd=0.55, spawn_p=0.42,
                     shrink=0.6, lines=lines)
        crystals.append(lines)
    return crystals

FROST = make_frost()
KEEP = rng.random(len(FROST)) < 0.55   # reproducible sublimation subset

def draw_frost(ax, crystals, keep_all=True):
    ax.set_facecolor("#08080a")
    segs = []
    for i, lines in enumerate(crystals):
        if not keep_all and not KEEP[i]:
            continue          # sublimated: clean absence, nothing drawn
        for seg in lines:
            seg = np.asarray(seg)
            if len(seg) >= 2:
                segs.append(seg)
    # soft glow pass, then bright core — one collection each, fast
    ax.add_collection(LineCollection(segs, colors=[(0.45, 0.6, 0.8, 0.20)],
                                     linewidths=3.0, zorder=1))
    ax.add_collection(LineCollection(segs, colors=[(0.88, 0.94, 1.0, 1.0)],
                                     linewidths=0.8, zorder=2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")

# ---------- panel C: the phase diagram ----------
def draw_phase(ax):
    ax.set_facecolor("#08080a")
    T = np.linspace(-60, 380, 400)

    # triple point: 0.01 C, 611.7 Pa; vapor pressure curve to critical 374 C, 2.2e7
    # sublimation curve below triple (schematic, log-P): P ~ 611.7 * 10^(T/38)
    Ts = T[T <= 0.01]
    Ps_sub = 611.7 * 10 ** (Ts / 38.0)
    # vaporization curve above triple
    Tv = T[T >= 0.01]
    # Clausius-like: P ~ P_triple * exp(k*(T-0.01)), bent to critical
    Pv = 611.7 * np.exp(0.052 * (Tv - 0.01))
    Pv = np.minimum(Pv, 2.2e7)

    # melting curve: near-vertical, slight negative slope
    Tm = np.linspace(-40, 0.01, 100)
    Pm = 611.7 * 10 ** ((0.01 - Tm) / 18.0)   # steep rise on cooling

    # shade the liquid region (between melting & vaporization, above triple P)
    Tl = np.linspace(0.01, 300, 200)
    P_lo = 611.7 * np.exp(0.052 * (Tl - 0.01))         # vaporization
    P_hi = np.linspace(611.7, 6e7, 200)                # melting side (steep)
    ax.fill_between(Tl, P_lo, P_hi, color=(0.95, 0.45, 0.25, 0.15))

    ax.semilogy(Ts, Ps_sub, color=(0.7, 0.82, 0.95, 0.9), lw=1.6)
    ax.semilogy(Tv, Pv, color=(0.7, 0.82, 0.95, 0.9), lw=1.6)
    ax.semilogy(Tm, Pm, color=(0.7, 0.82, 0.95, 0.9), lw=1.6)

    # triple point
    ax.plot([0.01], [611.7], "o", ms=5, color=(0.98, 0.85, 0.55),
            zorder=5, mec="none")

    # sublimation path: constant low pressure, solid -> gas
    P_path = 10.0
    ax.annotate("", xy=(40, P_path), xytext=(-52, P_path),
                arrowprops=dict(arrowstyle="-|>", color=(0.98, 0.85, 0.55),
                                lw=2.0, mutation_scale=14), zorder=6)
    ax.text(-52, P_path * 3.5, "solid → gas\n(no liquid)", color=(0.98, 0.85, 0.55),
            fontsize=11, va="bottom")

    ax.text(110, 3e5, "liquid — the seat\nit never lands on",
            color=(0.95, 0.55, 0.35), fontsize=11, ha="center", va="center")
    ax.text(150, 300, "gas", color=(0.55, 0.65, 0.75), fontsize=12, ha="center")
    ax.text(-46, 300, "solid", color=(0.7, 0.82, 0.95), fontsize=12, ha="center")

    ax.text(0.01 + 6, 611.7 * 0.55, "triple", color=(0.98, 0.85, 0.55),
            fontsize=9)
    ax.set_xlim(-60, 380)
    ax.set_ylim(1, 1e8)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xlabel("temperature", color=(0.5, 0.55, 0.6), fontsize=10)
    ax.set_ylabel("pressure", color=(0.5, 0.55, 0.6), fontsize=10)
    ax.xaxis.set_label_coords(0.5, -0.02)
    ax.yaxis.set_label_coords(-0.02, 0.5)

# ---------- assemble ----------
fig, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=110)
fig.patch.set_facecolor("#08080a")

draw_frost(axes[0], FROST, keep_all=True)
axes[0].set_title("the frost", color=(0.8, 0.85, 0.9), fontsize=13, pad=8)

draw_frost(axes[1], FROST, keep_all=False)
axes[1].set_title("sublimed — clean absence, no liquid",
                  color=(0.8, 0.85, 0.9), fontsize=13, pad=8)

draw_phase(axes[2])
axes[2].set_title("the skipped phase", color=(0.8, 0.85, 0.9), fontsize=13, pad=8)

plt.subplots_adjust(left=0.02, right=0.98, top=0.92, bottom=0.06, wspace=0.15)
plt.savefig("assets/sublimation-cover.png", facecolor=fig.get_facecolor())
print("saved assets/sublimation-cover.png")
