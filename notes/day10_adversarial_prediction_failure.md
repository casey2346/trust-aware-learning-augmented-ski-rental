# Day 10 Adversarial Prediction Failure Experiment

## Objective

Day 10 evaluates adversarial prediction failures.

The goal is to show that prediction-only algorithms can fail badly when predictions are wrong, while trust-aware fallback avoids collapse.

## Main Claim

Prediction-only algorithms are fragile because they fully trust the prediction.

Trust-aware algorithms reduce this fragility by falling back toward the deterministic baseline when confidence is low.

## Algorithms Compared

The experiment compares:

offline optimum
deterministic baseline
prediction-only
learning-augmented
trust-aware
Shared Parameters

The experiment uses:

B = 10
λ = 0.5
trust-aware confidence c = 0.0

The cost ratio is:

cost ratio = ALG / OPT
Case 1: Small T, Prediction Says Very Large

In this case:

T < B
p = 5B

The true season is short, so the offline optimum rents.

However, the prediction says the season will be very long.

Prediction-only therefore buys too early.

This causes unnecessary buying cost.

Example:

T = 1
B = 10
p = 50

prediction-only cost = 10
offline optimum = 1
cost ratio = 10
Case 2: Large T, Prediction Says Very Small

In this case:

T >= B
p = 1

The true season is long, so the offline optimum buys.

However, the prediction says the season will be very short.

Prediction-only therefore keeps renting.

As T grows, the prediction-only cost ratio grows.

Example:

T = 50
B = 10
p = 1

prediction-only cost = 50
offline optimum = 10
cost ratio = 5
Case 3: Systematically Biased Prediction

The experiment also tests systematic bias.

Biased Overestimate
p = T + B

This models a predictor that consistently overestimates the season length.

Biased Underestimate
p = max(0, T - B)

This models a predictor that consistently underestimates the season length.

Why Trust-Aware Does Not Collapse

The trust-aware algorithm uses confidence:

c ∈ [0, 1]

When confidence is low:

c = 0

the algorithm falls back to the deterministic baseline:

d_trust = B

Therefore, it avoids blindly following adversarial predictions.

Output

Day 10 generates:

experiments/day10_adversarial_prediction_failure.py
experiments/results/day10_adversarial_prediction_failure.csv
figures/adversarial_prediction_failure.png
notes/day10_adversarial_prediction_failure.md