# Day 9 First Set of Figures

## Objective

Day 9 generates the first set of report-ready figures for the ski rental project.

The required figures are:

figures/error_sweep_cost_ratio.png
figures/duration_sweep.png
figures/confidence_ablation.png
Figure 1: Prediction Error vs Cost Ratio

File:

figures/error_sweep_cost_ratio.png

This figure uses the Day 8 error-sweep experiment results.

It plots:

x-axis: prediction error fraction
y-axis: average cost ratio ALG / OPT

The figure compares:

deterministic
prediction-only
learning-augmented
trust-aware_c=0.0
trust-aware_c=0.5
trust-aware_c=1.0

for:

B = 10

averaged over all:

T = 1 to 5B
Figure 2: True Duration T vs Cost Ratio

File:

figures/duration_sweep.png

This figure uses the Day 8 adversarial-test results.

It plots:

x-axis: true number of skiing days T
y-axis: cost ratio ALG / OPT

The figure compares all major algorithms under adversarial predictions for:

B = 10
Figure 3: Confidence Level vs Cost Ratio

File:

figures/confidence_ablation.png

This figure uses the Day 8 adversarial-test results.

It plots:

x-axis: confidence level c
y-axis: average cost ratio ALG / OPT

The figure focuses on the trust-aware algorithm and shows how performance changes as confidence increases from:

0.0 to 1.0

The figure is averaged over all:

T = 1 to 5B

for:

B = 10