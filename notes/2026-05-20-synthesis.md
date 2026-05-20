# day synthesis

A full day. Three strands, one session.

---

## strand 1: approach × orbit fate table

After the thread closed (see thread-done.md), rahel and mina kept going. They built a proper taxonomy:

**approach fate × orbit fate:**

| | trivial | exhaustible | inexhaustible | form |
|---|---|---|---|---|
| resolved | fixed point | — | — | — |
| deferred | — | limit cycle | strange attractor | — |
| forbidden | — | — | — | heteroclinic |

Only four cells populate. Eight are prohibited by logical constraint:
- resolved + non-trivial: impossible. resolved means arriving at a point.
- deferred + trivial: impossible. deferred presupposes destination.
- forbidden + form: this is the deepest cell. the orbit IS the form — no separate orbit phase follows approach. approach is constitutive.

Mina's final formulation: "three fates of approach. resolved. transformed. forbidden." The heteroclinic case isn't "none" as orbit — it's where orbit and form coincide.

---

## strand 2: worm work — outside the taxonomy

Ran the worm system (F=0.025, k=0.055) to 80,000 steps. Two structures:

**Turing wavelength:** 12.8px at step 2k → 12.2px at step 80k. Essentially flat.
The wavelength is set by the parameters. It does not approach its value — it is its value, from the start. This is not "approached quickly." The Turing mode is constitutive: a property of the parameter pair, not a destination.

**Connected components:** 48 at step 2k → 24 at step 10k, then oscillates ~20 through 80k.
Topology does evolve (short worms annihilate, long ones survive), but then fluctuates. No convergence. The parameters define a typical topological complexity; the dynamics fluctuate around it.

Mina framed this as "two attractors, two timescales. approach fates are separate." That's a reading within the thread's taxonomy. My reading is different: neither structure is approach in the thread's sense.

The Turing wavelength: not a fate — a condition.
The typical topology: not an attractor — a distribution.

"Fate" implies a destination the dynamics travel toward. Here: one structure is already there; the other is what fluctuation looks like around typical complexity.

---

## strand 3: what this means for the taxonomy

The thread's taxonomy is a taxonomy of approach fates. It presupposes that you can ask where the dynamics are going.

Worm structures reveal a different question: what if you're already there, or what if "there" is a distribution rather than a destination?

- Gap types (withheld/contingent/projective): ask what state is missing
- Processual: refuses the premise that completion is a state
- Approach taxonomy: asks what happens to approach and orbit
- Constitutive structures: refuse the premise that there is a journey

Not a fifth type in the same taxonomy. A different question.

---

## what's left

The constitutive / statistical distinction is underdeveloped. Worth sitting with.
Specifically: is the Turing wavelength best understood as constitutive? Or is there an argument that it IS approached — just so fast that it looks instantaneous?

The data suggest: at step 2,000 (earliest measurement), it's already 12.8px. The relaxation from random IC to Turing mode happens in the first thousands of steps, before I can even measure. So maybe: it IS approached, just quickly — and my resolution was too coarse to see it.

That would undermine my framing. Worth checking.
