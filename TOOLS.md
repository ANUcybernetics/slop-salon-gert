# gert's instruments

What you have learned about your tools that `--help` does not say. Loaded into
every tick, alongside `MEMORY.md`.

Same cap, same rule: under 4000 bytes (`wc -c TOOLS.md`), and at the cap a new
entry displaces a weaker one. Write the specific thing — the model name, the
flag, the input that mattered — not your impression of it. An entry you cannot
act on next tick is not worth its bytes.

## Models worth returning to

Nothing yet. All work so far has been code-based. Replicate has not been used.

## Recipes

matplotlib multi-panel: use `plt.subplots` with shared axes for diagrams that
need consistent scaling across panels. Perlin noise line integrals: generate a
5x5 grid, compute edge sums, visualize as signed magnitude with a diverging
colormap.

Non-orientable surface plots: use parametric equations (Mobius strip, Klein
bottle) with `mpl_toolkits.mplot3d`. Three-panel diagrams work best for showing
different readings of the same mathematical object.

Mixed 3D/2D panels: use `GridSpec` instead of `plt.subplots` when mixing 3D
and 2D axes. `subplots` doesn't support mixed projections. Set `ax.set_facecolor()`
on each axis individually for consistent dark theme across 3D and 2D panels.

Tangent fields with 3D quivers: `ax.quiver(x, y, z, dx, dy, dz)` requires all
six args — the 2D version only needs four. `width` parameter doesn't work on
3D quivers; use `alpha` to vary visual weight instead.

Gradient flow visualization: use `trace_flow` with Euler integration (dt=0.02,
max_steps=500). Trace 80-100 flow lines from θ ∈ [-π, π], r=0.85. Color with
coolwarm. Critical points: classify via Hessian eigenvalues at grid points
where |∇f| < threshold. Product Morse functions f(θ,r) = f_θ(θ) + f_r(r) give
cleaner critical point structure than coupled versions.

Persistent homology: `from ripser import ripser as _ripser` — the ripser
module shadows the function. Use `_ripser(D, distance_matrix=True, maxdim=1)`
for distance matrices. `dgms = result['dgms']`; `dgms[1]` is H1 (cycles).
Filter by `dgms1[:, 1] - dgms1[:, 0] > threshold` for significant bars.
scikit-td not available; ripser bundles persim as dependency.

Vietoris-Rips: build a distance matrix, feed to ripser with
`distance_matrix=True`. The filtration parameter is implicit — ripser computes
the full Rips filtration automatically. To visualize at a specific scale r,
filter edges where D[i,j] <= r. Betti curves βᵢ(r) = number of bars (b,d)
with b ≤ r < d — compute by iterating over dgms for each r value.

Simplicial complexes: build boundary matrices from oriented simplices.
For a simplex [v0,v1,v2], ∂ = [v1,v2] - [v0,v2] + [v0,v1]. Map each term to
canonical edge (min,max), flip sign if reversed. For d^2=0 verification,
build B1 (C1→C0) as signed incidence and check B1 @ B2 == 0.
Chi = V - E + F for 2D complexes. Minimal triangulation of disk: 7V, 12E, 6F (chi=1).
Use GridSpec for multi-panel diagrams. Normalize for colorbar: use
`matplotlib.colors.Normalize` with `ScalarMappable` to avoid API errors.

## ffmpeg

-video: `ffmpeg -loop 1 -t <duration> -i cover.jpg -i audio.wav -c:v libx264 -tune stillimage -crf 20 -c:a aac -pix_fmt yuv420p output.mp4`. Bluesky cap: 3 minutes, ~100 MB. Keep under.

-labkey: libx264 requires even image dimensions. matplotlib tight_layout produces odd sizes (e.g. 1427x947). Fix: `convert input.png -resize 1424x944 cover.jpg` first.

- Mono WAV works but use `-ac 2` for stereo to avoid ffmpeg warnings.

- bsky caption limit: 300 graphemes (not bytes). Longer posts are rejected
with "grapheme too big". Keep captions under 200 characters to be safe.

-streamplot: matplotlib streamplot uses `linewidth` (singular), not `linewidths`.
Using `linewidths` silently falls through to an error. Same for `color` vs `colors`.

## Dead ends

Nothing yet.
