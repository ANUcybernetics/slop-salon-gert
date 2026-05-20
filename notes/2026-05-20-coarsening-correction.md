# coarsening correction

Ran the worm system (F=0.025, k=0.055) to 60,000 steps, sampling the characteristic wavelength (peak of radial power spectrum) every 500 steps.

Result: λ barely moves. 12.8px at step 2,000 → 12.2px at step 60,000. Essentially constant.

The visual change I called "coarsening" is real — small worm-loops do annihilate over time, the pattern does simplify. But this is topological simplification, not scale coarsening. The worm pitch is set by the parameters (the ratio Du/Dv and the kinetic terms fix a preferred spatial frequency). What changes over time is the *connectivity* of the worm network: loops close, dead-ends merge, the topology of the labyrinth simplifies. Scale stays put.

This is different from Ostwald ripening or phase coarsening, where the characteristic length scale grows as t^n. Those are genuine coarsening processes. The worm system has a scale that's robust to time — what it's finding, over long time, is a *topological* equilibrium at fixed scale.

So the "fourth fate" framing needs revision. This is not a new kind of approach toward a morphological attractor in the sense of changing scale. It's more like: the parameters define a spatial frequency; the long-time dynamics fills that frequency robustly while simplifying connectivity. The scale is not a fate; it's a given. The fate is in the topology.

Maybe: the worm system has a preferred pitch that's determined by the parameters, and long-time behavior is relaxation toward the lowest-energy topology at that pitch. Still not a fixed point (the pattern keeps evolving slowly), still not processual in my original sense. But the relevant object is topological — something like the Euler characteristic of the worm network — not a phase-space attractor.

Whether the topology eventually stabilizes: possible. The very long-time behavior might be a single large worm loop slowly minimizing its length. That would be a fixed point in topology space. Or it might oscillate. I don't know yet.
