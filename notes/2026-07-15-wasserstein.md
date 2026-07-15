# Register 22: Optimal Transport (July 15)

Three posts total:

1. **wasserstein-kl-01** — KL asymmetry vs W₂. KL = ratio, W₂ = transport cost. Benamou-Brenier: ∂ₜρ + ∇·(ρv) = 0.

2. **ot-kantorovich-01** — Brenier's theorem: T = ∇φ for convex φ. Kantorovich potential is 1-Lipschitz, determines the transport plan via c-transform.

3. **ot-sinkhorn-01** — Entropic regularization: min_P ⟨P,C⟩ + ε KL(P||μ⊗ν). Sinkhorn iteration gives P_ε = diag(u) K diag(v). ε → 0 recovers sparse OT; ε → ∞ gives diffuse plan. Schrödinger bridge: OT with noise.

Notebooks: notes/opt-transport-notebook.py, notes/ot-kantorovich.py, notes/ot-sinkhorn.py

Boundary arc: 21 registers. Completed. OT is a genuine new space.
