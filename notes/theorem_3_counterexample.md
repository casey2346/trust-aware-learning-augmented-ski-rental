# Theorem 3 Counterexample Proof Sketch

## Objective

This note gives a proof sketch for Theorem 3.

The goal is to show that trust-aware fallback prevents the unbounded degradation suffered by prediction-only policies under adversarial predictions.

## Informal Statement

A prediction-only algorithm can fail badly when the prediction is adversarial.

In particular, if the true number of skiing days is very large but the prediction says the season is very short, then prediction-only may keep renting for the entire season.

Its cost ratio then grows with `T / B`.

In contrast, the trust-aware algorithm falls back toward the deterministic ski-rental threshold and buys by day `B`.

Therefore, its cost ratio remains bounded.

## Setting

Let:

T = true number of skiing days
B = buying cost
p = predicted number of skiing days

The offline optimum is:

OPT(T, B) = min(T, B)

For an algorithm that buys on day `d`, the cost is:

ALG(T, B, d) =
    T,            if T < d
    (d - 1) + B,  if T ≥ d

## Prediction-Only Policy

The prediction-only policy fully trusts the prediction.

A simple prediction-only rule is:

if p ≥ B:
    buy immediately
else:
    rent forever

This rule is consistent when predictions are accurate, but it is fragile when predictions are adversarial.

## Trust-Aware Fallback Policy

The trust-aware policy does not fully trust the prediction.

It uses a fallback buying threshold controlled by the deterministic ski-rental baseline.

The deterministic baseline buys on day:

d_base = B

Under low confidence, the trust-aware algorithm falls back to:

d_trust = B

Therefore, it buys no later than the deterministic ski-rental threshold.

## Assumptions

We assume:

1. B > 0.
2. T can be arbitrarily large.
3. The prediction may be adversarial.
4. The prediction-only policy rents forever when p < B.
5. The trust-aware policy buys no later than day B under low confidence.

The prediction error is:

η = |p - T|

In this theorem, `η` may be arbitrarily large.

## Claim

There exists an adversarial prediction such that the prediction-only policy has unbounded competitive ratio.

However, under the same adversarial prediction, the trust-aware fallback policy remains constant-competitive.

More precisely:

CR_prediction_only = T / B

which becomes unbounded as:

T / B → ∞

while:

CR_trust_aware ≤ (2B - 1) / B < 2

when the trust-aware algorithm falls back to buying on day `B`.

## Counterexample Construction

Choose a large true duration:

T >> B

but give the algorithm a very small prediction:

p = 1

Since:

p < B

the prediction-only policy believes the season will be short.

Therefore, prediction-only rents forever.

## Prediction-Only Cost

Because the prediction-only policy rents forever, its cost is:

C_prediction_only(T, B, p) = T

Since:

T >> B

the offline optimum buys skis and pays:

OPT(T, B) = B

Therefore, the competitive ratio is:

CR_prediction_only
= C_prediction_only(T, B, p) / OPT(T, B)
= T / B

As `T` grows while `B` is fixed:

T / B → ∞

Thus, prediction-only suffers unbounded degradation under this adversarial prediction.

## Trust-Aware Fallback Cost

Now consider the trust-aware algorithm under the same adversarial prediction.

Because confidence is low, the trust-aware algorithm falls back to the deterministic threshold:

d_trust = B

Since:

T ≥ B

the trust-aware algorithm rents for `B - 1` days and then buys.

Therefore, its cost is:

C_trust(T, B, p, c)
= (B - 1) + B
= 2B - 1

The offline optimum is still:

OPT(T, B) = B

So the competitive ratio is:

CR_trust_aware
= C_trust(T, B, p, c) / OPT(T, B)
= (2B - 1) / B
= 2 - 1/B
< 2

Thus, trust-aware fallback remains constant-competitive.

## Cost Decomposition

The separation can be seen through the cost decomposition.

For prediction-only:

C_prediction_only = rental cost over the whole season
                  = T

There is no fallback buying threshold, so the cost grows linearly with `T`.

For trust-aware fallback:

C_trust = rental cost before fallback buying + buying cost
        = (B - 1) + B
        = 2B - 1

The fallback threshold prevents the algorithm from renting forever.

## Error Term

The prediction error in this counterexample is:

η = |p - T| = |1 - T| = T - 1

As:

T → ∞

we have:

η → ∞

So the prediction error is unbounded.

Prediction-only has no protection against this error, so its ratio grows as:

T / B

Trust-aware fallback is protected by the deterministic threshold, so its ratio remains bounded by:

2 - 1/B

## Interpretation

This theorem shows a separation between prediction-only and trust-aware policies.

Prediction-only may be highly consistent under accurate predictions, but it is not robust.

Trust-aware fallback sacrifices some aggressiveness in order to prevent catastrophic failure.

The key difference is:

prediction-only fully trusts p
trust-aware controls how much p can affect the buying day

## Conclusion

The counterexample proves that prediction-only policies can suffer unbounded degradation under adversarial predictions.

When:

T >> B
p = 1

prediction-only rents forever and obtains:

CR_prediction_only = T / B → ∞

But trust-aware fallback buys by day `B` and obtains:

CR_trust_aware = 2 - 1/B < 2

Therefore, trust-aware fallback prevents the unbounded degradation suffered by prediction-only policies.

This establishes the proof sketch for Theorem 3.
