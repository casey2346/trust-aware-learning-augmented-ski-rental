"""
Trust-aware learning-augmented ski rental algorithm.

Day 6 implements the core trust-aware fallback algorithm.

Goal:
    Do not blindly trust predictions.
    Use a confidence value c in [0, 1] to decide how strongly to use the prediction.

Definitions:
    T = true number of skiing days
    B = buying cost
    p = predicted number of skiing days
    c = confidence in the prediction

Baseline:
    deterministic buy day = B

Prediction-aware buy day:
    if p >= B:
        buy at ceil(lambda * B)
    else:
        buy at B

Trust-aware blended buy day:
    buy_day = ceil(c * predicted_buy_day + (1 - c) * baseline_buy_day)

Interpretation:
    c = 1 means fully trust the prediction.
    c = 0 means ignore the prediction and use deterministic baseline.
    0 < c < 1 gives a blended threshold.

This algorithm is designed to avoid collapsing when predictions are unreliable.
"""

from __future__ import annotations

import math

from src.ski_rental.problem import offline_optimum, online_cost, competitive_ratio
from src.ski_rental.baselines import deterministic_buy_day, deterministic_ski_rental
from src.ski_rental.learning_augmented import (
    learning_augmented_buy_day,
    learning_augmented_ski_rental,
)
from src.ski_rental.prediction_only import prediction_only_ski_rental
from src.predictors.noise_models import prediction_error, relative_prediction_error


def validate_trust_aware_inputs(
    true_days: int,
    buy_cost: int,
    predicted_days: int,
    lambda_value: float,
    confidence: float,
) -> None:
    """
    Validate inputs for the trust-aware algorithm.
    """
    if true_days < 0:
        raise ValueError("true_days must be non-negative.")
    if buy_cost <= 0:
        raise ValueError("buy_cost must be positive.")
    if predicted_days < 0:
        raise ValueError("predicted_days must be non-negative.")
    if not (0 < lambda_value <= 1):
        raise ValueError("lambda_value must be in (0, 1].")
    if not (0 <= confidence <= 1):
        raise ValueError("confidence must be in [0, 1].")


def confidence_from_estimated_error(
    estimated_relative_error: float,
    scale: float = 1.0,
) -> float:
    """
    Convert an estimated relative prediction error into confidence.

    Rule:
        confidence = max(0, 1 - estimated_relative_error / scale)

    Args:
        estimated_relative_error: Estimated relative prediction error.
        scale: Error scale controlling how quickly confidence decreases.

    Returns:
        Confidence value c in [0, 1].
    """
    if estimated_relative_error < 0:
        raise ValueError("estimated_relative_error must be non-negative.")
    if scale <= 0:
        raise ValueError("scale must be positive.")

    confidence = 1.0 - estimated_relative_error / scale
    return max(0.0, min(1.0, confidence))


def trust_aware_buy_day(
    predicted_days: int,
    buy_cost: int,
    lambda_value: float,
    confidence: float,
) -> int:
    """
    Compute the trust-aware buying day.

    Steps:
        1. Compute deterministic baseline buy day: B.
        2. Compute prediction-aware buy day.
        3. Blend them using confidence.

    Formula:
        d_trust = ceil(c * d_pred + (1 - c) * d_base)

    Args:
        predicted_days: Predicted number of skiing days p.
        buy_cost: Buying cost B.
        lambda_value: Aggressiveness parameter λ in (0, 1].
        confidence: Confidence c in [0, 1].

    Returns:
        Trust-aware buying day.
    """
    if buy_cost <= 0:
        raise ValueError("buy_cost must be positive.")
    if predicted_days < 0:
        raise ValueError("predicted_days must be non-negative.")
    if not (0 < lambda_value <= 1):
        raise ValueError("lambda_value must be in (0, 1].")
    if not (0 <= confidence <= 1):
        raise ValueError("confidence must be in [0, 1].")

    baseline_buy_day = deterministic_buy_day(buy_cost)

    predicted_buy_day = learning_augmented_buy_day(
        predicted_days=predicted_days,
        buy_cost=buy_cost,
        lambda_value=lambda_value,
    )

    blended_buy_day = confidence * predicted_buy_day + (1 - confidence) * baseline_buy_day

    return max(1, math.ceil(blended_buy_day))


