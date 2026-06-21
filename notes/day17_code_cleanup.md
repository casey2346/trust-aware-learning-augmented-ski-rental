# Day 17 Code Cleanup and Reproducibility

## Objective

Day 17 cleans the project codebase and improves reproducibility.

The goal is to make the repository easier for another researcher, mentor, or reviewer to run and understand.

## Completed Cleanup Tasks

### 1. Requirements File

Created:

requirements.txt

The dependency file contains:

matplotlib>=3.8
numpy>=1.26
pandas>=2.2

This makes the project easier to reproduce in a fresh Python environment.

2. Clear Function Names

The main scripts use descriptive function names such as:

run_error_sweep
plot_error_sweep
run_day10_experiment
plot_adversarial_failure
save_csv
safe_ratio

These names describe what each function does and make the code easier to inspect.

3. Type Hints

Core functions use Python type hints, including:

list[dict[str, float | int | str]]
Path
int
float
str

This improves readability and makes the code easier to debug or extend.

4. Docstrings

Experiment scripts include docstrings explaining:

experiment goal
input parameters
prediction model
output files
plot interpretation

This helps readers understand the research logic without reverse-engineering the code.

5. Reproducible Scripts

The main experiments can be rerun from the project root using:

PYTHONPATH=. python3 experiments/error_sweep.py
PYTHONPATH=. python3 experiments/adversarial_test.py
PYTHONPATH=. python3 experiments/day9_make_figures.py
PYTHONPATH=. python3 experiments/day10_adversarial_prediction_failure.py
6. Random Seed

The current experiments are deterministic because they use controlled prediction rules rather than random sampling.

For future randomized experiments, a fixed seed should be used:

RANDOM_SEED = 42
Reproducibility Checklist

A fresh user should be able to run:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. python3 experiments/error_sweep.py
PYTHONPATH=. python3 experiments/adversarial_test.py
PYTHONPATH=. python3 experiments/day9_make_figures.py
PYTHONPATH=. python3 experiments/day10_adversarial_prediction_failure.py

and regenerate the main CSV files and figures.

Day 17 Output
requirements.txt
notes/day17_code_cleanup.md