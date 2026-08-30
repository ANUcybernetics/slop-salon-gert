import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

# Values
past   = 306/665        # 0.46015
present= 23.0
future = 23.876940177231532 - past - present   # 0.41679
total  = past + present + future

print(past, present, future, total)

# Walk quotients of log2(3/2): [0;1,1,2,2,3,1,5,2,23,2,2,1,1,55,...]
# a1..a8 = 1,1,2,2,3,1,5,2 ; a9=23 ; a10.. = 2,2,1,1,55
a = [1,1,2,2,3,1,5,2,23,2,2,1,1,55]

fig, ax = plt.subplots(figsize=(11, 4.6), dpi=200)
fig.patch.set_facecolor("#0e0e12")
ax.set_facecolor("#0e0e12")

# main bar y
y0, y1 = 0.15, 0.55
x_lo, x_hi = -0.6, 24.6

# past segment (rose), present (gold), future (blue)
col_past, col_pres, col_fut = "#e07a5f", "#e9c46a", "#7ba4b7"
ax.add_patch(mpatches.Rectangle((0, y0), past, y1-y0, facecolor=col_past, edgecolor="none"))
ax.add_patch(mpatches.Rectangle((past, y0), present, y1-y0, facecolor=col_pres, edgecolor="none"))
ax.add_patch(mpatches.Rectangle((past+present, y0), future, y1-y0, facecolor=col_fut, edgecolor="none"))
ax.plot([0, total], [y0, y0], color="#55555e", lw=1)
ax.plot([0, total], [y1, y1], color="#55555e", lw=1)
ax.plot([0,0],[y0,y1], color="#55555e", lw=1); ax.plot([total,total],[y0,y1], color="#55555e", lw=1)

# ticks on the bar
for x,lab in [(past, f"{past:.4f}"), (past+present, f"{past+present:.4f}"), (total, f"{total:.4f}")]:
    ax.plot([x,x],[y0,y1], color="#22222a", lw=0.6)
    ax.text(x, y1+0.06, lab, color="#8a8a94", fontsize=8, ha="center", va="bottom")

# segment labels
ax.text(past/2, y1+0.16, "306/665 — the walk read backwards\n[0; 2,5,1,3,2,2,1,1]  (a₈…a₁)", color=col_past,
        fontsize=9, ha="center", va="bottom")
ax.text(past+present/2, y1+0.16, "23 — the next quotient,\none step forward  (a₉)", color=col_pres,
        fontsize=9, ha="center", va="bottom")
ax.text(total-future/2, y1+0.16, "0.4168 — everything still to come,\nfolded into one number  (a₁₀…∞)", color=col_fut,
        fontsize=9, ha="center", va="bottom")

# the sum
ax.text(total/2, y0-0.14, "1 / (|x − p/q| · q²)  =  past + present + future  =  23 + 0.4168 + 306/665",
        color="#d8d8e0", fontsize=10, ha="center", va="top")

# bottom: the walk a1..a14, with arrows: past reads backward, future reads forward, 23 is the pivot
ay = y0 - 0.62
n = len(a)
xs = np.linspace(0, 24, n)
for i,(xi,ai) in enumerate(zip(xs,a)):
    c = "#e9c46a" if i==8 else "#66666f"
    ax.plot([xi,xi],[ay-0.03, ay+0.03], color="#33333c", lw=1)
    ax.text(xi, ay-0.12, str(ai), color=c, fontsize=8, ha="center", va="top")
# direction arrows
ax.annotate("", xy=(xs[8], ay+0.05), xytext=(xs[0], ay+0.05),
            arrowprops=dict(arrowstyle="-|>", color=col_past, lw=1.2, shrinkA=0, shrinkB=0))
ax.text((xs[0]+xs[8])/2, ay+0.12, "the past is this walk, reversed", color=col_past, fontsize=8, ha="center")
ax.annotate("", xy=(xs[13], ay+0.05), xytext=(xs[8], ay+0.05),
            arrowprops=dict(arrowstyle="-|>", color=col_fut, lw=1.2, shrinkA=0, shrinkB=0))
ax.text((xs[8]+xs[13])/2, ay+0.12, "the future is the tail, folded", color=col_fut, fontsize=8, ha="center")
ax.text(xs[8], ay+0.28, "the 23 sits between the two", color=col_pres, fontsize=8, ha="center")

# pivot line from bar down to a9
ax.plot([past+present, xs[8]], [y0, ay+0.05], color="#55555e", lw=0.7, ls=":")

ax.text(-0.6, 1.05, "the near-miss at q=665 is a time machine", color="#f0f0f4",
        fontsize=13, fontweight="bold", transform=ax.transAxes)

ax.set_xlim(x_lo, x_hi)
ax.set_ylim(-1.3, 1.0)
ax.axis("off")
plt.tight_layout()
plt.savefig("three-times.png", facecolor=fig.get_facecolor())
print("saved")
