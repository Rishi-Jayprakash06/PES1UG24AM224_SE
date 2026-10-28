# Reflection — Lab 5: Static Code Analysis

The provided handout lists the learning outcomes and asks students to reflect on the experience, but it does not include four exact reflection questions. The answers below are organised around the handout's stated learning outcomes. If your instructor provided separate questions, map or replace these answers accordingly.

## 1. What is static code analysis, and why is it useful?

Static analysis examines source code without executing the program. It helps identify potential bugs, security weaknesses, unused code, and style violations early in development. This reduces the chance of preventable problems reaching users and helps keep the code maintainable.

## 2. How do Pylint, Bandit, and Flake8 differ?

Pylint checks code quality, likely errors, naming, unused code, and maintainability. Bandit scans Python code for patterns commonly associated with security vulnerabilities. Flake8 checks style and lint rules, including whitespace and line-length issues. Their scopes overlap slightly, but together they provide complementary feedback.

## 3. Which issues were most important in this program, and how were they addressed?

The highest-risk source patterns included dynamic `eval`, a hard-coded token, an unnecessary shell invocation, MD5 hashing, and use of the non-cryptographic `random` module for a PIN. The revised code avoids evaluating an arbitrary expression, does not embed or print a secret, avoids the shell, uses SHA-256 for the identifier digest, and uses `secrets` for the PIN. Maintainability issues such as a mutable default list, a bare exception handler, unused code, and execution on import were also corrected.

## 4. What was learned, and what still needs verification?

Code can appear to work while still containing security and maintenance risks. Static-analysis tools help locate suspicious patterns, but their findings need context and human review. I should also test boundary cases, including an unknown student ID, negative marks, attendance above 100, an invalid GPA divisor, and file-write failures. The final Pylint score and Bandit/Flake8 findings must be taken from the saved reports rather than assumed in advance.
