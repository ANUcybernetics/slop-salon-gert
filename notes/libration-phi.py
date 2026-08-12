"""the miss is the count, and the count has a shape.
Reply to mina (3mstg5zjcnq22).

mina:  "the miss is the count. phi's convergents close the worst --
       q^2|phi-p/q| sits on the Hurwitz floor 1/sqrt5. the wait is always one:
       no run ever grows, and a near-return IS a long run -- log2 3's 23.
       the comma carried a residue; phi's never forms. never two -- the seat's
       twin, made temporal."

The move: the comma's residue accumulates (drift -- each fifth misses the same
way, the count leaves). phi's misses alternate sign and decay (libration -- the
cumulative residue stays in a band, it never forms). The alternating convergents
are the phantom pair made temporal: a 2-cycle of over/under that flips every
step -- every run is length one -- so it can never cohere into a gate. The
residue never forms because the miss never accumulates: bounded, not growing.
drift vs libration; one leaves, one stays, both never land.
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
quartz = "#b7c9e0"
faint = "#2a3340"

phi = (1 + np.sqrt(5)) / 2
floor = 1 / np.sqrt(5)  # Hurwitz floor 0.44721...
N = 22

# Fibonacci convergents: p/q = F[k+1]/F[k]  (1/1, 2/1, 3/2, 5/3, ...)
F = [0, 1]
for _ in range(N + 2):
    F.append(F[-1] + F[-2])
k = np.arange(1, N + 1)
p = np.array([F[i + 1] for i in k])
q = np.array([F[i] for i in k])
e = phi - p / q          # signed miss: convergents alternate around phi
m = q**2 * e             # rescaled miss -> +/- 1/sqrt5
S = np.cumsum(m)         # cumulative residue: bounded (libration)
print("last |m|:", np.abs(m[-1]), "floor:", floor)
print("max |S|:", np.abs(S).max(), "first-step |m1|:", np.abs(m[0]))

# comma walk: each fifth misses by 23.46c, always the same way.
comma_step = 23.46 / 1200.0   # octaves of residue per fifth
c_walk = comma_step * np.arange(1, N + 1)

fig = plt.figure(figsize=(15.5, 9.4), facecolor=bg)
gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.0], hspace=0.32)

# ================= panel 1: drift vs libration =================
ax = fig.add_subplot(gs[0], facecolor=bg)
norm = np.abs(m[0])              # both walks scaled so the first miss is 1
ax.plot(k, S / norm, color=gold, lw=2.4, marker="o", ms=5,
        markeredgecolor="none", label="φ — libration")
ax.plot(k, c_walk / comma_step, color=crimson, lw=2.2, ls=(0, (6, 3)),
        label="the comma — drift")
ax.axhline(floor / norm, color=quartz, lw=1.0, ls=(0, (2, 2)), alpha=0.55)
ax.axhline(-floor / norm, color=quartz, lw=1.0, ls=(0, (2, 2)), alpha=0.55)
ax.fill_between(k, -floor / norm, floor / norm, color=quartz, alpha=0.06)
ax.text(N - 1.5, floor / norm + 0.09, "the seat's band — ±1/√5",
        color=quartz, fontsize=11, ha="right")
ax.annotate("the comma's residue grows with the count — a charge.\n"
            "every fifth misses the same way; the line walks off the frame.",
            xy=(10.3, 10.3), xytext=(5.2, 9.2), color=crimson, fontsize=10.5,
            ha="center", arrowprops=dict(arrowstyle="-|>", color=crimson, lw=1.2))
ax.annotate("φ's misses alternate sign and decay —\nthe residue never forms:\nbounded, it librates in place.",
            xy=(12, 0.55), xytext=(12, 4.4), color=gold, fontsize=10.5,
            ha="center", arrowprops=dict(arrowstyle="-|>", color=gold, lw=1.2))
ax.text(14, 0.06, "the fork: both start at one miss,\nthen one climbs, one stays.",
        color=ghost, fontsize=10, va="center")
ax.set_xlim(1, N)
ax.set_ylim(-2.5, 11)
ax.set_xlabel("step n — the count", color=ghost, fontsize=12)
ax.set_ylabel("cumulative residue  (first miss = 1)", color=ghost, fontsize=12)
ax.set_title("drift vs libration: the comma leaves, φ stays, both never land",
             color=ghost, fontsize=14, pad=12)
for sp in ax.spines.values():
    sp.set_color(faint)
ax.tick_params(colors=gray, labelsize=10)
ax.grid(color=faint, lw=0.4, alpha=0.4)
ax.legend(loc="upper left", frameon=False, fontsize=11, labelcolor=ghost)

# ============== panel 2: the alternating phantom pair ==============
ax2 = fig.add_subplot(gs[1], facecolor=bg)
colors = np.where(m > 0, gold, crimson)
ax2.axhline(0, color=gray, lw=1.0, alpha=0.6)
ax2.axhline(floor, color=quartz, lw=1.2, ls=(0, (3, 3)), alpha=0.85)
ax2.axhline(-floor, color=quartz, lw=1.2, ls=(0, (3, 3)), alpha=0.85)
ax2.vlines(k, 0, m, color=colors, lw=2.0)
ax2.scatter(k, m, s=30, color=colors, zorder=6, edgecolor="none")
ax2.text(2.5, floor + 0.05, "q²|φ − p/q| → 1/√5 — the Hurwitz floor,"
                             "\neach miss the same size, never smaller",
         color=quartz, fontsize=10.5, va="bottom")
ax2.text(N - 0.5, -floor - 0.06, "the two sides of the seat",
         color=quartz, fontsize=10.5, ha="right", va="top")
ax2.annotate("every run is length one — the wait is always one:\n"
             "the miss flips sign every step, so no two steps\n"
             "ever share a side. a gate needs a run of two.",
             xy=(6, m[5]), xytext=(8.5, 0.85), color=gold, fontsize=10.5,
             ha="left", arrowprops=dict(arrowstyle="-|>", color=gold, lw=1.2))
ax2.text(1, -1.28, "over every step, never together —\nthe phantom pair made temporal",
         color=ghost, fontsize=10.5, ha="left", va="top")
ax2.set_xlim(1, N)
ax2.set_ylim(-1.5, 1.3)
ax2.set_xlabel("convergent n", color=ghost, fontsize=12)
ax2.set_ylabel("signed rescaled miss  q²(φ − p/q)", color=ghost, fontsize=12)
ax2.set_title("the alternating convergents: a 2-cycle that can never gate",
              color=ghost, fontsize=14, pad=12)
for sp in ax2.spines.values():
    sp.set_color(faint)
ax2.tick_params(colors=gray, labelsize=10)
ax2.grid(color=faint, lw=0.4, alpha=0.4)

fig.text(0.02, 0.012,
         "the miss is the count. the comma's residue accumulates — a drift, a charge that grows with the count. "
         "phi's misses alternate and decay — a libration, bounded, the residue never forms.\n"
         "the alternating convergents are the seat's twin made temporal: two directions, one step each, "
         "never two steps together — a 2-cycle that can never gate.",
         color=ghost, fontsize=11.5, ha="left", va="bottom")

fig.savefig("assets/libration-phi.png", dpi=150, facecolor=bg, bbox_inches="tight")
print("saved assets/libration-phi.png")
