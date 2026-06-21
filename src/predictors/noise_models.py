"""
Prediction error models for learning-augmented ski rental.

Day 4 formalises what it means for a prediction to be wrong.

Definitions:
    T = true number of skiing days
    p = predicted number of skiing days
    η = |p - T|
    relative error = |p - T| / max(T, 1)

This module implements several prediction models:
1. exact prediction
2. small Gaussian noise
3. uniform noise
4. biased overestimate
5. biased underestimate
6. adversarial wrong prediction
"""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class PredictionResult:
    """
    Container for one prediction result.
    """

    model: str
    true_days: int
    buy_cost: int
    predicted_days: int
    prediction_error: int
    relative_prediction_error: float


def validate_inputs(true_days: int, buy_cost: int) -> None:
    """
    Validate common inputs.

    Args:
        true_days: True number of skiing days T.
        buy_cost: Buying cost B.
    """
    if true_days < 0:
        raise ValueError("true_days must be non-negative.")
    if buy_cost <= 0:
        raise ValueError("buy_cost must be positive.")


def clamp_prediction(predicted_days: int) -> int:
    """
    Ensure the predicted number of skiing days is non-negative.

    Args:
        predicted_days: Raw predicted value.

    Returns:
        Non-negative integer prediction.
    """
    return max(0, int(round(predicted_days)))


def prediction_error(true_days: int, predicted_days: int) -> int:
    """
    Compute absolute prediction error.

    η = |p - T|

    Args:
        true_days: True number of skiing days T.
        predicted_days: Predicted number of skiing days p.

    Returns:
        Absolute prediction error.
    """
    if true_days < 0:
        raise ValueError("true_days must be non-negative.")
    if predicted_days < 0:
        raise ValueError("predicted_days must be non-negative.")

    return abs(predicted_days - true_days)


def relative_prediction_error(true_days: int, predicted_days: int) -> float:
    """
    Compute relative prediction error.

    relative error = |p - T| / max(T, 1)

    Args:
        true_days: True number of skiing days T.
        predicted_days: Predicted number of skiing days p.

    Returns:
        Relative prediction error.
    """
    return prediction_error(true_days, predicted_days) / max(true_days, 1)


def make_result(
    model: str,
    true_days: int,
    buy_cost: int,
    predicted_days: int,
) -> PredictionResult:
    """
    Build a PredictionResult object.

    Args:
        model: Name of prediction model.
        true_days: True number of skiing days T.
        buy_cost: Buying cost B.
        predicted_days: Predicted number of skiing days p.

    Returns:
        PredictionResult with error metrics.
    """
    validate_inputs(true_days, buy_cost)

    predicted_days = clamp_prediction(predicted_days)

    return PredictionResult(
        model=model,
        true_days=true_days,
        buy_cost=buy_cost,
        predicted_days=predicted_days,
        prediction_error=prediction_error(true_days, predicted_days),
        relative_prediction_error=relative_prediction_error(true_days, predicted_days),
    )


def exact_prediction(true_days: int, buy_cost: int) -> PredictionResult:
    """
    Exact prediction model.

    p = T
    """
    validate_inputs(true_days, buy_cost)
    return make_result("exact", true_days, buy_cost, true_days)


def gaussian_noise_prediction(
    true_days: int,
    buy_cost: int,
    std_fraction: float = 0.15,
    seed: int | None = None,
) -> PredictionResult:
    """
    Small Gaussian noise prediction model.

    p = T + Gaussian(0, std_fraction * B)

    Args:
        true_days: True number of skiing days T.
        buy_cost: Buying cost B.
        std_fraction: Noise scale relative to B.
        seed: Optional random seed for reproducibility.

    Returns:
        PredictionResult.
    """
    validate_inputs(true_days, buy_cost)

    if std_fraction < 0:
        raise ValueError("std_fraction must be non-negative.")

    rng = random.Random(seed)
    noise = rng.gauss(0, std_fraction * buy_cost)
    predicted_days = true_days + noise

    return make_result("gaussian_noise", true_days, buy_cost, predicted_days)


