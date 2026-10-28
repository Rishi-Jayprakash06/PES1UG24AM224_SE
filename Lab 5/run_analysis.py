"""Run Pylint, Bandit, and Flake8 on original and fixed source files."""

from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REPORT_DIRS = {
    "before": ROOT / "reports" / "before",
    "after": ROOT / "reports" / "after",
}
SOURCES = {
    "before": Path("before") / "student_grade_system.py",
    "after": Path("student_grade_system.py"),
}
TOOLS = {
    "pylint": ["pylint"],
    "bandit": ["bandit", "-r"],
    "flake8": ["flake8"],
}


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    """Run a tool command and capture both output streams."""
    return subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def require_tools() -> None:
    """Stop early if a required analysis tool is unavailable."""
    missing = []
    for module in TOOLS:
        result = run_command([sys.executable, "-m", module, "--version"])
        if result.returncode != 0:
            missing.append(module)
    if missing:
        names = ", ".join(missing)
        raise SystemExit(
            f"Missing tools: {names}. Install them with: "
            "py -m pip install pylint bandit flake8"
        )


def run_analysis(stage: str, tool: str) -> tuple[str, int]:
    """Run one analyzer against one source file and save raw output."""
    source = SOURCES[stage]
    report_dir = REPORT_DIRS[stage]
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{tool}_report.txt"
    command = [sys.executable, "-m", *TOOLS[tool], str(source)]
    result = run_command(command)
    output = result.stdout
    if result.stderr:
        output += result.stderr
    report_path.write_text(output, encoding="utf-8")
    return output, result.returncode


def pylint_score(output: str) -> float | None:
    """Extract Pylint's score when the output contains one."""
    match = re.search(r"rated at ([0-9]+(?:\.[0-9]+)?)/10", output)
    return float(match.group(1)) if match else None


def bandit_issue_counts(output: str) -> dict[str, int] | None:
    """Extract Bandit's summary counts from its human-readable output."""
    match = re.search(
        r"Total issues \(by severity\):\s*"
        r"Undefined:\s*(\d+)\s*"
        r"Low:\s*(\d+)\s*"
        r"Medium:\s*(\d+)\s*"
        r"High:\s*(\d+)",
        output,
        re.DOTALL,
    )
    if not match:
        return None
    return dict(
        zip(
            ("Undefined", "Low", "Medium", "High"),
            (int(value) for value in match.groups()),
        )
    )


def finding_count(output: str) -> int:
    """Count non-empty tool output lines, useful for Flake8 findings."""
    return sum(bool(line.strip()) for line in output.splitlines())


def build_report(results: dict[str, dict[str, dict[str, Any]]]) -> str:
    """Create a short report with tool results and acceptance checks."""
    before_pylint = pylint_score(results["before"]["pylint"]["output"])
    after_pylint = pylint_score(results["after"]["pylint"]["output"])
    before_bandit = bandit_issue_counts(results["before"]["bandit"]["output"])
    after_bandit = bandit_issue_counts(results["after"]["bandit"]["output"])
    after_flake8 = finding_count(results["after"]["flake8"]["output"])

    def bandit_total(counts: dict[str, int] | None) -> int | None:
        return sum(counts.values()) if counts is not None else None

    after_bandit_total = bandit_total(after_bandit)
    pylint_ok = after_pylint is not None and after_pylint > 9.5
    bandit_ok = after_bandit_total == 0
    flake8_ok = after_flake8 == 0
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        "# Lab 5 — Static Analysis Report",
        "",
        f"Run date: {timestamp}",
        "",
        "## Measured before/after results",
        "",
        "| Tool | Before | After | Acceptance check |",
        "|---|---:|---:|---|",
        (
            "| Pylint score | "
            f"{before_pylint if before_pylint is not None else 'not parsed'} / 10 | "
            f"{after_pylint if after_pylint is not None else 'not parsed'} / 10 | "
            f"{'PASS' if pylint_ok else 'CHECK: target > 9.5'} |"
        ),
        (
            "| Bandit total findings | "
            f"{bandit_total(before_bandit) if before_bandit is not None else 'see report'} | "
            f"{after_bandit_total if after_bandit_total is not None else 'see report'} | "
            f"{'PASS' if bandit_ok else 'CHECK report'} |"
        ),
        (
            "| Flake8 output lines | "
            f"{finding_count(results['before']['flake8']['output'])} | "
            f"{after_flake8} | "
            f"{'PASS' if flake8_ok else 'CHECK report'} |"
        ),
        "",
        "## Commands and raw output",
        "",
        "The following files contain the captured output from the actual tool runs:",
        "",
        "- `reports/before/pylint_report.txt`",
        "- `reports/before/bandit_report.txt`",
        "- `reports/before/flake8_report.txt`",
        "- `reports/after/pylint_report.txt`",
        "- `reports/after/bandit_report.txt`",
        "- `reports/after/flake8_report.txt`",
        "",
        "Flake8's after-report is expected to be an empty file when it finds no violations.",
        "Review the full reports, test the program, and do not treat an unmet acceptance check as a pass.",
        "",
        "## Process exit codes",
        "",
        "| Tool | Before exit code | After exit code |",
        "|---|---:|---:|",
    ]
    for tool in TOOLS:
        lines.append(
            f"| {tool.title()} | {results['before'][tool]['returncode']} | "
            f"{results['after'][tool]['returncode']} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    """Run all six analyzer invocations and update the summary report."""
    require_tools()
    results: dict[str, dict[str, dict[str, Any]]] = {
        "before": {},
        "after": {},
    }
    for stage in ("before", "after"):
        for tool in TOOLS:
            output, returncode = run_analysis(stage, tool)
            results[stage][tool] = {
                "output": output,
                "returncode": returncode,
            }
            print(f"{stage}: {tool} report saved (exit {returncode})")
    (ROOT / "report.md").write_text(build_report(results), encoding="utf-8")
    print("Updated report.md with the analysis results.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
