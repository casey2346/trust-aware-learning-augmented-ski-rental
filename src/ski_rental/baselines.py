"""
Classical deterministic baseline algorithms for the ski rental problem.

Day 2 focuses on the standard deterministic 2-competitive ski rental algorithm.

Convention:
- Renting costs 1 per day.
- Buying costs B.
- If the algorithm buys on day d, it rents for d - 1 days and buys on day d.
- The classical deterministic baseline buys on day B.

Under this convention, when T >= B:

    ALG_det(T, B) = (B - 1) + B = 2B - 1

and

    OPT(T, B) = B

so the competitive ratio is:

    (2B - 1) / B = 2 - 1/B <= 2
"""

from __future__ import annotations

from src.ski_rental.problem import offline_optimum, online_cost, competitive_ratio


def deterministic_buy_day(buy_cost: int) -> int:
    """
    Return the buying day for the classical deterministic ski rental algorithm.

    The standard deterministic baseline buys on day B.

    Args:
        buy_cost: Buying cost B.

    Returns:
        Buying day d = B.
    """
    if buy_cost <= 0:
        raise ValueError("buy_cost must be positive.")

    return buy_cost


def deterministic_ski_rental(true_days: int, buy_cost: int) -> int:
    """
    Compute the cost of the classical deterministic ski rental algorithm.

    The algorithm buys on day B.

    Args:
        true_days: Unknown true number of skiing days T.
        buy_cost: Buying cost B.

    Returns:
        Cost of the deterministic ski rental algorithm.
    """
    if true_days < 0:
        raise ValueError("true_days must be non-negative.")
    if buy_cost <= 0:
        raise ValueError("buy_cost must be positive.")

    buy_day = deterministic_buy_day(buy_cost)
    return online_cost(true_days, buy_cost, buy_day)


def deterministic_ratio(true_days: int, buy_cost: int) -> float:
    """
    Compute the competitive ratio of the deterministic baseline.

    Args:
        true_days: Unknown true number of skiing days T.
        buy_cost: Buying cost B.

    Returns:
        Competitive ratio ALG_det / OPT.
    """
    buy_day = deterministic_buy_day(buy_cost)
    return competitive_ratio(true_days, buy_cost, buy_day)


def deterministic_table(max_days: int, buy_cost: int) -> list[dict[str, float]]:
    """
    Generate a table of T, OPT, deterministic cost, and competitive ratio.

    Args:
        max_days: Maximum true number of skiing days to evaluate.
        buy_cost: Buying cost B.

    Returns:
        A list of result dictionaries.
    """
    if max_days <= 0:
        raise ValueError("max_days must be positive.")
    if buy_cost <= 0:
        raise ValueError("buy_cost must be positive.")

    rows: list[dict[str, float]] = []

    for true_days in range(1, max_days + 1):
        opt = offline_optimum(true_days, buy_cost)
        alg = deterministic_ski_rental(true_days, buy_cost)
        ratio = deterministic_ratio(true_days, buy_cost)

        rows.append(
            {
                "T": true_days,
                "B": buy_cost,
                "OPT": opt,
                "ALG_det": alg,
                "competitive_ratio": ratio,
            }
        )

    return rows


if __name__ == "__main__":
    B = 10
    max_T = 30

    print("Day 2: Classical Deterministic Ski Rental Baseline")
    print(f"Buy cost B = {B}")
    print()
    print("T\tOPT\tALG_det\tCR")

    for row in deterministic_table(max_T, B):
        print(
            f"{int(row['T'])}\t"
            f"{int(row['OPT'])}\t"
            f"{int(row['ALG_det'])}\t"
            f"{row['competitive_ratio']:.3f}"
        )