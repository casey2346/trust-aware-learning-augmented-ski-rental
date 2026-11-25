# Trust-Aware Learning-Augmented Ski Rental under Unreliable Predictions

This project examines how unreliable predictions affect decisions in the classical ski-rental problem. It compares four policies: a deterministic baseline, a prediction-only policy, a bounded prediction-guided threshold, and a confidence-weighted threshold.

**Main finding:** Prediction-only can have an unbounded competitive ratio when a short-season prediction is badly wrong. Both bounded-threshold policies avoid this particular failure by buying no later than day `B`. The confidence parameter shifts the buying day; it does not, by itself, establish a stronger worst-case guarantee than the prediction-guided threshold already has.

The full assumptions and proofs appear in [`paper/technical_report.md`](paper/technical_report.md).

## Model

Let `T >= 1` be the unknown number of skiing days, `B >= 1` the integer purchase cost, and `p` the predicted duration. Renting costs one unit per day. Buying at the beginning of day `d` costs `B` after `d - 1` rental days.

```text
OPT(T, B) = min(T, B)
ALG(T, B, d) = T,         if T < d
               B + d - 1, if T >= d
CR(T, B, d) = ALG(T, B, d) / OPT(T, B)
```

The absolute prediction error is `eta = |p - T|`.

## The four policies

| Policy | Decision |
| --- | --- |
| Deterministic | Buy on day `B`. Its worst-case competitive ratio is `2 - 1/B`. |
| Prediction-only | Buy immediately if `p >= B`; otherwise rent throughout the season. |
| Prediction-guided | Buy on `d_pred = ceil(lambda * B)` if `p >= B`; otherwise buy on day `B`. |
| Trust-aware | Buy on `d_trust = ceil(c * d_pred + (1-c) * B)`. |

Here `lambda` is in `(0, 1]` and confidence `c` is in `[0, 1]`. At `c = 0`, trust-aware is identical to the deterministic baseline; at `c = 1`, it is identical to the prediction-guided policy. When `p < B`, both buying thresholds are `B` and confidence changes nothing. Integer rounding means the threshold changes in steps, not continuously.

## What can be proved

**Perfect prediction.** When `p = T`, the exact difference between the trust-aware and prediction-guided costs is

```text
C_trust - C_pred = ceil((1-c) * (B-d_pred)) >= 0.
```

At `c = 1` the costs coincide. When `d_pred < B`, the difference can remain one for `c < 1` arbitrarily close to one. Thus, continuous convergence as `c` approaches one from below would be an incorrect claim.

**Bounded buying thresholds.** For any fixed integer `1 <= d <= B`,

```text
ALG(T, B, d) / OPT(T, B) <= 1 + (B-1)/d.
```

The bound is attained at `T = d`. Because both bounded policies buy no earlier than `ceil(lambda * B)`, they satisfy, for any prediction and confidence,

```text
ALG / OPT <= 1 + (B-1)/ceil(lambda * B) <= 1 + 1/lambda.
```

The finite bound follows from the threshold range; it is not a newly established optimal consistency–robustness trade-off.

**Adversarial example.** For fixed `B > 1`, take `p = 1 < B` and let `T` grow. Prediction-only rents throughout the season, so its competitive ratio is `T/B` and grows without bound as `T` increases. Both bounded policies buy on day `B` in this example, with ratio `2 - 1/B` for `T >= B`, independently of confidence.

These statements concern the defined policies. They are not a general lower bound for all learning-augmented online algorithms.

## Experiments and figures

The scripts evaluate synthetic predictions, signed over- and underestimation, confidence levels, alternative `lambda` values, and adversarial scenarios. Main parameter choices include `B` in `{10, 20, 50}`, `T` from `1` to `5B`, and confidence in `{0, 0.25, 0.5, 0.75, 1}`; individual scripts use subsets. The experiments illustrate the mathematical behavior, rather than prove the bounds.

- **Signed error sweep:** [`figures/error_sweep.png`](figures/error_sweep.png) — predictions above and below the true duration.
- **Error versus cost ratio:** [`figures/error_sweep_cost_ratio.png`](figures/error_sweep_cost_ratio.png) — average cost ratio over sampled durations.
- **Duration sweep:** [`figures/duration_sweep.png`](figures/duration_sweep.png) — behavior under adversarial predictions.
- **Confidence ablation:** [`figures/confidence_ablation.png`](figures/confidence_ablation.png) — average ratio versus confidence.
- **Adversarial cases:** [`figures/adversarial_prediction_failure.png`](figures/adversarial_prediction_failure.png) — four misleading or biased prediction settings, with confidence fixed at `c = 0` in this experiment.

The adversarial-cases script fixes `c = 0`, so its trust-aware curve is the deterministic baseline; this figure is meant to illustrate prediction-only failures, not the effect of confidence. Confidence is varied separately in `experiments/adversarial_test.py` and shown in `figures/confidence_ablation.png`. At `c = 1`, trust-aware coincides with the prediction-guided policy.

## Reproduce the results

From the repository root, with Python 3 installed:

```bash
git clone https://github.com/casey2346/trust-aware-learning-augmented-ski-rental.git
cd trust-aware-learning-augmented-ski-rental
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
PYTHONPATH=. python3 experiments/run_all.py
```

This entry point runs the main experiment scripts and writes results under `experiments/results/` and `figures/`. The signed error sweep is implemented in `experiments/error_sweep.py`.

To regenerate selected figures individually:

```bash
PYTHONPATH=. python3 experiments/error_sweep.py
PYTHONPATH=. python3 experiments/adversarial_test.py
PYTHONPATH=. python3 experiments/make_figures.py
PYTHONPATH=. python3 experiments/adversarial_prediction_failure.py
```

## Where to look

The core cost and policy implementations are in [`src/ski_rental/`](src/ski_rental/), with prediction utilities in [`src/predictors/`](src/predictors/). The reproducible experiments are in [`experiments/`](experiments/). The technical report provides the definitive mathematical statements; [`notes/`](notes/) contains supporting and exploratory explanations. The supporting notes should use the same assumptions and bounds as the report.

## Limitations

The confidence parameter is supplied manually rather than estimated from calibrated predictions. The experiments are synthetic and do not test distribution shift or real prediction traces. The proposed interpolation is deliberately simple and is not proven to outperform other bounded-threshold policies or the best known learning-augmented ski-rental algorithms.

Useful next steps are to calibrate confidence, test real or semi-real traces, compare against stronger published baselines, and investigate genuinely error-sensitive bounds. A better worst-case theorem would require a different algorithmic insight, not just rewording the present bound.

## References

- Borodin, A., and El-Yaniv, R. *Online Computation and Competitive Analysis*. Cambridge University Press, 1998.
- Lykouris, T., and Vassilvitskii, S. *Competitive Caching with Machine Learned Advice*. ICML, 2018.
- Purohit, M., Svitkina, Z., and Kumar, R. *Improving Online Algorithms via ML Predictions*. NeurIPS, 2018.
- Angelopoulos, S., Dürr, C., Jin, S., Kamali, S., and Renault, M. *Online Computation with Untrusted Advice*. ITCS, 2020.
