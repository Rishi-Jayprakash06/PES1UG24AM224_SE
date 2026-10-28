# Lab 5 — Static Analysis Report

Generated: 2026-10-28 03:13:38 UTC

## Measured before/after results

| Tool | Before | After | Acceptance check |
|---|---:|---:|---|
| Pylint score | 5.71 / 10 | 10.0 / 10 | PASS |
| Bandit total findings | 6 | 0 | PASS |
| Flake8 output lines | 7 | 0 | PASS |

## Commands and raw output

The following files contain the captured output from the actual tool runs:

- `reports/before/pylint_report.txt`
- `reports/before/bandit_report.txt`
- `reports/before/flake8_report.txt`
- `reports/after/pylint_report.txt`
- `reports/after/bandit_report.txt`
- `reports/after/flake8_report.txt`

Flake8's after-report is expected to be an empty file when it finds no violations.
Review the full reports, test the program, and do not treat an unmet acceptance check as a pass.

## Process exit codes

| Tool | Before exit code | After exit code |
|---|---:|---:|
| Pylint | 28 | 0 |
| Bandit | 1 | 0 |
| Flake8 | 1 | 0 |
