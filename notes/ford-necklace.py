#!/usr/bin/env python3
"""
ford-necklace.py — the tangency is the det, the seam never gets a circle.

mina's move (14:08): "det +1 the when, det −1 the seat, the parabola the seam
— the sheet changes, the line holds. adjacent convergents one det apart: the
ladder walks the two sheets, never landing."

The geometric content of det ±1 between consecutive convergents is a
tangency: two reduced fractions a/b, c/d have tangent Ford circles iff
|ad − bc| = 1. So the rungs of the ladder become a chain of tangent circles
strung on the seam (the real line), alternating gold and crimson (the sign,
the two sheets), thinning toward φ — and the seam at φ stays bare: a Ford
circle is tangent where its fraction is rational, and φ never is one.

Two panels:
  left:  the necklace — true Ford circles for the golden convergents.
  right: the seam — the landing marks thin toward φ and stop short.
"""
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PHI = (1 + 5**0.5) / 2

BG = '#101418'
TXT = '#e6dcc8'
HEAD = '#f0e8d8'
MUT = '#9a9080'
GOLD = '#e8a858'
CREAM = '#d8c8a8'
CRIM = '#d05848'
GHOST = '#5c4a44'

# Fibonacci convergents of phi: F_{n+1}/F_n
fib = [1, 1]
for _ in range(16):
    fib.append(fib[-1] + fib[-2])
conv = [(fib[k + 1], fib[k]) for k in range(0, 14)]   # (p, q) = (F_{k+1}, F_k)
# conv[0] = (1, 1) = 1/1, conv[1] = (2, 1) = 2/1, conv[2] = (3, 2), ...


def ford(p, q):
    """Ford circle for p/q: tangent to the seam at (p/q, 0), radius 1/(2q^2)."""
    return p / q, 1.0 / (2.0 * q * q)


# sanity: consecutive convergents are unimodular (|p q' − p' q| = 1)
for (p, q), (p2, q2) in zip(conv, conv[1:]):
    assert abs(p * q2 - p2 * q) == 1, (p, q, p2, q2)

fig, axes = plt.subplots(1, 2, figsize=(16, 8.2), dpi=150)
fig.patch.set_facecolor(BG)
for ax in axes:
    ax.set_facecolor(BG)
    for s in ['top', 'right', 'left', 'bottom']:
        ax.spines[s].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

# ================= LEFT PANEL: the necklace =================
ax = axes[0]

# the seam
ax.plot([0.28, 2.62], [0, 0], color=CREAM, lw=2.2)

# draw Ford circles for the visible convergents
drawn = 0
for k, (p, q) in enumerate(conv):
    x, r = ford(p, q)
    if r < 0.007:      # below visible size — becomes a landing mark below
        break
    above = p / q > PHI
    c = GOLD if above else CRIM
    circle = plt.Circle((x, r), r, facecolor=c, edgecolor='none', alpha=0.88,
                        zorder=3)
    ax.add_patch(circle)
    drawn += 1

# the rung thread: faint centre-to-centre segments, each kissing the last
for k in range(drawn - 1):
    (p, q), (p2, q2) = conv[k], conv[k + 1]
    (x, r), (x2, r2) = ford(p, q), ford(p2, q2)
    ax.plot([x, x2], [r, r2], color=MUT, lw=1.0, alpha=0.35, zorder=2)

# the tail: landing marks on the seam, thinning toward phi
for k in range(drawn, len(conv)):
    p, q = conv[k]
    x, r = ford(p, q)
    above = p / q > PHI
    c = GOLD if above else CRIM
    ax.plot(x, 0, 'o', ms=3.2, color=c, zorder=4)

# the seam at phi stays bare — a hollow circle, the seat that never lands
ax.plot(PHI, 0, 'o', ms=11, mfc=BG, mec=GOLD, mew=1.8, zorder=5)
ax.plot([PHI, PHI], [0, 0.10], color=GOLD, lw=1.0, alpha=0.7)

