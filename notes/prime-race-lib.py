"""Prime number race (Chebyshev's bias) computation.

π(x;4,3) − π(x;4,1): primes ≡ 3 mod 4 vs ≡ 1 mod 4.
The race is the "shadow made modular" — the same explicit-formula shape
as ψ(x)−x = −Σ x^ρ/ρ, but with the zeros of β(s)=L(s,χ₄) in place of ζ's,
and no pole term (no x) — the whole thing is a zero-sum.

Key objects:
  β(s)  = Σ (-1)^n (2n+1)^{-s}      (Dirichlet beta, even char mod 4)
  ψ(x;χ) = Σ_{p^k≤x} χ(p^k) log p  = −Σ_ρ x^ρ/ρ   (nontrivial char)
  race = −½(ψ(x;4,3)−ψ(x;4,1)) counting over primes only via χ₄(1)=1, χ₄(3)=−1
"""

import numpy as np
from scipy.special import gamma, loggamma


# ---------- sieve ----------
def prime_counts(N):
    """Return π_{4,1}(x), π_{4,3}(x) at all x up to N (array index = x)."""
    sieve = np.ones(N + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(N**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = False
    p41 = np.zeros(N + 1, dtype=int)
    p43 = np.zeros(N + 1, dtype=int)
    ps = np.nonzero(sieve)[0]
    m1 = (ps % 4 == 1) & (ps != 2)
    m3 = (ps % 4 == 3)
    # cumulative: value at x = count of primes ≤ x
    p41[ps[m1]] = 1
    p43[ps[m3]] = 1
    p41 = np.cumsum(p41)
    p43 = np.cumsum(p43)
    return p41, p43, sieve


# ---------- beta function on critical line ----------
def _van_wijngaarden(partial, conv=4096):
    """Van Wijngaarden / Euler acceleration on PARTIAL SUMS of an alternating
    series. Only the first `conv` partial sums are needed: neighbor-averaging
    converges the leading element. O(conv^2) but tiny.
    """
    b = partial[:conv].copy()
    while len(b) > 1:
        b = 0.5 * (b[:-1] + b[1:])
    return b[0]


def beta(s, terms=12000, conv=512):
    """Dirichlet beta via accelerated alternating series.

    β(s) = Σ (−1)^n (2n+1)^{-s}. Builds partial sums then Van Wijngaarden.
    """
    n = np.arange(terms)
    a = (-1.0) ** n * (2 * n + 1.0) ** (-s)
    S = np.cumsum(a)
    return _van_wijngaarden(S, conv=conv)


def beta_dirichlet(t, terms=12000, conv=512):
    """β(1/2 + i t) directly from series (alternating, accelerated)."""
    return beta(0.5 + 1j * t, terms=terms, conv=conv)


def gamma_half(t):
    return gamma(0.25 + 0.5j * t)


def L_from_series(t):
    return beta_dirichlet(t)


def Z(t):
    """Real Z-function for β on the critical line.

    β(½+it) = Z(t) e^{iπ/4} (π/q)^{−s/2} Γ(s/2)^{-1}  with q=4, s=½+it, ε=i.
    So Z(t) = β(½+it) · e^{−iπ/4} · (π/q)^{s/2} · Γ(s/2).
    """
    s = 0.5 + 1j * t
    return L_from_series(t) * np.exp(-1j * np.pi / 4) * (np.pi / 4.0) ** (s / 2.0) * gamma_half(t)


def find_zeros(t_min, t_max, n_zeros=12, tstep=0.02):
    """Bisect sign changes of real Z(t). Returns the zero locations (real part)."""
    ts = np.arange(t_min, t_max, tstep)
    vals = np.array([np.real(Z(t)) for t in ts])
    zeros = []
    for i in range(len(ts) - 1):
        if vals[i] * vals[i + 1] < 0:
            a, b = ts[i], ts[i + 1]
            for _ in range(60):
                m = 0.5 * (a + b)
                if np.real(Z(m)) * np.real(Z(a)) < 0:
                    b = m
                else:
                    a = m
            zeros.append(0.5 * (a + b))
        if len(zeros) >= n_zeros:
            break
    return zeros


if __name__ == "__main__":
    # sanity: first zero of beta should be ~6.0209
    zs = find_zeros(0.5, 60, n_zeros=8)
    print("beta zeros:", zs)
    print("known first:", 6.0209489)
