# Lab 5 — Static Code Analysis

This folder contains the assigned Student Grade System, the revised source, issue log, reflection, and a script to run Pylint, Bandit, and Flake8 on both versions.

## Files

- `before/student_grade_system.py` — exact original source from the assigned repo.
- `student_grade_system.py` — fixed source file.
- `issues.md` — issue table with baseline line numbers and fixes.
- `reflection.md` — reflection answers aligned to the handout's learning outcomes.
- `run_analysis.py` — creates all six reports and updates `report.md` with measured results.
- `run_analysis.ps1` — Windows helper that installs the tools and runs the analysis.
- `reports/before/` — baseline Pylint, Bandit, and Flake8 results.
- `reports/after/` — final Pylint, Bandit, and Flake8 results.
- `.github/workflows/lab5-static-analysis.yml` — runs the checks and saves the reports when changes are pushed to `main`.

## Run locally on Windows

Open PowerShell in this folder and run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\run_analysis.ps1
```

Or run the commands manually:

```powershell
py -m pip install pylint bandit flake8
py run_analysis.py
```

The report files are actual tool output. The Flake8 output file may be empty when the file has no style violations; the summary in `report.md` will state the count.

## Acceptance checks

1. Confirm the final Pylint score in `report.md` is **greater than 9.5/10**.
2. Confirm the final Bandit report has no findings (or document any justified finding).
3. Confirm the final Flake8 report has no violations.
4. Run the fixed program with `py student_grade_system.py` from this directory and check that it runs.
5. Review the issue table and reflection before submitting.

## Commits

The main fixes are organized into three commits: Pylint/code quality, Bandit/security, and Flake8 formatting plus supporting documentation and automation. The workflow may add a separate commit with the six analysis reports.
