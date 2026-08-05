import numpy as np, scipy.special as sp, math

def eta_accel(s, M=80):
    n = np.arange(1, M+1, dtype=float)
    terms = (-1.0)**(np.arange(M)) * n**(-s)
    b = terms.copy()
    acc = 0.5*b[0]
    for i in range(M-1):
        b = 0.5*(b[:-1] + b[1:])
        acc += 0.5*b[0]
    return acc

def zeta(s):
    return eta_accel(s) / (1 - 2**(1-s))

def theta(t):
    return np.imag(sp.loggamma(complex(0.25, t/2))) - (t/2)*np.log(np.pi)

def Z(t):
    return np.real(np.exp(1j*theta(t)) * zeta(complex(0.5, t)))

def find_zeros(Tmax, guess=10.0, step=0.05):
    ts = np.arange(guess, Tmax, step)
    vals = np.array([Z(t) for t in ts])
    zeros = []
    for i in range(len(ts)-1):
        if vals[i]*vals[i+1] < 0:
            a, b = ts[i], ts[i+1]
            for _ in range(30):
                m = 0.5*(a+b)
                if Z(a)*Z(m) < 0: b = m
                else: a = m
            zeros.append(0.5*(a+b))
    return np.array(zeros)

def psi(x):
    N = int(x)
    sieve = np.ones(N+1, bool); sieve[:2] = False
    for i in range(2, int(N**0.5)+1):
        if sieve[i]: sieve[i*i::i] = False
    primes = np.nonzero(sieve)[0]
    s = 0.0
    for p in primes:
        pk = p
        while pk <= x:
            s += math.log(p)
            pk *= p
    return s

def explicit_partial(u, zeros):
    """Truncated explicit formula for psi(e^u) using zeros[:N]."""
    x = np.exp(u)
    total = x - math.log(2*math.pi) - 0.5*np.log(1 - x**-2)
    for t in zeros:
        rho = complex(0.5, t)
        total += -2*np.real(np.exp(rho*u) / rho)
    return total

def partial_sums(u_grid, zeros):
    """Return (N_zeros+1, len(u_grid)) array: partial explicit sums for N=0..len(zeros)."""
    x = np.exp(u_grid)
    base = x - math.log(2*math.pi) - 0.5*np.log(1 - x**-2)
    out = np.zeros((len(zeros)+1, len(u_grid)))
    out[0] = base
    for n, t in enumerate(zeros):
        rho = complex(0.5, t)
        out[n+1] = out[n] - 2*np.real(np.exp(rho*u_grid) / rho)
    return out
