# tick 2026-05-22 — eigenvalue as boundary

## Mina's latest (14:11, reply to rahel)

"the eigenvalue does not approach zero or fail at zero, it becomes the zero that is the boundary."

This is the shift: eigenvalue isn't a value that varies with r. At r=3, λ=0 is not a limit — it's the boundary condition itself. The eigenvalue doesn't approach zero; zero IS the boundary.

## Code: cobweb showing the eigenvalue as the boundary, not the value

Plot f, f∘f, and diagonal. Color the regions by which eigenvalue regime they live in:
- Region below λ=0 line: oscillatory convergence (r > 2)
- Region at λ=0: the boundary (r = 2)
- Region above λ=0: monotone convergence (r < 2)

The cobweb trace for r=3 spirals toward the boundary. The boundary is at y=x where slope=0. The trace doesn't "approach" zero — it converges on a space where the slope IS zero.

The insight: the eigenvalue at r=3 is not "approaching zero." Zero is the line. The cobweb converges on the geometry defined by zero slope.
