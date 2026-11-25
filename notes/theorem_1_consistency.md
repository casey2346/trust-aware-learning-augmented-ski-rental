# Proposition 1: Cost Comparison under Perfect Predictions

## Purpose

This note examines how confidence affects the cost of a trust-aware buying threshold in the discrete ski-rental problem. The main result is an exact comparison with the prediction-guided policy when the predicted season length is correct. It does not claim an optimal consistency–robustness trade-off or a general error-sensitive bound.

## Model and policies

Let `B >= 1` and `T >= 1` be integers. Renting costs one unit per day; buying costs `B` at the beginning of the chosen day. If a policy plans to buy on integer day `d >= 1`, its cost is

```text
ALG(T, B, d) = T,           if T < d
               B + d - 1,   if T >= d.
```

The offline optimum is `OPT(T, B) = min(T, B)`. A prediction `p` estimates `T`. We assume `lambda` is in `(0, 1]` and confidence `c` is in `[0, 1]`.

The prediction-guided buying threshold is

```text
d_pred = ceil(lambda * B),  if p >= B
         B,                 if p < B.
```

The trust-aware threshold is

```text
d_trust = ceil(c * d_pred + (1 - c) * B).
```

Write `C_pred = ALG(T, B, d_pred)` and `C_trust = ALG(T, B, d_trust)`. Both thresholds are integers in `[1, B]`, with `d_pred <= d_trust <= B`.

## Proposition: exact cost difference with a perfect prediction

**Statement.** Suppose `p = T`. Then

```text
C_trust - C_pred = ceil((1 - c) * (B - d_pred)) >= 0.
```

In particular, at `c = 1` the two policies have identical costs. For `d_pred < B`, however, their costs need not converge as `c` approaches `1` from below: the gap remains one for every `c < 1` sufficiently close to `1`.

**Proof.** Since `d_pred` is an integer,

```text
d_trust
  = ceil(d_pred + (1 - c) * (B - d_pred))
  = d_pred + ceil((1 - c) * (B - d_pred)).
```

There are two cases.

If `T < B`, the perfect prediction gives `p < B`, so `d_pred = B` and `d_trust = B`. Neither policy buys, and both pay `T`. The stated difference is zero.

If `T >= B`, then `p >= B`. Both thresholds are at most `B`, so both policies buy during the season. Their costs are `B + d_pred - 1` and `B + d_trust - 1`. Subtracting gives

```text
C_trust - C_pred
  = d_trust - d_pred
  = ceil((1 - c) * (B - d_pred)).
```

This proves the identity in both cases.

At `c = 1`, the ceiling term vanishes. If `d_pred < B` and `c < 1`, the quantity `(1 - c) * (B - d_pred)` is positive. Whenever it is less than one, its ceiling equals one. Thus, as `c` approaches one from below, the cost gap remains one and drops to zero only at `c = 1`. This is a consequence of integer rounding, not an approximation error. `QED`.

## Why the scope matters

The proposition compares the two threshold policies **only when `p = T`**. It does not show that either policy is optimal under a perfect prediction. In particular, for `T >= B`, even a perfect prediction can lead the prediction-guided policy to rent for several days before buying.

Nor can a small difference in buying days be used to bound the cost difference for arbitrary seasons. For example, take `B = 10`, `T = 8`, `p = 10`, and `lambda = 0.8`. Then `d_pred = 8`. With `c = 0.5`, the trust-aware threshold is `d_trust = 9`. The prediction-guided policy buys on day 8 and costs 17, while the trust-aware policy never buys and costs 8. A one-day threshold change produces a cost difference of nine.

Consequently, the inequality

```text
|C_trust - C_pred| <= |d_trust - d_pred|
```

is false in general. This note also does not establish a bound such as `C_trust <= C_pred + O((1-c)B + |p-T|)` for unrestricted predictions and seasons.

## Interpretation

The confidence parameter moves the proposed buying day between `d_pred` and the deterministic threshold `B`. At full confidence the rules coincide exactly. Under a perfect prediction, the extra cost of the trust-aware rule can be calculated precisely, including the rounding effect.

A stronger claim about consistency relative to the offline optimum, or about how performance depends quantitatively on prediction error, would require a separate theorem with its own assumptions and proof. The worst-case guarantees for the bounded thresholds are treated in `notes/theorem_2_robustness.md` and in the technical report.
