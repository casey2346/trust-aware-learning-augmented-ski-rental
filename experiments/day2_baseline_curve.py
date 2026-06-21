"""
Day 2 experiment: plot the competitive ratio curve for the classical
deterministic ski rental baseline.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt

from src.ski_rental.baselines import deterministic_table


def main() -> None:
    buy_cost = 10
    max_days = 5 * buy_cost

    project_root = Path(__file__).resolve().parents[1]
    figures_dir = project_root / "figures"
    results_dir = project_root / "experiments" / "results"

    figures_dir.mkdir(exist_ok=True)
    results_dir.mkdir(exist_ok=True)

    rows = deterministic_table(max_days=max_days, buy_cost=buy_cost)

    csv_path = results_dir / "day2_deterministic_baseline.csv"
    figure_path = figures_dir / "day2_deterministic_competitive_ratio.png"

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["T", "B", "OPT", "ALG_det", "competitive_ratio"],
        )
        writer.writeheader()
        writer.writerows(rows)

    true_days = [row["T"] for row in rows]
    ratios = [row["competitive_ratio"] for row in rows]

    plt.figure(figsize=(8, 5))
    plt.plot(true_days, ratios, marker="o", linewidth=2)
    plt.axhline(y=2.0, linestyle="--", linewidth=1)
    plt.xlabel("True number of skiing days T")
    plt.ylabel("Competitive ratio ALG / OPT")
    plt.title("Classical Deterministic Ski Rental Baseline")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(figure_path, dpi=200)
    plt.close()

    print("Day 2 baseline experiment completed.")
    print(f"Saved CSV: {csv_path}")
    print(f"Saved figure: {figure_path}")


if __name__ == "__main__":
    main()