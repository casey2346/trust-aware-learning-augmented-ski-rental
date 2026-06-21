"""
Core definitions for the classical ski rental problem.

This file implements the mathematical quantities used throughout the project:

1. offline optimum;
2. online algorithm cost;
3. competitive ratio;
4. classical deterministic baseline.

The implementation is intentionally simple because Day 1 focuses on correct
formal definitions rather than advanced algorithms.
"""

from __future__ import annotations


def offline_optimum(true_days: int, buy_cost: int) -> int:
    """
    Compute the offline optimal cost.

    The offline optimum knows the true number of skiing days in advance.

    Args:
        true_days: True number of skiing days T.
        buy_cost: Cost of buying skis B.

    Returns:
        The offline optimal cost min(T, B).
    """
    if true_days < 0:
        raise ValueError("true_days must be non-negative.")
    if buy_cost <= 0:
        raise ValueError("buy_cost must be positive.")

    return min(true_days, buy_cost)


def online_cost(true_days: int, buy_cost: int, buy_day: int) -> int:
    """
    Compute the cost of an online algorithm that buys on a fixed day.

    Convention:
    - Renting costs 1 per day.
    - Buying costs B.
    - If the algorithm buys on day d, it rents for d - 1 days and buys on day d.
    - If the season ends before day d, the algorithm never buys.

    Args:
        true_days: True number of skiing days T.
        buy_cost: Cost of buying skis B.
        buy_day: Day d on which the algorithm buys skis.

    Returns:
        Online algorithm cost ALG(T, B, d).
    """
    if true_days < 0:
        raise ValueError("true_days must be non-negative.")
    if buy_cost <= 0:
        raise ValueError("buy_cost must be positive.")
    if buy_day <= 0:
        raise ValueError("buy_day must be positive.")

    if true_days < buy_day:
        return true_days

    return (buy_day - 1) + buy_cost


def competitive_ratio(true_days: int, buy_cost: int, buy_day: int) -> float:
    """
    Compute the competitive ratio ALG / OPT for a fixed instance.

    Args:
        true_days: True number of skiing days T.
        buy_cost: Cost of buying skis B.
        buy_day: Day d on which the algorithm buys skis.

    Returns:
        Competitive ratio ALG(T, B, d) / OPT(T, B).
    """
    opt = offline_optimum(true_days, buy_cost)

    if opt == 0:
        return 1.0

    alg = online_cost(true_days, buy_cost, buy_day)
    return alg / opt


def deterministic_buy_day(buy_cost: int) -> int:
    """
    Classical deterministic ski rental baseline.

    The standard deterministic algorithm buys on day B.

    Args:
        buy_cost: Cost of buying skis B.

    Returns:
        Buying day d = B.
    """
    if buy_cost <= 0:
        raise ValueError("buy_cost must be positive.")

    return buy_cost


def deterministic_cost(true_days: int, buy_cost: int) -> int:
    """
    Compute the cost of the classical deterministic baseline.

    Args:
        true_days: True number of skiing days T.
        buy_cost: Cost of buying skis B.

    Returns:
        Cost of the deterministic ski rental baseline.
    """
    buy_day = deterministic_buy_day(buy_cost)
    return online_cost(true_days, buy_cost, buy_day)


def deterministic_competitive_ratio(true_days: int, buy_cost: int) -> float:
    """
    Compute the competitive ratio of the deterministic baseline.

    Args:
        true_days: True number of skiing days T.
        buy_cost: Cost of buying skis B.

    Returns:
        Competitive ratio of the deterministic baseline.
    """
    buy_day = deterministic_buy_day(buy_cost)
    return competitive_ratio(true_days, buy_cost, buy_day)


if __name__ == "__main__":
    B = 10

    print("Classical deterministic ski rental baseline")
    print(f"Buy cost B = {B}")
    print()
    print("T\tOPT\tALG_det\tCR")

    for T in range(1, 31):
        opt = offline_optimum(T, B)
        alg = deterministic_cost(T, B)
        cr = deterministic_competitive_ratio(T, B)

        print(f"{T}\t{opt}\t{alg}\t{cr:.3f}")