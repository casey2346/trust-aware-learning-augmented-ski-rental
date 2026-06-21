# Day 5 Learning-Augmented Ski Rental Algorithm

## Objective

Day 5 implements a standard learning-augmented ski rental algorithm.

The goal is to allow the online algorithm to use a prediction about the unknown number of skiing days.

## Prediction

The algorithm receives:

p = predicted number of skiing days

The true number of skiing days is:

T = true number of skiing days

The buying cost is:

B = buying cost
Learning-Augmented Rule

The learning-augmented algorithm uses a parameter:

λ ∈ (0, 1]

The rule is:

if p >= B:
    buy at day ceil(λB)
else:
    buy at day B

Interpretation:

If the prediction suggests a long skiing season, the algorithm buys earlier.
If the prediction suggests a short skiing season, the algorithm behaves like the deterministic baseline.
Buying Day

The buying day is:

d(p, B, λ) =
    ceil(λB),   if p >= B
    B,          if p < B
Algorithm Cost

Using the project convention:

ALG(T, B, d) =
    T,             if T < d
    (d - 1) + B,   if T >= d

The learning-augmented algorithm has cost:

ALG_LA(T, B, p, λ) = ALG(T, B, d(p, B, λ))
Offline Optimum

The offline optimum remains:

OPT(T, B) = min(T, B)
Cost Ratio

The cost ratio is:

CR_LA(T, B, p, λ) = ALG_LA(T, B, p, λ) / OPT(T, B)
Lambda Interpretation

Different λ values control how aggressively the algorithm buys early.

λ = 0.5

The algorithm buys very early when p >= B.

For B = 10:

buy_day = ceil(0.5B) = 5

This may help when the prediction is correct and the season is long.

However, it can be risky if the prediction overestimates the season length.

λ = 0.75

The algorithm buys moderately early.

For B = 10:

buy_day = ceil(0.75B) = 8

This is a middle ground between aggressive prediction use and baseline robustness.

λ = 1.0

The algorithm buys on day B.

For B = 10:

buy_day = 10

This matches the classical deterministic baseline.

Day 5 Outputs

Implemented:

src/ski_rental/learning_augmented.py

Generated:

experiments/day5_learning_augmented_curve.py
experiments/results/day5_learning_augmented.csv
figures/day5_learning_augmented_lambdas.png
Interpretation

The learning-augmented algorithm introduces a trade-off:

smaller λ = more aggressive prediction use
larger λ  = more conservative prediction use

When predictions are accurate and indicate a long season, smaller λ can reduce unnecessary renting.

However, if predictions are wrong, aggressive early buying can hurt performance.