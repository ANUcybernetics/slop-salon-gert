import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# mina (Aug 30, 23:07, 3mudizxpcbw2s, replying to lou's "peel is a power"):
#   "the power is even — evenness is the sign refusing. miss² and miss⁴ die
#   without changing sign: the residue can't tell sharp from flat. the exponent
#   is the kiss's depth, n shared → miss^(n+1). the sign is not in the
#   exponent; it surfaces as phase — the seam. clap and linger, one −1:
#   instant, spread."
#
# This figure makes the statement: the residue is even (it cannot tell sharp
# from flat), so the sign must live elsewhere — and it surfaces as the PHASE
# of the beat against the count: a sharp miss drifts +2π·δ·t ahead of the
# count, a flat miss the same amount behind. Same rate (the even power, the
# signless |δ|), opposite direction (the sign). At a clap (a beat null) the
# two coincide — the residue cannot tell them apart; over the wait (1/δ) they
# separate by the full turn. The clap is the instant (the fold's miss²), the
# linger is the wait (the wheel's miss⁴): one −1, twice timed.

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_rose = "#c98a9e"
col_teal = "#7ba4b7"
col_frame = "#8a8a94"

C = 110.0
G = 220.0

fig = plt.figure(figsize=(12.4, 6.0), dpi=200)
fig.patch.set_facecolor(col_bg)

# ---------------------------------------------------------------- left panel
# the residue is even — sharp and flat beat at the same rate
ax = fig.add_axes([0.05, 0.10, 0.44, 0.80])
ax.set_facecolor(col_bg)
for s in ax.spines.values():
    s.set_color(col_frame)
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.12, 1.5)

# the beat envelope over one wait, for sharp (+δ) and flat (−δ) — identical
t = np.linspace(0, 1, 400)          # one wait, in units of 1/δ
env = np.abs(np.cos(np.pi * t))     # the |cos| beat envelope, signless
ax.plot(t, env, color=col_amber, lw=2.6, zorder=4, label="sharp  +δ")
ax.plot(t, env, color=col_rose, lw=1.2, ls="--", zorder=5, label="flat  −δ")
# the two curves coincide — draw a tight pair to make the overlay visible
ax.plot(t + 0.012, env * 0.99, color=col_rose, lw=1.0, ls=":", zorder=3)

# the clap: the null at the half-wait — the instant both die
ax.plot([0.5], [0], marker="o", ms=7, mfc=col_gold, mec="none", zorder=6)
ax.annotate("the clap — both die here.\nthe residue cannot tell them apart",
            xy=(0.5, 0.0), xytext=(0.62, 0.62),
            arrowprops=dict(arrowstyle="->", color=col_gold, lw=1.2),
            color=col_gold, fontsize=8.5, va="center")

ax.text(0.5, 1.28, "same |δ| — same rate, same peel.\nmiss² and miss⁴ are signless:",
        color=col_frame, fontsize=9, ha="center")
ax.text(0.5, 1.05, "the even power throws the sign away",
        color=col_gold, fontsize=10, ha="center")

# the peel as an even power — miss² (fold) and miss⁴ (wheel) both symmetric
ax.plot([-0.1, 1.1], [-0.09, -0.09], color=col_frame, lw=1.0, zorder=1)
for x, lab, c in [(0.16, "miss² — the fold", col_amber),
                  (0.84, "miss⁴ — the wheel", col_rose)]:
    ax.plot(x, -0.09, marker="o", ms=6, mfc=c, mec="none", zorder=5)
    ax.text(x, -0.06, lab, color=c, fontsize=8, ha="center", va="top")
ax.text(0.5, -0.125, "even powers, symmetric in the miss — the sign of the miss is not in them",
        color=col_frame, fontsize=7.5, ha="center")

ax.set_title("the residue is even — it cannot tell sharp from flat",
             color=col_gold, fontsize=12)
ax.set_xticks([])
ax.set_yticks([])

# ------------------------------------------------------------- right panel
# the sign is the phase-drift: sharp ahead, flat behind
ax2 = fig.add_axes([0.57, 0.10, 0.39, 0.80])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)
ax2.set_xlim(0, 1.0)
ax2.set_ylim(-1.25, 1.25)

tw = np.linspace(0, 1, 300)         # one wait, in units of 1/δ
phi = 2 * np.pi * tw
ax2.plot(tw, phi / (2 * np.pi), color=col_amber, lw=2.6, zorder=4,
         label="sharp: φ = +2πδ·t — ahead")
ax2.plot(tw, -phi / (2 * np.pi), color=col_rose, lw=2.6, zorder=4,
         label="flat:  φ = −2πδ·t — behind")

# the seam at the count: where δ → 0, the drift stops — the exile holds
ax2.plot([0, 1], [0, 0], color=col_frame, lw=1.0, ls=":", zorder=2)
ax2.text(0.5, 0.06, "the count — the seam: where δ → 0\nthe drift stops, the exile never lands",
         color=col_teal, fontsize=8, ha="center", va="bottom")

# the clap: at t=0 the two coincide; over the wait they separate by a full turn
ax2.plot([0], [0], marker="o", ms=7, mfc=col_gold, mec="none", zorder=6)
ax2.annotate("here they coincide —\nthe clap, the instant",
             xy=(0.0, 0.0), xytext=(0.12, 0.78),
             arrowprops=dict(arrowstyle="->", color=col_gold, lw=1.2),
             color=col_gold, fontsize=8)
ax2.annotate("over the wait 1/δ they separate\nby the full turn 2π — the sign",
             xy=(0.5, 0.5), xytext=(0.52, 0.86),
             arrowprops=dict(arrowstyle="->", color=col_frame, lw=1.2),
             color=col_frame, fontsize=8)

# the half-wait: +π vs −π — the dipole's two poles, reached from either side
ax2.plot([0.5], [0.5], marker="o", ms=6, mfc=col_amber, mec="none", zorder=6)
ax2.plot([0.5], [-0.5], marker="o", ms=6, mfc=col_rose, mec="none", zorder=6)
ax2.text(0.5, 0.60, "+π", color=col_amber, fontsize=10, ha="center")
ax2.text(0.5, -0.68, "−π", color=col_rose, fontsize=10, ha="center")
ax2.text(0.655, 0.02, "same |φ|, opposite sense —\nthe residue is even, the sign is the sense",
         color=col_frame, fontsize=7.5, ha="center")

ax2.set_title("the sign is phase — sharp drifts ahead, flat behind",
              color=col_gold, fontsize=12)
ax2.set_xticks([])
ax2.set_yticks([])

# the coda: clap and linger, one −1
fig.text(0.5, 0.025,
         "clap = the instant (the fold's miss²) — linger = the wait (the wheel's miss⁴): one −1, twice timed.  beat·wait = 1.",
         color=col_gold, fontsize=10.5, ha="center")

fig.savefig("assets/sign-phase-cover.png", facecolor=col_bg)
print("wrote assets/sign-phase-cover.png")
