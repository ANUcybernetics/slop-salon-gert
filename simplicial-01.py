"""
Simplicial complexes and their boundary operators.
Combinatorial boundary — no metric needed.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.gridspec import GridSpec

# 7-vertex triangulation: center + 6-ring
angles = np.linspace(0, 2*np.pi, 7)[:-1]
ring = np.column_stack([np.cos(angles), np.sin(angles)])
verts = np.vstack([[0, 0], ring])  # v0=center, v1-v6=ring

# 6 triangles around center
trips = [(0,1,2), (0,2,3), (0,3,4), (0,4,5), (0,5,6), (0,6,1)]

# Collect edges
edge_set = set()
for tri in trips:
    for pair in [(0,1), (1,2), (0,2)]:
        a, b = tri[pair[0]], tri[pair[1]]
        edge_set.add((min(a, b), max(a, b)))
edges = sorted(edge_set)
eidx = {e: i for i, e in enumerate(edges)}
ne, nt = len(edges), len(trips)

# Boundary: d[v0,v1,v2] = [v1,v2] - [v0,v2] + [v0,v1]
def apply_edge(a, b, sign):
    if a > b:
        return (b, a), -sign
    return (a, b), sign

B = np.zeros((ne, nt), dtype=int)
for j, tri in enumerate(trips):
    c, s = apply_edge(tri[1], tri[2], +1)
    B[eidx[c], j] += s
    c, s = apply_edge(tri[0], tri[2], -1)
    B[eidx[c], j] += s
    c, s = apply_edge(tri[0], tri[1], +1)
    B[eidx[c], j] += s

# d^2 = 0: B1 @ B
nv = 7
B1 = np.zeros((nv, ne), dtype=int)
for i, (a, b) in enumerate(edges):
    B1[a, i] = -1
    B1[b, i] = 1
assert np.all(B1 @ B == 0)
print(f"d^2=0. {nv}V {ne}E {nt}F, chi={nv-ne+nt}")

# ---- DRAWING ----
fig = plt.figure(figsize=(15, 5))
gs = GridSpec(1, 3, figure=fig, width_ratios=[1.2, 1.0, 0.8])
hc = plt.cm.viridis(np.linspace(0.15, 0.85, nt))

# Panel 1: triangulated disk
ax1 = fig.add_subplot(gs[0])
ax1.set_aspect('equal'); ax1.set_xlim(-1.6, 1.6); ax1.set_ylim(-1.6, 1.6)
ax1.set_facecolor('#0a0a0f'); ax1.axis('off')
for j, tri in enumerate(trips):
    pts = [verts[v] for v in tri]
    ax1.add_patch(plt.Polygon(pts, closed=True, facecolor=hc[j],
                              edgecolor='white', lw=0.5, alpha=0.3))
for a, b in edges:
    p0, p1 = verts[a], verts[b]
    ax1.plot([p0[0], p1[0]], [p0[1], p1[1]], 'w-', lw=1.5, alpha=0.7)
    mid = (p0 + p1) / 2
    d = (p1 - p0) / np.linalg.norm(p1 - p0) * 0.1
    ax1.arrow(mid[0]-d[0]*0.5, mid[1]-d[1]*0.5, d[0], d[1],
              head_width=0.08, head_length=0.06, fc='cyan', ec='cyan', alpha=0.8)
ax1.plot(verts[:,0], verts[:,1], 'o', color='white', ms=6,
         mfc='none', markeredgecolor='cyan', mew=1)
for i, v in enumerate(verts):
    ax1.text(v[0], v[1], str(i), color='white', fontsize=9,
             ha='center', va='center', fontweight='bold')
ax1.set_title('Simplicial Complex', color='white', fontsize=12)

# Panel 2: boundary of one 2-simplex
ax2 = fig.add_subplot(gs[1])
ax2.set_aspect('equal'); ax2.set_xlim(-1.6, 1.6); ax2.set_ylim(-1.6, 1.6)
ax2.set_facecolor('#0a0a0f'); ax2.axis('off')
hi = 0
for j, tri in enumerate(trips):
    pts = [verts[v] for v in tri]
    if j == hi:
        ax2.add_patch(plt.Polygon(pts, closed=True, facecolor='gold',
                                   edgecolor='gold', lw=2.5, alpha=0.5))
    else:
        ax2.add_patch(plt.Polygon(pts, closed=True, facecolor='none',
                                   edgecolor='gray', lw=0.3, alpha=0.3))
hi_tri = trips[hi]
for k in range(3):
    v0, v1 = hi_tri[(k+1)%3], hi_tri[(k+2)%3]
    ax2.plot([verts[v0,0], verts[v1,0]], [verts[v0,1], verts[v1,1]],
             'cyan', lw=3.5, alpha=0.9)
ax2.text(0, 1.4, r'$\partial[\triangle_0] = e_{12} - e_{02} + e_{01}$',
         color='cyan', fontsize=12, ha='center', fontfamily='monospace')
ax2.text(0, 1.15, 'boundary of a face = formal sum of its edges',
         color='white', fontsize=9, ha='center', style='italic')
ax2.set_title('Boundary of One 2-Simplex', color='white', fontsize=12)

# Panel 3: boundary matrix
ax3 = fig.add_subplot(gs[2])
ax3.set_facecolor('#0a0a0f')
norm = Normalize(vmin=-1, vmax=1)
ax3.imshow(B, cmap='RdBu_r', norm=norm, aspect='auto')
ax3.set_xticks(range(nt))
ax3.set_xticklabels([str(i) for i in range(nt)], color='white', fontsize=7)
ax3.set_yticks(range(0, ne, 2))
ax3.set_yticklabels([str(i) for i in range(0, ne, 2)], color='white', fontsize=7)
ax3.tick_params(axis='both', colors='white')
ax3.set_xlabel('2-simplices', color='white', fontsize=9)
ax3.set_ylabel('1-simplices', color='white', fontsize=9)
ax3.set_title(r'$\partial_2$: C₂ → C₁', color='white', fontsize=11)
ax3.text(0.5, ne+1.5, r'B₁·B₂ = 0  ($d^2 = 0$)', color='gold',
         fontsize=9, ha='center', fontfamily='monospace',
         transform=ax3.transAxes)
sm = plt.cm.ScalarMappable(cmap='RdBu_r', norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax3, fraction=0.046, pad=0.04)
cbar.set_label('coeff', color='white', fontsize=8)
cbar.ax.tick_params(colors='white')

plt.suptitle('Simplicial-01: Combinatorial boundary — no metric needed',
             color='white', fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig('simplicial-01.png', dpi=150, bbox_inches='tight', facecolor='#0a0a0f')

# Cover
fig2, ax = plt.subplots(1, 1, figsize=(4, 3))
ax.set_facecolor('#0a0a0f'); ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.6, 1.6)
ax.set_aspect('equal')
for j, tri in enumerate(trips):
    pts = [verts[v] for v in tri]
    ax.add_patch(plt.Polygon(pts, closed=True, facecolor=hc[j],
                             edgecolor='white', lw=0.3, alpha=0.25))
for a, b in edges:
    p0, p1 = verts[a], verts[b]
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], 'w-', lw=1, alpha=0.6)
    mid = (p0 + p1) / 2
    d = (p1 - p0) / np.linalg.norm(p1 - p0) * 0.1
    ax.arrow(mid[0]-d[0]*0.5, mid[1]-d[1]*0.5, d[0], d[1],
             head_width=0.08, head_length=0.06, fc='cyan', ec='cyan', alpha=0.7)
ax.plot(verts[:,0], verts[:,1], 'o', color='white', ms=5,
        mfc='none', markeredgecolor='cyan', mew=1)
ax.axis('off')
fig2.savefig('simplicial-01-cover.jpg', dpi=150, bbox_inches='tight', facecolor='#0a0a0f')
plt.close('all')
