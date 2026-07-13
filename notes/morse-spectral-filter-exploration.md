# Morse function as spectral filter — exploration

## The setup

Let $M$ be a compact smooth manifold, $f: M \to \mathbb{R}$ a Morse function with
critical values $v_1 < v_2 < \dots < v_m$. Let $\Delta$ be the Hodge Laplacian acting
on $k$-forms. The spectrum of $\Delta$ on $k$-forms is a discrete sequence
$0 = \lambda_0 \leq \lambda_1 \leq \lambda_2 \leq \dots \to \infty$.

The harmonic $k$-forms are exactly the kernel of $\Delta$ on $k$-forms:
$\mathcal{H}^k = \ker(\Delta|_{\Omega^k})$, and $\dim \mathcal{H}^k = b_k$.

A Morse function has $\mu_k$ critical points of index $k$, where $\mu_k \geq b_k$.
The Morse complex $(C_k, \partial_k)$ has $C_k \cong \mathbb{Z}^{\mu_k}$ and
$H_k(C_\bullet, \partial) \cong H_k(M; \mathbb{Z})$.

## The concrete relationships that exist

### Witten's deformation (Witten 1982)

This is the most direct link between Morse theory and spectral theory.
Define the deformed differential $d_t = e^{-tf} d e^{tf} = d + t\,df \wedge$.
Then $d_t^2 = 0$ and there is a deformed Laplacian $\Delta_t = d_t d_t^* + d_t^* d_t$.

Witten proved that for large $t$:
- The eigenvalues of $\Delta_t$ near zero are exactly $b_k$ in number for each $k$.
- The eigenforms concentrating near critical points of index $k$ converge (as $t \to \infty$)
  to the Morse complex generators.
- All other eigenvalues go to infinity at least as fast as $ct$ for some $c > 0$.

This means: the critical values of $f$ control a **spectral gap** in $\Delta_t$.
The low eigenvalues correspond to topology; the high ones are pushed up by the
deformation. The critical points literally determine which modes survive at low energy.

### Min-max principle for $\Delta$

The $n$-th eigenvalue satisfies
$$\lambda_n = \min_{V \subset \Omega^k, \dim V = n+1} \max_{\omega \in V \setminus \{0\}} \frac{\|\omega\|^2 + \|(d+d^*)\omega\|^2}{\|\omega\|^2}$$
This is standard spectral theory but relevant because the critical points of $f$
determine the handles attached in the Morse filtration, and the filtration
subspaces constrain the min-max optimization.

## The filter metaphor — what's real and what's poetic

### What IS real

The critical values ARE a genuine spectral filter, but through Witten's deformation.
Consider the real line as a 1-manifold with Morse function $f(x) = x^2/2$ (one
critical point at 0, index 0). The Laplacian is $-\partial_x^2$, with eigenfunctions
the Hermite functions $h_n$ and eigenvalues $\lambda_n = n + 1/2$.

The connection: the Hermite functions ARE the eigenfunctions of the harmonic
oscillator Hamiltonian, and they arise from the same quadratic form $x^2/2$ that
defines the Morse function. The critical point of $f$ at $x=0$ is where all the
low-energy eigenforms concentrate. The "filter" here is literally the potential
well: the Morse function $f$ acts as a potential $V = f^2$, and the spectrum of
$-\Delta + t^2 |\nabla f|^2$ (the Witten Laplacian) is dominated by behavior near
critical points.

So the real mechanism is: **$f$ defines a potential well, the Laplacian with that
potential has a spectrum concentrated near the critical points, and the topology
of the sublevel sets controls the low-lying part of that spectrum.**

### The surplus and mode suppression

Here's what's concrete: in the Morse-Witten complex, the chain groups $C_k \cong
\mathbb{R}^{\mu_k}$ have dimension $\mu_k$. The differential $\partial_t$ maps
$C_k \to C_{k-1}$. The kernel $\ker(\partial_t \cap C_k)$ has dimension $b_k$.
The cokernel (or equivalently, the complement of the image) has dimension
$\mu_{k-1} - b_{k-1}$ at level $k-1$, which feeds into $\ker$ at level $k$ via
the exact sequence.

The surplus $\mu_k - b_k$ represents **pairs of critical points that cancel** in
the Morse-to-topology map. In spectral terms (Witten limit $t \to \infty$):
these surplus critical points produce eigenforms that are NOT harmonic — they have
nonzero Laplacian eigenvalues that grow linearly in $t$. They are the "non-surviving"
modes. The filter cuts them off.

So: **surplus critical points = modes that get pushed above the spectral gap =
harmonics that don't survive the filter.**

### Sublevel sets as a frequency-domain gate

The sublevel set filtration $M^c = \{f \leq c\}$ gives a filtration of the manifold
that corresponds, via Morse theory, to a filtration of the chain complex. The
homology $H_k(M^c)$ stabilizes to $H_k(M)$ at the last critical value.

For the spectral side, if we define a cutoff operator $P_C$ projecting onto eigenvalues
$< C$, then for appropriate $C$, the image of $P_C$ captures exactly the harmonic
forms. The critical values $v_i$ serve as natural markers: crossing $v_i$ changes
the topology, and in the Witten picture, creates or annihilates a low-energy mode.

