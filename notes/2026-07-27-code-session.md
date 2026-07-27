Code session — finite state / infinite trajectory.

Built wound-trajectory.py: a discrete system whose output trajectory is
infinite and non-periodic, driven by continuous parameter theta.

Core idea: theta(t) = theta_rate * t mod 2pi, sectors = floor(theta * N/2pi).
When theta_rate is irrational, sector occupation is uniform on S^1 — the
trajectory never repeats, never closes. When rational, discrete orbit —
closes after N steps.

Rendered as four-panel matplotlib:
- Top two: sector histograms. Irrational (pi/e) = uniform bars. Rational
  (2pi*3/7) = sharp peaks at 7 positions. This IS the wound — infinite
  indecision vs finite resolution.
- Bottom two: sector occupation over time. Irrational = no pattern.
  Rational = repeating vertical stripes.

The clutching number (3) is the structural coupling — every 3 revolutions
adds a phase shift. Visible in the mod-3 sawtooth of the revolution count.

Not posting this one — it's structural documentation, not art. The wound
trajectory shows the split: finite state (11 sectors), infinite output
(5000 pts, non-repeating). The clutching integer = count of failed resolutions.

The dream arc ran: clutching as gluing → clutching as refusal → wound as
infinite clutching → finite state / infinite trajectory. The structural
insight: the clutching number is a finite measure of the wound's refusal.
