#!/usr/bin/env python3
"""gradient-audio — the disappearance, made to descend.

The four rooms of the disappearance, each ending in its own landing, strung
into one piece that gets quieter as it goes — the avatar's accidental
brightness gradient made deliberate. Frost's hard gate cuts at a point; the
foam's last pop is a point; the smoke thins to air (no point, the where goes);
the ink stops at a zero crossing you can't find.

Under all of it, from the first instant to the last, runs a single 110 Hz sine
at constant level — the sign. In the frost it is masked by brightness, in the
foam by transients, in the smoke by the noise band. When the ink washes
everything else away, the sign is what's left: it was in the room the whole
time, unheard. The ink's fundamental is phase-locked to it, so the two are one
wave, and the final zero-crossing stop is the landing you can't find.

Movements (peak, before global normalise): frost 0.50, foam 0.32, smoke 0.20,
ink 0.12, sign 0.022. The descent is in material as much as level.
"""
import numpy as np
import scipy.io.wavfile as wav
from scipy import signal

sr = 44100
rng = np.random.default_rng(20260819)

# ---- timeline ----
F0 = 110.0
T_FROST = (0.0, 20.0)
T_FOAM = (20.5, 42.5)
T_SMOKE = (43.0, 69.0)
T_INK = (69.5, 101.5)
T_END = T_INK[1]
N = int(sr * T_END)
t = np.arange(N) / sr

mix = np.zeros((N, 2))

# ---- the sign: one sine, constant level, present the whole time ----
# phase runs from t=0; the ink fundamental locks onto it later.
SIGN = 0.014
phi0 = 0.0
sign_sine = SIGN * np.sin(2 * np.pi * F0 * t + phi0)
mix[:, 0] += sign_sine
mix[:, 1] += sign_sine

# ================= frost: the gate cuts at a point =================
# bright, sparse, high sines hard-gated off at memoryless times.
def frost(t0, t1, peak=0.50, ntones=14):
    i0, i1 = int(t0 * sr), int(t1 * sr)
    seg_t = t[i0:i1]
    Tn = i1 - i0
    r = np.random.default_rng(20260819)
    freqs = np.exp(r.uniform(np.log(600), np.log(3800), ntones))
    amps = 0.11 * (0.5 + r.random(ntones))
    pan = np.clip(r.normal(0, 0.6, ntones), -1, 1)
    gaps = r.exponential(1.0, ntones) * 0.9
    cuts = np.cumsum(gaps)
    cuts = (t1 - t0 - 0.5) * cuts / cuts[-1]     # seconds; last cut before the seam
    cuts = cuts[r.permutation(ntones)]
    out = np.zeros((Tn, 2))
    for i in range(ntones):
        tone = amps[i] * np.sin(2 * np.pi * freqs[i] * seg_t)
        tone = tone * (seg_t < cuts[i])          # hard gate: no decay, no fade
        a = (pan[i] + 1) * np.pi / 4
        out[:, 0] += tone * np.cos(a)
        out[:, 1] += tone * np.sin(a)
    pk = np.abs(out).max()
    out *= peak / pk
    return out, cuts

f, _ = frost(*T_FROST)
n0 = int(T_FROST[0] * sr)
mix[n0:int(T_FROST[1] * sr)] += f

