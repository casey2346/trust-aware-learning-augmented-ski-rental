# Day 8 Complete Experiment Framework

## Objective

Day 8 builds the complete experiment framework for the trust-aware learning-augmented ski rental project.

The goal is to evaluate all implemented algorithms under controlled prediction-error regimes and adversarial prediction regimes.

## Scripts

Day 8 adds three experiment scripts:

experiments/error_sweep.py
experiments/adversarial_test.py
experiments/run_all.py
Algorithms Compared

The experiments compare:

offline optimum
deterministic baseline
prediction-only
learning-augmented
trust-aware
Experimental Variables

The experiments use:

B ∈ {10, 20, 50}
T ∈ {1, 2, ..., 5B}
prediction error from 0% to 100%
confidence c ∈ {0.0, 0.25, 0.5, 0.75, 1.0}
λ = 0.5
Experiment 1: Error Sweep

The error sweep evaluates algorithm performance as prediction error increases.

The generated prediction is:

p = T · (1 + error_fraction)

where:

error_fraction ∈ {0.0, 0.1, 0.2, ..., 1.0}

This creates controlled overestimation errors from 0% to 100%.

The main metric is:

cost ratio = ALG / OPT

Output:

experiments/results/day8_error_sweep.csv
figures/day8_error_sweep.png
Experiment 2: Adversarial Prediction Test

The adversarial test evaluates robustness when predictions intentionally push algorithms toward the wrong action.

The adversarial prediction rule is:

if T < B:
    p = 5B
else:
    p = 1

This causes:

short season -> predictor wrongly suggests buying
long season  -> predictor wrongly suggests renting

Output:

experiments/results/day8_adversarial_test.csv
figures/day8_adversarial_test.png
Master Runner

The script:

experiments/run_all.py

runs both experiments automatically.

Command:

PYTHONPATH=. python3 experiments/run_all.py
Interpretation

The full experiment framework allows the project to test the key claim:

Trust-aware algorithms can reduce blind prediction use and preserve robustness when predictions become unreliable.

The deterministic baseline is robust but cannot exploit predictions.

Prediction-only can perform well when predictions are accurate, but can fail badly under adversarial prediction errors.

Learning-augmented algorithms use predictions, but still need a trust mechanism.

Trust-aware algorithms interpolate between prediction use and deterministic fallback.