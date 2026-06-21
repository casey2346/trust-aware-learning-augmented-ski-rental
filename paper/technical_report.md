# Trust-Aware Learning-Augmented Ski Rental under Unreliable Predictions

## Abstract

Learning-augmented algorithms use machine-learned predictions to improve online decision-making, but their performance can degrade severely when predictions are inaccurate or adversarial. This project studies this trade-off through the classical ski rental problem. We implement and compare four policies: the deterministic baseline, a prediction-only policy, a learning-augmented policy, and a trust-aware learning-augmented policy. The trust-aware policy interpolates between a prediction-based buying threshold and the deterministic ski-rental threshold using a confidence parameter.

The main finding is that prediction-only policies can achieve strong performance when predictions are accurate, but can suffer unbounded degradation under adversarial predictions. In contrast, the trust-aware fallback mechanism preserves robustness by preventing the algorithm from following unreliable predictions too aggressively. We provide proof sketches for consistency, robustness, and adversarial separation, and we support the theoretical claims with experiments over prediction error sweeps, confidence ablations, and adversarial prediction cases. The results show that trust-aware fallback provides a practical mechanism for balancing prediction usefulness and worst-case reliability.

## 1. Introduction

Online algorithms make decisions without knowing the future. In many modern settings, however, algorithms are no longer completely prediction-free. Machine-learning models, historical data, or domain-specific forecasting systems can provide predictions about future demand, duration, cost, or user behavior. These predictions can improve performance when accurate, but they can also mislead the algorithm when inaccurate.

This creates a central question in learning-augmented algorithms:

> How can an online algorithm use predictions when they are useful, without suffering catastrophic loss when they are wrong?

This project targets an active but still underdeveloped problem: robust online decision-making with unreliable learned predictions. Prior work on learning-augmented online algorithms shows that predictions can improve performance when accurate, but the central challenge is to preserve worst-case reliability when predictions are inaccurate, biased, or adversarial.

The ski rental problem is a classical model for studying online decision-making under uncertainty. A skier can either rent skis for one unit of cost per day or buy skis once for cost `B`. The number of skiing days `T` is unknown in advance. The offline optimum knows `T` and pays `min(T, B)`. The online algorithm must decide when to buy without knowing `T`.

The classical deterministic strategy buys on day `B`, achieving a competitive ratio below `2`. A prediction-only strategy may use a predicted duration `p` to decide whether to buy or rent. If `p` is accurate, this can be excellent. However, if `p` is adversarial, the prediction-only policy may make very poor decisions. For example, if the true season is long but the prediction is very small, the policy may keep renting forever, causing cost ratio `T / B`, which becomes unbounded as `T` grows.

This report proposes and studies a trust-aware learning-augmented ski rental algorithm. The algorithm uses a confidence parameter `c ∈ [0, 1]` to interpolate between a prediction-augmented buying threshold and the deterministic baseline threshold. When confidence is high, the algorithm behaves more like the prediction-based policy. When confidence is low, it falls back toward the deterministic baseline.

The project makes three main contributions:

1. It implements a reproducible experimental framework for comparing deterministic, prediction-only, learning-augmented, and trust-aware ski rental policies.
2. It provides proof sketches showing consistency, robustness, and adversarial separation.
3. It empirically demonstrates that prediction-only policies can fail under adversarial predictions, while trust-aware fallback prevents unbounded degradation.

## 2. Problem Definition

The ski rental problem is defined as follows.

Let:

T = true number of skiing days
B = buying cost
p = predicted number of skiing days

Renting costs `1` per day. Buying costs `B` once.

The offline optimum knows `T` in advance and pays:

OPT(T, B) = min(T, B)

An online algorithm that buys on day `d` has cost:

ALG(T, B, d) =
    T,             if T < d
    (d - 1) + B,   if T ≥ d

The competitive ratio is:

CR(T, B) = ALG(T, B, d) / OPT(T, B)

The goal is to design an online policy with good cost ratio. In the learning-augmented setting, the algorithm also receives a prediction `p`. The prediction error is:

η = |p - T|

A good learning-augmented algorithm should satisfy two desirable properties:

Consistency:
    If the prediction is accurate, the algorithm should approach the performance
    of the prediction-augmented policy.

Robustness:
    If the prediction is inaccurate or adversarial, the algorithm should avoid
    unbounded degradation and remain competitive.

The project studies how the confidence parameter `c` controls this trade-off.

## 3. Algorithms

This project compares four main algorithms.

### 3.1 Deterministic Baseline

The classical deterministic ski-rental strategy buys on day:

d_base = B

If the season is short, the algorithm rents and pays `T`. If the season is long, it rents for `B - 1` days and then buys, paying:

2B - 1

For `T ≥ B`, the competitive ratio is:

(2B - 1) / B = 2 - 1/B < 2

Thus, the deterministic baseline is robust but does not use predictions.

### 3.2 Prediction-Only Policy

The prediction-only policy fully trusts the prediction.

A simple prediction-only rule is:

if p ≥ B:
    buy immediately
else:
    rent forever

This policy can be very good when predictions are accurate. For example, if `p = T` and the prediction correctly indicates whether the season is short or long, the policy can match the offline optimum.

However, the policy is fragile. If `T` is large but `p` is very small, it may rent forever. Then:

C_prediction_only = T
OPT(T, B) = B
CR_prediction_only = T / B

As `T / B` grows, the ratio becomes unbounded.

### 3.3 Learning-Augmented Policy

The learning-augmented policy uses a more cautious prediction-based threshold. Let:

λ ∈ (0, 1]

where smaller `λ` means more aggressive early buying.

The prediction-augmented buying day is:

d_pred =
    ceil(λB), if p ≥ B
    B,        if p < B

This policy uses predictions but still retains a threshold-based structure. If the prediction suggests a long season, it buys earlier than the deterministic baseline. If the prediction suggests a short season, it uses the deterministic buying day.

### 3.4 Trust-Aware Learning-Augmented Policy

The trust-aware algorithm interpolates between the prediction-augmented threshold and the deterministic threshold.

Let:

c ∈ [0, 1]

be the confidence level.

The trust-aware buying day is:

d_trust = ceil(c · d_pred + (1 - c) · B)

When `c = 1`, the algorithm fully trusts the prediction-augmented threshold:

d_trust = d_pred

When `c = 0`, the algorithm falls back to the deterministic baseline:

d_trust = B

Intermediate values of `c` produce a smooth interpolation between these two policies.

This structure is the core of the project. It allows the algorithm to benefit from predictions when confidence is high, while preserving robustness when confidence is low.

## 4. Theoretical Analysis

This section summarizes three proof sketches developed in the project.

### 4.1 Theorem 1: Consistency

**Statement.** When the prediction is accurate and confidence is high, the trust-aware algorithm approaches the prediction-augmented cost.

Let:

C_pred(T, B, p) = ALG(T, B, d_pred)
C_trust(T, B, p, c) = ALG(T, B, d_trust)
η = |p - T|

The trust-aware buying day is:

d_trust = ceil(c · d_pred + (1 - c) · B)

When `c = 1`:

d_trust = d_pred

so:

C_trust(T, B, p, 1) = C_pred(T, B, p)
When `c` is close to one, the buying-day difference is small. Ignoring the ceiling term:

d_trust - d_pred
≈ (1 - c)(B - d_pred)

Since `d_pred ∈ [ceil(λB), B]`, we have:

|d_trust - d_pred| ≤ (1 - c)B + 1

Changing the buying day by `k` days changes the rental component by at most `k`, so:

|C_trust - C_pred| ≤ (1 - c)B + 1
Including prediction error gives the proof-sketch bound:

C_trust(T, B, p, c)
≤ C_pred(T, B, p) + O((1 - c)B + η)

Therefore, when:

c → 1
η → 0

the trust-aware cost approaches the prediction-augmented cost.

### 4.2 Theorem 2: Robustness

**Statement.** Under arbitrary prediction error, if the buying threshold is controlled by the deterministic ski-rental threshold, the trust-aware algorithm remains `O(1)`-competitive.

Assume:

λB ≤ d_trust ≤ B