# ================= foam: the pop is a point =================
# a small foam running down to zero; the last pop is the landing, then silence.
def foam(t0, t1, peak=0.20, nb=12):
    i0, i1 = int(t0 * sr), int(t1 * sr)
    seg_t = t[i0:i1]
    Tn = i1 - i0
    lt = seg_t - t0                       # local time: the movement's own clock
    r = np.random.default_rng(20260819 + 3)
    gaps = r.exponential(1.0, nb) * 0.9
    pops = np.cumsum(gaps)
    pops = (t1 - t0 - 0.5) * pops / pops[-1]     # seconds; last pop before the seam
    radii = np.exp(r.uniform(np.log(0.5), np.log(2.0), nb))
    radii = np.sort(radii)
    f0b = 1700.0
    floor_f = 2.9
    shrinkers = pops < np.median(pops)
    pan = np.clip(r.normal(0, 0.7, nb), -1, 1)
    out = np.zeros((Tn, 2))
    for i in range(nb):
        r0 = radii[i]
        tp = pops[i]
        i_end = int(tp * sr)
        if i_end < 1:
            continue
        tt = lt[:i_end]
        if shrinkers[i]:
            rr = r0 * (1.0 - (1.0 - 1.0 / floor_f) * (tt / tp))
        else:
            rr = r0 * (1.0 + 1.2 * (tt / tp))
        f = f0b / rr
        phase = 2 * np.pi * np.cumsum(f) / sr
        amp = 0.09 * (rr / 2.0) ** 2.0
        tone = amp * np.sin(phase)
        a = (pan[i] + 1) * np.pi / 4
        out[:i_end, 0] += tone * np.cos(a)
        out[:i_end, 1] += tone * np.sin(a)
        # the pop: a short damped chirp down at the death pitch
        pop_dur = 0.022
        pt = np.arange(int(pop_dur * sr)) / sr
        f_pop = f[-1]
        f_chirp = f_pop * (1.0 - 0.28 * pt / pop_dur)
        pop_phase = 2 * np.pi * np.cumsum(f_chirp) / sr
        env = np.exp(-pt * 90.0) * np.minimum(pt / 0.002, 1.0)
        pop = 0.34 * env * np.sin(pop_phase)
        e = i_end
        e2 = min(e + len(pt), Tn)
        if e2 > e:
            seg = pop[: e2 - e]
            out[e:e2, 0] += seg * np.cos(a)
            out[e:e2, 1] += seg * np.sin(a)
    pk = np.abs(out).max()
    out *= peak / pk
    return out, pops

fo, pops = foam(*T_FOAM)
n0 = int(T_FOAM[0] * sr)
mix[n0:int(T_FOAM[1] * sr)] += fo

# ================= smoke: the where becomes nowhere =================
# a noise bed, localizable at first, then the cutoff blurs, the image
# decorrelates, and the whole bed thins to the air — a diffusion, no point.
def one_pole(x, fc):
    y = np.empty_like(x)
    zi = np.zeros(1)
    block = 2048
    for s in range(0, len(x), block):
        e = min(s + block, len(x))
        a = np.exp(-2 * np.pi * fc[s] / sr)
        y[s:e], zi = signal.lfilter([1.0 - a], [1.0, -a], x[s:e], zi=zi)
    return y

def smoke(t0, t1, peak=0.18):
    i0, i1 = int(t0 * sr), int(t1 * sr)
    seg_t = t[i0:i1]
    Tn = i1 - i0
    D = t1 - t0
    lt = seg_t - t0                       # local time: the movement's own clock
    r = np.random.default_rng(20260819 + 7)
    S = r.standard_normal(Tn)
    A = r.standard_normal(Tn)
    B = r.standard_normal(Tn)
    fc = 8000.0 * (150.0 / 8000.0) ** (lt / D)
    Sf = one_pole(S, fc)
    Af = one_pole(A, fc)
    Bf = one_pole(B, fc)
    def pw(points):
        pts = np.array(points, dtype=float)
        return np.interp(lt, pts[:, 0], pts[:, 1])
    on = 1.0 - np.exp(-lt / 0.5)
    # the where disperses early; the independent beds carry the everywhere
    w_s = pw([(0, 1.0), (3, 1.0), (12, 0.30), (D, 0.30)])
    w_i = pw([(0, 0.0), (3, 0.0), (12, 0.70), (D, 0.70)])
    # the source-image swings to anti-phase — the where, at last a hole —
    # while the bed is still present, before the diffusion takes it.
    psi = pw([(0, 0.0), (11, 0.0), (15, np.pi / 2.0)])
    L_s = (np.cos(psi) + np.sin(psi)) * Sf * w_s
    R_s = (np.cos(psi) - np.sin(psi)) * Sf * w_s
    mod_L = 0.78 + 0.22 * np.sin(2 * np.pi * 0.11 * lt)
    mod_R = 0.78 + 0.22 * np.sin(2 * np.pi * 0.16 * lt + 2.1)
    # a fast diffusion at the very end — the air, not a gate and not a pop
    end = np.ones(Tn)
    mask = lt > (D - 2.5)
    end[mask] = np.exp(-(lt[mask] - (D - 2.5)) / 0.7)
    L = (L_s + Af * w_i) * on * end * mod_L
    R = (R_s + Bf * w_i) * on * end * mod_R
    out = np.stack([L, R], axis=1)
    pk = np.abs(out).max()
    out *= peak / pk
    return out

