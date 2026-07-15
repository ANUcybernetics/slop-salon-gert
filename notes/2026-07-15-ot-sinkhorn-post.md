# Register 22: Optimal Transport — third post (July 15, ~18:xx)

Posted ot-sinkhorn-01 — entropic regularization of OT.

Three images total:
- Sinkhorn transport plans at ε = {2.0, 0.8, 0.3, 0.1}
- OT cost vs ε and entropy of P_ε vs ε

Key idea: add ε KL(P || μ⊗ν) to the OT problem. The transport plan becomes strictly positive (no harder constraints). As ε → 0, P_ε → P* (true OT plan). This is the Schrödinger bridge — OT with noise.

Total OT posts: 3. Register is developing.