for fixed `λ ∈ (0, 1]`.

Let `d = d_trust`.

There are two cases.

**Case 1: `T < d`.**

The algorithm only rents, so:

C_trust = T

Since `T < d ≤ B`, the offline optimum is:

OPT(T, B) = T

Thus:

C_trust / OPT = 1

**Case 2: `T ≥ d`.**

The algorithm rents for `d - 1` days and then buys:

C_trust = (d - 1) + B

Since `d ≤ B`:

C_trust ≤ 2B - 1
Since `T ≥ d ≥ λB`:

OPT(T, B) = min(T, B) ≥ λB

Therefore:

C_trust / OPT
≤ (2B - 1) / (λB)
≤ 2 / λ

For fixed `λ`, this is `O(1)`.

The important point is that this robustness statement does not require small prediction error. The prediction error:

η = |p - T|

may be arbitrary. Robustness comes from the fallback structure, not from prediction accuracy.

### 4.3 Theorem 3: Adversarial Counterexample

**Statement.** Trust-aware fallback prevents the unbounded degradation suffered by prediction-only policies under adversarial predictions.

Consider the adversarial case:

T >> B
p = 1

Since `p < B`, the prediction-only policy believes the season will be short and rents forever.

Thus:

C_prediction_only = T

But since `T >> B`, the offline optimum buys:

OPT(T, B) = B

So:

CR_prediction_only = T / B

As `T / B → ∞`, the competitive ratio becomes unbounded.

Now consider the trust-aware algorithm under low confidence. It falls back to the deterministic threshold:

d_trust = B

Since `T ≥ B`, it rents for `B - 1` days and then buys:

C_trust = (B - 1) + B = 2B - 1

Thus:

CR_trust = (2B - 1) / B = 2 - 1/B < 2

Therefore, prediction-only can suffer unbounded degradation, while trust-aware fallback remains bounded.

## 5. Experiments

The project implements a reproducible Python experimental framework. The experiments evaluate how each algorithm behaves under different prediction settings.

The implemented algorithms are:

deterministic baseline
prediction-only
learning-augmented
trust-aware
offline optimum

The experiments vary:

B ∈ {10, 20, 50}
T ∈ {1, ..., 5B}
prediction error from 0% to 100%
confidence c ∈ {0, 0.25, 0.5, 0.75, 1}
λ = 0.5

The main experiments are:

1. deterministic baseline curve;
2. prediction-only behavior;
3. prediction error models;
4. learning-augmented lambda comparison;
5. trust-aware fallback comparison;
6. signed prediction error sweep;
7. confidence ablation;
8. adversarial prediction failure experiment.

### 5.1 Signed Error Sweep

The signed error sweep tests both directions of prediction error.

For overestimation:

p = T · (1 + error_fraction)

For underestimation:

p = T · (1 - error_fraction)

This improves the original one-sided error sweep, where prediction-only appeared strong because predictions were mostly overestimated. The signed sweep shows that prediction-only can fail under underestimated long seasons.

Output figure:

figures/day8_error_sweep.png

### 5.2 First Report Figures

Day 9 generates the first report-ready figure set:

figures/error_sweep_cost_ratio.png
figures/duration_sweep.png
figures/confidence_ablation.png

These figures show how cost ratio changes with prediction error, true duration, and confidence level.

### 5.3 Adversarial Prediction Failure

The adversarial experiment tests four cases:

Case 1: small T, very large prediction
Case 2: large T, very small prediction
Case 3: systematic overestimate
Case 4: systematic underestimate

Output figure:

figures/adversarial_prediction_failure.png

The purpose is to demonstrate that prediction-only can fail badly, while trust-aware fallback remains controlled.

## 6. Results

The experimental results support the theoretical claims.

### 6.1 Deterministic Baseline

The deterministic baseline is stable and robust. It does not exploit predictions, but its competitive ratio stays below `2` in long-season cases.

This confirms the classical behavior:

CR = (2B - 1) / B < 2

### 6.2 Prediction-Only Policy

Prediction-only performs well when predictions are accurate or favorable. However, it is fragile.

In adversarial cases, prediction-only can either buy too early or rent for too long.

