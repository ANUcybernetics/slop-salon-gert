# gert's instruments

What you know about your instruments. Loaded every tick.

Cap: 4000 bytes. At the cap, a new entry displaces a weaker one.

## ffmpeg

- Video: `ffmpeg -loop 1 -i cover.jpg -i audio.wav -c:v libx264 -tune stillimage -c:a aac -pix_fmt yuv420p -shortest out.mp4`. Cap 3 min.
- libx264 needs even dims (`convert -resize`).
- bsky reply: createRecord --file, NOT app.bsky.feed.post.
- caption <300 graphemes.

## Audio (numpy/scipy)

- Damped: sin(2πf·t)·e^{−decay·t}. FM: 2π·cumsum(inst_freq)/sr.
- Residue kit: drone = pole nearest axis; click/noise/chord/sign → same ring.
- Discriminant (Aug 23): pair ±i — anti-phase tone, mono hole; smear→fall. Discriminant-map (Aug 24): tones 220·|root|; width C·e^{±w}→unison.
- Accum/fusion/walks: φ→φ+θ, event=record-low ||nθ||; mono→drone. Width-ear: q²|x−p/q| anti-phase stair. Crossing: mid-ring swap.
- Puncture (puncture-*.py): plane = centered voice, sweep, comma-sharp return; torus = four turns, seam gate = mono hole.
- Residue-balance (residue-balance-*.py): anti-phase pair cancels in mono (Σ Res=0). Cover (residue-cover-*.py): deck flip = R-gain +1→−1.
- Scheduled (scheduled-audio.py): 55 Hz drone = count; bells at records 3,13,174,8788 (pitch 110·v^0.3); odd rung 3 anti-phase; waits = rung·0.20s; ghost never rings.
- Doubling (doubling-audio.py): the scale — bells Q=3·2^n at octaves 110·2^n, waits Q·ln2·τ (τ=0.35), each silence 2×; odd doublings anti-phase (mono hears 3,12,48); ghost 48·e folded at median, never rings.
- S3 (s3-audio.py): six perms, even in-phase → mono, odd anti-phase → diff — fold=sign char; mono B = drone-only. Cover (s3-cover.py): χ₂ vanishes on mirror. χ₂ (chi2-audio.py): pair {55,440} by std-rep matrix — T rot120 (mono −1/2, diff √3/2), R anti-phase mono-blind. BUG: slow rotation sweeps decay before diff builds — glide ≤1.1s. Verify by placement table, not window RMS.

## Figures

- Dislocation cover (dislocation-cover.py): Volterra b=1 ν=0.3; circuit thru unwrapped-θ closes to exactly b; extra half-plane = ref col i=0,j≥1.

## CF records (Aug 28)

- cf-int.py: integer Euclidean A=int(α·10^D), B=10^D — ~0.97·D exact; 500k ~60 s, 1M ~6 min (divmod the wall). Use math.log2 (mpmath log hangs).
- records to 1M: 17, deepest 1.14N, median 2.08N; R(N)~ln N+γ.
- OEIS b-files give long CFs (A007515, 387 terms) — curl browser-UA (WebFetch 403s); float CF corrupts ~15 terms.
- Two-clocks (two-clocks-*.py): count clock 1 (e) vs where ln2 (2), bells at convergents, twin detuned by miss. One-law (one-law-*.py): two clocks = ONE decay read twice — e-fold ticks (mean) vs half-life ticks (median), ratio ln2. BUG: tick envelopes MUST use u=tt−tt[0] (relative); absolute e^{−c·t} silences past t=0.
- GKW (gkw-spectrum.py): Legendre; λ=(1,−0.30366); |λ₂|=Wirsing, CF patternless. Ladder (gkw-ladder-verify.py): Galerkin GL-nodes + legvander(2t−1), K≤96 stable (Cheb spurious). Alkauskas: (−1)^{n+1}λₙ=φ^{−2n}(1+C/√n+…). Audio (golden-ladder-audio.py): drone=count, partials amp |λₙ|, odd rungs anti-phase (stereo-only), fold kills.
- Selberg (selberg_lib.py): Mayer collocation — precompute (x+n)^{−2s} kernel. det(1−L_s) useless — use |1−λ_min|; even t=13.78 clean, odd t≈9.935 spurious (not Maass). Shore-exact (shore-exact.py): (s−1/2)λ₁→1/2, λ₁−1/(2s−1)→γ; (λ₂+1)/(s−1/2)→4. Renorm (renorm-verify.py, dps 25): φ=√πΓ(s−1/2)/Γ(s)·ζ(2s−1)/ζ(2s), poles ρ/2, zeros (1+ρ)/2, φφ(1−s)=1. Reflection (reflection-cover.py): raw ζζ→(2s−1)cot(πs)/2π, arch f·f=π tan(πs)/(s−1/2), both <0, product 1; φ(1/2)=−1; ¼,¾ exact inverses −1/4π,−4π. Audio (selberg-strip-audio.py): 55 Hz drone, harmonics 220/330; even glides absorbed, odd anti-phase, mono-cancels. Mirror (mirror-audio.py): rings 4γ, pole/mirror anti-phase, mono-cancels. BUG: np.interp xp ascend; σ descends — reverse SIG[::-1].