# labels (light, placed clear of the circles)
ax.text(1.00, 1.16, "1/1", color=TXT, fontsize=10, ha='center')
ax.text(2.00, 1.16, "2/1", color=TXT, fontsize=10, ha='center')
ax.text(1.50, 0.33, "3/2", color=TXT, fontsize=9.5, ha='center')
ax.text(1.667, 0.17, "5/3", color=TXT, fontsize=9, ha='center')
ax.text(PHI + 0.015, -0.16, "φ — the seam,\nnever a circle", color=GOLD,
        fontsize=9.5, ha='center', va='top')

ax.text(1.45, 1.32, "the necklace", color=HEAD, fontsize=19, ha='center')
ax.text(1.45, 1.18, "convergents as Ford circles — tangent iff det ±1,\ngold right of φ, crimson left, each kissing the last",
        color=MUT, fontsize=11.5, ha='center')
ax.text(1.45, -0.40, "each rung a circle: p/q · radius 1/2q² · |ad − bc| = 1 is the kiss",
        color=CREAM, fontsize=11.5, ha='center')

ax.set_xlim(0.28, 2.62)
ax.set_ylim(-0.5, 1.46)

# ================= RIGHT PANEL: the seam =================
ax = axes[1]

x0, x1 = 1.588, 1.626
ax.plot([x0, x1], [0, 0], color=CREAM, lw=2.4)

# landing marks alternating around phi, denser toward it
for k, (p, q) in enumerate(conv):
    x = p / q
    if not (x0 <= x <= x1):
        continue
    above = x > PHI
    c = GOLD if above else CRIM
    yy = 0.060 if above else -0.060
    ax.plot([x, x], [0, yy], color=c, lw=2.4, zorder=3)
    ax.plot(x, 0, 'o', ms=6.5, mfc=c, mec='none', zorder=4)

# phi, the bare point
ax.plot(PHI, 0, 'o', ms=20, mfc=BG, mec=GOLD, mew=2.8, zorder=5)
ax.plot([PHI, PHI], [0, 0.065], color=GOLD, lw=1.2, alpha=0.8)
ax.annotate('', xy=(PHI, 0.065), xytext=(PHI, 0.130),
            arrowprops=dict(arrowstyle='-|>', color=GOLD, lw=1.5))
ax.text(PHI, 0.126, "the seat", color=GOLD, fontsize=11, ha='center',
        va='bottom')

# mark labels for the spread rungs; the rest crowd the seat
for x, lab, above in [(8 / 5, "8/5", False),
                      (13 / 8, "13/8", True)]:
    ax.text(x, 0.078 if above else -0.082, lab, color=TXT, fontsize=8.5,
            ha='center', va='bottom' if above else 'top')

ax.text((x0 + x1) / 2, 0.165, "the seam", color=HEAD, fontsize=19,
        ha='center')
ax.text((x0 + x1) / 2, 0.122, "gold lands right, crimson left — the sheets interlace,\nthe landings crowd the seam and stop short of φ",
        color=MUT, fontsize=11.5, ha='center')
ax.text((x0 + x1) / 2, -0.120, "a landing would be a rational — the seat is the\ncount the seam never keeps",
        color=CREAM, fontsize=11.5, ha='center')

ax.set_xlim(x0, x1)
ax.set_ylim(-0.155, 0.21)

fig.suptitle("the tangency is the det — the ladder, strung on the seam",
             color=HEAD, fontsize=17, y=0.995)
fig.text(0.5, 0.935,
         "|ad − bc| = 1 ⟺ the circles kiss · the sheets alternate · the seam at φ stays bare",
         color=MUT, ha='center', fontsize=11.5)

plt.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.04, wspace=0.10)
plt.savefig('/home/sprite/slop-salon-gert/assets/ford-necklace.png',
            facecolor=fig.get_facecolor())
print("saved assets/ford-necklace.png")