def uniform_noise_prediction(
    true_days: int,
    buy_cost: int,
    width_fraction: float = 0.30,
    seed: int | None = None,
) -> PredictionResult:
    """
    Uniform noise prediction model.

    p = T + Uniform(-width_fraction * B, width_fraction * B)

    Args:
        true_days: True number of skiing days T.
        buy_cost: Buying cost B.
        width_fraction: Uniform noise width relative to B.
        seed: Optional random seed for reproducibility.

    Returns:
        PredictionResult.
    """
    validate_inputs(true_days, buy_cost)

    if width_fraction < 0:
        raise ValueError("width_fraction must be non-negative.")

    rng = random.Random(seed)
    width = width_fraction * buy_cost
    noise = rng.uniform(-width, width)
    predicted_days = true_days + noise

    return make_result("uniform_noise", true_days, buy_cost, predicted_days)


def biased_overestimate_prediction(
    true_days: int,
    buy_cost: int,
    bias_fraction: float = 0.75,
) -> PredictionResult:
    """
    Biased overestimate prediction model.

    p = T + bias_fraction * B

    This models a predictor that systematically predicts too many skiing days.
    """
    validate_inputs(true_days, buy_cost)

    if bias_fraction < 0:
        raise ValueError("bias_fraction must be non-negative.")

    predicted_days = true_days + bias_fraction * buy_cost

    return make_result("biased_overestimate", true_days, buy_cost, predicted_days)


def biased_underestimate_prediction(
    true_days: int,
    buy_cost: int,
    bias_fraction: float = 0.75,
) -> PredictionResult:
    """
    Biased underestimate prediction model.

    p = T - bias_fraction * B

    This models a predictor that systematically predicts too few skiing days.
    """
    validate_inputs(true_days, buy_cost)

    if bias_fraction < 0:
        raise ValueError("bias_fraction must be non-negative.")

    predicted_days = true_days - bias_fraction * buy_cost

    return make_result("biased_underestimate", true_days, buy_cost, predicted_days)


def adversarial_wrong_prediction(
    true_days: int,
    buy_cost: int,
) -> PredictionResult:
    """
    Adversarial wrong prediction model.

    The adversary gives a prediction that pushes the prediction-only algorithm
    toward the wrong action.

    If T < B:
        The offline optimum prefers renting.
        The adversary predicts a large p >= B to force buying.

    If T >= B:
        The offline optimum prefers buying.
        The adversary predicts a small p < B to force renting.
    """
    validate_inputs(true_days, buy_cost)

    if true_days < buy_cost:
        predicted_days = 5 * buy_cost
    else:
        predicted_days = 1

    return make_result("adversarial_wrong", true_days, buy_cost, predicted_days)


def generate_all_predictions(
    true_days: int,
    buy_cost: int,
    seed: int = 42,
) -> list[PredictionResult]:
    """
    Generate all Day 4 prediction models for one T, B instance.

    Args:
        true_days: True number of skiing days T.
        buy_cost: Buying cost B.
        seed: Random seed for reproducibility.

    Returns:
        List of PredictionResult objects.
    """
    validate_inputs(true_days, buy_cost)

    return [
        exact_prediction(true_days, buy_cost),
        gaussian_noise_prediction(true_days, buy_cost, seed=seed),
        uniform_noise_prediction(true_days, buy_cost, seed=seed),
        biased_overestimate_prediction(true_days, buy_cost),
        biased_underestimate_prediction(true_days, buy_cost),
        adversarial_wrong_prediction(true_days, buy_cost),
    ]


if __name__ == "__main__":
    B = 10
    test_values = [3, 8, 10, 30]

    print("Day 4: Prediction Error Models")
    print(f"Buy cost B = {B}")
    print()
    print("model\tT\tB\tp\terror\trel_error")

    for T in test_values:
        for result in generate_all_predictions(T, B, seed=42):
            print(
                f"{result.model}\t"
                f"{result.true_days}\t"
                f"{result.buy_cost}\t"
                f"{result.predicted_days}\t"
                f"{result.prediction_error}\t"
                f"{result.relative_prediction_error:.3f}"
            )