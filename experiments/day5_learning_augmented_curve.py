"""
Day 5 experiment: evaluate learning-augmented ski rental under different lambda values.

The learning-augmented rule is:

    if p >= B:
        buy at day ceil(lambda * B)
    else:
        buy at day B

This experiment compares λ = 0.5, 0.75, 1.0 under several prediction regimes.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt

from src.ski_rental.learning_augmented import learning_augmented_table


def main() -> None:
    buy_cost = 10
    max_days = 5 * buy_cost
    lambda_values = [0.5, 0.75, 1.0]
    prediction_modes = ["exact", "overestimate", "underestimate"]

    project_root = Path(__file__).resolve().parents[1]
    figures_dir = project_root / "figures"
    results_dir = project_root / "experiments" / "results"

    figures_dir.mkdir(exist_ok=True)
    results_dir.mkdir(exist_ok=True)

    all_rows = []

    for mode in prediction_modes:
        rows = learning_augmented_table(
            max_days=max_days,
            buy_cost=buy_cost,
            lambda_values=lambda_values,
            prediction_mode=mode,
        )
        all_rows.extend(rows)

    csv_path = results_dir / "day5_learning_augmented.csv"
    figure_path = figures_dir / "day5_learning_augmented_lambdas.png"

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "prediction_mode",
                "lambda",
                "T",
                "B",
                "p",
                "buy_day",
                "OPT",
                "ALG_learning_augmented",
                "cost_ratio",
                "prediction_error",
                "relative_prediction_error",
            ],
        )
        writer.writeheader()
        writer.writerows(all_rows)

    plt.figure(figsize=(10, 6))

    # Plot exact prediction only as the main Day 5 performance curve.
    # The full CSV includes exact, overestimate, and underestimate scenarios.
    for lambda_value in lambda_values:
        rows = [
            row
            for row in all_rows
            if row["prediction_mode"] == "exact"
            and abs(float(row["lambda"]) - lambda_value) < 1e-9
        ]

        true_days = [row["T"] for row in rows]
        ratios = [row["cost_ratio"] for row in rows]

        plt.plot(
            true_days,
            ratios,
            marker="o",
            linewidth=2,
            label=f"λ = {lambda_value}",
        )

    plt.axhline(y=1.0, linestyle="--", linewidth=1, label="offline optimum ratio")
    plt.axhline(y=2.0, linestyle="--", linewidth=1, label="2-competitive reference")

    plt.xlabel("True number of skiing days T")
    plt.ylabel("Cost ratio ALG / OPT")
    plt.title("Learning-Augmented Ski Rental under Exact Predictions")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(figure_path, dpi=200)
    plt.close()

    print("Day 5 learning-augmented experiment completed.")
    print(f"Saved CSV: {csv_path}")
    print(f"Saved figure: {figure_path}")


if __name__ == "__main__":
    main()