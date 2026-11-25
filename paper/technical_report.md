# Trust-Aware Learning-Augmented Ski Rental under Unreliable Predictions

## Abstract

Online algorithms can benefit from predictions, but misleading advice can turn a good decision into a costly one. I examine this tension in the ski-rental problem by comparing four policies: the deterministic baseline, a prediction-only policy, a prediction-guided threshold policy, and a confidence-weighted variant that interpolates between the latter and the deterministic buying day.

With exact duration advice, prediction-only matches the offline optimum; under adversarial advice, its competitive ratio can be unbounded. The threshold policies avoid this failure by buying no later than day `B`. I prove a cost comparison under perfect predictions, characterize the worst-case competitive ratio of a fixed threshold, and exhibit an adversarial separation from prediction-only. Synthetic error sweeps and confidence ablations illustrate how the buying rule behaves, without claiming an improved optimal consistency–robustness trade-off.

## 1. Introduction

Online algorithms make decisions without knowing the future. In many modern settings, however, algorithms are no longer completely prediction-free. Machine-learning models, historical data, or domain-specific forecasting systems can provide predictions about future demand, duration, cost, or user behavior. These predictions can improve performance when accurate, but they can also mislead the algorithm when inaccurate.

This creates a central question in learning-augmented algorithms:

> How can an online algorithm use predictions when they are useful, without suffering catastrophic loss when they are wrong?

The ski rental problem is a classical model for studying online decision-making under uncertainty. A skier can either rent skis for one unit of cost per day or buy skis once for cost `B`. The number of skiing days `T` is unknown in advance. The offline optimum knows `T` and pays `min(T, B)`. The online algorithm must decide when to buy without knowing `T`.

The classical deterministic strategy buys on day `B`, achieving a competitive ratio below `2`. A prediction-only strategy may use a predicted duration `p` to decide whether to buy or rent. If `p` is accurate, this can be excellent. However, if `p` is adversarial, the prediction-only policy may make very poor decisions. For example, if the true season is long but the prediction is very small, the policy may keep renting forever, causing cost ratio `T / B`, which becomes unbounded as `T` grows.

I study a confidence-based buying rule that moves between a prediction-guided threshold and the classical deterministic threshold. The question is what this rule guarantees, and how much the outcome changes when the prediction is wrong.

The work combines Python implementations, mathematical analysis, and controlled experiments. I compare four policies, prove bounds for the threshold rules, and use adversarial examples to examine the consequences of trusting a prediction completely.

## 2. Problem Definition

The model has discrete time, with integer buying cost `B ≥ 1`, integer season length `T ≥ 1`, and integer buying thresholds `d ≥ 1`. Renting costs one unit per day. Buying at the beginning of day `d` incurs `B` after `d - 1` rental days, if the season lasts that long.

Here `T` is the true number of skiing days, `B` is the cost of buying, and `p` is the predicted duration.

The offline optimum knows `T` in advance and pays `OPT(T, B) = min(T, B)`.

An online algorithm that buys on day `d` has cost:

```text
ALG(T, B, d) = T,           if T < d
               (d - 1) + B, if T ≥ d
```

The competitive ratio is `CR(T, B) = ALG(T, B, d) / OPT(T, B)`.

The learning-augmented policies additionally receive the prediction `p`, with absolute error `η = |p - T|`.

The usual goals are **consistency** (low cost relative to `OPT` with exact predictions) and **robustness** (a bounded worst-case competitive ratio even with incorrect predictions). The result in Section 4.1 is narrower than a consistency guarantee relative to `OPT`: it compares two threshold policies under a perfect prediction. The confidence parameter `c` lets us examine how the chosen buying day varies between them.

## 3. Algorithms

This project compares four main algorithms.

### 3.1 Deterministic Baseline

The classical deterministic ski-rental strategy buys on day `d_base = B`.

If the season is short, the algorithm rents and pays `T`. If the season is long, it rents for `B - 1` days and then buys, paying `2B - 1`.

For `T ≥ B`, the competitive ratio is `(2B - 1) / B = 2 - 1/B < 2`

Thus, the deterministic baseline is robust but does not use predictions.

### 3.2 Prediction-Only Policy

The prediction-only policy fully trusts the prediction.

A simple prediction-only rule is:

```text
if p ≥ B:
    buy immediately
else:
    rent forever
```

This policy can be very good when predictions are accurate. For example, if `p = T` and the prediction correctly indicates whether the season is short or long, the policy can match the offline optimum.

However, the policy is fragile. If `T` is large but `p` is very small, it may rent forever. Then:

```text
C_prediction_only = T
OPT(T, B) = B
CR_prediction_only = T / B
```

