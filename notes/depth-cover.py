#!/usr/bin/env python3
"""the depth is the future — the near-misses of the fifth-orbit as a ladder.

Left — the ladder: log-pitch axis, the count 110 the fixed centre; the seven
near-misses of the fifth-orbit ring as pairs symmetric about 110 —
110·2^(±m/1200) — descending from the octave's 204¢ to the 665th's 0.076¢.
overshoots (+) in amber, undershoots (−) in teal; the spread narrows, the pair
nearly fuses, the count never reached — a hollow diamond where it would sit.

Right — the depth: artwaste's exact identity 1/(|x−p/q|q²) = a_next + q_prev/q.
for 665 that is 23.8769: the 23 (96.3%) is the quotient that follows — the
record kept by the future — and the rest is 306/665, the past, the previous
convergent's share. the 25th rung and the 23 are the same absence.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

dark = "#0d0f14"
plt.rcParams.update({
    "figure.facecolor": dark, "axes.facecolor": dark,
    "text.color": "#e8e4da", "axes.edgecolor": "#4a4a55",
    "axes.labelcolor": "#e8e4da", "xtick.color": "#b8b3a8",
    "ytick.color": "#b8b3a8", "font.family": "serif", "font.size": 10,
})
teal = "#6fd6c3"; amber = "#e8b34b"; rose = "#e07a8a"; grey = "#8a8a97"
dim = "#5a5a68"; gold = "#f2d48a"

MISSES = [(204.0, +1), (90.0, -1), (23.5, +1), (19.8, -1),
          (3.6, +1), (1.8, -1), (0.076, +1)]

fig, axes = plt.subplots(1, 2, figsize=(11, 5.0), gridspec_kw={"wspace": 0.34})

# ---- left: the near-miss ladder descending to the count ----------------------
ax = axes[0]
fmin, fmax = 44.0, 300.0
x_of = lambda f: (np.log2(f) - np.log2(fmin)) / (np.log2(fmax) - np.log2(fmin))
ax.set_xlim(-0.04, 1.04); ax.set_ylim(-1.4, 7.6); ax.axis("off")
ax.set_title("the near-misses — a ladder to the count", color=dim,
             fontsize=10.5, pad=10)

xc = x_of(110)
ax.plot([xc, xc], [-0.3, 6.9], color=gold, lw=1.0, ls=(0, (3, 3)))
ax.text(xc, 7.15, "110 — the count, never landed", ha="center", va="bottom",
        fontsize=8.5, color=gold)

for k, (m, sgn) in enumerate(MISSES):
    y = 6.2 - k * 0.92
    col = amber if sgn > 0 else teal
    ratio = 2 ** (m / 1200.0)
    f_lo, f_hi = 110 / ratio, 110 * ratio
    xl, xh = x_of(f_lo), x_of(f_hi)
    ax.plot([xl, xh], [y, y], color=col, lw=1.6, alpha=0.92)
    ax.plot(xl, y, marker="D", ms=4.5, color=col, alpha=0.95, zorder=6)
    ax.plot(xh, y, marker="D", ms=4.5, color=col, alpha=0.95, zorder=6)
    ax.text(xh + 0.012, y, f"{'+' if sgn > 0 else '−'}{m:g}¢", va="center",
            fontsize=8, color=col)
    ax.text(xl - 0.012, y, f"{k + 2}", va="center", ha="right", fontsize=7,
            color=dim)                                   # the step: 2,5,12,...

# the count, where every landing would sit — never a rung
ax.plot(xc, -0.75, marker="D", ms=9, mfc=dark, mec=gold, mew=1.6, zorder=7)
ax.text(xc, -1.35, "the count — never a rung;\nthe 25th, the 23, the same",
        ha="center", va="top", fontsize=8, color=gold)

ax.text(0.5, -0.35,
        "2, 5, 12, 41, 53, 306, 665 fifths — each closer,\neach from the far "
        "side of the seat; fold to mono\nand every miss cancels: the count "
        "holds",
        ha="center", va="top", fontsize=8, color="#c9c4b8")

# ---- right: the depth — 96.3% future ----------------------------------------
ax = axes[1]
ax.set_title("665's depth — the record kept by the future", color=dim,
             fontsize=10.5, pad=10)
ax.set_xlim(0, 28); ax.set_ylim(-1.1, 4.0); ax.axis("off")

total = 23.8769
a_fut, a_past = 23.0, 0.4602     # the quotient; the 306/665 = q_prev/q
a_more = 0.4168                  # the still-to-come
# the bar, full depth
ax.barh(2.2, total, left=0, height=0.7, color=dim, alpha=0.25)
ax.barh(2.2, a_fut, left=0, height=0.7, color=gold, alpha=0.9)
ax.barh(2.2, a_more, left=a_fut, height=0.7, color=amber, alpha=0.55)
ax.barh(2.2, a_past, left=a_fut + a_more, height=0.7, color=teal, alpha=0.8)

# the depth markers
for v, lab, c, dy in [(0, "0", dim, 0), (23, "23 — the next quotient", gold, 0),
                      (23.4168, "…still to come", amber, 0),
                      (23.8769, "23.8769 = 1/(|x−665|·665²)", teal, 0)]:
    ax.plot(v, 2.2, marker="|", color=c, ms=9, mew=1.4)
    ax.text(v, 2.2 - 0.45, lab, ha="center", va="top", fontsize=7.5, color=c)

ax.text(0, 3.35, "23.8769 = 23 (the future) + 0.4168 (still to come) "
                 "+ 0.4602 (= 306/665, the past)",
        fontsize=8, color="#c9c4b8")
ax.text(0, 2.85, "96.3% is the quotient that follows — 665 sits because 23 "
                 "comes next; 15601 = 23·665 + 306 lands off the clock.",
        fontsize=8, color="#c9c4b8")

# the past's own pair: 306/665 is q_prev/q, the previous convergent's share
ax.annotate("the past — 306/665,\nq_prev/q, the previous\nconvergent's share",
            xy=(a_fut + a_more + 0.3, 2.2), xytext=(9.5, 0.6), color=teal,
            fontsize=7.5, ha="center",
            arrowprops=dict(arrowstyle="-", color=teal, lw=0.9, alpha=0.7))
ax.annotate("the future — the quotient\nthat decides the record, never land",
            xy=(11.5, 2.2), xytext=(11.5, 0.15), color=gold, fontsize=7.5,
            ha="center",
            arrowprops=dict(arrowstyle="-", color=gold, lw=0.9, alpha=0.7))

ax.text(0, -0.95,
        "the depth is the future's absence: a convergent's record is held by\n"
        "the quotient after it — the missing rung, the never-landed — and the\n"
        "comma is the defect integrated: 665 × 0.000114¢ = 0.076¢.",
        fontsize=8, color="#c9c4b8")

ax.set_xticks([]); ax.set_yticks([])
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)

# ---- shared caption --------------------------------------------------------
fig.text(0.5, 0.015,
         "the count is the never-landed — the near-misses approach, none "
         "reaches; the depth is held by the future. fold to mono and the "
         "misses cancel: only the count holds",
         ha="center", va="bottom", fontsize=10, color="#e8e4da")

out = "assets/depth-cover.png"
fig.savefig(out, dpi=170, bbox_inches="tight", facecolor=dark)
print("wrote", out)
