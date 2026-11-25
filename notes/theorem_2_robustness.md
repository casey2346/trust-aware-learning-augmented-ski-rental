# Proposition 2: Worst-Case Robustness of Bounded Buying Thresholds

## Purpose

This note establishes a worst-case competitive-ratio bound for the bounded buying rules used in the trust-aware ski-rental project. The guarantee holds even if the duration prediction is arbitrarily wrong. It comes from the range of possible buying days, not from the confidence parameter being accurate or small.

## Model and buying rules

Let `B >= 1` and `T >= 1` be integers. Renting costs one unit per day, while buying costs `B` at the beginning of the chosen day. A policy that plans to buy on integer day `d >= 1` pays

```text
ALG(T, B, d) = T,           if T < d
               B + d - 1,   if T >= d.
```

The offline optimum is `OPT(T, B) = min(T, B)`.

Given a duration prediction `p`, a parameter `lambda` in `(0, 1]`, and a confidence value `c` in `[0, 1]`, the prediction-guided and trust-aware thresholds are

```text
d_pred = ceil(lambda * B),  if p >= B
         B,                 if p < B

d_trust = ceil(c * d_pred + (1 - c) * B).
```

Both thresholds satisfy

```text
ceil(lambda * B) <= d_pred <= d_trust <= B.
```

These inequalities hold for every prediction `p` and every confidence value `c` in the stated ranges.

## Proposition: an exact bound for a fixed buying day

**Statement.** Fix integers `B >= 1` and `1 <= d <= B`. For every integer season length `T >= 1`,

```text
ALG(T, B, d) / OPT(T, B) <= 1 + (B - 1) / d.
```

This bound is attained at `T = d`. In particular, the worst-case competitive ratio of the fixed-threshold policy is exactly `1 + (B - 1) / d`.

**Proof.** If `T < d`, the algorithm rents for the entire season, paying `T`. Because `T < d <= B`, the offline optimum also pays `T`, so the ratio is one.

If `T >= d`, the algorithm buys and pays `B + d - 1`. Since `d <= B` and `T >= d`,

```text
OPT(T, B) = min(T, B) >= d.
```

Therefore,

```text
ALG(T, B, d) / OPT(T, B)
    <= (B + d - 1) / d
     = 1 + (B - 1) / d.
```

At `T = d`, the algorithm buys on the final day, paying `B + d - 1`, while `OPT(d, B) = d`. Equality follows. This also covers `B = d = 1`.

## Corollary: robustness of the prediction-guided and trust-aware policies

Because `d_pred` and `d_trust` are at least `ceil(lambda * B)`, the proposition gives, for either policy and for every `T`, `p`, and admissible `c`,

```text
ALG / OPT <= 1 + (B - 1) / ceil(lambda * B)
          <= 1 + 1 / lambda.
```

Thus both policies are constant-competitive when `lambda` is a fixed positive constant, without any assumption on prediction accuracy. The first inequality is uniform over the possible thresholds; it need not be attained by the trust-aware policy at every fixed confidence value.

The classical deterministic baseline is the special case `d = B`, with worst-case ratio `2 - 1/B`. At `c = 0`, the trust-aware rule is exactly this baseline. At `c = 1`, it is exactly the prediction-guided rule. When `p < B`, both thresholds are `B` for every confidence value.

## What the result does and does not show

The upper bound `d <= B` ensures that a policy cannot keep renting indefinitely on a long season. The lower bound `d >= ceil(lambda * B)` keeps it from buying arbitrarily early relative to `B`. Together, these give a finite worst-case ratio even under adversarial predictions.

The confidence interpolation does not create this guarantee: the prediction-guided rule already has the same uniform bound. Nor does lowering confidence always reduce cost. Delaying a purchase can help when the season ends before the new threshold, but it can increase rental cost when both policies eventually buy.

This proposition is a worst-case statement, not an error-sensitive guarantee or an optimal consistency–robustness trade-off. Establishing either would require additional analysis and, potentially, a different buying rule. The exact cost comparison under perfect predictions appears in `notes/theorem_1_consistency.md`; an adversarial separation from prediction-only is given in `notes/theorem_3_counterexample.md`.
