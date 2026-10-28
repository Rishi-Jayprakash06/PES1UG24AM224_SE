# Lab 5 — Issue Log

Line numbers in this table refer to `before/student_grade_system.py`, copied from the assigned repository. Tool rule identifiers are listed where applicable; confirm exact findings and severities in the reports for each version.

| Issue | Type / tool | Baseline line(s) | Description / risk | Fix approach |
|---|---|---:|---|---|
| Dynamic `eval(gpa_expr)` | Security — Bandit may report B307 | 44 | Executes a caller-supplied Python expression and may allow arbitrary code execution. | Removed expression evaluation; GPA now uses a numeric divisor validated to be positive. |
| Hard-coded portal token, printed | Security — Bandit may report B105 | 64, 72 | Secret-like value is embedded in source and printed to output. | Removed the literal; only report whether `GRADE_PORTAL_TOKEN` is configured in the environment. |
| Shell call with filename | Security — Bandit may report B605 | 60 | Uses a shell for a simple status message and concatenates a filename into the command. | Removed shell invocation and print the export status directly. |
| MD5 digest | Security — Bandit may report B324, depending on version/context | 49 | MD5 is unsuitable for security-sensitive hashing. | Switched to SHA-256. This simple digest is not an authentication or password-storage mechanism. |
| Non-cryptographic PIN generator | Security — Bandit may report B311 | 53 | `random.randint` is not intended for security-sensitive tokens. | Use `secrets.randbelow` to generate a four-digit PIN. |
| Mutable default list | Correctness / Pylint | 15 | `grade_list=[]` reuses the same list across calls. | Default to `None` and append only if a list was explicitly supplied. |
| Bare exception handler | Correctness / Pylint | 23–27 | Silently ignores any exception, including unrelated programming errors. | Validate the student ID and attendance increment, then return a Boolean result. |
| Unused `json` import and `grace_marks` variable | Quality / Pylint | 6, 31 | Dead code makes the implementation harder to understand. | Removed unused import and variable. |
| `== None` and redundant `if/else` | Style / Pylint | 32–38 | Non-idiomatic null comparison and unnecessary branching. | Use `is None` and return the Boolean comparison directly. |
| File without safe context handling | Quality / Pylint | 57–59 | Manual file opening/closing may leave the file open if a write fails. | Use `Path.write_text(..., encoding="utf-8")`. |
| Program executes on import | Maintainability | 75 | Importing the module runs the demonstration and writes an output file. | Add an `if __name__ == "__main__":` guard. |
| CamelCase function name and old string formatting | Style / Pylint and Flake8 | 15, 19 | Naming/formatting are not idiomatic, and the formatting is less readable. | Rename to `add_grade`, use an f-string, type annotations, and standard line wrapping. |

## Verification checklist

- [ ] Review all three `reports/before/` files.
- [ ] Review all three `reports/after/` files.
- [ ] Confirm the final Pylint score is greater than 9.5.
- [ ] Confirm all Bandit findings are addressed or explicitly justified.
- [ ] Confirm Flake8 has no final violations.
- [ ] Record the measured result in `report.md`.
- [ ] Test the fixed program with valid and invalid inputs.