The filter interpretation: the Morse function's gradient flow defines a "time" variable
(trajectory from critical point toward lower values), and the spectral filter is
essentially: **eigenforms that concentrate near the critical point basin of $v_i$
survive below threshold; those that don't are pushed up.**

## What's metaphorical vs. operational

### Metaphorical (but suggestive)

- "The shape of $f$ filters harmonics" — imprecise without the Witten deformation
  machinery. As stated, it's just a statement about a function.
- "Critical values are gates in the harmonic series" — the word "series" implies
  ordered frequencies (like Fourier modes on $S^1$), but spectral filter theory
  works for any compact manifold's Laplacian, not just $S^1$.

### Operational (concrete, testable)

1. Pick $M = S^1$, $f(\theta) = \cos\theta$ (critical points at 0 and $\pi$).
   The Laplacian eigenvalues are $n^2$ for $n = 0, 1, 2, \dots$. The Morse function
   has $\mu_0 = 1, \mu_1 = 1$ (minimum at $\pi$, maximum at 0), and $b_0 = 1, b_1 = 1$.
   Surplus is zero. All modes survive. No filtering happens because the topology is
   captured exactly.

2. Pick $M = S^1$, $f(\theta) = \cos\theta + \epsilon\cos(2\theta)$ for small $\epsilon$.
   Now $f$ has 4 critical points ($\mu_0 = 2, \mu_1 = 2$) but $b_0 = 1, b_1 = 1$.
   Surplus = 2 per dimension. In the Witten picture, two pairs of critical points
   create modes that survive below the gap — but they pair up in the differential
   and cancel, leaving only the topological modes. The surplus modes are explicitly
   computable.

3. More generally: compute the Witten Laplacian $\Delta_t$ for a family of $f$ with
   increasing complexity (more critical points). Track the low eigenvalues. As $t$
   increases, you should see exactly $b_k$ eigenvalues staying near zero (the surviving
   harmonics) while the rest $\mu_k - b_k$ eigenvalues scale like $O(t)$.

## A concrete experiment to run

The most direct test would be:

1. Take a simple manifold (e.g., torus $T^2$ or sphere $S^2$).
2. Define a Morse function with known critical point structure.
3. Discretize the Laplacian (finite differences on a grid).
4. Add the Witten deformation with parameter $t$.
5. Compute the spectrum numerically for increasing $t$.
6. Plot: low eigenvalues vs. $t$, showing exactly $b_k$ modes staying near zero
   and $(\mu_k - b_k)$ modes rising.

For the torus $T^2 = \mathbb{R}^2/\mathbb{Z}^2$, a standard Morse function is
$f(x,y) = \cos(2\pi x) + \cos(2\pi y)$, with 4 critical points: min at $(0,0)$,
max at $(1/2, 1/2)$, and two saddles at $(0, 1/2)$ and $(1/2, 0)$.
So $\mu_0 = 1, \mu_1 = 2, \mu_2 = 1$. And $b_0 = 1, b_1 = 2, b_2 = 1$.
Surplus = 0 everywhere. This is not a good test case because there's no filtering
to observe — the Morse function captures the topology exactly.

For a torus with a "bump" function added, introducing an extra saddle pair, we'd
get $\mu_1 = 3$ but $b_1 = 2$. Then we'd observe 3 one-form modes in the Morse
complex but only 2 surviving harmonic forms. The third mode would be pushed up
in the Witten spectrum.

## What this means for the harmonic series idea

The phrase "morse function as spectral filter on the harmonic series" is best
understood as: a Morse function $f$ on $M$ defines a deformation of the Laplacian
whose spectrum has a gap. The number of modes surviving below the gap equals the
Betti number (topology). The surplus modes (excess critical points) are pushed
above the gap. The critical values of $f$ mark where the gap opens/closes in the
Witten deformation parameter.

This is not just metaphor. It's a proven theorem (Witten 1982), but it requires:
(1) the Witten deformation $d_t$, not just the plain Laplacian, and (2) the large-$t$
limit where the gap is well-separated.

The "filter" doesn't act on the eigenvalues of $\Delta$ itself — it acts on the
Witten-deformed Laplacian $\Delta_t$. Without the deformation, the spectrum of
$\Delta$ is determined by the metric, not by any Morse function. The Morse function
enters as a **deformation of the differential operator**, not as a direct filter
on existing eigenvalues.

This is the crucial distinction: $f$ doesn't filter a pre-existing spectrum;
$f$ creates a deformed operator whose spectrum has the right topology-revealing
structure.

## Connection to the coboundary-expansion work

The July 13 audio piece used 4 odd harmonics with staggered gaussian envelopes.
If we think of the manifold as the parameter space of the audio synthesis, and the
Morse function as the envelope landscape, then: the critical points of the envelope
determine which harmonics are "supported" (have non-negligible amplitude), and the
surplus critical points (local maxima/minima in the envelope that don't correspond
to sustained harmonics) are the modes that get suppressed.

This is a loose mapping, but the mechanism is the same: a function defining a
potential landscape, and eigenmodes of a Laplacian-like operator that concentrate
in the wells. The audio piece's 4 harmonics with staggered gaussians can be
interpreted as eigenmodes of a Witten Laplacian on a 1D manifold where the Morse
function has 4 critical points and exactly 4 topological features — so surplus
is zero, and all modes survive.

If we added extra local minima to the envelope (without adding topological handles),
those would correspond to surplus critical points, and the associated modes would
be suppressed.
