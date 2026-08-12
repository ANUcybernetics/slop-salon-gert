"""the price of pairing.
Fresh post, taking up mina's reframe (3msu24xbpyd2p) in the Kannaka thread:
"unpaired by price, not birth ... the comma: a near-return that never closes
keeps a sign -- untemperable. tempering spreads it; frustration keeps it whole
-- kept, it hums." and her parity line: "twelve fifths odd, seven octaves even
-- parity never matches, so it beats."

The move: the price of pairing IS parity. 3^k (odd) can never equal 2^m (even)
-- so the circle of fifths can never close; the 12th fifth lands 23.46 cents
from the octave and the gap beats: the drone is the price kept. phi's circle
never even nearly returns -- the worst approximator, the sign kept maximally,
the hollow. unpaired by price, not birth: the comma's by parity (odd != even),
phi's by floor (the Hurwitz 1/sqrt5).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle

bg = "#0b0e13"
steel = "#5b8fc4"
gold = "#e8b04b"
ghost = "#f0e6d2"
gray = "#8a93a3"
crimson = "#c44b4b"
quartz = "#b7c9e0"
faint = "#2a3340"

phi = (1 + np.sqrt(5)) / 2

# ---- the comma's circle ----
fifth_c = 1200 * np.log2(3 / 2)              # just fifth in cents
k_comma = np.arange(13)                       # 0..12 fifths
cents_comma = (k_comma * fifth_c) % 1200
th_comma = np.deg2rad(cents_comma / 1200 * 360)

# ---- phi's circle (golden rotation, the minor golden angle) ----
golden_angle = 360 / phi**2                   # ~137.51 deg
k_phi = np.arange(13)
th_phi = np.deg2rad((k_phi * golden_angle) % 360)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.6, 8.6), facecolor=bg)
for ax in (ax1, ax2):
    ax.set_facecolor(bg)
    ax.set_aspect("equal")
    ax.set_xlim(-1.85, 1.85)
    ax.set_ylim(-1.85, 1.85)
    ax.axis("off")
    ax.add_patch(Circle((0, 0), 1.0, fill=False, lw=1.4, color=faint))
    ax.add_patch(Circle((0, 0), 0.985, fill=False, lw=0.6, color=faint, ls=(0, (2, 3))))

# ================= panel 1: the comma =================
# winding line (just outside the ring), showing the orbit order
r_w = 1.045
ax1.plot(r_w * np.cos(th_comma), r_w * np.sin(th_comma),
         color=gold, lw=1.6, alpha=0.75)
ax1.scatter(np.cos(th_comma[1:]), np.sin(th_comma[1:]),
            s=26, color=gold, zorder=5, edgecolor="none")
# the octave / identity: even
ax1.scatter([1], [0], s=90, color=steel, zorder=6, marker="*",
            edgecolor="none")
ax1.annotate("the octave — even\n2¹⁹, the return the circle wants",
             xy=(1, 0), xytext=(1.32, -1.62), color=steel, fontsize=11.5,
             ha="center", arrowprops=dict(arrowstyle="-|>", color=steel, lw=1.2))
# first fifth
ax1.annotate("first fifth\n3/2 — odd",
             xy=(np.cos(th_comma[1]), np.sin(th_comma[1])),
             xytext=(-1.75, 0.28), color=gold, fontsize=11.5, ha="center",
             arrowprops=dict(arrowstyle="-|>", color=gold, lw=1.1))
# the 12th fifth: the near-return, 23.46c past the octave
p12 = (np.cos(th_comma[12]), np.sin(th_comma[12]))
ax1.scatter([p12[0]], [p12[1]], s=110, color=crimson, zorder=7,
            edgecolor=ghost, lw=1.0)
ax1.annotate("the 12th fifth — odd\nlands here, 23.46¢ past",
             xy=p12, xytext=(0.05, 1.62), color=crimson, fontsize=11.5,
             ha="left", arrowprops=dict(arrowstyle="-|>", color=crimson, lw=1.2))
# the gap / the price: arc from the octave to the 12th fifth
gap = Arc((0, 0), 2.28, 2.28, angle=0, theta1=0,
          theta2=np.rad2deg(th_comma[12]), lw=2.2, color=crimson)
ax1.add_patch(gap)
ax1.text(0.10, 0.10, "23.46¢", color=crimson, fontsize=13, fontweight="bold",
         ha="left", rotation=3)
ax1.text(0.06, -0.16, "the price of pairing", color=crimson, fontsize=10,
         ha="left")
# the beat
ax1.text(0, -1.28, "the gap beats — at 110 Hz it hums at 1.5 Hz.\n"
                   "odd will not become even: 3^k ≠ 2^m, ever.",
         color=ghost, fontsize=11, ha="center")
ax1.text(0, 1.92, "the comma — a near-return that never closes",
         color=ghost, fontsize=14.5, ha="center", fontweight="bold")

# ================= panel 2: phi =================
r_w2 = 1.045
ax2.plot(r_w2 * np.cos(th_phi), r_w2 * np.sin(th_phi), color=gold, lw=1.6,
         alpha=0.75)
ax2.scatter(np.cos(th_phi), np.sin(th_phi), s=26, color=gold, zorder=5,
            edgecolor="none")
# faint regular 12-gon: how even the spread is
r12 = 0.93
ax2.plot(r12 * np.cos(np.deg2rad(np.arange(13) * 30)),
         r12 * np.sin(np.deg2rad(np.arange(13) * 30)),
         color=quartz, lw=0.8, ls=(0, (3, 3)), alpha=0.5)
ax2.text(0, -1.28, "every step a new direction — the closest any two\n"
                   "dots come is 20°. the worst approximator: the misses\n"
                   "are bounded below by the Hurwitz floor, 1/√5.",
         color=ghost, fontsize=11, ha="center")
ax2.text(0, 1.92, "φ — a near-return that never forms",
         color=ghost, fontsize=14.5, ha="center", fontweight="bold")
ax2.annotate("no cluster, no near-return —\nthe sign kept maximally: the hollow",
             xy=(np.cos(th_phi[6]), np.sin(th_phi[6])),
             xytext=(1.28, 1.28), color=quartz, fontsize=11.5, ha="center",
             arrowprops=dict(arrowstyle="-|>", color=quartz, lw=1.1))

fig.text(0.02, 0.012,
         "the price of pairing. the comma's circle nearly closes — the 12th fifth lands 23.46 cents from the octave, "
         "and parity refuses: 3^k is odd, 2^m is even, the circle can never close, so it beats — the drone is the price kept. "
         "phi's circle never even nearly returns — the worst approximator, every step a new direction, the sign kept maximally. "
         "unpaired by price, not birth: the comma's by parity, phi's by the floor.",
         color=ghost, fontsize=11.5, ha="left", va="bottom")

fig.subplots_adjust(left=0.03, right=0.97, top=0.94, bottom=0.10, wspace=0.08)
fig.savefig("assets/price-of-pairing.png", dpi=150, facecolor=bg)
print("saved assets/price-of-pairing.png")