As `T / B` grows, the ratio becomes unbounded.

### 3.3 Learning-Augmented Policy

The learning-augmented policy uses a more cautious prediction-based threshold. Let `λ ∈ (0, 1]`, where smaller `λ` means more aggressive early buying.

The prediction-augmented buying day is:

```text
d_pred = ceil(λB), if p ≥ B
         B,        if p < B
```

This policy uses predictions but still retains a threshold-based structure. If the prediction suggests a long season, it buys earlier than the deterministic baseline. If the prediction suggests a short season, it uses the deterministic buying day.

### 3.4 Trust-Aware Learning-Augmented Policy

The trust-aware algorithm interpolates between the prediction-augmented threshold and the deterministic threshold.

Let `c ∈ [0, 1]` be the confidence level.

The trust-aware buying day is `d_trust = ceil(c · d_pred + (1 - c) · B)`.

When `c = 1`, the algorithm fully trusts the prediction-augmented threshold: `d_trust = d_pred`.

When `c = 0`, the algorithm falls back to the deterministic baseline: `d_trust = B`.

Intermediate values of `c` interpolate the unrounded thresholds; the final integer ceiling makes the realized buying day change in discrete steps.

This structure is the core of the project. When `p ≥ B`, confidence controls how early the purchase occurs, while the deadline `d_trust ≤ B` ensures a finite worst-case bound for every confidence level. When `p < B`, confidence has no effect because both thresholds are `B`.

## 4. Theoretical Analysis

This section gives self-contained statements and proofs for the mathematical properties of the policies as defined in Section 3. The claims concern this discrete threshold model; they are not statements of a novel optimal learning-augmented competitive ratio.

### 4.1 Proposition 1: Cost Comparison under Perfect Predictions

**Statement.** Let `B ≥ 1` be an integer, `λ ∈ (0,1]`, and `c ∈ [0,1]`. Define

```text
d_pred = ceil(λB),  if p ≥ B
         B,         if p < B

d_trust = ceil(c * d_pred + (1 - c) * B).
```

Under a perfect prediction `p = T`, the trust-aware and prediction-augmented policies have the same cost when `c = 1`. More generally, under perfect predictions, the trust-aware policy incurs an additional cost of exactly `ceil((1-c)(B-d_pred))` compared with the prediction-augmented policy.

**Proof.** Since `d_pred` and `B` are integers and `d_pred ≤ B`, write

```text
d_trust = d_pred + ceil((1-c)(B-d_pred)).
```

In particular, `d_trust ≥ d_pred`.

**Case 1: `T < B`.** Perfect prediction implies `p < B`, so `d_pred = d_trust = B`. Neither policy buys, and both cost `T`.

**Case 2: `T ≥ B`.** Perfect prediction implies `p ≥ B`, so `d_pred = ceil(λB)`. Both buying thresholds are at most `B ≤ T`; both policies therefore buy. Their costs are

```text
C_pred  = B + d_pred - 1,
C_trust = B + d_trust - 1.
```

It follows that

```text
0 ≤ C_trust - C_pred
  = d_trust - d_pred
  = ceil((1-c)(B-d_pred))
  ≤ (1-c)(B-d_pred) + 1.
```

When `c = 1`, this difference is exactly zero. Because the buying threshold uses an integer ceiling, however, if `B > d_pred`, then for `c < 1` sufficiently close to one the difference is **one**, not zero. Hence the cost is equal at full confidence, but it need not converge continuously to that value as `c` approaches one from below. This discrete rounding effect must not be hidden by a smooth approximation.

**Scope and limitation.** This proof is for **perfect predictions**. It does not imply

```text
|C_trust - C_pred| ≤ |d_trust - d_pred|
```

for arbitrary `T` and `p`: if the season ends between the thresholds, one policy buys and the other does not, so the cost difference may be much larger than their one-day threshold difference. No general additive error-sensitive bound of the form `O((1-c)B + |p-T|)` is proved here.

### 4.2 Proposition 2: Worst-Case Robustness of a Bounded Buying Threshold

**Statement.** Fix integer `B ≥ 1` and an integer threshold `d` with `1 ≤ d ≤ B`. For every season length `T ≥ 1`, the cost ratio satisfies

```text
ALG(T,B,d) / OPT(T,B) ≤ 1 + (B-1)/d.
```

For this fixed threshold, the bound is attained when `T = d` (including the degenerate case `B = d = 1`). Consequently, because the trust-aware threshold obeys `d_trust ≥ ceil(λB)`, it is worst-case competitive with ratio at most

```text
1 + (B-1)/ceil(λB) ≤ 1 + 1/λ,
```

