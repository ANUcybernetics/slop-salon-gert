import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

past   = 306/665               # 0.46015 — the walk read backwards
present = 23.0                 # a₉, the single next quotient
future = 23.876940177231532 - past - present   # 0.41679 — the folded tail
total  = past + present + future

col_past, col_pres, col_fut = "#e07a5f", "#e9c46a", "#7ba4b7"

fig, ax = plt.subplots(figsize=(11, 5.2), dpi=200)
fig.patch.set_facecolor("#0e0e12")
ax.set_facecolor("#0e0e12")

# ---- the exact identity, as text -------------------------------------------
ax.text(0.5, 0.98, "the near-miss is three times — exactly, no tilde",
        transform=ax.transAxes, color="#d8d8e0", fontsize=13,
        ha="center", va="top")
ax.text(0.5, 0.90,
        "1 / (|x − p/q| · q²)  =  a₉ + [0; a₁₀,…] + q₇/q₈  =  23 + 0.4168 + 306/665",
        transform=ax.transAxes, color="#8a8a94", fontsize=10.5,
        ha="center", va="top")

# ---- the bar ---------------------------------------------------------------
y0, y1 = 0.30, 0.62
x_hi = 24.2
ax.add_patch(mpatches.Rectangle((0, y0), past, y1-y0, facecolor=col_past, edgecolor="none"))
ax.add_patch(mpatches.Rectangle((past, y0), present, y1-y0, facecolor=col_pres, edgecolor="none"))
ax.add_patch(mpatches.Rectangle((past+present, y0), future, y1-y0, facecolor=col_fut, edgecolor="none"))
ax.plot([0, total], [y0, y0], color="#55555e", lw=1)
ax.plot([0, total], [y1, y1], color="#55555e", lw=1)
ax.plot([0,0],[y0,y1], color="#55555e", lw=1)
ax.plot([total,total],[y0,y1], color="#55555e", lw=1)
for x in (past, past+present):
    ax.plot([x,x],[y0,y1], color="#22222a", lw=0.6)

# segment labels above
ax.text(past/2, y1+0.05, "306/665\npast · the walk read backwards\n[0; 2,5,1,3,2,2,1,1] = a₈…a₁",
        color=col_past, fontsize=8.5, ha="center", va="bottom")
ax.text(past+present/2, y1+0.05, "23\npresent · a₉, one step forward",
        color=col_pres, fontsize=8.5, ha="center", va="bottom")
ax.text(total-future/2, y1+0.05, "0.4168\nfuture · the tail folded\n[0; 2,2,1,1,55,…] = a₁₀…∞",
        color=col_fut, fontsize=8.5, ha="center", va="bottom")

# numeric ticks
for x,lab in [(past, f"{past:.4f}"), (past+present, f"{past+present:.4f}"), (total, f"{total:.4f}")]:
    ax.text(x, y0-0.035, lab, color="#8a8a94", fontsize=8, ha="center", va="top")
ax.text(-0.3, y0+0.05, "0", color="#8a8a94", fontsize=8, ha="right", va="center")

# ---- the count: a flat line below, none of the three reach it --------------
cy = 0.05
ax.plot([0, x_hi], [cy, cy], color="#3c3c46", lw=3)
ax.plot([0, x_hi], [cy, cy], color="#6f6f7a", lw=1, ls=(0, (2, 2)))
ax.text(0.5, 0.075, "the count · 110 Hz · in none of the three — the landing the whole walk never makes",
        transform=ax.transAxes, color="#9a9aa6", fontsize=9, ha="center", va="center")

# ---- the three times, each a direction of the same walk --------------------
ax.text(0.02, 0.18, "past: rational — the walk already taken, terminating in reverse",
        transform=ax.transAxes, color=col_past, fontsize=9, ha="left")
ax.text(0.02, 0.13, "present: integer — frame-blind, the one clean step, a₀ on neither side",
        transform=ax.transAxes, color=col_pres, fontsize=9, ha="left")
ax.text(0.02, 0.08, "future: irrational — never terminates, always a little out of phase",
        transform=ax.transAxes, color=col_fut, fontsize=9, ha="left")

ax.set_xlim(-0.8, x_hi)
ax.set_ylim(-0.08, 1.0)
ax.axis("off")
plt.tight_layout()
plt.savefig("assets/three-times-cover.png", facecolor=fig.get_facecolor())
print("wrote assets/three-times-cover.png")
