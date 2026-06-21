"""
Day 10: Adversarial prediction failure experiment.

Goal:
    Show that prediction-only can fail badly under adversarial predictions,
    while trust-aware fallback avoids collapse.

Adversarial cases:
    Case 1:
        T is small, prediction says very large.
        Prediction-only buys too early.

    Case 2:
        T is large, prediction says very small.
        Prediction-only rents too long.

    Case 3:
        Prediction is systematically overestimated.

    Case 4:
        Prediction is systematically underestimated.

Required output:
    figures/adversarial_prediction_failure.png
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
    if opt == 0:
        return 1.0
    return cost / opt


def adversarial_prediction(true_days: int, buy_cost: int) -> int:
    """
    Case 1:
        If T < B, prediction says very large.

    Case 2:
        If T >= B, prediction says very small.
    """
    if true_days < buy_cost:
        return 5 * buy_cost

    return 1


def biased_overestimate_prediction(true_days: int, buy_cost: int) -> int:
    """
    Case 3:
        Systematic overestimate.
    """
    return true_days + buy_cost


def biased_underestimate_prediction(true_days: int, buy_cost: int) -> int:
    """
    Case 4:
        Systematic underestimate.
    """
    return max(0, true_days - buy_cost)


def evaluate_one_case(
    case_name: str,
    true_days: int,
    buy_cost: int,
    predicted_days: int,
    lambda_value: float,
    trust_confidence: float,
) -> list[dict[str, float | int | str]]:
    """
    Evaluate all algorithms for one adversarial or biased case.
    """
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

    trust_aware_cost = trust_aware_ski_rental(
        true_days=true_days,
        buy_cost=buy_cost,
        predicted_days=predicted_days,
        lambda_value=lambda_value,
        confidence=trust_confidence,
    )

    algorithms = [
        ("offline_optimum", opt),
        ("deterministic", deterministic_cost),
        ("prediction_only", prediction_only_cost),
        ("learning_augmented", learning_augmented_cost),
        (f"trust_aware_c={trust_confidence}", trust_aware_cost),
    ]

    rows: list[dict[str, float | int | str]] = []

    for algorithm, cost in algorithms:
        rows.append(
            {
                "case": case_name,
                "algorithm": algorithm,
                "T": true_days,
                "B": buy_cost,
                "p": predicted_days,
                "lambda": (
                    lambda_value
                    if algorithm in {"learning_augmented", f"trust_aware_c={trust_confidence}"}
                    else ""
                ),
                "confidence": (
                    trust_confidence
                    if algorithm == f"trust_aware_c={trust_confidence}"
                    else ""
                ),
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

    return rows


def run_day10_experiment() -> list[dict[str, float | int | str]]:
    """
    Run Day 10 adversarial prediction failure experiment.
    """
    buy_cost = 10
    lambda_value = 0.5
    trust_confidence = 0.0

    rows: list[dict[str, float | int | str]] = []

    # Case 1: T small, prediction very large.
    for true_days in range(1, buy_cost):
        predicted_days = adversarial_prediction(true_days, buy_cost)
        rows.extend(
            evaluate_one_case(
                case_name="small_T_large_prediction",
                true_days=true_days,
                buy_cost=buy_cost,
                predicted_days=predicted_days,
                lambda_value=lambda_value,
                trust_confidence=trust_confidence,
            )
        )

    # Case 2: T large, prediction very small.
    for true_days in range(buy_cost, 51):
        predicted_days = adversarial_prediction(true_days, buy_cost)
        rows.extend(
            evaluate_one_case(
                case_name="large_T_small_prediction",
                true_days=true_days,
                buy_cost=buy_cost,
                predicted_days=predicted_days,
                lambda_value=lambda_value,
                trust_confidence=trust_confidence,
            )
        )

    # Case 3: systematic overestimate.
    for true_days in range(1, 51):
        predicted_days = biased_overestimate_prediction(true_days, buy_cost)
        rows.extend(
            evaluate_one_case(
                case_name="biased_overestimate",
                true_days=true_days,
                buy_cost=buy_cost,
                predicted_days=predicted_days,
                lambda_value=lambda_value,
                trust_confidence=trust_confidence,
            )
        )

    # Case 4: systematic underestimate.
    for true_days in range(1, 51):
        predicted_days = biased_underestimate_prediction(true_days, buy_cost)
        rows.extend(
            evaluate_one_case(
                case_name="biased_underestimate",
                true_days=true_days,
                buy_cost=buy_cost,
                predicted_days=predicted_days,
                lambda_value=lambda_value,
                trust_confidence=trust_confidence,
            )
        )

    return rows


def save_csv(rows: list[dict[str, float | int | str]], csv_path: Path) -> None:
    csv_path.parent.mkdir(exist_ok=True)

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "case",
                "algorithm",
                "T",
                "B",
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


def plot_adversarial_failure(
    rows: list[dict[str, float | int | str]],
    figure_path: Path,
) -> None:
    """
    Plot one report-ready figure with four adversarial/bias panels.
    """
    figure_path.parent.mkdir(exist_ok=True)

    cases_to_plot = [
        ("small_T_large_prediction", "Case 1: Small T, Very Large Prediction"),
        ("large_T_small_prediction", "Case 2: Large T, Very Small Prediction"),
        ("biased_overestimate", "Case 3: Systematic Overestimate"),
        ("biased_underestimate", "Case 4: Systematic Underestimate"),
    ]

    algorithms_to_plot = [
        "prediction_only",
        "learning_augmented",
        "deterministic",
        "trust_aware_c=0.0",
    ]

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    axes = axes.flatten()

    for ax, (case_name, title) in zip(axes, cases_to_plot):
        case_rows = [row for row in rows if row["case"] == case_name]

        for algorithm in algorithms_to_plot:
            selected = [row for row in case_rows if row["algorithm"] == algorithm]
            selected.sort(key=lambda row: int(row["T"]))

            x_values = [int(row["T"]) for row in selected]
            y_values = [float(row["cost_ratio"]) for row in selected]

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
        ax.set_xlabel("True number of skiing days T")
        ax.set_ylabel("Cost ratio ALG / OPT")
        ax.grid(True, alpha=0.3)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3)
    fig.suptitle(
        "Adversarial and Biased Prediction Failures with Trust-Aware Fallback",
        fontsize=14,
    )
    fig.tight_layout(rect=[0, 0.10, 1, 0.94])
    fig.savefig(figure_path, dpi=200)
    plt.close(fig)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]

    csv_path = (
        project_root
        / "experiments"
        / "results"
        / "day10_adversarial_prediction_failure.csv"
    )

    figure_path = (
        project_root
        / "figures"
        / "adversarial_prediction_failure.png"
    )

    rows = run_day10_experiment()
    save_csv(rows, csv_path)
    plot_adversarial_failure(rows, figure_path)

    print("Day 10 adversarial prediction failure experiment completed.")
    print(f"Saved CSV: {csv_path}")
    print(f"Saved figure: {figure_path}")


if __name__ == "__main__":
    main()