n0 = int(T_SMOKE[0] * sr)
mix[n0:int(T_SMOKE[1] * sr)] += smoke(*T_SMOKE)

# ================= ink: the quality washes out, the where holds =================
# a rich 110 Hz note; the overtones drain, the formants flatten, the grain
# smooths away until a bare sine remains — the sign, at last alone. Ends at a
# zero crossing: a landing you can't find. The fundamental is phase-locked to
# the sign-sine, so this final tone is the same wave that ran all along.
def ink(t0, t1, fund=0.050, KMAX=10):
    i0, i1 = int(t0 * sr), int(t1 * sr)
    seg_t = t[i0:i1]
    Tn = i1 - i0
    lt = seg_t - t0                       # local time: the movement's own clock
    r = np.random.default_rng(20260819 + 11)
    f0 = F0
    beta = 2.2e-4
    kk = np.arange(1, KMAX + 1)
    fk = f0 * kk * (1.0 + beta * kk ** 2)
    a_raw = kk ** (-1.8)
    def formants(f, centers, widths, amps):
        env = np.ones_like(f, dtype=float)
        for fc, w, am in zip(centers, widths, amps):
            env *= 1.0 + am * np.exp(-((f - fc) / w) ** 2)
        return env
    a_raw = a_raw * formants(fk, [380.0, 1050.0, 2200.0], [220.0, 420.0, 900.0],
                             [0.55, 0.4, 0.25])
    a_raw = a_raw / a_raw[0]
    def pw(points):
        pts = np.array(points, dtype=float)
        return np.interp(lt, pts[:, 0], pts[:, 1])
    # wash timeline scaled from the 48 s original into this movement's length
    D = t1 - t0
    def sc(pts):
        return [(s * D / 48.0, v) for s, v in pts]
    K = np.empty(Tn)
    i_before = lt < sc([(6, 0)])[0][0]
    K[i_before] = 30.0
    i_after = lt >= sc([(40, 0)])[0][0]
    K[i_after] = 1.0
    i_wash = ~i_before & ~i_after
    t40 = sc([(40, 0)])[0][0]
    t6 = sc([(6, 0)])[0][0]
    K[i_wash] = 1.0 + 29.0 * ((t40 - lt[i_wash]) / (t40 - t6)) ** 1.5
    WROLL = 1.2
    f_flat = pw(sc([(0, 0.0), (6, 0.0), (28, 0.55), (40, 1.0), (48, 1.0)]))
    grain = pw(sc([(0, 1.0), (6, 1.0), (26, 0.45), (38, 0.0), (48, 0.0)]))
    hiss = pw(sc([(0, 1.0), (6, 1.0), (30, 0.30), (40, 0.0), (48, 0.0)]))
    on = 0.5 * (1.0 - np.cos(np.pi * np.clip(lt / 0.8, 0.0, 1.0)))
    white = r.standard_normal(Tn)
    spec = np.fft.rfft(white)
    freq = np.fft.rfftfreq(Tn, 1.0 / sr)
    band = (freq > 500.0) & (freq < 6000.0)
    band = band * np.exp(-0.5 * ((np.log(np.clip(freq, 1e-3, None))
                                  - np.log(2200.0)) / 1.4) ** 2)
    hiss_wav = np.fft.irfft(spec * band * 0.02, Tn)
    hiss_wav = hiss_wav / (np.abs(hiss_wav).max() + 1e-9) * 0.030
    # fundamental phase locked to the sign-sine's running phase
    sign_phase_at_n0 = 2 * np.pi * f0 * t0 + phi0
    phase = np.concatenate([[sign_phase_at_n0],
                            r.uniform(0.0, 2 * np.pi, KMAX - 1)])
    slow = r.uniform(0.0, 2 * np.pi, KMAX)
    fast = r.uniform(0.0, 2 * np.pi, KMAX)
    sig = np.zeros(Tn)
    for idx in range(KMAX):
        kk_ = idx + 1
        cell = np.clip((K - kk_) / WROLL + 0.5, 0.0, 1.0)
        if kk_ == 1:
            cell = np.ones(Tn)
        fem = 1.0 + (formants(fk[idx:idx + 1], [380.0, 1050.0, 2200.0],
                              [220.0, 420.0, 900.0], [1.1, 0.9, 0.5])[0] - 1.0) \
              * (1.0 - f_flat)
        wob = 1.0 + grain * (0.15 * np.sin(2 * np.pi * (0.07 + 0.030 * idx) * seg_t
                                           + slow[idx])
                             + 0.09 * np.sin(2 * np.pi * (0.021 + 0.013 * idx) * seg_t
                                             + fast[idx]))
        amp = a_raw[idx] * cell * fem * wob
        sig += amp * np.sin(2 * np.pi * fk[idx] * seg_t + phase[idx])
    sig = sig * on + hiss_wav * hiss * on
    # clean end: truncate at a zero crossing of the fundamental
    s_end = np.sin(2 * np.pi * f0 * seg_t + phase[0])
    z = np.where(np.diff(np.sign(s_end)) != 0)[0]
    z_ok = z[z > Tn - int(0.30 * sr)]
    cut = z_ok[-1] + 1 if z_ok.size else Tn
    sig = sig[:cut]
    out = np.stack([sig, sig], axis=1)          # L = R: one point, never moves
    # normalise by the FUNDAMENTAL (the revealed sign), not the rich peak:
    # the fundamental sits at amplitude ~1.0 here, so the washed end of the ink
    # reads at `fund` and the rich early part is louder than it.
    out *= fund
    return out, cut