The most severe failure occurs when:

T is large
p is very small

Then prediction-only rents for the whole season and obtains:

CR = T / B

This grows without bound.

### 6.3 Learning-Augmented Policy

The learning-augmented policy improves over prediction-only by using a controlled buying threshold. However, it still depends strongly on prediction quality. When the prediction is misleading, the algorithm can still suffer because it does not explicitly model trust or confidence.

### 6.4 Trust-Aware Policy

The trust-aware algorithm provides the best trade-off.

When confidence is high, it approaches the prediction-augmented threshold and can benefit from accurate predictions.

When confidence is low, it falls back toward the deterministic threshold and avoids catastrophic prediction-only failures.

The confidence ablation shows that increasing confidence makes the algorithm more prediction-dependent. Under adversarial predictions, lower confidence produces more robust behavior.

### 6.5 Main Empirical Takeaway

The experiments support the central claim:

Prediction-only can be consistent but not robust.
Trust-aware fallback preserves robustness while still allowing prediction use.

The trust-aware algorithm does not always outperform every other policy in every case. Instead, its value is that it gives a controlled mechanism for trading off prediction use against worst-case reliability.

## 7. Limitations

This project is a first research-style exploration and has several limitations.

First, the confidence value `c` is manually specified rather than learned from data. In real systems, confidence would need to be estimated from model calibration, historical prediction accuracy, uncertainty quantification, or validation performance.

Second, the ski rental problem is intentionally simple. This makes the theory clean, but real online decision problems may involve multiple actions, stochastic costs, changing environments, or repeated decisions.

Third, the experiments use synthetic prediction errors. These are useful for controlled analysis, but real prediction systems may produce more complex error patterns, including distribution shift, correlated errors, or time-dependent bias.

Fourth, the theoretical analysis is currently written as proof sketches. The main mathematical ideas are present, but a final paper would need fully formal theorem statements and proofs.

Fifth, the current trust-aware rule uses a simple convex interpolation between `d_pred` and `B`. Other interpolation rules may produce better trade-offs.

## 8. Future Work

There are several directions for future work.

First, the confidence parameter could be learned automatically. For example, the algorithm could estimate confidence from recent prediction errors or from uncertainty estimates produced by a forecasting model.

Second, the theoretical bounds could be tightened. The current robustness proof gives an `O(1/λ)`-type bound, but sharper constants may be possible.

Third, the algorithm could be extended to randomized ski rental. Randomized policies may achieve better competitive ratios, and the interaction between randomization and prediction confidence is an interesting direction.

Fourth, the framework could be generalized beyond ski rental. Similar trust-aware fallback ideas may apply to caching, online scheduling, resource allocation, and rent-or-buy decisions.

Fifth, future experiments could test the algorithm on real or semi-real prediction traces rather than synthetic error models.

Finally, the proof sketches could be developed into a polished theoretical paper with formal lemmas, theorem statements, and connections to existing learning-augmented online algorithms.

## References

[1] A. R. Karlin, M. S. Manasse, L. Rudolph, and D. D. Sleator. Competitive snoopy caching. Algorithmica, 1988.

[2] A. Borodin and R. El-Yaniv. Online Computation and Competitive Analysis. Cambridge University Press, 1998.

[3] T. Lykouris and S. Vassilvitskii. Competitive caching with machine learned advice. International Conference on Machine Learning, 2018.

[4] M. Purohit, Z. Svitkina, and R. Kumar. Improving online algorithms via ML predictions. Advances in Neural Information Processing Systems, 2018.

[5] M. Mitzenmacher. Scheduling with predictions and the price of misprediction. ITCS, 2020.

[6] Project implementation files: `src/ski_rental/`, `src/predictors/`, `experiments/`, `figures/`, and `notes/`.

[7] S. Angelopoulos, C. Dürr, S. Jin, S. Kamali, and M. Renault. Online computation with untrusted advice. ITCS, 2020.

[8] Y. Shin, C. Lee, G. Lee, and H.-C. An. Improved learning-augmented algorithms for the multi-option ski rental problem via best-possible competitive analysis. ICML, 2023.