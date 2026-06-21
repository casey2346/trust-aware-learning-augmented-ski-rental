# Day 4 Prediction Error Model

## Objective

Day 4 formalises prediction error for the learning-augmented ski rental project.

The goal is to make the phrase "wrong prediction" mathematically precise and implement several prediction noise models.

## Core Definitions

Let:

T = true number of skiing days
p = predicted number of skiing days
B = buying cost

The absolute prediction error is:

η = |p - T|

The relative prediction error is:

η_rel = |p - T| / max(T, 1)

The relative error is useful because the same absolute error may be more serious when T is small.

For example:

T = 2, p = 7  gives  |p - T| = 5, relative error = 2.5
T = 50, p = 55 gives |p - T| = 5, relative error = 0.1
Implemented Prediction Models

Day 4 implements six prediction models.

1. Exact Prediction
p = T

This is the ideal case.

Prediction error:

η = 0

This model represents perfect prediction.

2. Small Gaussian Noise
p = T + Gaussian(0, σ)

where:

σ = 0.15B

This models random prediction noise around the true value.

3. Uniform Noise
p = T + Uniform(-w, w)

where:

w = 0.30B

This models bounded random noise.

4. Biased Overestimate
p = T + 0.75B

This models a predictor that systematically overestimates the number of skiing days.

This can cause a prediction-only algorithm to buy too early.

5. Biased Underestimate
p = T - 0.75B

This models a predictor that systematically underestimates the number of skiing days.

This can cause a prediction-only algorithm to rent for too long.

6. Adversarial Wrong Prediction

The adversarial predictor gives a prediction that pushes the algorithm toward the wrong action.

If:

T < B

then renting is better, so the adversary predicts:

p = 5B

This may cause the algorithm to buy unnecessarily.

If:

T >= B

then buying is better, so the adversary predicts:

p = 1

This may cause the algorithm to rent for too long.

Day 4 Outputs

Implemented:

src/predictors/noise_models.py

Generated:

experiments/day4_noise_models.py
experiments/results/day4_noise_models.csv
figures/day4_noise_models_predictions.png
Interpretation

Day 4 creates the foundation for later experiments.

The project can now evaluate algorithms under multiple prediction regimes:

exact prediction
small random noise
bounded random noise
biased overestimate
biased underestimate
adversarial wrong prediction

This is important because a learning-augmented algorithm should not only perform well when predictions are accurate.

It should also remain robust when predictions are noisy, biased, shifted, or adversarial.