# Algorithm Blocks

This note specifies the four ski-rental policies used in the project. Each policy chooses a buying deadline before the season length is known. Predictions and confidence values, where applicable, are assumed to be available before day 1.

## Model and notation

Let `B >= 1` be an integer purchase cost, `T >= 1` the unknown integer season length, and `p` a prediction of `T`. Renting costs one unit per day. Buying at the beginning of day `d` incurs the purchase cost after `d - 1` rental days. If the season ends before day `d`, no purchase is made.

```text
ALG(T, B, d) = T,           if T < d
               B + d - 1,   if T >= d
OPT(T, B)    = min(T, B)
CR           = ALG / OPT
```

For the policies below, `lambda` belongs to `(0, 1]` and confidence `c` belongs to `[0, 1]`. A buying day is a planned threshold, not a claim that a purchase occurs after the season has ended.

## Algorithm 1 — Deterministic baseline

The classical deterministic rule ignores the prediction and buys on day `B` if the season lasts that long.

```text
Input: integer purchase cost B >= 1
Set d_base = B.
Rent on days 1 through d_base - 1, while the season continues.
If day d_base occurs, buy at its beginning.
```

Its cost is

```text
C_base(T, B) = ALG(T, B, B)
             = T,        if T < B
               2B - 1,   if T >= B.
```

Its exact worst-case competitive ratio is `2 - 1/B`, attained at `T = B`. The rule has a bounded guarantee but does not use a prediction.

## Algorithm 2 — Prediction-only baseline

This deliberately simple baseline treats the forecast as decisive: it buys immediately when the predicted season is at least as long as the purchase cost, and otherwise rents throughout the actual season.

```text
Input: B, prediction p
If p >= B:
    Buy at the beginning of day 1.
Else:
    Rent on every day of the season; never buy.
```

For `T >= 1`, its cost is

```text
C_only(T, B, p) = B,   if p >= B
                  T,   if p < B.
```

When `p = T`, this cost equals `OPT(T, B)` exactly. Under arbitrary predictions, however, the rule has no uniform competitive-ratio bound: for fixed `B > 1`, choosing `p = 1 < B` and letting `T` increase gives `CR = T/B`, which grows without bound. For an overestimated short season (`p >= B` but `T < B`), it instead pays `B/T` times the optimum; for a fixed integer `B`, this ratio is at most `B`.

These statements refer to this particular prediction-only baseline, not to every algorithm that uses predictions.

## Algorithm 3 — Prediction-guided bounded threshold

This policy uses an earlier buying deadline when the prediction indicates a long season. Otherwise, it uses the deterministic deadline.

```text
Input: B, prediction p, lambda in (0, 1]
If p >= B:
    Set d_pred = ceil(lambda * B).
Else:
    Set d_pred = B.
Rent on days 1 through d_pred - 1, while the season continues.
If day d_pred occurs, buy at its beginning.
```

Thus

```text
d_pred(p, B, lambda) = ceil(lambda * B),   if p >= B
                       B,                  if p < B
C_guided(T, B, p, lambda) = ALG(T, B, d_pred).
```

For instance, when `B = 10` and `p >= B`, the deadlines for `lambda = 0.5`, `0.75`, and `1` are days 5, 8, and 10, respectively. A smaller `lambda` makes the buying deadline earlier in the long-season-prediction branch. Earlier buying may reduce the cost of a long season, but it may also lead to an unnecessary purchase if the season is short.

Because `ceil(lambda * B) <= d_pred <= B`, this policy has a finite worst-case competitive-ratio bound for every fixed `lambda > 0`, regardless of prediction accuracy.

## Algorithm 4 — Confidence-weighted bounded threshold

This policy interpolates between the prediction-guided deadline and the deterministic deadline. Here `c` is an externally supplied parameter; this project does not estimate or calibrate it from prediction data.

```text
Input: B, prediction p, lambda in (0, 1], c in [0, 1]
If p >= B:
    Set d_pred = ceil(lambda * B).
Else:
    Set d_pred = B.
Set d_trust = ceil(c * d_pred + (1 - c) * B).
Rent on days 1 through d_trust - 1, while the season continues.
If day d_trust occurs, buy at its beginning.
```

The resulting cost is

```text
C_trust(T, B, p, lambda, c) = ALG(T, B, d_trust).
```

Since `d_pred` and `B` are integers,

```text
d_trust = d_pred + ceil((1 - c) * (B - d_pred)).
```

In particular:

- At `c = 0`, `d_trust = B`, so the rule is the deterministic baseline.
- At `c = 1`, `d_trust = d_pred`, so the rule is the prediction-guided policy.
- When `p < B`, `d_pred = d_trust = B` at **every** confidence value.
- Between the endpoints, the buying day moves in integer steps rather than changing continuously with `c`.

Confidence controls the selected buying threshold, but a lower confidence does not necessarily mean a lower realised cost. The policy also does not obtain a stronger *uniform worst-case guarantee* merely by introducing `c`: the prediction-guided threshold already has the same bound.

## Comparison and guarantees

| Policy | Buying rule | What is established |
| --- | --- | --- |
| Deterministic | `d = B` | Exact worst-case ratio `2 - 1/B` |
| Prediction-only | Buy on day 1 if `p >= B`; otherwise never buy | Optimal cost for `p = T`; unbounded ratio is possible for arbitrary predictions |
| Prediction-guided | `d_pred = ceil(lambda * B)` if `p >= B`, otherwise `B` | Uniform bound `1 + (B - 1)/ceil(lambda * B)` |
| Trust-aware | `d_trust = ceil(c * d_pred + (1 - c) * B)` | The same uniform bound; recovers the deterministic and prediction-guided rules at `c = 0` and `c = 1` |

The common bound follows because both bounded-threshold policies satisfy

```text
ceil(lambda * B) <= d <= B,
ALG(T, B, d) / OPT(T, B)
    <= 1 + (B - 1)/d
    <= 1 + (B - 1)/ceil(lambda * B)
    <= 1 + 1/lambda.
```

For any **fixed** integer threshold `1 <= d <= B`, the first bound is exact in the worst case, at `T = d`. The bound uniform over predictions and confidence values need not be attained for every fixed confidence setting.

These four definitions support a controlled comparison of how buying deadlines respond to predictions and confidence. They do **not** establish an optimal consistency–robustness trade-off, show that confidence weighting outperforms the prediction-guided policy, or provide an error-sensitive guarantee. The proofs and their precise scope are in [`paper/technical_report.md`](paper/technical_report.md) and the three supporting notes under [`notes/`](notes/).
