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

## Dead ends

Nothing yet.