def trust_aware_ski_rental(
    true_days: int,
    buy_cost: int,
    predicted_days: int,
    lambda_value: float,
    confidence: float,
) -> int:
    """
    Compute the cost of the trust-aware learning-augmented algorithm.

    Args:
        true_days: True number of skiing days T.
        buy_cost: Buying cost B.
        predicted_days: Predicted number of skiing days p.
        lambda_value: Aggressiveness parameter λ.
        confidence: Prediction confidence c.

    Returns:
        Trust-aware algorithm cost.
    """
    validate_trust_aware_inputs(
        true_days=true_days,
        buy_cost=buy_cost,
        predicted_days=predicted_days,
        lambda_value=lambda_value,
        confidence=confidence,
    )

    buy_day = trust_aware_buy_day(
        predicted_days=predicted_days,
        buy_cost=buy_cost,
        lambda_value=lambda_value,
        confidence=confidence,
    )

    return online_cost(
        true_days=true_days,
        buy_cost=buy_cost,
        buy_day=buy_day,
    )


def trust_aware_ratio(
    true_days: int,
    buy_cost: int,
    predicted_days: int,
    lambda_value: float,
    confidence: float,
) -> float:
    """
    Compute ALG_trust / OPT.
    """
    validate_trust_aware_inputs(
        true_days=true_days,
        buy_cost=buy_cost,
        predicted_days=predicted_days,
        lambda_value=lambda_value,
        confidence=confidence,
    )

    buy_day = trust_aware_buy_day(
        predicted_days=predicted_days,
        buy_cost=buy_cost,
        lambda_value=lambda_value,
        confidence=confidence,
    )

    return competitive_ratio(
        true_days=true_days,
        buy_cost=buy_cost,
        buy_day=buy_day,
    )


def choose_adversarial_prediction(true_days: int, buy_cost: int) -> int:
    """
    Generate an adversarially wrong prediction.

    If T < B:
        prediction says very large p = 5B.
    If T >= B:
        prediction says very small p = 1.
    """
    if true_days < buy_cost:
        return 5 * buy_cost

    return 1


