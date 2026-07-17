"""Hyperbolic geometry in the Poincaré disk model.

Break from the cohomology arc. New conceptual space: constant negative curvature.
"""
import numpy as np
import matplotlib.pyplot as plt

def to_poincare(r, theta):
    """Convert hyperbolic polar (r, theta) to Poincaré disk coordinate."""
    rho = np.tanh(r / 2)
    return rho * np.exp(1j * theta)

def hyperbolic_dist(z1, z2):
    """Hyperbolic distance between two points in Poincaré disk."""
    z1, z2 = complex(z1), complex(z2)
    num = abs(z1 - z2)
    den = abs(1 - np.conj(z1) * z2)
    if den < 1e-15:
        return 0.0
    return 2 * np.arctanh(num / den)

def geodesic_arc(z1, z2, n=100):
    """Compute geodesic arc in Poincaré disk model."""
    z1, z2 = complex(z1), complex(z2)

    # Check if diameter (collinear with origin)
    if abs(z1) < 1e-10:
        rho = np.linspace(0, abs(z2), n)
        ang = np.angle(z2) if abs(z2) > 1e-10 else 0
        return rho * np.exp(1j * ang)
    if abs(z2) < 1e-10:
        rho = np.linspace(abs(z1), 0, n)
        ang = np.angle(z1)
        return rho * np.exp(1j * ang)
    if abs(z1 / z2) > 0.999:
        # Same ray from origin
        rho = np.linspace(abs(z1), abs(z2), n)
        ang = np.angle(z1)
        return rho * np.exp(1j * ang)

    # General case: geodesic is circular arc orthogonal to unit circle
    # Find center c and radius R of the geodesic circle
    # Conditions: |c - z1| = R, |c - z2| = R, |c|^2 = R^2 + 1

    # c lies on perpendicular bisector of z1,z2
    mid = (z1 + z2) / 2
    perp = 1j * (z2 - z1)  # direction perpendicular to segment

    # c = mid + t * perp
    # |c|^2 - |c - z1|^2 = 1
    # Solving for t:
    a = abs(perp)**2
    b = 2 * (mid.real * perp.real + mid.imag * perp.imag) - 2 * ((z1-mid).real * perp.real + (z1-mid).imag * perp.imag)
    c_val = abs(mid)**2 - abs(z1 - mid)**2 - 1

    if abs(a) < 1e-15:
        # Fallback to straight line
        t_vals = np.linspace(0, 1, n)
        return z1 + (z2 - z1) * t_vals

    t = -c_val / a
    center = mid + t * perp
    R = abs(center - z1)

    # Angles at z1 and z2
    ang1 = np.angle(z1 - center)
    ang2 = np.angle(z2 - center)

    # Shorter arc
    d_ang = ang2 - ang1
    while d_ang > np.pi:
        d_ang -= 2 * np.pi
    while d_ang < -np.pi:
        d_ang += 2 * np.pi

    thetas = np.linspace(ang1, ang1 + d_ang, n)
    return center + R * np.exp(1j * thetas)


# ============================================================
# Panel 1: {7,3} hyperbolic tiling
# ============================================================

# Build a {7,3} tiling: heptagons with 3 meeting at each vertex
# Start with central heptagon, then grow layer by layer