uniformly over the prediction `p` and confidence `c` for fixed `λ > 0`.

**Proof.** If `T < d`, no purchase occurs and, because `T < d ≤ B`, both the online and offline costs equal `T`; the ratio is one.

If `T ≥ d`, the online cost is `B + d - 1`. The offline optimum is `min(T,B) ≥ d`, so

```text
ALG/OPT ≤ (B+d-1)/d = 1 + (B-1)/d.
```

Taking `T=d` gives `OPT=d` and equality. Finally, in Section 3.4 the trust-aware threshold lies between `d_pred` and `B`, and `d_pred ≥ ceil(λB)`, yielding the claimed uniform bound.

**Interpretation.** Bounded thresholds provide robustness independent of prediction accuracy. This is a worst-case guarantee, **not** a proof that confidence interpolation beats the ordinary learning-augmented threshold. Both already have finite worst-case ratios in this model. The classical baseline `d=B` achieves `2 - 1/B`.

### 4.3 Proposition 3: An Adversarial Separation from Prediction-Only

**Statement.** For each fixed integer `B > 1`, the prediction-only policy in Section 3.2 has no finite competitive ratio when predictions are unrestricted. By contrast, the threshold-bounded policies in Sections 3.3 and 3.4 are competitive for fixed `λ > 0`.

**Proof.** Fix `p=1 < B` and let `T` grow without bound. Prediction-only rents forever, giving

```text
C_prediction_only = T,
OPT(T,B) = B  (for T ≥ B),
C_prediction_only/OPT = T/B → ∞.
```

For the same prediction `p=1`, the prediction-augmented rule selects `d_pred=B`; hence the trust-aware rule also has `d_trust=B` **for every confidence `c`**, not just low confidence. Its cost for `T ≥ B` is `2B-1`, yielding ratio `2-1/B < 2`.

Proposition 2 establishes the general finite bound for arbitrary predictions. This separation shows why a finite buying deadline protects against an indefinitely misleading short-season prediction. It does **not** establish a new lower bound for all learning-augmented algorithms or an optimal trade-off among possible trust mechanisms.

## 5. Experiments

The repository includes Python implementations, experiment scripts, and generated figures for comparing the policies under different prediction settings. The analytical guarantees follow from the stated threshold rules. Reproducing the plots requires running the scripts with the repository dependencies.

The implementations cover the deterministic baseline, prediction-only, learning-augmented, and trust-aware policies, with the offline optimum used for comparison.

The reported parameter grid uses `B ∈ {10, 20, 50}`, `T ∈ {1, ..., 5B}`, prediction errors from 0% to 100%, and confidence values `c ∈ {0, 0.25, 0.5, 0.75, 1}`, with `λ = 0.5` for the main comparison. The separate lambda-comparison experiment varies `λ`.

The experimental scripts cover baseline and prediction-only behavior, different prediction-error models, variation in `λ`, trust-aware comparisons, signed error sweeps, confidence ablations, and adversarial cases.

### 5.1 Signed Error Sweep

The signed error sweep tests both directions of prediction error.

For overestimation, `p = T · (1 + error_fraction)`. For underestimation, `p = T · (1 - error_fraction)`.

This improves the original one-sided error sweep, where prediction-only appeared strong because predictions were mostly overestimated. The signed sweep shows that prediction-only can fail under underestimated long seasons.

Output figure: `figures/error_sweep.png`.

### 5.2 Generated Figures

The scripts generate these comparison figures: `figures/error_sweep_cost_ratio.png`, `figures/duration_sweep.png`, and `figures/confidence_ablation.png`.

These figures show how cost ratio changes with prediction error, true duration, and confidence level.

### 5.3 Adversarial Prediction Failure

The adversarial experiment tests four cases:

- Small `T` with a very large prediction
- Large `T` with a very small prediction
- Systematic overestimation
- Systematic underestimation

Output figure: `figures/adversarial_prediction_failure.png`.

The purpose is to demonstrate that prediction-only can fail badly, while trust-aware fallback remains controlled.

## 6. Results

The experiments illustrate the behavior of the policies analyzed above. Their worst-case guarantees follow from the mathematical arguments in Section 4, not from the plotted samples.

### 6.1 Deterministic Baseline

The deterministic baseline is stable and robust. It does not exploit predictions, but its competitive ratio stays below `2` in long-season cases.

This matches the classical ratio `CR = (2B - 1) / B < 2`.

### 6.2 Prediction-Only Policy

Prediction-only performs well when predictions are accurate or favorable. However, it is fragile.

In adversarial cases, prediction-only can either buy too early or rent for too long.

For a sufficiently long season and an erroneously short prediction, prediction-only rents throughout the season and obtains `CR = T / B`.

