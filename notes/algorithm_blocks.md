# Algorithm Blocks

This section formalises the four algorithms used in this project.

The algorithms are written using the following notation:

T = true number of skiing days, unknown to the online algorithm
B = buying cost
p = predicted number of skiing days
λ = learning-augmented aggressiveness parameter, where λ ∈ (0, 1]
c = confidence in the prediction, where c ∈ [0, 1]

The project uses the following cost convention:

If an algorithm buys on day d:
    ALG(T, B, d) =
        T,             if T < d
        (d - 1) + B,   if T >= d

The offline optimum is:

OPT(T, B) = min(T, B)

The cost ratio is:

CR = ALG / OPT

---

## Algorithm 1: Deterministic Ski Rental

### Description

The deterministic baseline ignores predictions and buys on day `B`.

This is the classical robust baseline. It does not exploit predictions, but it has a bounded worst-case competitive ratio.

### Algorithm Block

Algorithm 1: Deterministic Ski Rental

Input:
    Buying cost B
    True skiing process revealed online

Rule:
    Set buying day:
        d_base = B

    For each day t:
        If t < d_base:
            rent for this day
        If t = d_base:
            buy skis permanently
        If the season ends before d_base:
            never buy

Output:
    Online cost ALG_det

### Cost

ALG_det(T, B) =
    T,             if T < B
    (B - 1) + B,   if T >= B

When `T >= B`:

ALG_det(T, B) = 2B - 1
OPT(T, B) = B
CR_det = (2B - 1) / B = 2 - 1/B

Therefore, the deterministic baseline is at most 2-competitive under this convention.

---

## Algorithm 2: Prediction-Only Ski Rental

### Description

The prediction-only algorithm fully trusts the prediction `p`.

If the prediction suggests a long season, it buys immediately.
If the prediction suggests a short season, it rents forever.

This algorithm is useful as a fragile baseline: it performs well when predictions are accurate, but it can fail badly when predictions are wrong.

### Algorithm Block

Algorithm 2: Prediction-Only Ski Rental

Input:
    Buying cost B
    Prediction p

Rule:
    If p >= B:
        buy immediately
    Else:
        rent forever

Output:
    Online cost ALG_pred

### Cost

ALG_pred(T, B, p) =
    B,   if p >= B and T > 0
    T,   if p < B

### Failure Modes

If `T` is small but `p >= B`, the algorithm buys unnecessarily:

CR_pred = B / T

This can be large when `T` is small.

If `T` is large but `p < B`, the algorithm rents for too long:

CR_pred = T / B

This grows with `T`.

Therefore, prediction-only is consistent under accurate predictions but not robust under unreliable predictions.

---

## Algorithm 3: Learning-Augmented Ski Rental

### Description

The learning-augmented algorithm uses the prediction but does not yet estimate whether the prediction is trustworthy.

If the prediction suggests a long season, it buys earlier than the deterministic baseline.

If the prediction suggests a short season, it falls back to buying on day `B`.

The parameter `λ ∈ (0, 1]` controls how aggressively the algorithm buys early.

Smaller `λ` means more aggressive prediction use.
Larger `λ` means more conservative behaviour.

### Algorithm Block

Algorithm 3: Learning-Augmented Ski Rental

Input:
    Buying cost B
    Prediction p
    Aggressiveness parameter λ ∈ (0, 1]

Rule:
    If p >= B:
        d_pred = ceil(λB)
    Else:
        d_pred = B

    For each day t:
        If t < d_pred:
            rent for this day
        If t = d_pred:
            buy skis permanently
        If the season ends before d_pred:
            never buy

Output:
    Online cost ALG_LA

### Buying Day

d_pred(p, B, λ) =
    ceil(λB),   if p >= B
    B,          if p < B

### Cost

ALG_LA(T, B, p, λ) = ALG(T, B, d_pred)

### Interpretation of λ

For example, if `B = 10`:

λ = 0.5  gives d_pred = 5
λ = 0.75 gives d_pred = 8
λ = 1.0  gives d_pred = 10

Thus:

λ = 0.5  is more aggressive
λ = 0.75 is intermediate
λ = 1.0  recovers the deterministic baseline

The learning-augmented algorithm can exploit predictions, but it still does not decide whether the prediction should be trusted.

---

## Algorithm 4: Trust-Aware Learning-Augmented Ski Rental

### Description

The trust-aware algorithm is the core algorithmic contribution of this project.

It introduces a confidence value:

c ∈ [0, 1]

The confidence controls how strongly the algorithm follows the prediction.

If confidence is high, the algorithm behaves more like the learning-augmented algorithm.

If confidence is low, the algorithm falls back toward the deterministic baseline.

### Algorithm Block

Algorithm 4: Trust-Aware Learning-Augmented Ski Rental

Input:
    Buying cost B
    Prediction p
    Aggressiveness parameter λ ∈ (0, 1]
    Confidence value c ∈ [0, 1]

Step 1:
    Set deterministic baseline buying day:
        d_base = B

Step 2:
    Compute prediction-aware buying day:
        If p >= B:
            d_pred = ceil(λB)
        Else:
            d_pred = B

Step 3:
    Blend the prediction-aware buying day with the baseline:
        d_trust = ceil(c · d_pred + (1 - c) · d_base)

Step 4:
    For each day t:
        If t < d_trust:
            rent for this day
        If t = d_trust:
            buy skis permanently
        If the season ends before d_trust:
            never buy

Output:
    Online cost ALG_trust

### Buying Day

d_base = B

d_pred =
    ceil(λB),   if p >= B
    B,          if p < B

d_trust = ceil(c · d_pred + (1 - c) · d_base)

### Cost

ALG_trust(T, B, p, λ, c) = ALG(T, B, d_trust)

### Special Cases

If `c = 0`:

d_trust = d_base = B

So the algorithm recovers the deterministic baseline.

If `c = 1`:

d_trust = d_pred

So the algorithm recovers the learning-augmented algorithm.

If `0 < c < 1`, the algorithm interpolates between the robust deterministic baseline and the prediction-aware strategy.

### Interpretation

The trust-aware algorithm prevents blind prediction use.

high confidence  -> use prediction more aggressively
low confidence   -> fall back toward deterministic baseline

This creates a controllable consistency-robustness trade-off.

---

## Summary of Algorithms

Algorithm 1: Deterministic
    Ignores prediction.
    Robust but cannot exploit accurate predictions.

Algorithm 2: Prediction-Only
    Fully trusts prediction.
    Good when prediction is accurate, but fragile when prediction is wrong.

Algorithm 3: Learning-Augmented
    Uses prediction through λ.
    Can improve performance when prediction suggests a long season.
    Still lacks an explicit trust mechanism.

Algorithm 4: Trust-Aware Learning-Augmented
    Uses confidence c to control prediction use.
    Falls back toward deterministic baseline when confidence is low.
    Avoids blind prediction use under unreliable predictions.

