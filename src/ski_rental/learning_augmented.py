"""
Learning-augmented ski rental algorithm.

Day 5 implements a standard learning-augmented version of the ski rental problem.

Prediction:
    p = predicted number of skiing days

Rule:
    if p >= B:
        buy at day ceil(lambda * B)
    else:
        buy at day B

where lambda is in (0, 1].

Interpretation:
    - If the prediction suggests a long season, the algorithm buys earlier.
    - If the prediction suggests a short season, the algorithm behaves like the
      deterministic baseline and buys on day B.

This algorithm uses predictions, but it is not yet trust-aware.
"""

from __future__ import annotations

import math

from src.ski_rental.problem import offline_optimum, online_cost, competitive_ratio
from src.predictors.noise_models import prediction_error, relative_prediction_error


def validate_learning_augmented_inputs(
    true_days: int,
    buy_cost: int,
    predicted_days: int,
    lambda_value: float,
) -> None:
    """
    Validate inputs for the learning-augmented algorithm.
    """
    if true_days < 0:
        raise ValueError("true_days must be non-negative.")
    if buy_cost <= 0:
        raise ValueError("buy_cost must be positive.")
    if predicted_days < 0:
        raise ValueError("predicted_days must be non-negative.")
    if not (0 < lambda_value <= 1):
        raise ValueError("lambda_value must be in (0, 1].")


def learning_augmented_buy_day(
    predicted_days: int,
    buy_cost: int,
    lambda_value: float,
) -> int:
    """
    Compute the buying day for the learning-augmented algorithm.

    Rule:
        if p >= B:
            buy at day ceil(lambda * B)
        else:
            buy at day B

    Args:
        predicted_days: Predicted number of skiing days p.
        buy_cost: Buying cost B.
        lambda_value: Aggressiveness parameter λ in (0, 1].

    Returns:
        Buying day d.
    """
    if buy_cost <= 0:
        raise ValueError("buy_cost must be positive.")
    if predicted_days < 0:
        raise ValueError("predicted_days must be non-negative.")
    if not (0 < lambda_value <= 1):
        raise ValueError("lambda_value must be in (0, 1].")

    if predicted_days >= buy_cost:
        return max(1, math.ceil(lambda_value * buy_cost))

    return buy_cost


def learning_augmented_ski_rental(
    true_days: int,
    buy_cost: int,
    predicted_days: int,
    lambda_value: float,
) -> int:
    """
    Compute the cost of the learning-augmented ski rental algorithm.

    Args:
        true_days: True number of skiing days T.
        buy_cost: Buying cost B.
        predicted_days: Predicted number of skiing days p.
        lambda_value: Aggressiveness parameter λ in (0, 1].

    Returns:
        Cost of the learning-augmented algorithm.
    """
    validate_learning_augmented_inputs(
        true_days=true_days,
        buy_cost=buy_cost,
        predicted_days=predicted_days,
        lambda_value=lambda_value,
    )

    buy_day = learning_augmented_buy_day(
        predicted_days=predicted_days,
        buy_cost=buy_cost,
        lambda_value=lambda_value,
    )

    return online_cost(
        true_days=true_days,
        buy_cost=buy_cost,
        buy_day=buy_day,
    )


def learning_augmented_ratio(
    true_days: int,
    buy_cost: int,
    predicted_days: int,
    lambda_value: float,
) -> float:
    """
    Compute ALG_learning_augmented / OPT.
    """
    validate_learning_augmented_inputs(
        true_days=true_days,
        buy_cost=buy_cost,
        predicted_days=predicted_days,
        lambda_value=lambda_value,
    )

    buy_day = learning_augmented_buy_day(
        predicted_days=predicted_days,
        buy_cost=buy_cost,
        lambda_value=lambda_value,
    )

    return competitive_ratio(
        true_days=true_days,
        buy_cost=buy_cost,
        buy_day=buy_day,
    )


def choose_prediction(
    true_days: int,
    buy_cost: int,
    prediction_mode: str,
) -> int:
    """
    Choose a prediction p for a given prediction scenario.

    Modes:
        exact:
            p = T
        overestimate:
            p = 5B
        underestimate:
            p = 1
        threshold:
            p = B

    Args:
        true_days: True number of skiing days T.
        buy_cost: Buying cost B.
        prediction_mode: Prediction scenario.

    Returns:
        Predicted number of skiing days p.
    """
    if prediction_mode == "exact":
        return true_days

    if prediction_mode == "overestimate":
        return 5 * buy_cost

    if prediction_mode == "underestimate":
        return 1

    if prediction_mode == "threshold":
        return buy_cost

    raise ValueError(
        "prediction_mode must be one of: exact, overestimate, underestimate, threshold."
    )


def learning_augmented_table(
    max_days: int,
    buy_cost: int,
    lambda_values: list[float],
    prediction_mode: str,
) -> list[dict[str, float | str]]:
    """
    Generate evaluation rows for the learning-augmented algorithm.

    Args:
        max_days: Maximum true number of skiing days.
        buy_cost: Buying cost B.
        lambda_values: List of λ values.
        prediction_mode: Prediction scenario.

    Returns:
        List of result dictionaries.
    """
    if max_days <= 0:
        raise ValueError("max_days must be positive.")
    if buy_cost <= 0:
        raise ValueError("buy_cost must be positive.")
    if not lambda_values:
        raise ValueError("lambda_values must not be empty.")

    rows: list[dict[str, float | str]] = []

    for lambda_value in lambda_values:
        if not (0 < lambda_value <= 1):
            raise ValueError("Each lambda value must be in (0, 1].")

        for true_days in range(1, max_days + 1):
            predicted_days = choose_prediction(
                true_days=true_days,
                buy_cost=buy_cost,
                prediction_mode=prediction_mode,
            )

            buy_day = learning_augmented_buy_day(
                predicted_days=predicted_days,
                buy_cost=buy_cost,
                lambda_value=lambda_value,
            )

            opt = offline_optimum(true_days, buy_cost)
            alg = learning_augmented_ski_rental(
                true_days=true_days,
                buy_cost=buy_cost,
                predicted_days=predicted_days,
                lambda_value=lambda_value,
            )
            ratio = learning_augmented_ratio(
                true_days=true_days,
                buy_cost=buy_cost,
                predicted_days=predicted_days,
                lambda_value=lambda_value,
            )

            rows.append(
                {
                    "prediction_mode": prediction_mode,
                    "lambda": lambda_value,
                    "T": true_days,
                    "B": buy_cost,
                    "p": predicted_days,
                    "buy_day": buy_day,
                    "OPT": opt,
                    "ALG_learning_augmented": alg,
                    "cost_ratio": ratio,
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
    lambdas = [0.5, 0.75, 1.0]

    for mode in ["exact", "overestimate", "underestimate"]:
        print()
        print(f"Learning-augmented algorithm: {mode}")
        print("lambda\tT\tp\tbuy_day\tOPT\tALG\tCR")

        rows = learning_augmented_table(
            max_days=max_T,
            buy_cost=B,
            lambda_values=lambdas,
            prediction_mode=mode,
        )

        for row in rows:
            print(
                f"{row['lambda']:.2f}\t"
                f"{int(row['T'])}\t"
                f"{int(row['p'])}\t"
                f"{int(row['buy_day'])}\t"
                f"{int(row['OPT'])}\t"
                f"{int(row['ALG_learning_augmented'])}\t"
                f"{float(row['cost_ratio']):.3f}"
            )