This grows without bound.

### 6.3 Learning-Augmented Policy

The learning-augmented policy imposes a finite buying deadline and therefore avoids the unbounded worst-case loss of prediction-only. Its performance can still vary substantially with the prediction: buying early helps on long seasons but can be costly when the season is shorter than predicted. In this implementation, its worst-case guarantee is already finite, even without an explicit confidence parameter.

### 6.4 Trust-Aware Policy

In the evaluated experimental settings, the trust-aware policy offers a tunable trade-off between buying early in response to a long-season prediction and retaining the deterministic buying deadline. It is not uniformly best across all instances.

For `p ≥ B`, increasing confidence moves the buying threshold toward `ceil(λB)`, which can help on sufficiently long seasons but may hurt on shorter-than-predicted seasons. For `p < B`, both thresholds equal `B`, regardless of confidence.

For `p ≥ B`, lower confidence shifts the buying threshold toward `B`. The finite worst-case bound comes from the enforced threshold range, not from confidence calibration.

The confidence ablation illustrates how outcomes vary when predictions favor early buying. The worst-case guarantee applies across all confidence settings; lower confidence does not automatically improve cost on every adversarial instance.

### 6.5 Main Empirical Takeaway

The experiments illustrate two behaviours already captured by the model and the proofs:

- Prediction-only matches the offline optimum when its prediction is exact, but can fail without bound when the prediction is wrong.
- The learning-augmented and trust-aware threshold rules have finite worst-case bounds and can buy earlier when `p ≥ B`.

These conclusions follow from the specified algorithms; the experiments illustrate them rather than establish a new competitive guarantee.

The confidence parameter makes the buying decision easy to inspect, but the experiments do not establish an improvement over the other bounded-threshold policies.

## 7. Limitations

This is a deliberately small model. The confidence parameter `c` is set manually, rather than estimated from calibrated predictions or past errors. A practical method would need to learn or update confidence, and would also have to account for the reliability and cost of doing so.

The experiments use synthetic durations and prediction errors. They make it possible to isolate particular failure cases, but do not capture distribution shift, correlated errors, or the richer decisions found in real online systems. The rule itself is also deliberately simple: it interpolates between two buying thresholds, and other ways of combining prediction and fallback may behave differently.

Finally, the proofs in Section 4 establish properties of these specific threshold policies. They do not give an error-sensitive competitive-ratio theorem, an optimal consistency–robustness frontier, or superiority over existing algorithms. Because buying days are integer-valued, the ceiling operation also creates a one-day discontinuity as confidence approaches one from below.

## 8. Future Work

A natural next step is to derive prediction-error-sensitive guarantees and compare them directly with established learning-augmented ski-rental results. The exact worst-case ratio for a fixed threshold is already characterized in Proposition 2, so improving the general guarantee would require a different algorithmic idea, not merely a sharper analysis of the same threshold. Randomized decisions are another possible direction, but they would need a separate model and proof.

Confidence is manually specified here. Estimating it from past prediction errors, calibration data, or uncertainty estimates would make the model more realistic. Such an extension should also measure the cost of obtaining and updating confidence, rather than assuming it is available for free.

The current experiments use synthetic durations and prediction errors. Testing real or semi-real traces, checking sensitivity to distribution shift, and examining related online problems such as caching would help distinguish behaviour specific to ski rental from properties that generalize. Any stronger claim would need carefully stated assumptions, comparisons with the literature, and reproducible experiments.

## References

[1] A. R. Karlin, M. S. Manasse, L. Rudolph, and D. D. Sleator. Competitive snoopy caching. Algorithmica, 1988.

[2] A. Borodin and R. El-Yaniv. Online Computation and Competitive Analysis. Cambridge University Press, 1998.

[3] T. Lykouris and S. Vassilvitskii. Competitive caching with machine learned advice. International Conference on Machine Learning, 2018.

[4] M. Purohit, Z. Svitkina, and R. Kumar. Improving online algorithms via ML predictions. Advances in Neural Information Processing Systems, 2018.

[5] M. Mitzenmacher. Scheduling with predictions and the price of misprediction. ITCS, 2020.

[6] Project implementation files: `src/ski_rental/`, `src/predictors/`, `experiments/`, `figures/`, and `notes/`.

[7] S. Angelopoulos, C. Dürr, S. Jin, S. Kamali, and M. Renault. Online computation with untrusted advice. ITCS, 2020.

[8] Y. Shin, C. Lee, G. Lee, and H.-C. An. Improved learning-augmented algorithms for the multi-option ski rental problem via best-possible competitive analysis. ICML, 2023.
