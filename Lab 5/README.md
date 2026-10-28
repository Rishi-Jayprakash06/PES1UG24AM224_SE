# Lab 5 — Static Code Analysis

Assigned source repository: https://github.com/SETAPESU26/L5_42_student_grade_system

## Deliverables

- `student_grade_system.py`: corrected source code
- `issues.md`: table of identified issues and fixes
- `reflection.md`: lab reflection answers
- `pylint_report_before.txt` and `pylint_report_after.txt`
- `bandit_report_before.txt` and `bandit_report_after.txt`
- `flake8_report_before.txt` and `flake8_report_after.txt`
- `report.md`: summary and verification results

## Generate the tool reports on Windows

Open PowerShell in this folder after adding the source and documentation files, create and activate a virtual environment, install the tools, and run them against both the original and corrected files:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pylint bandit flake8
python -m pylint before\student_grade_system.py > pylint_report_before.txt
python -m bandit -r before\student_grade_system.py > bandit_report_before.txt
python -m flake8 before\student_grade_system.py > flake8_report_before.txt
python -m pylint student_grade_system.py > pylint_report_after.txt
python -m bandit -r student_grade_system.py > bandit_report_after.txt
python -m flake8 student_grade_system.py > flake8_report_after.txt
```

Use the actual tool output in the reports. Do not manually invent scores or findings. Verify that the final Pylint score exceeds 9.5, all Bandit findings have been addressed, and Flake8 has no remaining formatting issues.

## Required commits

Create three meaningful commits corresponding to the Pylint/code-quality fixes, Bandit/security fixes, and Flake8/style fixes. The repository activity should reflect the actual changes in each commit.
