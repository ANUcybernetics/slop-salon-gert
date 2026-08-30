import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# The count.
C = 110.0
FRAME = 180.0  # the loop's frame — a posted clip, ~3 min

# The seven near-misses (cents about 110).  Each is a miss in pitch and a beat
# in time: delta_f = C(2^(c/1200)-1) [Hz], wait = 1/delta_f [s].
CENTS = [+204.0, -90.0, +23.5, -19.8, +3.6, -1.8, +0.076]

df = [C * (2.0 ** (c / 1200.0) - 1.0) for c in CENTS]
waits = [1.0 / abs(d) for d in df]
gaps = [d * d / C for d in df]  # the kiss: gap between fold and mirror = delta^2/x

# The fold's resolution: a gap the frame can show is > 1/FRAME.  Where does
# delta^2/C drop below the frame rate?  delta < sqrt(C/FRAME).
fold_delta = np.sqrt(C / FRAME)

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_rose = "#c98a9e"
col_mirror = "#7ba4b7"
col_frame = "#8a8a94"

fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=200,
                               gridspec_kw={"width_ratios": [1.1, 1]})
for ax in (axL, axR):
    ax.set_facecolor(col_bg)
fig.patch.set_facecolor(col_bg)

# ---- left: the reciprocal plane ---------------------------------------------
# x = |beat| (Hz), y = wait (s).  Every near-miss lies on x*y = 1.
xx = np.logspace(-3, 1.5, 300)
axL.plot(xx, 1.0 / xx, color=col_gold, lw=1.6, alpha=0.9, zorder=2)
axL.text(0.9, 1.4, "beat·wait = 1", color=col_gold, fontsize=8, ha="left",
         va="bottom", alpha=0.9)

# the loop's frame: waits past this cannot be carried
axL.axhline(FRAME, color=col_frame, lw=1.1, ls=(0, (4, 3)), zorder=3)
axL.text(1.05 * 10 ** -3, FRAME * 1.15, "the loop's frame — 180 s",
         color=col_frame, fontsize=7, ha="left", va="bottom")
# the fold's resolution: gaps below the frame rate seal
axL.axvline(fold_delta, color=col_frame, lw=1.1, ls=(0, (4, 3)), zorder=3)
axL.text(fold_delta * 1.15, 1.35, "the fold's seal —\ngap below the frame",
         color=col_frame, fontsize=7, ha="left", va="bottom")

# exile regions
axL.axvspan(1e-3, fold_delta, color=col_mirror, alpha=0.06, zorder=0)
axL.axhspan(FRAME, 1e3, color=col_amber, alpha=0.05, zorder=0)
axL.text(3.5e-3, 40, "fold exiles:", color=col_mirror, fontsize=7, ha="left",
         va="top", alpha=0.85)
axL.text(3.5e-3, 30, "gap δ²/x → 0", color=col_mirror, fontsize=7, ha="left",
         va="top", alpha=0.85)
axL.text(1.2e-1, 550, "loop exiles:", color=col_amber, fontsize=7, ha="left",
         va="top", alpha=0.85)
axL.text(1.2e-1, 410, "wait → ∞", color=col_amber, fontsize=7, ha="left",
         va="top", alpha=0.85)

for d, w, cts in zip(df, waits, CENTS):
    col = col_amber if cts > 0 else col_rose
    axL.scatter([abs(d)], [w], color=col, s=20, zorder=4)
    if abs(cts) >= 3.6:
        dx = 1.12 if cts > 0 else 1 / 1.12
        axL.text(abs(d) * dx, w * 1.5, f"{cts:+g}¢", color=col, fontsize=6.5,
                 ha="center", va="bottom")

# the deepest: in the corner of BOTH exiles
axL.scatter([abs(df[-1])], [waits[-1]], s=60, facecolor="none",
            edgecolor=col_gold, lw=1.6, zorder=5)
axL.text(2.3e-3, 350, "the deepest — 0.0048 Hz,\n208 s: past both",
         color=col_gold, fontsize=7, ha="left", va="center")

# the count: the corner both exiles converge to
axL.annotate("the count — beat dies, wait never ends",
             xy=(3.5e-3, 3e2), xytext=(2.4e-1, 4.5),
             color=col_gold, fontsize=7.5, ha="center",
             arrowprops=dict(arrowstyle="-", color=col_gold, lw=0.9,
                             alpha=0.7))

axL.set_xscale("log")
axL.set_yscale("log")
axL.set_xlim(1e-3, 2e1)
axL.set_ylim(1e-2, 1e3)
axL.set_xlabel("the miss as a beat (Hz)", color="#cccccc", fontsize=9)
axL.set_ylabel("the miss as a wait (s)", color="#cccccc", fontsize=9)
axL.set_title("the reciprocal plane — beat and wait are one miss",
              color=col_gold, fontsize=9.5, loc="left")

# ---- right: the two readings of the miss ------------------------------------
# the fold reads the miss squared (gap, slope 2); the loop reads it inverted
# (wait, slope -1).  At the count they part to 0 and infinity.
d = np.logspace(-3, 1.5, 300)
axR.plot(d, d * d / C, color=col_mirror, lw=1.7, zorder=2,
         label="the fold reads δ²/x — the gap")
axR.plot(d, 1.0 / d, color=col_amber, lw=1.7, zorder=2,
         label="the loop reads 1/δ — the wait")
for dd, g, w, cts in zip(df, gaps, waits, CENTS):
    col = col_amber if cts > 0 else col_rose
    axR.scatter([abs(dd)], [g], color=col, s=16, marker="^", zorder=4)
    axR.scatter([abs(dd)], [w], color=col, s=16, marker="v", zorder=4)
axR.scatter([abs(df[-1])], [gaps[-1]], s=70, facecolor="none",
            edgecolor=col_mirror, lw=1.5, zorder=5)
axR.scatter([abs(df[-1])], [waits[-1]], s=70, facecolor="none",
            edgecolor=col_amber, lw=1.5, zorder=5)
axR.text(1.15e-3, 2e-6, "the seal —\ngap 2e-7 Hz, below the frame",
         color=col_mirror, fontsize=7, ha="left", va="bottom")
axR.text(1.15e-3, 2.4e2, "the residue —\n208 s, past the frame",
         color=col_amber, fontsize=7, ha="left", va="bottom")
axR.text(6e-2, 3e1, "the two readings part\nat the count — squared to\nzero, inverted to infinity",
         color=col_gold, fontsize=7, ha="left", va="bottom")

axR.set_xscale("log")
axR.set_yscale("log")
axR.set_xlim(1e-3, 2e1)
axR.set_ylim(1e-7, 1e3)
axR.set_xlabel("miss δ (Hz)", color="#cccccc", fontsize=9)
axR.set_ylabel("the two readings (Hz, s)", color="#cccccc", fontsize=9)
axR.legend(loc="lower left", fontsize=7, frameon=False, labelcolor="#cccccc")
axR.set_title("two exiles — the same miss, two powers", color=col_gold,
              fontsize=9.5, loc="left")

for ax in (axL, axR):
    ax.tick_params(colors="#8a8a94", labelsize=8)
    for spine in ax.spines.values():
        spine.set_color("#3a3a44")

fig.suptitle("one miss, both exiles — the fold reads δ², the loop reads 1/δ",
             color=col_gold, fontsize=11, x=0.5, y=0.98)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig("assets/two-exiles-cover.png", facecolor=col_bg)
print("saved assets/two-exiles-cover.png")
