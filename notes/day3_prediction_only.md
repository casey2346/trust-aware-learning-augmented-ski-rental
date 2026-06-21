# Day 3 Prediction-Only Ski Rental Algorithm

## Objective

Day 3 implements a prediction-only ski rental algorithm.

The goal is to show that fully trusting predictions can work very well when predictions are accurate, but can fail badly when predictions are unreliable.

## Prediction

The algorithm receives:

```text
p = predicted number of skiing days

The true number of skiing days is:

T = true number of skiing days

The buying cost is:

B = buying cost
Prediction Error

The absolute prediction error is:

η = |p - T|

The relative prediction error is:

η_rel = |p - T| / max(T, 1)
Prediction-Only Algorithm

The prediction-only algorithm fully trusts the prediction.

The rule is:

if p >= B:
    buy immediately
else:
    rent forever

Therefore, the cost is:

ALG_pred(T, B, p) =
    B,    if p >= B and T > 0
    T,    if p < B
Offline Optimum

The offline optimum is:

OPT(T, B) = min(T, B)
Cost Ratio

The cost ratio is:

CR_pred(T, B, p) = ALG_pred(T, B, p) / OPT(T, B)
Scenario 1: Exact Prediction

If:

p = T

then the prediction-only algorithm chooses the same high-level action as the offline optimum:

if T < B, it rents;
if T >= B, it buys.

Therefore, the cost ratio is:

CR_pred = 1

This shows strong consistency under accurate predictions.

Scenario 2: Overestimation Failure

If:

T is small
p >= B

then the prediction-only algorithm buys immediately.

Cost:

ALG_pred = B

Offline optimum:

OPT = T

Cost ratio:

CR_pred = B / T

When T is very small, this ratio can be large.

Example:

T = 1
B = 10
p = 50

ALG_pred = 10
OPT = 1
CR_pred = 10

This shows that overestimating the number of skiing days can cause severe degradation.

Scenario 3: Underestimation Failure

If:

T is large
p < B

then the prediction-only algorithm rents forever.

Cost:

ALG_pred = T

Offline optimum:

OPT = B

Cost ratio:

CR_pred = T / B

As T grows, this ratio can become large.

Example:

T = 50
B = 10
p = 1

ALG_pred = 50
OPT = 10
CR_pred = 5

This shows that underestimating the number of skiing days can also cause severe degradation.

Day 3 Outputs

Implemented:

src/ski_rental/prediction_only.py

Generated:

experiments/day3_prediction_only_curve.py
experiments/results/day3_prediction_only.csv
figures/day3_prediction_only_cost_ratio.png
Interpretation

The prediction-only algorithm has strong consistency when predictions are accurate.

However, it has poor robustness under unreliable predictions.

This motivates the next algorithmic step:

trust-aware learning-augmented ski rental

The trust-aware algorithm should use predictions when they are reliable, but fall back to the deterministic baseline when prediction reliability is low.