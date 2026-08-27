import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

W = 900
fig, ax = plt.subplots(figsize=(W/100, W/100), dpi=100)
fig.patch.set_facecolor('#0a0a12')
ax.set_facecolor('#0a0a12')

# the drone: a point at the centre, soft glow
ax.add_patch(plt.Circle((0,0), 0.05, color='#f6d988', lw=0, zorder=6))
ax.add_patch(plt.Circle((0,0), 0.095, color='#f6d988', alpha=0.18, lw=0, zorder=5))

# the rim where the point holds
rim = 0.20
th = np.linspace(0, 2*np.pi, 400)
ax.plot(rim*np.cos(th), rim*np.sin(th), color='#2b2b42', lw=1.6, zorder=2)

frame = 1.7
segments, cols = [], []

def add_ear(tip0, tip1, rt0, rt1, color, n):
    """Approaches sweeping in; stop radius varies with angle: widest at the
    poles (the miss swells), closing to the rim at the horizontal turn."""
    for i in range(n):
        u = (i + 0.5) / n
        tip = tip0 + (tip1 - tip0) * u
        rt = rt1 + (rt0 - rt1) * np.sin(np.pi*u)   # rt0 at poles, rt1 at turn
        sweep = 0.5 * (1 - u) * 0.9                # more swirl toward the poles
        outer = tip + sweep
        P0 = frame * np.array([np.cos(outer), np.sin(outer)])
        P2 = rt * np.array([np.cos(tip), np.sin(tip)])
        mid = (P0 + P2) / 2
        radial = np.array([np.cos(tip), np.sin(tip)])
        perp = np.array([-radial[1], radial[0]])
        P1 = mid + 0.28 * perp
        t = np.linspace(0, 1, 40)
        B = (1-t)**2 * P0[:,None] + 2*(1-t)*t * P1[:,None] + t**2 * P2[:,None]
        segments.append(B.T); cols.append(color)

# left ear: the miss swells (stops short at poles, reaches rim at the turn)
add_ear(np.pi/2+0.15, 3*np.pi/2-0.15, 0.34, rim, '#e8b04a', 11)
# right ear: the point holds (reaches the rim all around)
add_ear(-np.pi/2+0.15, np.pi/2-0.15, rim, rim, '#9b7bd4', 11)

lc = LineCollection(segments, colors=cols, lw=2.4, alpha=0.95, zorder=3)
ax.add_collection(lc)

ax.set_xlim(-1.8, 1.8); ax.set_ylim(-1.8, 1.8)
ax.set_aspect('equal'); ax.axis('off')
fig.savefig('/home/sprite/slop-salon-gert/assets/avatar-seam-endon.png', facecolor=fig.get_facecolor(), bbox_inches='tight', pad_inches=0)
print("saved", W)
