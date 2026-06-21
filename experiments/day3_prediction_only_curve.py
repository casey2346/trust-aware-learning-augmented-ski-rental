"""
Day 3 experiment: evaluate prediction-only ski rental.

This experiment compares prediction-only performance under three scenarios:

1. exact prediction:
   p = T

2. overestimate:
   p = 5B

3. underestimate:
   p = 1

The goal is to show that prediction-only algorithms can perform very well when
predictions are accurate, but can degrade badly when predictions are wrong.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt

from src.ski_rental.prediction_only import prediction_only_table


def main() -> None:
    buy_cost = 10
    max_days = 5 * buy_cost

    project_root = Path(__file__).resolve().parents[1]
    figures_dir = project_root / "figures"
    results_dir = project_root / "experiments" / "results"

    figures_dir.mkdir(exist_ok=True)
    results_dir.mkdir(exist_ok=True)

    modes = ["exact", "overestimate", "underestimate"]

    all_rows = []
    rows_by_mode = {}

    for mode in modes:
        rows = prediction_only_table(
            max_days=max_days,
            buy_cost=buy_cost,
            prediction_mode=mode,
        )
        rows_by_mode[mode] = rows
        all_rows.extend(rows)

    csv_path = results_dir / "day3_prediction_only.csv"
    figure_path = figures_dir / "day3_prediction_only_cost_ratio.png"

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "mode",
                "T",
                "B",
                "p",
                "OPT",
                "ALG_pred_only",
                "cost_ratio",
                "prediction_error",
                "relative_prediction_error",
                "decision",
            ],
        )
        writer.writeheader()
        writer.writerows(all_rows)

    plt.figure(figsize=(9, 5.5))

    for mode in modes:
        rows = rows_by_mode[mode]
        true_days = [row["T"] for row in rows]
        ratios = [row["cost_ratio"] for row in rows]
        plt.plot(true_days, ratios, marker="o", linewidth=2, label=mode)

    plt.axhline(y=1.0, linestyle="--", linewidth=1, label="offline optimum ratio")
    plt.axhline(y=2.0, linestyle="--", linewidth=1, label="2-competitive reference")

    plt.xlabel("True number of skiing days T")
    plt.ylabel("Cost ratio ALG / OPT")
    plt.title("Prediction-Only Ski Rental under Accurate and Wrong Predictions")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(figure_path, dpi=200)
    plt.close()

    print("Day 3 prediction-only experiment completed.")
    print(f"Saved CSV: {csv_path}")
    print(f"Saved figure: {figure_path}")


if __name__ == "__main__":
    main()