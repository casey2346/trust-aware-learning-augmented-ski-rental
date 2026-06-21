# Day 6 Trust-Aware Fallback Algorithm

## Objective

Day 6 implements the core trust-aware fallback algorithm.

The goal is to avoid blindly trusting predictions.

Instead of using predictions directly, the algorithm introduces a confidence value:

c ∈ [0, 1]

This confidence controls how strongly the algorithm follows the prediction.

Motivation

Previous algorithms showed two extremes:

prediction-only algorithm:
    uses prediction completely
    can fail badly when prediction is wrong

deterministic baseline:
    ignores prediction completely
    is robust but cannot benefit from accurate predictions

The trust-aware algorithm aims to combine both:

use predictions when confidence is high
fallback to deterministic baseline when confidence is low
Definitions

Let:

T = true number of skiing days
B = buying cost
p = predicted number of skiing days
c = prediction confidence
λ = learning-augmented aggressiveness parameter

The deterministic baseline buying day is:

d_base = B

The prediction-aware buying day is:

d_pred =
    ceil(λB),   if p >= B
    B,          if p < B

The trust-aware buying day is:

d_trust = ceil(c · d_pred + (1 - c) · d_base)
Interpretation

If:

c = 1

then:

d_trust = d_pred

The algorithm fully trusts the prediction.

If:

c = 0

then:

d_trust = d_base = B

The algorithm ignores the prediction and falls back to the deterministic baseline.

If:

0 < c < 1

then the algorithm interpolates between the prediction-aware rule and the deterministic baseline.

Cost

Using the project convention:

ALG(T, B, d) =
    T,             if T < d
    (d - 1) + B,   if T >= d

the trust-aware cost is:

ALG_trust(T, B, p, λ, c) = ALG(T, B, d_trust)
Offline Optimum

The offline optimum remains:

OPT(T, B) = min(T, B)
Cost Ratio

The trust-aware cost ratio is:

CR_trust = ALG_trust / OPT
Adversarial Prediction Model

Day 6 evaluates the algorithm under adversarial predictions.

If:

T < B

then the adversary predicts:

p = 5B

This tries to make the algorithm buy too early.

If:

T >= B

then the adversary predicts:

p = 1

This tries to make the algorithm rent for too long.

Why Trust-Aware Does Not Collapse

When confidence is low:

c ≈ 0

the algorithm falls back to:

d_trust = B

This recovers the deterministic baseline.

Therefore, even if the prediction is adversarially wrong, the algorithm does not fully follow it.

This prevents the severe degradation of prediction-only policies.

Day 6 Outputs

Implemented:

src/ski_rental/trust_aware.py

Generated:

experiments/day6_trust_aware_curve.py
experiments/results/day6_trust_aware.csv
figures/day6_trust_aware_fallback.png