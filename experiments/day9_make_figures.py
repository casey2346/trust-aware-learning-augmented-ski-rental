"""
Day 9: Generate the first set of report-ready figures.

Required figures:
1. figures/error_sweep_cost_ratio.png
2. figures/duration_sweep.png
3. figures/confidence_ablation.png

Data sources:
- experiments/results/day8_error_sweep.csv
- experiments/results/day8_adversarial_test.csv
"""

from __future__ import annotations

import csv
from pathlib import Path
import matplotlib.pyplot as plt


def load_csv(csv_path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with csv_path.open("r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def average(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def plot_error_sweep_cost_ratio(rows: list[dict[str, str]], figure_path: Path) -> None:
    """
    Figure 1:
    prediction error vs cost ratio

    Uses day8_error_sweep.csv
    Restriction:
    - B = 10
    - average over all T
    """
    figure_path.parent.mkdir(exist_ok=True)

    selected_rows = [row for row in rows if int(row["B"]) == 10]

    algorithms = [
        "deterministic",
        "prediction_only",
        "learning_augmented",
        "trust_aware_c=0.0",
        "trust_aware_c=0.5",
        "trust_aware_c=1.0",
    ]

    plt.figure(figsize=(10, 6))

    for algorithm in algorithms:
        x_values = []
        y_values = []

        for i in range(11):
            error_fraction = i / 10

            matching = [
                row for row in selected_rows
                if row["algorithm"] == algorithm
                and abs(float(row["error_fraction"]) - error_fraction) < 1e-9
            ]

            if not matching:
                continue

            avg_ratio = average([float(row["cost_ratio"]) for row in matching])

            x_values.append(error_fraction)
            y_values.append(avg_ratio)

        plt.plot(
            x_values,
            y_values,
            marker="o",
            linewidth=2,
            label=algorithm,
        )

    plt.axhline(y=1.0, linestyle="--", linewidth=1, label="offline optimum ratio")
    plt.axhline(y=2.0, linestyle="--", linewidth=1, label="2-competitive reference")

    plt.xlabel("Prediction error fraction")
    plt.ylabel("Average cost ratio ALG / OPT")
    plt.title("Prediction Error vs Cost Ratio (B = 10)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(figure_path, dpi=200)
    plt.close()


def plot_duration_sweep(rows: list[dict[str, str]], figure_path: Path) -> None:
    """
    Figure 2:
    true duration T vs cost ratio

    Uses day8_adversarial_test.csv
    Restriction:
    - B = 10
    """
    figure_path.parent.mkdir(exist_ok=True)

    selected_rows = [row for row in rows if int(row["B"]) == 10]

    algorithms = [
        "deterministic",
        "prediction_only",
        "learning_augmented",
        "trust_aware_c=0.0",
        "trust_aware_c=0.5",
        "trust_aware_c=1.0",
    ]

    plt.figure(figsize=(10, 6))

    for algorithm in algorithms:
        matching = [row for row in selected_rows if row["algorithm"] == algorithm]

        matching.sort(key=lambda row: int(row["T"]))

        x_values = [int(row["T"]) for row in matching]
        y_values = [float(row["cost_ratio"]) for row in matching]

        plt.plot(
            x_values,
            y_values,
            marker="o",
            linewidth=2,
            label=algorithm,
        )

    plt.axhline(y=1.0, linestyle="--", linewidth=1, label="offline optimum ratio")
    plt.axhline(y=2.0, linestyle="--", linewidth=1, label="2-competitive reference")

    plt.xlabel("True number of skiing days T")
    plt.ylabel("Cost ratio ALG / OPT")
    plt.title("True Duration T vs Cost Ratio under Adversarial Predictions (B = 10)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(figure_path, dpi=200)
    plt.close()


def plot_confidence_ablation(rows: list[dict[str, str]], figure_path: Path) -> None:
    """
    Figure 3:
    confidence level vs cost ratio

    Uses day8_adversarial_test.csv
    Restriction:
    - B = 10
    - average over all T
    - trust-aware algorithms only
    """
    figure_path.parent.mkdir(exist_ok=True)

    selected_rows = [row for row in rows if int(row["B"]) == 10]

    confidence_values = [0.0, 0.25, 0.5, 0.75, 1.0]

    x_values = []
    y_values = []

    for confidence in confidence_values:
        algorithm_name = f"trust_aware_c={confidence}"

        matching = [
            row for row in selected_rows
            if row["algorithm"] == algorithm_name
        ]

        avg_ratio = average([float(row["cost_ratio"]) for row in matching])

        x_values.append(confidence)
        y_values.append(avg_ratio)

    deterministic_rows = [row for row in selected_rows if row["algorithm"] == "deterministic"]
    learning_augmented_rows = [row for row in selected_rows if row["algorithm"] == "learning_augmented"]

    deterministic_avg = average([float(row["cost_ratio"]) for row in deterministic_rows])
    learning_augmented_avg = average([float(row["cost_ratio"]) for row in learning_augmented_rows])

    plt.figure(figsize=(10, 6))

    plt.plot(
        x_values,
        y_values,
        marker="o",
        linewidth=2,
        label="trust-aware average cost ratio",
    )

    plt.axhline(y=deterministic_avg, linestyle="--", linewidth=1, label="deterministic average")
    plt.axhline(y=learning_augmented_avg, linestyle="--", linewidth=1, label="learning-augmented average")
    plt.axhline(y=1.0, linestyle="--", linewidth=1, label="offline optimum ratio")

    plt.xlabel("Confidence level c")
    plt.ylabel("Average cost ratio ALG / OPT")
    plt.title("Confidence Level vs Cost Ratio under Adversarial Predictions (B = 10)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(figure_path, dpi=200)
    plt.close()


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]

    error_sweep_csv = project_root / "experiments" / "results" / "day8_error_sweep.csv"
    adversarial_csv = project_root / "experiments" / "results" / "day8_adversarial_test.csv"

    figures_dir = project_root / "figures"
    figures_dir.mkdir(exist_ok=True)

    error_rows = load_csv(error_sweep_csv)
    adversarial_rows = load_csv(adversarial_csv)

    plot_error_sweep_cost_ratio(
        error_rows,
        figures_dir / "error_sweep_cost_ratio.png",
    )

    plot_duration_sweep(
        adversarial_rows,
        figures_dir / "duration_sweep.png",
    )

    plot_confidence_ablation(
        adversarial_rows,
        figures_dir / "confidence_ablation.png",
    )

    print("Day 9 figures generated successfully.")
    print(f"Saved: {figures_dir / 'error_sweep_cost_ratio.png'}")
    print(f"Saved: {figures_dir / 'duration_sweep.png'}")
    print(f"Saved: {figures_dir / 'confidence_ablation.png'}")


if __name__ == "__main__":
    main()