"""
Day 8 experiment: adversarial prediction test.

This experiment evaluates algorithms under adversarial predictions.

Adversarial rule:
    if T < B:
        p = 5B
    if T >= B:
        p = 1

This intentionally pushes prediction-based algorithms toward the wrong decision.
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


def adversarial_prediction(true_days: int, buy_cost: int) -> int:
    """
    Generate adversarially wrong prediction.

    If T < B:
        p = 5B
    If T >= B:
        p = 1
    """
    if true_days < buy_cost:
        return 5 * buy_cost

    return 1


def safe_ratio(cost: int, opt: int) -> float:
    """
    Compute cost / OPT safely.
    """
    if opt == 0:
        return 1.0
    return cost / opt


def run_adversarial_test() -> list[dict[str, float | int | str]]:
    """
    Run adversarial prediction experiment.

    Returns:
        List of result rows.
    """
    buy_cost_values = [10, 20, 50]
    lambda_value = 0.5
    confidence_values = [0.0, 0.25, 0.5, 0.75, 1.0]

    rows: list[dict[str, float | int | str]] = []

    for buy_cost in buy_cost_values:
        max_days = 5 * buy_cost

        for true_days in range(1, max_days + 1):
            predicted_days = adversarial_prediction(
                true_days=true_days,
                buy_cost=buy_cost,
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

            rows.append(
                {
                    "experiment": "adversarial_test",
                    "algorithm": "offline_optimum",
                    "B": buy_cost,
                    "T": true_days,
                    "p": predicted_days,
                    "lambda": "",
                    "confidence": "",
                    "OPT": opt,
                    "ALG": opt,
                    "cost_ratio": 1.0,
                    "prediction_error": prediction_error(true_days, predicted_days),
                    "relative_prediction_error": relative_prediction_error(
                        true_days, predicted_days
                    ),
                }
            )

            rows.append(
                {
                    "experiment": "adversarial_test",
                    "algorithm": "deterministic",
                    "B": buy_cost,
                    "T": true_days,
                    "p": predicted_days,
                    "lambda": "",
                    "confidence": "",
                    "OPT": opt,
                    "ALG": deterministic_cost,
                    "cost_ratio": safe_ratio(deterministic_cost, opt),
                    "prediction_error": prediction_error(true_days, predicted_days),
                    "relative_prediction_error": relative_prediction_error(
                        true_days, predicted_days
                    ),
                }
            )

            rows.append(
                {
                    "experiment": "adversarial_test",
                    "algorithm": "prediction_only",
                    "B": buy_cost,
                    "T": true_days,
                    "p": predicted_days,
                    "lambda": "",
                    "confidence": "",
                    "OPT": opt,
                    "ALG": prediction_only_cost,
                    "cost_ratio": safe_ratio(prediction_only_cost, opt),
                    "prediction_error": prediction_error(true_days, predicted_days),
                    "relative_prediction_error": relative_prediction_error(
                        true_days, predicted_days
                    ),
                }
            )

            rows.append(
                {
                    "experiment": "adversarial_test",
                    "algorithm": "learning_augmented",
                    "B": buy_cost,
                    "T": true_days,
                    "p": predicted_days,
                    "lambda": lambda_value,
                    "confidence": 1.0,
                    "OPT": opt,
                    "ALG": learning_augmented_cost,
                    "cost_ratio": safe_ratio(learning_augmented_cost, opt),
                    "prediction_error": prediction_error(true_days, predicted_days),
                    "relative_prediction_error": relative_prediction_error(
                        true_days, predicted_days
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
                        "experiment": "adversarial_test",
                        "algorithm": f"trust_aware_c={confidence}",
                        "B": buy_cost,
                        "T": true_days,
                        "p": predicted_days,
                        "lambda": lambda_value,
                        "confidence": confidence,
                        "OPT": opt,
                        "ALG": trust_aware_cost,
                        "cost_ratio": safe_ratio(trust_aware_cost, opt),
                        "prediction_error": prediction_error(true_days, predicted_days),
                        "relative_prediction_error": relative_prediction_error(
                            true_days, predicted_days
                        ),
                    }
                )

    return rows


def save_csv(rows: list[dict[str, float | int | str]], csv_path: Path) -> None:
    """
    Save adversarial test results.
    """
    csv_path.parent.mkdir(exist_ok=True)

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "experiment",
                "algorithm",
                "B",
                "T",
                "p",
                "lambda",
                "confidence",
                "OPT",
                "ALG",
                "cost_ratio",
                "prediction_error",
                "relative_prediction_error",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def plot_adversarial_test(
    rows: list[dict[str, float | int | str]],
    figure_path: Path,
) -> None:
    """
    Plot adversarial test cost ratios for B = 10.
    """
    figure_path.parent.mkdir(exist_ok=True)

    algorithms_to_plot = [
        "prediction_only",
        "learning_augmented",
        "deterministic",
        "trust_aware_c=0.0",
        "trust_aware_c=0.5",
        "trust_aware_c=1.0",
    ]

    selected_rows = [row for row in rows if row["B"] == 10]

    plt.figure(figsize=(10, 6))

    for algorithm in algorithms_to_plot:
        matching_rows = [row for row in selected_rows if row["algorithm"] == algorithm]

        true_days = [row["T"] for row in matching_rows]
        ratios = [row["cost_ratio"] for row in matching_rows]

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
    plt.title("Day 8 Adversarial Prediction Test")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(figure_path, dpi=200)
    plt.close()


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]

    csv_path = project_root / "experiments" / "results" / "day8_adversarial_test.csv"
    figure_path = project_root / "figures" / "day8_adversarial_test.png"

    rows = run_adversarial_test()
    save_csv(rows, csv_path)
    plot_adversarial_test(rows, figure_path)

    print("Day 8 adversarial test completed.")
    print(f"Saved CSV: {csv_path}")
    print(f"Saved figure: {figure_path}")


if __name__ == "__main__":
    main()