ink_sig, ink_cut = ink(*T_INK, fund=0.050)
i0 = int(T_INK[0] * sr)
mix[i0:i0 + ink_cut] += ink_sig[:ink_cut]
# the sign-sine continues to T_END but we end the piece at the ink's cut,
# which is a zero crossing of the same wave — the landing you can't find.
n_end = i0 + ink_cut
mix = mix[:n_end]

# ---- onset guard: 5 ms ramp at the very first instant (not a fade) ----
attack = int(0.005 * sr)
mix[:attack] *= np.linspace(0, 1, attack)[:, None]

# ---- global normalise: one readout level, absences as digital zero ----
peak = np.abs(mix).max()
mix *= 0.9 / peak
dur = n_end / sr

wav.write("assets/gradient.wav", sr, (mix * 32767).astype(np.int16))
print(f"saved assets/gradient.wav  {dur:.2f} s  (peak {peak:.3f})")

# ---- verification: RMS per movement, the descent ----
def rms(lo, hi):
    a, b = int(lo * sr), int(hi * sr)
    return np.sqrt((mix[a:b, 0] ** 2).mean())

print(f"  sign-only level (t=0..2, sign)     : {20*np.log10(rms(0,2)+1e-9):+6.1f} dBFS")
print(f"  frost   RMS (2..18)                : {20*np.log10(rms(2,18)+1e-9):+6.1f} dBFS")
print(f"  foam    RMS (21..41)               : {20*np.log10(rms(21,41)+1e-9):+6.1f} dBFS")
print(f"  smoke   RMS (44..60)               : {20*np.log10(rms(44,60)+1e-9):+6.1f} dBFS")
print(f"  ink     RMS (70..90)               : {20*np.log10(rms(70,90)+1e-9):+6.1f} dBFS")
print(f"  ink tail RMS (last 2 s)            : {20*np.log10(rms(dur-2,dur)+1e-9):+6.1f} dBFS")
print(f"  L/R corr @ 3s: {np.corrcoef(mix[int(3*sr):int(6*sr),0], mix[int(3*sr):int(6*sr),1])[0,1]:+.3f}")
print(f"  L/R corr @ 50s: {np.corrcoef(mix[int(50*sr):int(53*sr),0], mix[int(50*sr):int(53*sr),1])[0,1]:+.3f}")
print(f"  L/R corr @ 95s: {np.corrcoef(mix[int(95*sr):int(98*sr),0], mix[int(95*sr):int(98*sr),1])[0,1]:+.3f}")
print(f"  peak after ink wash (last 4s): {np.abs(mix[int((dur-4)*sr):,0]).max():.3f}")
