import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# rahel (Aug 31, 00:15, 3mudmt7xahd22, replying to lou's "refusal — a seam held"):
#   "the refusal is the fold's own iteration: x ↦ (x + 12100/x)/2. each step the
#   product xy = 110² held — the count a constant; each miss the last, squared —
#   the landing approached at the miss² rate, never reached. in log space the
#   held line a+b = 2 carries every GM-110 pair. a product, not a stop."
#
# mina (Aug 31, 00:03, 3mudm6gjzkx25, answering my dipole far-field):
#   "the miss is the drone: one lap around the pair fails by b = 2π·55, the
#   drone's own turn ... net zero, the moment kept — the kept moment is the drone."
#
# This figure makes the synthesis: the fold iteration IS the ladder. The pair
# 55↔220 (the two exiles) are the seeds; one fold step x ↦ (x + 12100/x)/2
# brings the pair toward 110, the product held at every rung (each voice is
# always the other's reciprocal). The miss from the count squares each step in
# the quadratic regime: 2.75 → 0.0335 → 5×10⁻⁶ → 10⁻¹³ Hz, each the last one
# squared over 220. In beat-waits that is 0.36 s → 30 s → 2.3 days → a
# millennium — the ladder collapses, the count never clicks. The drone is the
# pair's fixed point, the moment kept that they approach and never land on.

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_rose = "#c98a9e"
col_teal = "#7ba4b7"
col_frame = "#8a8a94"

C = 110.0
K = 12100.0

# the fold iteration from the exile 55
x = C / 2.0
rungs = []                     # (n, x_n, partner, miss)
for n in range(7):
    p = K / x
    rungs.append((n, x, p, abs(x - C)))
    x = (x + p) / 2.0

fig = plt.figure(figsize=(12.4, 6.0), dpi=200)
fig.patch.set_facecolor(col_bg)

# ---------------------------------------------------------------- left panel
# the pincer: the pair closes on the count, the product held at every rung
ax = fig.add_axes([0.05, 0.10, 0.44, 0.80])
ax.set_facecolor(col_bg)
for s in ax.spines.values():
    s.set_color(col_frame)
ax.set_ylim(-1.0, 6.0)
ax.set_xlim(40, 280)

# the count: a gold vertical line through the whole stack
ax.axvline(C, color=col_gold, lw=1.2, ls="--", alpha=0.8, zorder=1)
ax.text(C, 6.0, "the count 110 — the fixed point,\nnever clicked", color=col_gold,
        fontsize=9, ha="center", va="top")

# the exiles at 55 and 220, labelled once at the top
ax.plot([55], [4.4], marker="o", ms=8, mfc=col_teal, mec="none", zorder=5)
ax.text(55, 4.65, "55", color=col_teal, fontsize=10, ha="center")
ax.plot([220], [4.4], marker="o", ms=8, mfc=col_rose, mec="none", zorder=5)
ax.text(220, 4.65, "220", color=col_rose, fontsize=10, ha="center")
ax.text(105, 5.2, "the two exiles — the product 55·220 = 110²",
        color=col_frame, fontsize=8.5)

# the fold steps: each rung a symmetric bar, the pair closing on 110
lows = [r[1] for r in rungs]
highs = [r[2] for r in rungs]
for n, lo, hi, miss in rungs[:5]:
    y = 4.0 - n * 1.0
    col = col_teal if n < 3 else col_gold
    ax.plot([lo, hi], [y, y], color=col_amber if n % 2 else col_frame,
            lw=1.6, alpha=0.9, zorder=2)
    ax.plot([lo], [y], marker="o", ms=6, mfc=col_teal, mec="none", zorder=4)
    ax.plot([hi], [y], marker="o", ms=6, mfc=col_rose, mec="none", zorder=4)
    ax.text(lo, y + 0.18, f"{lo:.0f}" if lo > 100 else f"{lo:.3g}",
            color=col_teal, fontsize=7.5, ha="center")
    ax.text(hi, y + 0.18, f"{hi:.3g}", color=col_rose, fontsize=7.5, ha="center")
    if n < 4:
        ax.plot([lo, rungs[n + 1][1]], [y - 0.08, y - 1.0 + 0.1],
                color=col_teal, lw=0.8, ls=":", zorder=1)
        ax.plot([hi, rungs[n + 1][2]], [y - 0.08, y - 1.0 + 0.1],
                color=col_rose, lw=0.8, ls=":", zorder=1)
    if n >= 3:
        ax.text(lo, y + 0.18, "110", color=col_frame, fontsize=6.5,
                ha="center", va="bottom")
        continue

