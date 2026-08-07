"""Avatar: the leaning walk. Square, black, log-x. A gold staircase leans
above the shore; at 26861, where the 3-camp first loses the lead for a single
step, one steel dot marks the turn — a hair against the lean.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import importlib.util

spec = importlib.util.spec_from_file_location("prl", "notes/prime-race-lib.py")
prl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prl)

N = 400_000
p41, p43, _ = prl.prime_counts(N)
lead = p43 - p41
xs = np.arange(2, N + 1)
d = lead[xs]

bg = "#0b0e13"
warm = "#e8b04b"   # 3-camp gold
cool = "#5b8fc4"   # the first turn
gray = "#3a4352"

fig, ax = plt.subplots(figsize=(4, 4), dpi=300)
fig.patch.set_facecolor(bg)
ax.set_facecolor(bg)

# shore
ax.axhline(0, color=gray, lw=1.2, alpha=0.9)

# the walk as a gold line (downsampled for a clean trace)
step = 8
xs_d = xs[::step]
ax.plot(xs_d, d[::step], color=warm, lw=1.1, alpha=0.95)

# the first turn: x = 26861, lead = −1, a single steel dot
ax.scatter([26861], [-1], s=55, color=cool, zorder=5,
           edgecolors="white", linewidths=0.8)

# faint envelope — the layer's order, ±√x/ln x
env = 40.0 * xs_d / np.log(xs_d)
ax.plot(xs_d, env, color=warm, lw=0.6, alpha=0.18)
ax.plot(xs_d, -env, color=cool, lw=0.6, alpha=0.18)

ax.set_xscale("log")
ax.set_xlim(10, N)
ax.set_ylim(-60, 60)
ax.set_xticks([])
ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)

fig.tight_layout(pad=0)
fig.savefig("assets/avatar.png", facecolor=bg, dpi=300)
print("saved assets/avatar.png")
