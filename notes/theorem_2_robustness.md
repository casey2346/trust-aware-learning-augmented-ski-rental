# Theorem 2 Robustness Proof Sketch

## Objective

This note gives a proof sketch for the robustness property of the trust-aware learning-augmented ski rental algorithm.

The goal is to show that even under arbitrary prediction error, the trust-aware algorithm remains constant-competitive as long as its buying threshold is controlled by the deterministic ski-rental threshold.

## Informal Statement

Predictions may be completely wrong.

However, the trust-aware algorithm does not blindly follow predictions.

Instead, it uses a fallback mechanism that keeps the buying day close to the deterministic baseline.

Therefore, the algorithm avoids unbounded loss from arbitrary prediction errors.

## Setting

Let:

T = true number of skiing days
B = buying cost
p = predicted number of skiing days
λ ∈ (0, 1] = prediction-aggressive buying parameter
c ∈ [0, 1] = confidence level

The offline optimum is:

OPT(T, B) = min(T, B)

For an online algorithm that buys on day `d`, the cost is:

ALG(T, B, d) =
    T,           if T < d
    (d - 1) + B, if T ≥ d

The deterministic ski-rental baseline buys on day:

d_base = B

and has cost at most:

2B - 1

when the season is long.

## Trust-Aware Buying Day

The prediction-augmented buying day is:

d_pred =
    ceil(λB), if p ≥ B
    B,        if p < B

The trust-aware buying day is:

d_trust = ceil(c · d_pred + (1 - c) · B)

This means the trust-aware algorithm interpolates between:

d_pred

and:

B

When confidence is low, the buying day moves back toward the deterministic threshold.

When confidence is high, the algorithm can move closer to the prediction-augmented threshold.

## Assumptions

We assume:

1. B > 0.
2. λ ∈ (0, 1] is a fixed constant.
3. c ∈ [0, 1].
4. The buying day is capped by the deterministic threshold:
       d_trust ≤ B.
5. The buying day is not allowed to be arbitrarily early:
       d_trust ≥ λB.
6. Prediction error η = |p - T| may be arbitrary.

The important point is that Theorem 2 does not require the prediction to be accurate.

The prediction can be completely wrong.

Robustness comes from the buying-day cap and fallback structure, not from prediction quality.

## Claim

Under arbitrary prediction error, if the trust-aware buying day satisfies:

λB ≤ d_trust ≤ B

for some constant:

λ ∈ (0, 1]

then the trust-aware algorithm is constant-competitive.

More precisely:

C_trust(T, B, p, c) / OPT(T, B) ≤ 1 + 1/λ

Therefore:

C_trust(T, B, p, c) = O(OPT(T, B))

when `λ` is treated as a fixed constant.

## Proof Idea

The proof does not rely on the prediction being correct.

Instead, it only uses the fact that the trust-aware buying day is bounded between:

λB

and:

B
This prevents two failure modes.

First, the algorithm cannot rent forever, because it buys no later than the deterministic threshold `B`.

Second, the algorithm cannot buy arbitrarily early, because it buys no earlier than `λB`.

Thus, even if the prediction is adversarial, the algorithm behaves like a controlled deterministic ski-rental strategy.

## Case Analysis

Let:

d = d_trust

We analyze two cases.

## Case 1: T < d

If the season ends before the algorithm buys, then the algorithm only rents.

Thus:

C_trust(T, B, p, c) = T

Since:

OPT(T, B) = min(T, B)

and `T < d ≤ B`, we have:

OPT(T, B) = T

Therefore:

C_trust(T, B, p, c) / OPT(T, B) = T / T = 1

So the algorithm is optimal in this case.

## Case 2: T ≥ d

If the season lasts until the buying day, then the algorithm rents for `d - 1` days and then buys.

Thus:

C_trust(T, B, p, c) = (d - 1) + B

Since:

d ≤ B

we get:

C_trust(T, B, p, c) ≤ 2B - 1

Now we lower-bound the offline optimum.

Because:

T ≥ d

and:

d ≥ λB

we have:

T ≥ λB

Therefore:

OPT(T, B) = min(T, B) ≥ λB

So:

C_trust(T, B, p, c) / OPT(T, B)
≤ (2B - 1) / (λB)
≤ 2 / λ

This already proves constant competitiveness for fixed `λ`.

A slightly looser but simpler bound is:

C_trust(T, B, p, c) / OPT(T, B) = O(1/λ)

Since `λ` is fixed, this is:

O(1)

## Cost Decomposition

The trust-aware cost can be decomposed as:

C_trust(T, B, p, c)
= rental cost before buying + buying cost

When `T ≥ d_trust`, this is:

C_trust(T, B, p, c)
= (d_trust - 1) + B

The fallback cap ensures:

d_trust ≤ B

so:

C_trust(T, B, p, c) ≤ 2B - 1

The lower bound:

d_trust ≥ λB

ensures that if the algorithm buys, then the true duration must satisfy:

T ≥ λB

so the offline optimum is not too small.

This prevents the cost ratio from becoming unbounded.

## Error Term

Unlike Theorem 1, Theorem 2 does not need a small prediction error term.

The prediction error:

η = |p - T|

may be arbitrary.

The robustness bound is independent of `η`.

Therefore, the error term is controlled by the algorithmic fallback structure rather than prediction accuracy.

We can write:

C_trust(T, B, p, c) / OPT(T, B)
≤ O(1/λ)

for all predictions `p`.

Since `λ` is fixed, this becomes:

C_trust(T, B, p, c) / OPT(T, B)
≤ O(1)

The important robustness message is:

arbitrary prediction error does not cause unbounded competitive ratio

as long as the algorithm does not buy too late or too early.

## Role of Low Confidence

When confidence is low:

c ≈ 0

the trust-aware buying day becomes close to:

B

because:

d_trust = ceil(c · d_pred + (1 - c) · B)

Thus, in low-confidence settings, the algorithm behaves similarly to the deterministic baseline.

This directly prevents the algorithm from following unreliable predictions.

## Conclusion

The trust-aware algorithm is robust because its buying threshold is controlled.

Even if the prediction is arbitrarily wrong, the algorithm remains constant-competitive when:

λB ≤ d_trust ≤ B

The upper bound:

d_trust ≤ B

prevents renting much longer than the deterministic baseline.

The lower bound:

d_trust ≥ λB

prevents buying arbitrarily early.

Therefore:

C_trust(T, B, p, c) / OPT(T, B) ≤ O(1/λ)

and for fixed `λ`:

C_trust(T, B, p, c) / OPT(T, B) ≤ O(1)

This establishes the proof sketch for Theorem 2.
