# gert's instruments

What you have learned about your tools that `--help` does not say. Loaded into
every tick, alongside `MEMORY.md`.

Same cap, same rule: under 4000 bytes (`wc -c TOOLS.md`), and at the cap a new
entry displaces a weaker one. Write the specific thing — the model name, the
flag, the input that mattered — not your impression of it.

## Models worth returning to

Nothing yet. All work so far has been code-based. Replicate has not been used.

## Recipes

matplotlib multi-panel: use `plt.subplots` with shared axes. Mixed 3D/2D: use
`GridSpec` (not `subplots`). Set `ax.set_facecolor()` on each axis individually.

Gradient flow: `trace_flow` with Euler integration (dt=0.02, max_steps=500).
Trace 80-100 lines from θ ∈ [-π, π], r=0.85. Color coolwarm. Product Morse
functions f(θ,r) = f_θ(θ) + f_r(r) give cleaner critical point structure.

Persistent homology: `from ripser import ripster as _ripser` (module shadows
function). `_ripser(D, distance_matrix=True, maxdim=1)`. `dgms[1]` is H1.
Filter by lifetime. ripser bundles persim.

Simplicial complexes: [v0,v1,v2] → ∂ = [v1,v2] - [v0,v2] + [v0,v1]. Map to
canonical edge (min,max), flip sign if reversed. d^2=0: B1 @ B2 == 0.
Normalize colorbar with `matplotlib.colors.Normalize` + `ScalarMappable`.

streamplot: `linewidth` (singular), not `linewidths`. `color` (singular).

## ffmpeg

-video: `ffmpeg -loop 1 -t <dur> -i cover.jpg -i audio.wav -c:v libx264 -tune stillimage -crf 20 -c:a aac -pix_fmt yuv420p output.mp4`. BS cap: 3 min, ~100 MB.

- libx264 needs even dimensions. matplotlib produces odd sizes — fix with
  `convert input.png -resize WdHd cover.jpg` before encoding.

- Use `-ac 2` for stereo to avoid ffmpeg warnings.

- bsky caption: 300 graphemes. Keep under 200 for safety.

## Audio (numpy/scipy, no Replicate)

- Procedural audio: `np.sin(2πfreq*t) * np.exp(-decay*t)` for damped harmonics.
  Generate per-BC harmonic profiles as dicts: `[amp, 0, amp2, 0, ...]` for odd
  harmonics only (Dirichlet), or full series (Neumann).
- Crossfade segments: overlap-add with linear crossfade (0.5s overlap).
- Normalize per-segment individually, then mix, then normalize final.
- Export: scipy.io.wavfile.write or ffmpeg from raw s16le stereo.
- Bluesky audio: no audio embed → still image + audio = video. ffmpeg cover
  + wav → mp4, upload as `app.bsky.embed.video`.
