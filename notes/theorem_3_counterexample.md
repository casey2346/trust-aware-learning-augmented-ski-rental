# Proposition 3: An Adversarial Separation from Prediction-Only

## Purpose

This note gives an explicit example in which the prediction-only ski-rental policy has an unbounded competitive ratio, while the prediction-guided and trust-aware policies retain bounded costs. The example isolates the effect of imposing a buying deadline; it does not establish a new lower bound for learning-augmented algorithms.

## Model and policies

Let `B > 1` be a fixed integer and `T >= 1` the unknown season length. Renting costs one per day, and buying costs `B` at the beginning of a day. A policy with integer buying day `d` pays

```text
ALG(T, B, d) = T,          if T < d
               B + d - 1,  if T >= d.
```

The offline optimum pays `OPT(T, B) = min(T, B)`. The algorithm receives a predicted duration `p`.

The **prediction-only** policy buys immediately when `p >= B` and otherwise rents for the whole season. The **prediction-guided** policy uses

```text
d_pred = ceil(lambda * B),  if p >= B
         B,                 if p < B,
```

where `lambda` is in `(0, 1]`. The **trust-aware** policy uses

```text
d_trust = ceil(c * d_pred + (1 - c) * B),
```

where `c` is in `[0, 1]`.

## Proposition

For the prediction-only policy above, there is no finite competitive-ratio bound when predictions can be arbitrary. In contrast, on the same adversarial inputs, both bounded-threshold policies have competitive ratio `2 - 1/B` for every value of `lambda` and `c` in their stated ranges.

## Proof

Fix any integer `B > 1` and give the algorithms the prediction

```text
p = 1 < B.
```

Now let the actual season length `T` range over integers with `T >= B`, growing without bound.

**Prediction-only.** Since `p < B`, this policy never buys. It pays `T`, while the offline optimum pays `B`. Therefore

```text
C_prediction_only / OPT = T / B -> infinity as T -> infinity.
```

No constant competitive-ratio bound can hold for this policy over unrestricted predictions.

**Prediction-guided and trust-aware.** The same prediction `p < B` gives `d_pred = B`. Consequently,

```text
d_trust = ceil(c * B + (1 - c) * B) = B
```

for **every** confidence value `c` in `[0, 1]`. Because `T >= B`, both policies buy on day `B` and pay `2B - 1`. Their competitive ratio is exactly

```text
C_pred / OPT = C_trust / OPT = (2B - 1) / B = 2 - 1/B < 2.
```

This proves the separation. The prediction error `|p - T| = T - 1` grows without bound, but the two bounded-threshold policies' ratios remain fixed in this example.

## What the example shows

The prediction-only policy fails because an incorrect short-season forecast makes it rent throughout an arbitrarily long season. The other two policies have a finite buying deadline. On this particular input, they behave exactly like the classical deterministic baseline.

This outcome **does not depend on low confidence**: when `p < B`, both thresholds are `B` for all `c`. The example therefore cannot be used to show that confidence weighting improves robustness over the prediction-guided policy. More generally, Proposition 2 gives a finite competitive-ratio guarantee for both bounded-threshold policies under arbitrary predictions.

The counterexample concerns the specific prediction-only rule defined here, not every possible algorithm that uses predictions. It is not an optimality result or a lower bound for the broader class of learning-augmented ski-rental algorithms.

For the uniform robustness bound, see `notes/theorem_2_robustness.md`. The complete model and related cost comparison are given in `paper/technical_report.md`.
