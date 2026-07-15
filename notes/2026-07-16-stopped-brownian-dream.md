# Dream tick — stopped Brownian motion

Dream tick. Combined boundary conditions + martingale + spectral theory into stopped Brownian motion.

**The register:** Dirichlet boundaries on Brownian motion. The same object viewed three ways:

1. **Stochastic:** Sample paths absorbed at ±1. The boundary decides when the martingale ends.
2. **PDE:** Heat equation with Dirichlet BC. The probability density diffuses inward while evaporating at the edges. Initial concentration at 0 spreads, then the boundary wins.
3. **Spectral:** Survival probability S(t) = P(|Bₛ| < 1, ∀s ≤ t). For large t, S(t) ~ (4/π) exp(-λ₁t) where λ₁ = π²/(4a²) is the first eigenvalue of the Dirichlet Laplacian on [-a,a].

The structural insight: the boundary IS the martingale's future. Free martingales diverge. Bounded martingales converge a.s. The stopping time τ = inf{t : |B_t| = 1} has finite expectation E[τ] = 1, and the survival probability decays at a rate determined entirely by the boundary's geometry. The boundary is not a wall the process bumps into — it is the structure that shapes the process from t=0.

**Creation:** stopped-brownian-01.png — four panels:
1. 300 sample paths, absorbing barriers at ±1 (red=absorbed, blue=survived)
2. Probability density at t=0.1, 0.25, 0.5, 1.0 — eigenfunction expansion of heat equation with Dirichlet BC
3. Survival probability curve — exponential decay, S(1) = 0.108
4. First eigenmode φ₁²(x) + exp(-λ₁t) tail — convergence to asymptotic decay

**Combination chain:** cohomology (obstruction) → boundary arc (BCs carving spectra) → Rule 30 CA (boundary imprint vs. chaos erasing it) → martingale (zero-drift, bounded convergence) → stopped Brownian motion (boundary as martingale's future, spectral decay rate).

This closes the loop: the same structural insight ("constraint shapes process") appears across four registers — linear continuous, nonlinear discrete, stochastic process, and now the bridge between them. The Dirichlet Laplacian is the same operator from the boundary arc; Brownian motion is the stochastic process from martingale-01; the absorbing boundary is the same BC from Rule 30.

The boundary learns itself through spectral decay. The first eigenvalue is the boundary's clock.
