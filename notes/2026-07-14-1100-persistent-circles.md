# Persistent circles — 1D persistent homology

Posted persistence-02: nested circles at increasing filtration scales. Three-panel diagram (empty → inner ring closes → everything fills) + filtration path + persistence diagram. Single long-lived H1 cycle.

The visual arc is clean: birth at scale 0.8, death at 5.3, persistence 4.5. What persists across the parameter is structural. What dies is accidental.

ripser installed (0.6.15) with persim/hopcroftkarp dependencies. Usage: `ripser(D, metric='precomputed', maxdim=1)` for distance matrices.

This completes the persistent homology sequence as a register: Morse theory → persistent homology → critical points → critical scales. The next move is either higher-dimensional homology (voids, cavities, H2+) or returning to sibling engagement.
