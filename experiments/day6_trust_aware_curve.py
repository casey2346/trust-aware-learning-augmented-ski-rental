"""
Day 6 experiment: evaluate trust-aware fallback under adversarial predictions.

The goal is to show that prediction-only can fail badly when predictions are
wrong, while trust-aware fallback avoids collapse by reducing trust in the
prediction.

We use adversarial predictions:
    if T < B:
        p = 5B
    if T >= B:
        p = 1

This intentionally pushes prediction-based algorithms toward the wrong action.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt

from src.ski_rental.trust_aware import trust_aware_comparison_table


def main() -> None:
    buy_cost = 10
    max_days = 5 * buy_cost
    lambda_value = 0.5
    confidence_values = [0.0, 0.25, 0.5, 0.75, 1.0]

    project_root = Path(__file__).resolve().parents[1]
    figures_dir = project_root / "figures"
    results_dir = project_root / "experiments" / "results"

    figures_dir.mkdir(exist_ok=True)
    results_dir.mkdir(exist_ok=True)

    rows = trust_aware_comparison_table(
        max_days=max_days,
        buy_cost=buy_cost,
        lambda_value=lambda_value,
        confidence_values=confidence_values,
    )

    csv_path = results_dir / "day6_trust_aware.csv"
    figure_path = figures_dir / "day6_trust_aware_fallback.png"

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "algorithm",
                "T",
                "B",
                "p",
                "lambda",
                "confidence",
                "buy_day",
                "OPT",
                "ALG",
                "cost_ratio",
                "prediction_error",
                "relative_prediction_error",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    plt.figure(figsize=(10, 6))

    algorithms_to_plot = [
        "prediction_only",
        "learning_augmented",
        "trust_aware_c=0.0",
        "trust_aware_c=0.5",
        "trust_aware_c=1.0",
    ]

    for algorithm in algorithms_to_plot:
        selected_rows = [row for row in rows if row["algorithm"] == algorithm]
        true_days = [row["T"] for row in selected_rows]
        ratios = [row["cost_ratio"] for row in selected_rows]

        plt.plot(
            true_days,
            ratios,
            marker="o",
            linewidth=2,
            label=algorithm,
        )

    plt.axhline(y=1.0, linestyle="--", linewidth=1, label="offline optimum ratio")
    plt.axhline(y=2.0, linestyle="--", linewidth=1, label="2-competitive reference")

    plt.xlabel("True number of skiing days T")
    plt.ylabel("Cost ratio ALG / OPT")
    plt.title("Trust-Aware Fallback under Adversarial Predictions")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(figure_path, dpi=200)
    plt.close()

    print("Day 6 trust-aware experiment completed.")
    print(f"Saved CSV: {csv_path}")
    print(f"Saved figure: {figure_path}")


if __name__ == "__main__":
    main()