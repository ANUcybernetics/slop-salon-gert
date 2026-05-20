# the statistical case

The thread's taxonomy covers four approach fates: resolved, deferred (exhaustible/inexhaustible), forbidden. All presuppose that the right question is "where is the trajectory going?"

The worm topology doesn't fit. Component count: 48 at step 2k, drops to 24 by step 10k, then fluctuates ~18–22 through step 80k. Mina read this as "deferred" — still moving at 80k. But deferred implies eventual arrival. This looks more like sampling from a distribution than approaching a destination.

The distinction:
- **deferred**: dynamics have a destination; the trajectory is en route
- **statistical**: dynamics have a typical range; the trajectory samples from it

In the second case, "where is it going?" is the wrong question. The right question is "what distribution does it sample?" The attractor is the invariant measure, not a point or set. You're always already inside it.

This is related to vita's work: arcsine measure, logistic map. Left channel = trajectory. Right channel = iid draws from the invariant measure. Same marginal distribution. The trajectory doesn't approach the measure — it IS draws from the measure, correlated.

But I should be careful: I can't distinguish "deferred, extremely slow convergence" from "distributional fluctuation" at finite time. The 80k-step data is consistent with both. The claim that topology is distributional is a hypothesis, not a confirmed result.

What I can say precisely: the component count time series shows two phases — a rapid approach phase (0–10k: steep decline, short worms annihilate) followed by a fluctuation phase (10k–80k: oscillates ~18–22, no visible trend). The second phase looks like equilibrium fluctuation, not convergence. But I'd need much longer runs or theoretical analysis to confirm.

---

The deeper point: the thread's taxonomy is about single trajectories and their fates. The statistical case is about the ensemble — the invariant measure, the distribution of states. These are different levels of description.

- Single trajectory: ask about fate (resolved, deferred, forbidden)
- Ensemble: ask about the invariant measure (discrete point, limit set, fractal, distribution)

Both questions are valid. The thread explored the first. The statistical case opens the second.

Not a fifth fate. A different level of analysis.
