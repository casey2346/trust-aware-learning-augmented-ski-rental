# Signed Error Sweep and Bias Improvement

## Objective

This update improves the experimental completeness of the project.

The original error sweep mainly used overestimated predictions:

p = T · (1 + error_fraction)

This is useful, but it does not fully show how algorithms behave under underestimated predictions.

To make the experiments stronger, this update adds a signed error sweep and expands the adversarial failure figure.

Signed Error Sweep

The signed error sweep tests both directions of prediction error.

Overestimate
p = T · (1 + error_fraction)
Underestimate
p = T · (1 - error_fraction)

This allows the project to compare how algorithms behave when predictions are too high versus too low.

Why This Matters

Prediction-only algorithms can look strong under some overestimate settings.

However, they can fail badly when predictions underestimate a long season.

Therefore, signed error testing gives a more complete picture of robustness.

Updated Day 10 Figure

The adversarial prediction failure figure is expanded from three panels to four panels:

Case 1: Small T, Very Large Prediction
Case 2: Large T, Very Small Prediction
Case 3: Systematic Overestimate
Case 4: Systematic Underestimate

This makes the systematic bias analysis more complete.

Outputs
experiments/signed_error_sweep.py
experiments/results/signed_error_sweep.csv
figures/signed_error_sweep_cost_ratio.png
figures/adversarial_prediction_failure.png
notes/signed_error_and_bias_improvement.md