"""
Run all main experiments for the trust-aware learning-augmented ski rental project.

This script is the main reproducibility entry point.

Run from the project root:

    PYTHONPATH=. python3 experiments/run_all.py
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_script(script_path: Path) -> None:
    """
    Run one experiment script from the project root.

    Args:
        script_path: Path to the experiment script.
    """
    print()
    print("=" * 80)
    print(f"Running {script_path.name}")
    print("=" * 80)

    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)

    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
        env=env,
        check=True,
    )

    print(f"Finished {script_path.name}")


def main() -> None:
    """
    Run all main reproducible experiments.
    """
    scripts = [
        PROJECT_ROOT / "experiments" / "day2_baseline_curve.py",
        PROJECT_ROOT / "experiments" / "day3_prediction_only_curve.py",
        PROJECT_ROOT / "experiments" / "day4_noise_models.py",
        PROJECT_ROOT / "experiments" / "day5_learning_augmented_curve.py",
        PROJECT_ROOT / "experiments" / "day6_trust_aware_curve.py",
        PROJECT_ROOT / "experiments" / "error_sweep.py",
        PROJECT_ROOT / "experiments" / "adversarial_test.py",
        PROJECT_ROOT / "experiments" / "day9_make_figures.py",
        PROJECT_ROOT / "experiments" / "day10_adversarial_prediction_failure.py",
    ]

    for script in scripts:
        if not script.exists():
            raise FileNotFoundError(f"Missing script: {script}")

        run_script(script)

    print()
    print("=" * 80)
    print("All main experiments completed successfully.")
    print("=" * 80)


if __name__ == "__main__":
    main()