"""
Prediction-only ski rental algorithm.

Day 3 implements an algorithm that fully trusts the prediction.

Prediction:
    p = predicted number of skiing days

Rule:
    if p >= B:
        buy immediately on day 1
    else:
        never buy and rent every day

This algorithm is intentionally fragile:
- If the prediction is accurate, it performs very well.
- If the prediction is wrong, it can perform badly.

This motivates the later trust-aware algorithm.
"""

from __future__ import annotations

from src.ski_rental.problem import offline_optimum


def prediction_error(true_days: int, predicted_days: int) -> int:
    """
    Compute absolute prediction error.

    Args:
        true_days: True number of skiing days T.
        predicted_days: Predicted number of skiing days p.

    Returns:
        Absolute prediction error |p - T|.
    """
    if true_days < 0:
        raise ValueError("true_days must be non-negative.")
    if predicted_days < 0:
        raise ValueError("predicted_days must be non-negative.")

    return abs(predicted_days - true_days)


def relative_prediction_error(true_days: int, predicted_days: int) -> float:
    """
    Compute relative prediction error.

    Args:
        true_days: True number of skiing days T.
        predicted_days: Predicted number of skiing days p.

    Returns:
        Relative prediction error |p - T| / max(T, 1).
    """
    return prediction_error(true_days, predicted_days) / max(true_days, 1)


def prediction_only_decision(predicted_days: int, buy_cost: int) -> str:
    """
    Return the decision made by the prediction-only algorithm.

    Rule:
        if p >= B:
            buy immediately
        else:
            rent forever

    Args:
        predicted_days: Predicted number of skiing days p.
        buy_cost: Buying cost B.

    Returns:
        "buy_immediately" or "rent_forever".
    """
    if predicted_days < 0:
        raise ValueError("predicted_days must be non-negative.")
    if buy_cost <= 0:
        raise ValueError("buy_cost must be positive.")

    if predicted_days >= buy_cost:
        return "buy_immediately"

    return "rent_forever"


def prediction_only_ski_rental(
    true_days: int,
    buy_cost: int,
    predicted_days: int,
) -> int:
    """
    Compute the cost of the prediction-only ski rental algorithm.

    Rule:
        if p >= B:
            buy immediately, cost = B
        else:
            rent for all T days, cost = T

    Args:
        true_days: True number of skiing days T.
        buy_cost: Buying cost B.
        predicted_days: Predicted number of skiing days p.

    Returns:
        Cost of the prediction-only algorithm.
    """
    if true_days < 0:
        raise ValueError("true_days must be non-negative.")
    if buy_cost <= 0:
        raise ValueError("buy_cost must be positive.")
    if predicted_days < 0:
        raise ValueError("predicted_days must be non-negative.")

    decision = prediction_only_decision(predicted_days, buy_cost)

    if decision == "buy_immediately":
        if true_days == 0:
            return 0
        return buy_cost

    return true_days


def prediction_only_ratio(
    true_days: int,
    buy_cost: int,
    predicted_days: int,
) -> float:
    """
    Compute the cost ratio ALG_pred / OPT.

    Args:
        true_days: True number of skiing days T.
        buy_cost: Buying cost B.
        predicted_days: Predicted number of skiing days p.

    Returns:
        Cost ratio of prediction-only algorithm against offline optimum.
    """
    opt = offline_optimum(true_days, buy_cost)

    if opt == 0:
        return 1.0

    alg = prediction_only_ski_rental(true_days, buy_cost, predicted_days)
    return alg / opt


def prediction_only_table(
    max_days: int,
    buy_cost: int,
    prediction_mode: str,
) -> list[dict[str, float | str]]:
    """
    Generate evaluation rows for the prediction-only algorithm.

    Prediction modes:
        exact:
            p = T
        overestimate:
            p = 5B
        underestimate:
            p = 1

    Args:
        max_days: Maximum true number of skiing days.
        buy_cost: Buying cost B.
        prediction_mode: Prediction scenario.

    Returns:
        List of result dictionaries.
    """
    if max_days <= 0:
        raise ValueError("max_days must be positive.")
    if buy_cost <= 0:
        raise ValueError("buy_cost must be positive.")
    if prediction_mode not in {"exact", "overestimate", "underestimate"}:
        raise ValueError(
            "prediction_mode must be one of: exact, overestimate, underestimate."
        )

    rows: list[dict[str, float | str]] = []

    for true_days in range(1, max_days + 1):
        if prediction_mode == "exact":
            predicted_days = true_days
        elif prediction_mode == "overestimate":
            predicted_days = 5 * buy_cost
        else:
            predicted_days = 1

        opt = offline_optimum(true_days, buy_cost)
        alg = prediction_only_ski_rental(true_days, buy_cost, predicted_days)
        ratio = prediction_only_ratio(true_days, buy_cost, predicted_days)
        error = prediction_error(true_days, predicted_days)
        relative_error = relative_prediction_error(true_days, predicted_days)
        decision = prediction_only_decision(predicted_days, buy_cost)

        rows.append(
            {
                "mode": prediction_mode,
                "T": true_days,
                "B": buy_cost,
                "p": predicted_days,
                "OPT": opt,
                "ALG_pred_only": alg,
                "cost_ratio": ratio,
                "prediction_error": error,
                "relative_prediction_error": relative_error,
                "decision": decision,
            }
        )

    return rows


if __name__ == "__main__":
    B = 10
    max_T = 50

    for mode in ["exact", "overestimate", "underestimate"]:
        print()
        print(f"Prediction-only algorithm: {mode}")
        print("T\tp\tOPT\tALG_pred\tCR\tDecision")

        for row in prediction_only_table(max_T, B, mode):
            print(
                f"{int(row['T'])}\t"
                f"{int(row['p'])}\t"
                f"{int(row['OPT'])}\t"
                f"{int(row['ALG_pred_only'])}\t"
                f"{float(row['cost_ratio']):.3f}\t"
                f"{row['decision']}"
            )