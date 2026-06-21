"""
Day 8 experiment: signed prediction error sweep.

This experiment improves the original error sweep by testing both directions
of prediction error:

1. Overestimate:
    p = T * (1 + error_fraction)

2. Underestimate:
    p = T * (1 - error_fraction)

This makes the experiment more complete because prediction-only algorithms may
look strong under overestimation but can fail under underestimation.

Algorithms compared:
1. offline optimum
2. deterministic baseline
3. prediction-only
4. learning-augmented
5. trust-aware

Experimental variables:
- B in {10, 20, 50}
- T from 1 to 5B
- prediction error from 0% to 100%
- confidence from 0 to 1
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt

from src.ski_rental.problem import offline_optimum
from src.ski_rental.baselines import deterministic_ski_rental
from src.ski_rental.prediction_only import prediction_only_ski_rental
from src.ski_rental.learning_augmented import learning_augmented_ski_rental
from src.ski_rental.trust_aware import trust_aware_ski_rental
from src.predictors.noise_models import prediction_error, relative_prediction_error


def safe_ratio(cost: int, opt: int) -> float:
    """
    Compute cost / OPT safely.
    """
    if opt == 0:
        return 1.0
    return cost / opt


def signed_prediction(true_days: int, error_fraction: float, direction: str) -> int:
    """
    Generate signed prediction error.

    Overestimate:
        p = T * (1 + error_fraction)

    Underestimate:
        p = T * (1 - error_fraction)
    """
    if true_days < 0:
        raise ValueError("true_days must be non-negative.")

    if not (0 <= error_fraction <= 1):
        raise ValueError("error_fraction must be in [0, 1].")

    if direction == "overestimate":
        return max(0, int(round(true_days * (1 + error_fraction))))

    if direction == "underestimate":
        return max(0, int(round(true_days * (1 - error_fraction))))

    raise ValueError("direction must be either 'overestimate' or 'underestimate'.")


def run_error_sweep() -> list[dict[str, float | int | str]]:
    """
    Run signed prediction error sweep experiment.

    Returns:
        List of result rows.
    """
    buy_cost_values = [10, 20, 50]
    error_fractions = [i / 10 for i in range(0, 11)]
    directions = ["overestimate", "underestimate"]
    confidence_values = [0.0, 0.25, 0.5, 0.75, 1.0]
    lambda_value = 0.5

    rows: list[dict[str, float | int | str]] = []

    for buy_cost in buy_cost_values:
        max_days = 5 * buy_cost

        for true_days in range(1, max_days + 1):
            for direction in directions:
                for error_fraction in error_fractions:
                    predicted_days = signed_prediction(
                        true_days=true_days,
                        error_fraction=error_fraction,
                        direction=direction,
                    )

                    opt = offline_optimum(true_days, buy_cost)

                    deterministic_cost = deterministic_ski_rental(
                        true_days=true_days,
                        buy_cost=buy_cost,
                    )

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

                    base_rows = [
                        ("offline_optimum", opt, "", ""),
                        ("deterministic", deterministic_cost, "", ""),
                        ("prediction_only", prediction_only_cost, "", ""),
                        ("learning_augmented", learning_augmented_cost, lambda_value, 1.0),
                    ]

                    for algorithm, cost, lam, conf in base_rows:
                        rows.append(
                            {
                                "experiment": "signed_error_sweep",
                                "direction": direction,
                                "algorithm": algorithm,
                                "B": buy_cost,
                                "T": true_days,
                                "p": predicted_days,
                                "lambda": lam,
                                "confidence": conf,
                                "error_fraction": error_fraction,
                                "OPT": opt,
                                "ALG": cost,
                                "cost_ratio": safe_ratio(cost, opt),
                                "prediction_error": prediction_error(true_days, predicted_days),
                                "relative_prediction_error": relative_prediction_error(
                                    true_days,
                                    predicted_days,
                                ),
                            }
                        )

                    for confidence in confidence_values:
                        trust_aware_cost = trust_aware_ski_rental(
                            true_days=true_days,
                            buy_cost=buy_cost,
                            predicted_days=predicted_days,
                            lambda_value=lambda_value,
                            confidence=confidence,
                        )

                        rows.append(
                            {
                                "experiment": "signed_error_sweep",
                                "direction": direction,
                                "algorithm": f"trust_aware_c={confidence}",
                                "B": buy_cost,
                                "T": true_days,
                                "p": predicted_days,
                                "lambda": lambda_value,
                                "confidence": confidence,
                                "error_fraction": error_fraction,
                                "OPT": opt,
                                "ALG": trust_aware_cost,
                                "cost_ratio": safe_ratio(trust_aware_cost, opt),
                                "prediction_error": prediction_error(true_days, predicted_days),
                                "relative_prediction_error": relative_prediction_error(
                                    true_days,
                                    predicted_days,
                                ),
                            }
                        )

    return rows


def save_csv(rows: list[dict[str, float | int | str]], csv_path: Path) -> None:
    """
    Save result rows to CSV.
    """
    csv_path.parent.mkdir(exist_ok=True)

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "experiment",
                "direction",
                "algorithm",
                "B",
                "T",
                "p",
                "lambda",
                "confidence",
                "error_fraction",
                "OPT",
                "ALG",
                "cost_ratio",
                "prediction_error",
                "relative_prediction_error",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def plot_error_sweep(
    rows: list[dict[str, float | int | str]],
    figure_path: Path,
) -> None:
    """
    Plot signed error sweep as two panels:
    overestimate and underestimate.

    The plot uses B = 10 and averages over T.
    """
    figure_path.parent.mkdir(exist_ok=True)

    algorithms_to_plot = [
        "deterministic",
        "prediction_only",
        "learning_augmented",
        "trust_aware_c=0.0",
        "trust_aware_c=0.5",
        "trust_aware_c=1.0",
    ]

    directions = [
        ("overestimate", "Overestimate Sweep"),
        ("underestimate", "Underestimate Sweep"),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for ax, (direction, title) in zip(axes, directions):
        selected_rows = [
            row
            for row in rows
            if row["B"] == 10 and row["direction"] == direction
        ]

        for algorithm in algorithms_to_plot:
            x_values = []
            y_values = []

            for error_fraction in [i / 10 for i in range(0, 11)]:
                matching_rows = [
                    row
                    for row in selected_rows
                    if row["algorithm"] == algorithm
                    and abs(float(row["error_fraction"]) - error_fraction) < 1e-9
                ]

                if not matching_rows:
                    continue

                avg_ratio = sum(float(row["cost_ratio"]) for row in matching_rows) / len(
                    matching_rows
                )

                x_values.append(error_fraction)
                y_values.append(avg_ratio)

            ax.plot(
                x_values,
                y_values,
                marker="o",
                linewidth=2,
                label=algorithm,
            )

        ax.axhline(y=1.0, linestyle="--", linewidth=1, label="offline optimum ratio")
        ax.axhline(y=2.0, linestyle="--", linewidth=1, label="2-competitive reference")
        ax.set_title(title)
        ax.set_xlabel("Prediction error fraction")
        ax.set_ylabel("Average cost ratio ALG / OPT")
        ax.grid(True, alpha=0.3)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4)
    fig.suptitle(
        "Day 8 Signed Error Sweep: Overestimate vs Underestimate",
        fontsize=14,
    )
    fig.tight_layout(rect=[0, 0.16, 1, 0.92])
    fig.savefig(figure_path, dpi=200)
    plt.close(fig)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]

    csv_path = project_root / "experiments" / "results" / "day8_error_sweep.csv"
    figure_path = project_root / "figures" / "day8_error_sweep.png"

    rows = run_error_sweep()
    save_csv(rows, csv_path)
    plot_error_sweep(rows, figure_path)

    print("Day 8 signed error sweep completed.")
    print(f"Saved CSV: {csv_path}")
    print(f"Saved figure: {figure_path}")


if __name__ == "__main__":
    main()