def trust_aware_comparison_table(
    max_days: int,
    buy_cost: int,
    lambda_value: float,
    confidence_values: list[float],
) -> list[dict[str, float | str]]:
    """
    Generate a comparison table under adversarial predictions.

    Compared algorithms:
        1. offline optimum
        2. deterministic baseline
        3. prediction-only
        4. learning-augmented
        5. trust-aware with different confidence values

    Args:
        max_days: Maximum true number of skiing days.
        buy_cost: Buying cost B.
        lambda_value: Aggressiveness parameter λ.
        confidence_values: List of confidence values.

    Returns:
        List of result dictionaries.
    """
    if max_days <= 0:
        raise ValueError("max_days must be positive.")
    if buy_cost <= 0:
        raise ValueError("buy_cost must be positive.")
    if not (0 < lambda_value <= 1):
        raise ValueError("lambda_value must be in (0, 1].")
    if not confidence_values:
        raise ValueError("confidence_values must not be empty.")

    rows: list[dict[str, float | str]] = []

    for true_days in range(1, max_days + 1):
        predicted_days = choose_adversarial_prediction(true_days, buy_cost)

        opt = offline_optimum(true_days, buy_cost)

        deterministic_cost = deterministic_ski_rental(true_days, buy_cost)
        prediction_only_cost = prediction_only_ski_rental(
            true_days=true_days,
            buy_cost=buy_cost,
            predicted_days=predicted_days,
        )
        learning_augmented_cost = learning_augmented_ski_rental(
            true_days=true_days,
            buy_cost=buy_cost,
            predicted_days=predicted_days,
            lambda_value=lambda_value,
        )

        rows.append(
            {
                "algorithm": "deterministic",
                "T": true_days,
                "B": buy_cost,
                "p": predicted_days,
                "lambda": lambda_value,
                "confidence": "",
                "buy_day": deterministic_buy_day(buy_cost),
                "OPT": opt,
                "ALG": deterministic_cost,
                "cost_ratio": deterministic_cost / opt if opt > 0 else 1.0,
                "prediction_error": prediction_error(true_days, predicted_days),
                "relative_prediction_error": relative_prediction_error(
                    true_days, predicted_days
                ),
            }
        )

        rows.append(
            {
                "algorithm": "prediction_only",
                "T": true_days,
                "B": buy_cost,
                "p": predicted_days,
                "lambda": "",
                "confidence": "",
                "buy_day": "",
                "OPT": opt,
                "ALG": prediction_only_cost,
                "cost_ratio": prediction_only_cost / opt if opt > 0 else 1.0,
                "prediction_error": prediction_error(true_days, predicted_days),
                "relative_prediction_error": relative_prediction_error(
                    true_days, predicted_days
                ),
            }
        )

        rows.append(
            {
                "algorithm": "learning_augmented",
                "T": true_days,
                "B": buy_cost,
                "p": predicted_days,
                "lambda": lambda_value,
                "confidence": 1.0,
                "buy_day": learning_augmented_buy_day(
                    predicted_days=predicted_days,
                    buy_cost=buy_cost,
                    lambda_value=lambda_value,
                ),
                "OPT": opt,
                "ALG": learning_augmented_cost,
                "cost_ratio": learning_augmented_cost / opt if opt > 0 else 1.0,
                "prediction_error": prediction_error(true_days, predicted_days),
                "relative_prediction_error": relative_prediction_error(
                    true_days, predicted_days
                ),
            }
        )

        for confidence in confidence_values:
            trust_cost = trust_aware_ski_rental(
                true_days=true_days,
                buy_cost=buy_cost,
                predicted_days=predicted_days,
                lambda_value=lambda_value,
                confidence=confidence,
            )

            rows.append(
                {
                    "algorithm": f"trust_aware_c={confidence}",
                    "T": true_days,
                    "B": buy_cost,
                    "p": predicted_days,
                    "lambda": lambda_value,
                    "confidence": confidence,
                    "buy_day": trust_aware_buy_day(
                        predicted_days=predicted_days,
                        buy_cost=buy_cost,
                        lambda_value=lambda_value,
                        confidence=confidence,
                    ),
                    "OPT": opt,
                    "ALG": trust_cost,
                    "cost_ratio": trust_cost / opt if opt > 0 else 1.0,
                    "prediction_error": prediction_error(true_days, predicted_days),
                    "relative_prediction_error": relative_prediction_error(
                        true_days, predicted_days
                    ),
                }
            )

    return rows


if __name__ == "__main__":
    B = 10
    max_T = 50
    lambda_value = 0.5
    confidence_values = [0.0, 0.25, 0.5, 0.75, 1.0]

    print("Day 6: Trust-Aware Learning-Augmented Ski Rental")
    print(f"Buy cost B = {B}")
    print(f"lambda = {lambda_value}")
    print()
    print("algorithm\tT\tp\tconfidence\tbuy_day\tOPT\tALG\tCR")

    rows = trust_aware_comparison_table(
        max_days=max_T,
        buy_cost=B,
        lambda_value=lambda_value,
        confidence_values=confidence_values,
    )

    for row in rows:
        if str(row["algorithm"]).startswith("trust_aware"):
            print(
                f"{row['algorithm']}\t"
                f"{int(row['T'])}\t"
                f"{int(row['p'])}\t"
                f"{row['confidence']}\t"
                f"{int(row['buy_day'])}\t"
                f"{int(row['OPT'])}\t"
                f"{int(row['ALG'])}\t"
                f"{float(row['cost_ratio']):.3f}"
            )