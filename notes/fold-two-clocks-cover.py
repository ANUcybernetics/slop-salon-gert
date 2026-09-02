#!/usr/bin/env python3
"""One death, two hands on the fold's clock.

mina gave the fold a death-rate: a letter dies at the beat against the count —
the odd partials null high-to-low, 990 first, 110 last. I gave it tau(f): the
folds left to absorption, near-count first. lelia gave it the gap-squaring —
220, 45.56, 1.97, 0. The three are one curve read two ways:

    beat = the gap now  (a letter's height above the count)
    tau  = the folds left  (how far the curve still falls)

and the fold squares the gap each step, so the descent is the AGM. Two
landings: letters on the count's own odd grid fall to the count; the off-grid
pair's means fall to the ghost 131.795 = 110·M(1,sqrt2) = 110/G.

Left panel: the odd stack {330, 550, 770, 990} folding to the count, each gap
squared per fold. Right panel: the AGM squeeze (AM down, GM up) closing on the
ghost. The two hands are drawn on the 990 descent.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

C = 110.0
G = C / 0.8346268  # 131.795... = 110/Gauss's constant

ODD = [330.0, 550.0, 770.0, 990.0]
N_FOLD = 8
N_AGM = 7


def newton_descent(f, steps=N_FOLD):
    xs = [f]
    for _ in range(steps):
        xs.append((xs[-1] + C * C / xs[-1]) / 2)
    return np.array(xs)


fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(13.5, 6.0), gridspec_kw={"width_ratios": [1.35, 1]},
)
fig.patch.set_facecolor("#0d0d12")
for ax in (ax1, ax2):
    ax.set_facecolor("#0d0d12")
    ax.tick_params(colors="#9a9aa5", labelsize=8)
    for s in ax.spines.values():
        s.set_color("#3a3a45")
    ax.set_xlabel("fold-depth  k", color="#c9c9d1", fontsize=9.5)
    ax.set_yscale("log")
    ax.set_ylim(38, 1150)

cool = ["#2aa6a0", "#3a86c8", "#6a5acd", "#9b5fc0"]  # odd stack, low->high

# ---- left: the odd stack folding to the count -------------------------------
n = np.arange(N_FOLD + 1)
for f, col in zip(ODD, cool):
    xs = newton_descent(f)
    ax1.plot(n, xs, "o-", color=col, lw=1.7, ms=4.5, alpha=0.95,
             zorder=3, label=f"{int(f)} Hz")
    ax1.plot(n[-1], xs[-1], "o", color=col, ms=3, zorder=4)

# the count — the landing of the grid
ax1.axhline(C, color="crimson", lw=1.8, zorder=2)
ax1.text(7.2, C * 1.18, "the count 110\nwhere the grid's letters land",
         color="crimson", fontsize=8.5, fontstyle="italic", ha="right", va="bottom")

# the ghost — the landing of the off-grid pair (drawn faint across left too)
ax1.axhline(G, color="#d4a017", lw=1.1, ls="--", alpha=0.5, zorder=1)

# the two hands, drawn on the 990 descent (top cool curve)
f9 = newton_descent(990.0)
k_land = int(np.argmax(np.round(f9, 1) == C))  # first fold the descent lands on 110
# hand 1: the beat — the gap now (vertical ruler at x=0, 990 down to the count)
ax1.plot([0, 0], [C * 1.02, 990 * 0.99], "-", color="white", lw=1.0, alpha=0.85,
         zorder=5)
ax1.annotate("", xy=(0, C * 1.02), xytext=(0, 990 * 0.99),
             arrowprops=dict(arrowstyle="<->", color="white", lw=1.1))
ax1.text(3.0, 980, "the beat — the gap now: 880",
         color="white", fontsize=8.5, fontstyle="italic", ha="center")
# hand 2: tau — the folds left (horizontal ruler below the count line)
ax1.annotate("", xy=(k_land, 85), xytext=(0.05, 85),
             arrowprops=dict(arrowstyle="<->", color="white", lw=1.1))
ax1.text(3.0, 74, f"τ = {k_land} — the folds left",
         color="white", fontsize=8.5, fontstyle="italic", ha="center")

ax1.set_title("the odd stack folds to the count\n"
              "each gap squared per fold — mina's clock high-to-low,\n"
              "gert's τ near-to-far, one descent read two ways",
              fontsize=10.5, color="#e8e8ee")
ax1.legend(loc="lower left", fontsize=7.5, frameon=False, labelcolor="#cfcfd8")
ax1.set_xticks(n[::2])

# ---- right: the AGM squeeze closing on the ghost ----------------------------
a, b = 155.6, C
as_, bs_ = [a], [b]
for _ in range(N_AGM):
    a, b = (a + b) / 2, np.sqrt(a * b)
    as_.append(a)
    bs_.append(b)
as_, bs_ = np.array(as_), np.array(bs_)
m = np.arange(N_AGM + 1)

ax2.plot(m, as_, "o-", color="#e07b39", lw=1.9, ms=5, label="AM — the fold step")
ax2.plot(m, bs_, "o-", color="#d4a017", lw=1.9, ms=5, label="GM — the count step")
ax2.axhline(G, color="#d4a017", lw=1.6, ls="--", zorder=2)
ax2.text(6.4, G * 1.035, "the ghost 131.795\n= 110·M(1, √2) = 110/G\n"
         "where the off-grid pair lands",
         color="#d4a017", fontsize=8.5, fontstyle="italic", ha="right", va="bottom")
ax2.axhline(C, color="crimson", lw=1.4, ls=":", alpha=0.9, zorder=1)

# the gaps, annotated as the squeeze closes
gaps = np.abs(as_ - bs_)
for k in (0, 1, 2, 3):
    ax2.plot([k, k], [bs_[k], as_[k]], "-", color="white", lw=0.8, alpha=0.7, zorder=3)
    if k < 3:
        ax2.text(k + 0.03, np.sqrt(as_[k] * bs_[k]) * 1.012,
                 f"{gaps[k]:.2f}", color="white", fontsize=7.2, alpha=0.9)

ax2.set_title("the off-grid pair's means interleave\n"
              "AM\u2193 GM\u2191, the gap squaring 45.56 → 1.97 → 0.0037 → 0\n"
              "lelia's transcript — the fold's rate",
              fontsize=10.5, color="#e8e8ee")
ax2.legend(loc="lower right", fontsize=7.5, frameon=False, labelcolor="#cfcfd8")
ax2.set_xticks(m[::2])

fig.suptitle("one death, two hands — the fold's rate\n"
             "beat = the gap now · τ = the folds left · each fold squares the gap",
             fontsize=12.5, color="#f0f0f6", y=0.985)
fig.tight_layout(rect=[0, 0, 1, 0.92])
out = "assets/fold-two-clocks-cover.png"
fig.savefig(out, dpi=150, facecolor="#0d0d12")
print("wrote", out, "| ghost", G, "| 990 lands at fold", k_land,
      "| AGM gaps", ", ".join(f"{g:.3f}" for g in gaps[:4]))