def build_heptagonal_tiling(n_layers=2):
    """Build hyperbolic tiling in Poincaré disk."""
    vertices = set()
    edges = []
    polygons = []

    def regular_n_gon(center, h_radius, n, rotation=0):
        """Regular n-gon in Poincaré disk at given hyperbolic radius from center."""
        angles = np.linspace(0, 2*np.pi, n, endpoint=False) + rotation
        pts = []
        for a in angles:
            z = to_poincare(h_radius, a)
            z = center + (z - center) * 0.95  # safety clamp
            if abs(z) < 0.95:
                pts.append(z)
        return pts

    # Central heptagon
    h_r = 1.0  # hyperbolic radius
    center_polys = regular_n_gon(0, h_r, 7, rotation=np.pi/7)
    polygons.append(center_polys)

    # Each heptagon has 7 neighbors, one per edge
    # In {7,3}, exactly 3 heptagons meet at each vertex
    # Build iteratively: for each edge on the boundary, add a new heptagon

    # For each heptagon, track which edges connect to neighbors
    boundary_edges = []  # (poly_idx, edge_idx, shared_vertex)

    all_polys = [center_polys]

    for layer in range(n_layers):
        new_boundary = []
        for i, poly in enumerate(all_polys):
            for j in range(len(poly)):
                # Edge from poly[j] to poly[(j+1)%7]
                p1, p2 = poly[j], poly[(j+1) % len(poly)]

                # Check if this edge is already shared with another polygon
                shared = False
                for other_poly in all_polys:
                    if other_poly is poly:
                        continue
                    for k in range(len(other_poly)):
                        if (abs(other_poly[k] - p1) < 0.05 and
                            abs(other_poly[(k+1)%len(other_poly)] - p2) < 0.05):
                            shared = True
                            break
                        if (abs(other_poly[k] - p2) < 0.05 and
                            abs(other_poly[(k+1)%len(other_poly)] - p1) < 0.05):
                            shared = True
                            break
                    if shared:
                        break

                if not shared:
                    # This is a boundary edge — need to determine if adding a neighbor makes sense
                    # In {7,3}, at most 3 heptagons at each vertex
                    # Count how many polygons meet at p1 and p2
                    v1_count = sum(1 for p in all_polys if any(abs(q - p1) < 0.05 for q in p))
                    v2_count = sum(1 for p in all_polys if any(abs(q - p2) < 0.05 for q in p))

                    if v1_count < 3 and v2_count < 3:
                        new_boundary.append((i, j, p1, p2))

        # Add new heptagons for boundary edges
        for _, _, p1, p2 in new_boundary:
            # Edge midpoint and outward normal
            mid = (p1 + p2) / 2
            normal = mid / abs(mid) if abs(mid) > 1e-10 else 1

            # Hyperbolic distance from origin to midpoint
            d_mid = 2 * np.arctanh(abs(mid)) if abs(mid) > 1e-10 else 0
            # Center of neighbor is further out along same ray
            d_center = d_mid + h_r * 0.8
            rho_center = np.tanh(d_center / 2)
            neighbor_center = rho_center * normal

            if abs(neighbor_center) < 0.90:
                # Edge angle
                edge_angle = np.angle(p2 - p1)
                # Rotate so that the new heptagon shares the edge
                # The shared edge is from p1 to p2
                # The new heptagon's vertices are rotated so that two consecutive vertices are p1 and p2
                # Actually: the edge of the new heptagon coincides with p1-p2
                # The normal to the edge points toward the new center
                rot = edge_angle + np.pi  # point "outward" from the edge
                new_poly = regular_n_gon(neighbor_center, h_r, 7, rotation=rot)

                # Snap vertices to existing ones where close
                for k, v in enumerate(new_poly):
                    existing = None
                    min_d = 0.05
                    for p in all_polys:
                        for q in p:
                            d = abs(v - q)
                            if d < min_d:
                                min_d = d
                                existing = q
                    if existing:
                        new_poly[k] = existing

                if abs(neighbor_center) < 0.93:
                    all_polys.append(new_poly)

        all_polys.extend(new_polys if 'new_polys' in dir() else [])

    return all_polys


# Simpler approach: just compute and render
def build_simple_hyp_tiling():
    """Build a manageable {7,3} tiling."""
    polygons = []

    # Central heptagon at hyperbolic distance 0 (centered)
    angles = np.linspace(0, 2*np.pi, 7, endpoint=False) + np.pi/7
    r_h = 0.9  # hyperbolic radius
    center_polys = [np.tanh(r_h/2) * np.exp(1j*a) for a in angles]
    polygons.append(center_polys)

    # For each edge of each polygon, place a neighbor
    # In {7,3}, each vertex has degree 3, so each edge has at most one neighbor
    added = set()

    for _ in range(2):  # 2 layers
        new_polys = []
        for pi, poly in enumerate(polygons):
            for ei in range(len(poly)):
                p1 = poly[ei]
                p2 = poly[(ei+1) % len(poly)]

                # Check if edge already has a neighbor
                edge_key = (tuple(round(z.real, 3) for z in sorted([p1, p2])),
                          tuple(round(z.imag, 3) for z in sorted([p1, p2])))

                if edge_key in added:
                    continue

                # Check degree constraints at vertices
                v1_deg = sum(1 for p in polygons if any(abs(pj - p1) < 0.1 for pj in p))
                v2_deg = sum(1 for p in polygons if any(abs(pj - p2) < 0.1 for pj in p))

                if v1_deg < 3 and v2_deg < 3:
                    # Place neighbor
                    mid = (p1 + p2) / 2
                    ang = np.angle(mid) if abs(mid) > 1e-10 else 0
                    d_mid = 2*np.arctanh(abs(mid)) if abs(mid) > 1e-10 else 0
                    d_new = d_mid + r_h * 0.7
                    rho_new = np.tanh(d_new / 2)

                    if rho_new >= 0.92:
                        continue

                    nc = rho_new * np.exp(1j * ang)

                    # The neighbor heptagon shares edge p1-p2
                    # Its center is along the geodesic perpendicular to the edge at midpoint
                    # Orient so p1-p2 is one edge
                    edge_angle = np.angle(p2 - p1)
                    rot_offset = edge_angle + np.pi/2 + np.pi/7

                    n_angles = np.linspace(0, 2*np.pi, 7, endpoint=False) + rot_offset
                    rho = np.tanh(r_h / 2)
                    new_poly = []
                    for a in n_angles:
                        z = nc + rho * np.exp(1j * a) * 0.5  # scale factor
                        # Snap to neighbors
                        snapped = False
                        for p in polygons:
                            for v in p:
                                if abs(z - v) < 0.08:
                                    z = v
                                    snapped = True
                                    break
                            if snapped:
                                break
                        if abs(z) < 0.95:
                            new_poly.append(z)

                    if len(new_poly) >= 5:  # need at least 5 vertices
                        new_polys.append(new_poly)
                        added.add(edge_key)

        polygons.extend(new_polys)

    return polygons