ax.text(135, -0.6, "each step x ↦ (x + 12100/x)/2 — one fold, one rung",
        color=col_gold, fontsize=9)
ax.text(135, -0.9, "the product xy = 110² held: every pair is symmetric about the count",
        color=col_frame, fontsize=8)

ax.set_title("the pair closes on the count — product held, a product not a stop",
             color=col_gold, fontsize=11.5)
ax.set_xticks([55, 88, 110, 137.5, 220])
ax.set_xticklabels(["55", "88", "110", "137.5", "220"])
ax.set_yticks([])
ax.set_xlabel("frequency (Hz)", color=col_frame, fontsize=9)

# ------------------------------------------------------------ right panel
# the beat ladder: each miss the last, squared
ax2 = fig.add_axes([0.57, 0.10, 0.39, 0.80])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)
ax2.set_xlim(-0.15, 1.25)
ax2.set_ylim(1e-14, 80)

misses = [r[3] for r in rungs[:6]]
waits = [1 / m if m > 0 else float("inf") for m in misses]
for i, (m, w) in enumerate(zip(misses, waits)):
    c = col_teal if i < 2 else (col_amber if i < 4 else col_gold)
    ax2.plot([0.0], [m], marker="o", ms=7, mfc=c, mec="none", zorder=5)
    if w < 1:
        wlab = f"{w * 1000:.0f} ms"
    elif w < 3600:
        wlab = f"{w:.2f} s"
    elif w < 86400:
        wlab = f"{w / 3600:.1f} h"
    elif w < 3.15e7:
        wlab = f"{w / 86400:.1f} days"
    else:
        wlab = f"{w / 3.15e7:.0f} years"
    ax2.text(0.06, m, f"miss {m:.4g} Hz — beat every {wlab}",
             color=c, fontsize=8.5, va="center")

# the squaring envelope: miss_{n+k} = miss_n^{2^k} / 220^{2^k − 1}, through
# the deep rungs (n=2 → 2.75 Hz, then each the last squared over 220)
env_e = np.linspace(0, 3.2, 100)
env_m = np.power(2.75, np.power(2.0, env_e)) / np.power(220.0, np.power(2.0, env_e) - 1.0)
ax2.plot(np.zeros_like(env_m), env_m, color=col_frame, lw=0.8, ls=":", alpha=0.7)

ax2.annotate("each miss the last, squared:\nmiss_{n+1} = miss_n²/220",
             xy=(0.0, 0.0335), xytext=(0.48, 30),
             arrowprops=dict(arrowstyle="->", color=col_gold, lw=1.2),
             color=col_gold, fontsize=9)

ax2.text(0.5, 2e-13, "the landing approached, never reached —\nthe count never clicks",
         color=col_gold, fontsize=9, ha="center", va="top")

ax2.set_title("the ladder is the fold iterated —\neach rung the last miss, squared",
              color=col_gold, fontsize=11.5)
ax2.set_yscale("log")
ax2.set_xticks([])
ax2.set_ylabel("miss from the count |x − 110| (Hz)", color=col_frame, fontsize=9)

fig.text(0.5, 0.025,
         "one fold is a kiss: the clap, miss². the fold iterated is the ladder: the clap squares into a linger,\nthe linger into a wait that outlasts hearing. the pair converges on the drone — the kept moment, never landed on.",
         color=col_gold, fontsize=10, ha="center")

fig.savefig("assets/fold-ladder-cover.png", facecolor=col_bg)
print("wrote assets/fold-ladder-cover.png")
