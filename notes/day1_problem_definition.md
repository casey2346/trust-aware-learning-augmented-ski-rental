# Day 1 Problem Definition Notes

## Objective

To define the classical ski rental problem precisely and establish the mathematical foundation for a learning-augmented online algorithm under unreliable predictions.

Focuses on definitions only:

- ski rental problem;
- buy cost;
- rent cost;
- unknown time horizon;
- offline optimum;
- online algorithm cost;
- competitive ratio.

## 1. Problem Setup

The ski rental problem is a classical online decision-making problem.

A skier will ski for an unknown number of days. On each day, the skier must decide whether to rent skis or buy skis.

Definitions:

T = true number of skiing days
B = cost of buying skis
rent cost = 1 per day

The online algorithm does not know T.

The offline optimum knows T.

2. Offline Optimum

The offline optimum knows the true number of skiing days.

It compares two possible strategies:

rent every day: cost = T
buy immediately: cost = B

Therefore:

OPT(T, B) = min(T, B)

This is the benchmark for all online algorithms.

3. Online Algorithm Cost

Assume an online algorithm buys on day d.

There are two cases.

Case 1

If:

T < d

then the season ends before the algorithm buys.

The algorithm only rents.

ALG(T, B, d) = T

Case 2

If:

T >= d

then the algorithm rents for d - 1 days and buys on day d.

ALG(T, B, d) = (d - 1) + B

Therefore:

ALG(T, B, d) =
    T,             if T < d
    (d - 1) + B,   if T >= d
    
4. Competitive Ratio

The competitive ratio is:

CR(T, B, d) = ALG(T, B, d) / OPT(T, B)

An algorithm is c-competitive if:

ALG(T, B, d) <= c · OPT(T, B)

for all possible values of T.

5. Classical Deterministic Baseline

The classical deterministic algorithm buys on day B.

d = B

The cost is:

ALG_det(T, B) =
    T,             if T < B
    (B - 1) + B,   if T >= B

When T >= B:

OPT(T, B) = B
ALG_det(T, B) = 2B - 1

So:

CR = (2B - 1) / B = 2 - 1/B

Therefore, the deterministic baseline is at most 2-competitive.

6. Learning-Augmented Extension

In the learning-augmented setting, the algorithm receives a prediction:

p = predicted number of skiing days

Prediction error:

η = |p - T|

Relative prediction error:

η_rel = |p - T| / max(T, 1)

The research goal is to use this prediction when it is useful, while avoiding bad decisions when the prediction is unreliable.

7. Trust-Aware Motivation

A prediction-only algorithm can fail if it trusts an incorrect prediction.

If the prediction overestimates the number of skiing days, the algorithm may buy too early.

If the prediction underestimates the number of skiing days, the algorithm may rent too long.

A trust-aware algorithm should therefore combine:

prediction-based decision-making
+
confidence or reliability estimation
+
fallback to a robust deterministic baseline