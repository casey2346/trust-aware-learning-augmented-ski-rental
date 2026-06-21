"""
Day 4 experiment: generate predictions from different noise models.

This experiment evaluates prediction models for several fixed T, B instances.

The goal is to make prediction error explicit:
    η = |p - T|
    relative error = |p - T| / max(T, 1)
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt

from src.predictors.noise_models import generate_all_predictions


def main() -> None:
    buy_cost = 10
    true_days_values = [3, 8, 10, 30]
    seed = 42

    project_root = Path(__file__).resolve().parents[1]
    figures_dir = project_root / "figures"
    results_dir = project_root / "experiments" / "results"

    figures_dir.mkdir(exist_ok=True)
    results_dir.mkdir(exist_ok=True)

    all_results = []

    for true_days in true_days_values:
        results = generate_all_predictions(
            true_days=true_days,
            buy_cost=buy_cost,
            seed=seed,
        )
        all_results.extend(results)

    csv_path = results_dir / "day4_noise_models.csv"
    figure_path = figures_dir / "day4_noise_models_predictions.png"

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "model",
                "T",
                "B",
                "p",
                "prediction_error",
                "relative_prediction_error",
            ],
        )
        writer.writeheader()

        for result in all_results:
            writer.writerow(
                {
                    "model": result.model,
                    "T": result.true_days,
                    "B": result.buy_cost,
                    "p": result.predicted_days,
                    "prediction_error": result.prediction_error,
                    "relative_prediction_error": result.relative_prediction_error,
                }
            )

    labels = []
    predictions = []
    true_days_reference = []

    for result in all_results:
        labels.append(f"{result.model}\nT={result.true_days}")
        predictions.append(result.predicted_days)
        true_days_reference.append(result.true_days)

    x_values = list(range(len(labels)))

    plt.figure(figsize=(13, 6))
    plt.bar(x_values, predictions, label="predicted days p")
    plt.scatter(x_values, true_days_reference, marker="x", s=80, label="true days T")
    plt.axhline(y=buy_cost, linestyle="--", linewidth=1, label="buy cost B")
    plt.xticks(x_values, labels, rotation=60, ha="right")
    plt.ylabel("Number of skiing days")
    plt.title("Day 4 Prediction Noise Models")
    plt.grid(True, axis="y", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(figure_path, dpi=200)
    plt.close()

    print("Day 4 noise model experiment completed.")
    print(f"Saved CSV: {csv_path}")
    print(f"Saved figure: {figure_path}")


if __name__ == "__main__":
    main()