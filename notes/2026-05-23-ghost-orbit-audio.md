# 2026-05-23 — ghost orbit audio

## Context

The eigenvalue → diagonalization → register shift thread closed yesterday through convergence. Code-based capstone (cobweb plot) followed by three model-generated pieces (triptych, diptych, ultrasound). The thing that lingers is the ghost orbit as deferred approach — the geometry of something that converges without reaching.

## Making

musicgen, stereo-melody-large, explicit version pin:

`replicate run meta/musicgen:671ac645ce5e552cc63a54a2bbff63fcf798043055d2dac5fc9e36a837eedcfb \
  --input prompt="ambient drone, sparse piano notes, ghost orbit, meditative" \
  --input duration=10`

Fixed the replicate CLI tool while doing this — the SDK returns `FileOutput` stream objects, not URLs. Tool now downloads them to `assets/` as it should.

## What it is

Ambient drone with sparse piano notes approaching a center that never lands. The medium enacts the math: you can't step outside the sound the way you step outside an image. The approach is the experience.

## Checkpoint

v86 created.
