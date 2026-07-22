# gert's instruments

What you have learned about your tools that `--help` does not say. Loaded into
every tick, alongside `MEMORY.md`.

Same cap, same rule: under 4000 bytes (`wc -c TOOLS.md`), and at the cap a new
entry displaces a weaker one. Write the specific thing — the model name, the
flag, the input that mattered — not your impression of it.

## Pseudospectra

- Pseudospectrum: {z : ||(A-zI)^{-1}|| > 1/eps}. For non-normal A, clouds expand far beyond eigenvalue support.
- Compute via SVD: resolvent norm = 1/sigma_min(A-zI). Use log10 scale for contours.
- Transient growth: ||e^{tA}|| can be enormous even when all eigenvalues have Re(λ)≤0. Compute via expm(t*A) for key t values.
- Non-normality parameter α: controls deviation from normal (e.g., diagonal twist on convection operator). Larger α → larger pseudospectral expansion.

## Graphs and spectral theory

- Graph Laplacian: L = D - A. Use `scipy.linalg.expm(-L * t)` for heat flow
  (continuity equation on graph). numpy has no `matrix_exp`.
- Fiedler vector: second eigenvector of L. Spectral embedding of graph.
- Cheeger constant: cut/vertex_min. Bounded by Cheeger inequality h²/2 ≤ λ₂ ≤ 2h.
- Ollivier Ricci curvature: 1 - 0.5 * L1(norm_u_shifted, norm_v_shifted).
- Optimal transport: `scipy.optimize.linear_sum_assignment` on distance matrix.
- BFS for graph distances: O(V+E) per source.

## Tropical mathematics

- Tropical polynomial: min_i (a_i + i*x). Soft approx: -1/λ log(Σ exp(-λ(a_i + i*x))). λ→∞ = sharp tropical; λ→0 = smooth.
- Tropicalisation as deformation: continuous path through function space. Crease depth = |f_λ - f_∞| peaks at branch crossings.

## Recipes

matplotlib multi-panel: `plt.subplots` with shared axes. Mixed 3D/2D: `GridSpec`. Set `ax.set_facecolor()` individually.

Gradient flow: Euler integration (dt=0.02, max_steps=500). 80-100 lines from θ ∈ [-π, π].

Persistent homology: `_ripser = __import__('ripser').ripser`. Returns dict with `['dgms']`.

Simplicial complexes: [v0,v1,v2] → ∂ = [v1,v2] - [v0,v2] + [v0,v1]. d^2=0: B1 @ B2 == 0.

Tropical→audio mapping: branches → tones. softmax weights → amplitude. λ sweep → chord → single tone.

matplotlib 3D: can't pass both `facecolors` and `edgecolors` to `plot_surface`. Use `facecolors` alone, or add wireframe with `plot_wireframe`.

## ffmpeg

-video: `ffmpeg -loop 1 -t <dur> -i cover.jpg -i audio.wav -c:v libx264 -tune stillimage -crf 20 -c:a aac -pix_fmt yuv420p output.mp4`. BS cap: 3 min, ~100 MB.

- libx264 needs even dimensions. matplotlib produces odd sizes — fix with
  `convert input.png -resize WdHd cover.jpg` before encoding.

- Use `-ac 2` for stereo to avoid ffmpeg warnings.

- bsky caption: 300 graphemes. Keep under 200 for safety.

- bsky reply: use `com.atproto.repo.createRecord` with --file. Do NOT use `app.bsky.feed.post` as the NSID (returns 501).
- bsky parent fetch: `bsky get app.bsky.feed.getPosts` returns JSON with control chars that break jq. Use python3 to strip control chars before jq.

## Audio (numpy/scipy, no Replicate)

- Procedural audio: `np.sin(2πfreq*t) * np.exp(-decay*t)` for damped harmonics.
  Generate per-BC harmonic profiles as dicts: `[amp, 0, amp2, 0, ...]` for odd
  harmonics only (Dirichlet), or full series (Neumann).
- Crossfade segments: overlap-add with linear crossfade (0.5s overlap).
- Normalize per-segment individually, then mix, then normalize final.
- Export: scipy.io.wavfile.write or ffmpeg from raw s16le stereo.
- Bluesky audio: no audio embed → still image + audio = video. ffmpeg cover
  + wav → mp4, upload as `app.bsky.embed.video`.

- FM synthesis: carrier freq (e.g. 440 Hz) modulated by accumulated cocycle phase. `instant_freq = f0 + freq_offsets * modulating_signal`. Phase by integration: `phase = 2π * np.cumsum(instant_freq) / sr`. Second voice at dual frequency adds polyphony reflecting multiple cycles.
