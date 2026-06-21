# Day 2 Classical Deterministic Baseline

## Objective

Day 2 implements and evaluates the classical deterministic ski rental algorithm.

The goal is to establish a clean baseline before introducing prediction-only, learning-augmented, and trust-aware algorithms.

## Convention

This project uses the following convention:

- Renting costs 1 per day.
- Buying costs B.
- If an algorithm buys on day d, it rents for d - 1 days and buys on day d.
- If the season ends before day d, the algorithm never buys.

Therefore:

ALG(T, B, d) =
    T,             if T < d
    (d - 1) + B,   if T >= d

Classical Deterministic Algorithm

The classical deterministic ski rental baseline buys on day B.

d = B

Therefore:

ALG_det(T, B) =
    T,             if T < B
    (B - 1) + B,   if T >= B
Offline Optimum

The offline optimum knows T in advance:

OPT(T, B) = min(T, B)
Competitive Ratio

For each instance:

CR(T, B) = ALG_det(T, B) / OPT(T, B)

When T < B:

ALG_det(T, B) = T
OPT(T, B) = T
CR(T, B) = 1

When T >= B:

ALG_det(T, B) = 2B - 1
OPT(T, B) = B
CR(T, B) = (2B - 1) / B = 2 - 1/B

Thus, the deterministic baseline is at most 2-competitive.

Day 2 Output

Implemented:

src/ski_rental/baselines.py

Generated:

experiments/results/day2_deterministic_baseline.csv
figures/day2_deterministic_competitive_ratio.png
Interpretation

The deterministic baseline is robust because its worst-case competitive ratio is bounded by 2.

However, it does not use any prediction. Therefore, it cannot improve when accurate predictions are available.

This motivates the next stage of the project: prediction-only and learning-augmented ski rental algorithms.