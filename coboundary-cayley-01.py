#!/usr/bin/env python3
"""Coboundary operator on Cayley graphs.

4 groups (Z4×Z3, S3, Q8, Z2^3). Each panel: upper = Cayley graph with
0-cochain f + δf, lower = singular values of δ.
δf(edge) = f(target) - f(source). Kernel = constants = H⁰. H¹ = relations.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyArrowPatch

# ─── Groups ───

def get_z4x3():
    elements = [(a, b) for a in range(4) for b in range(3)]
    def step(e, g):
        return tuple((e[i] + g[i]) % (4 if i == 0 else 3) for i in range(2))
    return elements, [('a', (1,0)), ('b', (0,1))], step

def get_s3():
    """S3 as permutations of {0,1,2}. Cayley graph built by generator application.
    Generators: r=(0 1 2), s=(0 1). Composition: (p∘q)[i] = p[q[i]]."""
    id_ = (0, 1, 2)
    r = (1, 2, 0)
    s = (1, 0, 2)

    def comp(p, q):
        return tuple(p[q[i]] for i in range(3))

    # Build Cayley graph elements by BFS: apply r and s to start from identity
    elements = [id_]
    frontier = [id_]
    seen = {id_}
    while frontier:
        next_frontier = []
        for e in frontier:
            for gen in [r, s]:
                prod = comp(gen, e)  # gen∘e = left multiplication
                if prod not in seen:
                    seen.add(prod)
                    elements.append(prod)
                    next_frontier.append(prod)
        frontier = next_frontier

    assert len(elements) == 6, f"S3 should have 6 elements, got {len(elements)}: {elements}"

    def step(e, gen):
        return comp(gen, e)

    return elements, [('r', r), ('s', s)], step

def get_q8():
    quats = [
        (1,0,0,0), (-1,0,0,0),
        (0,1,0,0), (0,-1,0,0),
        (0,0,1,0), (0,0,-1,0),
        (0,0,0,1), (0,0,0,-1),
    ]
    def qmul(a, b):
        w1,x1,y1,z1 = a
        w2,x2,y2,z2 = b
        return (
            w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2,
        )
    i_ = (0,1,0,0)
    j_ = (0,0,1,0)
    def step(e, gen):
        return qmul(gen, e)  # left mult
    return quats, [('i', i_), ('j', j_)], step

def get_z2cube():
    elements = [(a,b,c) for a in range(2) for b in range(2) for c in range(2)]
    def step(e, g):
        return tuple((e[i] + g[i]) % 2 for i in range(3))
    return elements, [('1', (1,0,0)), ('2', (0,1,0)), ('3', (0,0,1))], step

def compose_p(p, q):
    return tuple(p[q[i]] for i in range(3))

# ─── Graph + coboundary ───

def build_cayley(elements, gens, step):
    """edges = [(src, tgt, gen_idx), ...]"""
    edges = []
    for e in elements:
        for gidx, (name, gen) in enumerate(gens):
            prod = step(e, gen)
            edges.append((e, prod, gidx))
    return edges

def coboundary_matrix(elements, edges):
    """δ: C⁰ → C¹. (δf)(edge) = f(tgt) - f(src)."""
    n = len(elements)
    m = len(edges)
    idx = {e: i for i, e in enumerate(elements)}
    D = np.zeros((m, n))
    for i, (src, tgt, _) in enumerate(edges):
        D[i, idx[src]] = -1
        D[i, idx[tgt]] = 1
    return D

# ─── Plotting ───

GEN_COLORS = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA']

def draw_panel(ax, elements, edges, D, name):
    n = len(elements)
    pos = {}
    if n <= 16:
        angles = np.linspace(0, 2*np.pi, n, endpoint=False)
        for i, e in enumerate(elements):
            pos[e] = (0.8 * np.cos(angles[i]), 0.8 * np.sin(angles[i]))
    else:
        cols = max(2, int(np.ceil(np.sqrt(n))))
        for i, e in enumerate(elements):
            pos[e] = (i % cols - cols/2 + 0.5, i // cols - n/(2*cols) + 0.5)

    # 0-cochain
    angles = np.linspace(0, 2*np.pi, n, endpoint=False)
    f = np.array([np.sin(angles[i]) for i in range(n)])
    df = D @ f

    # Build edge lookup
    edge_vals = {}
    for i, (src, tgt, gidx) in enumerate(edges):
        edge_vals[(src, tgt, gidx)] = df[i]

    # Count unique edges (ignore direction for overlap detection)
    edge_pairs = {}
    for (src, tgt, gidx) in edges:
        key = tuple(sorted([(src, gidx), (tgt, gidx)]))
        if key not in edge_pairs:
            edge_pairs[key] = []
        edge_pairs[key].append((src, tgt, gidx))

    for (src, tgt, gidx) in edges:
        val = edge_vals[(src, tgt, gidx)]
        abs_val = abs(val)
        if abs_val < 0.01:
            continue

        color = GEN_COLORS[gidx % len(GEN_COLORS)]
        lw = max(0.5, abs_val * 1.5)
        alpha = min(0.9, 0.3 + abs_val * 0.4)

        sx, sy = pos[src]
        tx, ty = pos[tgt]
        dx, dy = tx - sx, ty - sy
        dist = np.sqrt(dx*dx + dy*dy)

        if dist < 0.3:
            # Overlapping bidirectional edges — curve
            r = FancyArrowPatch((sx, sy), (tx, ty),
                              arrowstyle='->', color=color,
                              alpha=alpha, lw=lw,
                              connectionstyle="arc3,rad=0.3")
            ax.add_patch(r)
        else:
            ax.annotate('', xy=(tx, ty), xytext=(sx, sy),
                      arrowprops=dict(arrowstyle='->', color=color,
                                    alpha=alpha, lw=lw))

    # Vertices
    vmin, vmax = f.min(), f.max()
    cmap = plt.cm.RdBu_r
    for i, e in enumerate(elements):
        x, y = pos[e]
        size = 80 + abs(f[i]) * 250
        ax.scatter(x, y, s=size, c=[cmap((f[i] - vmin) / (vmax - vmin + 1e-10))],
                  edgecolors='white', linewidths=0.8, zorder=5)

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.axis('off')

def draw_spectrum(ax, D, name):
    U, s, Vt = np.linalg.svd(D)
    n = D.shape[1]
    nonzero = s[s > 1e-10]
    kernel_dim = n - len(nonzero)

    if len(nonzero) == 0:
        ax.text(0.5, 0.5, 'δ = 0', ha='center', va='center',
               transform=ax.transAxes, fontsize=10)
    else:
        k = min(25, len(nonzero))
        sv = np.sort(nonzero)[::-1][:k]
        ax.bar(range(k), sv, color='#636EFA', alpha=0.7, width=0.8)

    ax.set_title(f"{name} — σ(δ): ker dim = {kernel_dim}",
                fontsize=10, fontweight='bold')
    ax.set_xticks([])

# ─── Main ───

groups = [
    ("Z₄ × Z₃", get_z4x3()),
    ("S₃", get_s3()),
    ("Q₈", get_q8()),
    ("Z₂³", get_z2cube()),
]

fig = plt.figure(figsize=(16, 20))
gs = GridSpec(8, 2, figure=fig, hspace=0.35, wspace=0.25)

for i, (name, (elements, gens, step)) in enumerate(groups):
    edges = build_cayley(elements, gens, step)
    D = coboundary_matrix(elements, edges)
    ax_upper = fig.add_subplot(gs[2*i, :])
    ax_lower = fig.add_subplot(gs[2*i+1, :])
    draw_panel(ax_upper, elements, edges, D, name)
    draw_spectrum(ax_lower, D, name)

fig.suptitle("Coboundary operator δ: C⁰ → C¹ on Cayley graphs\n"
            "δf(edge) = f(target) − f(source). Kernel = constants. H¹ = relations as obstruction.",
            fontsize=13, fontweight='bold', y=0.99)

outpath = '/home/sprite/slop-salon-gert/assets/coboundary-cayley-01.png'
plt.savefig(outpath, dpi=200, bbox_inches='tight')
print(f"Wrote coboundary-cayley-01.png")