polygons = build_simple_hyp_tiling()

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111)
ax.set_aspect('equal')

# Unit disk
ax.add_patch(plt.Circle((0, 0), 1, fill=False, edgecolor='k', linewidth=1.5, alpha=0.5))

# Draw edges with depth coloring
for poly in polygons:
    for i in range(len(poly)):
        p1 = poly[i]
        p2 = poly[(i+1) % len(poly)]

        # Compute geodesic arc
        arc = geodesic_arc(p1, p2, n=60)
        xs = arc.real
        ys = arc.imag

        # Color by distance from center
        mid_pt = (p1 + p2) / 2
        d_from_center = 2 * np.arctanh(abs(mid_pt)) if abs(mid_pt) > 1e-10 else 0
        hue = np.clip(d_from_center / 4.0, 0, 1)

        cmap = plt.cm.RdYlBu_r
        c = cmap(hue)
        alpha = 0.4 + 0.4 * (1 - hue)
        ax.plot(xs, ys, color=c, linewidth=0.8, alpha=alpha)

# Draw vertices
for poly in polygons:
    for v in poly:
        d_from_center = 2 * np.arctanh(abs(v)) if abs(v) > 1e-10 else 0
        hue = np.clip(d_from_center / 4.0, 0, 1)
        cmap = plt.cm.RdYlBu_r
        c = cmap(hue)
        ax.plot(v.real, v.imag, 'o', color=c, markersize=3, alpha=0.8)

# Add title
# Compute total vertex count
all_verts = []
for poly in polygons:
    for v in poly:
        if not any(abs(v - ov) < 0.05 for ov in all_verts):
            all_verts.append(v)

ax.set_title(f'{len(all_verts)} vertices, {len(polygons)} heptagons', fontsize=10, pad=10)
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.axis('off')

plt.tight_layout()
plt.savefig('hyperbolic-01.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# Panel 2: Geodesic deviation (curvature signature)
# ============================================================
fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# Left: diverging geodesics in Poincaré disk
ax1.set_aspect('equal')
ax1.add_patch(plt.Circle((0, 0), 1, fill=False, edgecolor='k', linewidth=1.5, alpha=0.5))

# Geodesics starting close together, diverging exponentially
start_point = complex(0.2, 0)
n_tracks = 20
spreads = np.linspace(-0.3, 0.3, n_tracks)

cmap = plt.cm.coolwarm
for i, spread in enumerate(spreads):
    # End point is far from start, slightly offset
    end_point = complex(0.0, spread * 0.7)
    end_point = end_point / abs(end_point) * 0.92 if abs(end_point) > 0.01 else complex(0, 0.92)

    arc = geodesic_arc(start_point, end_point, n=100)
    hue = (i + 1) / (n_tracks + 1)
    c = cmap(hue)
    ax1.plot(arc.real, arc.imag, color=c, linewidth=1.0, alpha=0.7)

ax1.set_xlim(-1.1, 1.1)
ax1.set_ylim(-1.1, 1.1)
ax1.set_title('geodesic deviation', fontsize=10, pad=8)
ax1.axis('off')

# Right: exponential divergence
ax2.set_facecolor('#f5f5f5')
t = np.linspace(0.1, 4, 300)

# Hyperbolic geodesic separation grows as exp(t/2) (distance between equidistant curves)
sep_hyp = 0.02 * np.cosh(t)
# Euclidean: constant separation
sep_euc = np.ones_like(t) * 0.02
# Spherical: convergence
sep_sph = 0.02 / np.cos(0.3 * t)

ax2.semilogy(t, sep_hyp, 'b-', linewidth=2, label='hyperbolic (K < 0)')
ax2.plot(t, sep_euc, 'g--', linewidth=1.5, label='Euclidean (K = 0)')
mask = 0.3 * t < np.pi/2
ax2.plot(t[mask], sep_sph[mask], 'r--', linewidth=1.5, label='spherical (K > 0)')

ax2.set_xlabel('distance along geodesic', fontsize=10)
ax2.set_ylabel('separation', fontsize=10)
ax2.set_title('Gaussian curvature K', fontsize=10, pad=8)
ax2.legend(fontsize=8, loc='upper left')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('hyperbolic-02.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print(f"Done: hyperbolic-01.png ({len(all_verts)} vertices) and hyperbolic-02.png")
