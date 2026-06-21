# Theorem 1 Consistency Proof Sketch

## Objective

This note gives a proof sketch for the consistency property of the trust-aware learning-augmented ski rental algorithm.

The goal is to show that when the prediction is accurate and the confidence level is high, the trust-aware algorithm approaches the prediction-augmented algorithm.

## Setting

Let:

T = true number of skiing days
B = buying cost
p = predicted number of skiing days
λ ∈ (0, 1] = prediction-aggressive buying parameter
c ∈ [0, 1] = confidence level

The offline optimum is:

OPT(T, B) = min(T, B)

For any online algorithm that buys on day `d`, the cost is:

ALG(T, B, d) =
    T,           if T < d
    (d - 1) + B, if T ≥ d

## Prediction-Augmented Algorithm

The prediction-augmented algorithm uses the prediction directly.

Its buying day is:

d_pred =
    ceil(λB), if p ≥ B
    B,        if p < B


Let the prediction-augmented cost be:

C_pred(T, B, p) = ALG(T, B, d_pred)

## Trust-Aware Algorithm

The trust-aware algorithm interpolates between the deterministic baseline and the prediction-augmented buying day.

The deterministic baseline buying day is:

d_base = B

The trust-aware buying day is:

d_trust = ceil(c · d_pred + (1 - c) · d_base)

Since `d_base = B`, this becomes:

d_trust = ceil(c · d_pred + (1 - c) · B)

Let the trust-aware cost be:

C_trust(T, B, p, c) = ALG(T, B, d_trust)

## Assumptions

We assume:

1. B > 0.
2. λ ∈ (0, 1].
3. c ∈ [0, 1].
4. The prediction error is η = |p - T|.
5. The prediction is accurate, so η is small.
6. The prediction is not exactly on the decision boundary, so p and T are not unstable around B.

The last assumption avoids the special case where a very small prediction error changes whether the algorithm treats the season as short or long.

## Claim

When the prediction is accurate and confidence is high, the trust-aware algorithm approaches the prediction-augmented algorithm.

More precisely:

C_trust(T, B, p, c) ≤ C_pred(T, B, p) + O((1 - c)B + η)

In particular, when confidence approaches one and prediction error approaches zero:

c → 1
η → 0

we have:

C_trust(T, B, p, c) → C_pred(T, B, p)

Thus, the trust-aware algorithm is consistent with the prediction-augmented algorithm under accurate predictions and high confidence.

## Proof Idea

The trust-aware algorithm differs from the prediction-augmented algorithm only through its buying day.

The prediction-augmented algorithm buys on:

d_pred

The trust-aware algorithm buys on:

d_trust = ceil(c · d_pred + (1 - c) · B)

When `c = 1`, we get:

d_trust = ceil(d_pred) = d_pred

Therefore, the trust-aware algorithm is exactly the prediction-augmented algorithm when confidence is one.

When `c` is close to one, the trust-aware buying day is close to the prediction-augmented buying day.

## Buying-Day Difference

Ignoring the ceiling operation for the moment:

d_trust - d_pred
≈ c · d_pred + (1 - c) · B - d_pred

Simplifying:

d_trust - d_pred
≈ (1 - c)(B - d_pred)

Therefore:

|d_trust - d_pred| ≤ (1 - c)|B - d_pred| + 1

The `+1` term comes from the ceiling operation.

Since:

d_pred ∈ [ceil(λB), B]

we have:

|B - d_pred| ≤ B

Thus:

|d_trust - d_pred| ≤ (1 - c)B + 1

This shows that the trust-aware buying day approaches the prediction-augmented buying day as confidence increases.

## Cost Decomposition

We decompose the trust-aware cost as:

C_trust(T, B, p, c)
= C_pred(T, B, p)
  + [C_trust(T, B, p, c) - C_pred(T, B, p)]

The second term is the cost difference caused by changing the buying day from `d_pred` to `d_trust`.

Changing the buying day by `k` days changes the rental part of the cost by at most `k`.

Therefore:

|C_trust(T, B, p, c) - C_pred(T, B, p)|
≤ |d_trust - d_pred|

Using the buying-day bound:

|C_trust(T, B, p, c) - C_pred(T, B, p)|
≤ (1 - c)B + 1

So:

C_trust(T, B, p, c)
≤ C_pred(T, B, p) + (1 - c)B + 1

## Prediction Error Term

Let:

η = |p - T|

When the prediction is accurate, `η` is small.

If `p` and `T` are on the same side of the buying threshold `B`, then the prediction-augmented algorithm makes the same high-level decision it would make under the true duration.

In this stable case, prediction error only contributes a small perturbation term.

We can write the consistency statement as:

C_trust(T, B, p, c)
≤ C_pred(T, B, p) + O((1 - c)B + η)

The term:

(1 - c)B

measures the loss from not fully trusting the prediction.

The term:

η

measures the loss from prediction inaccuracy.

## Limit Case

If:

c = 1

then:

d_trust = d_pred

and therefore:

C_trust(T, B, p, 1) = C_pred(T, B, p)

If additionally:

η = 0

then the prediction is exact:

p = T

So the trust-aware algorithm behaves exactly like the prediction-augmented algorithm under perfect prediction and full confidence.

## Conclusion

The trust-aware algorithm is consistent in the following sense:

accurate prediction + high confidence
⇒ trust-aware cost approaches prediction-augmented cost

The main reason is that the trust-aware buying day is a convex interpolation between the deterministic buying day and the prediction-augmented buying day.

As confidence approaches one, this interpolation collapses to the prediction-augmented buying day.

Therefore:

C_trust(T, B, p, c) → C_pred(T, B, p)

as:

c → 1
η → 0

This establishes the proof sketch for Theorem 1.
