"""Manage student marks, attendance, passing status, and grade-sheet export."""

import hashlib
import os
import secrets
from pathlib import Path
from typing import Any


gradebook: dict[str, dict[str, Any]] = {
    "S01": {"name": "Alice", "marks": [85, 90, 78], "attendance": 92},
    "S02": {"name": "Bob", "marks": [60, 55, 65], "attendance": 74},
    "S03": {"name": "Charlie", "marks": [40, 42, 38], "attendance": 65},
}


def add_grade(
    student_id: str, mark: float, grade_list: list[str] | None = None
) -> bool:
    """Record a non-negative mark for a known student."""
    if student_id not in gradebook or mark < 0:
        return False
    gradebook[student_id]["marks"].append(mark)
    if grade_list is not None:
        grade_list.append(
            f"Recorded score {mark:g} for student id {student_id}"
        )
    return True


def record_attendance(student_id: str, present_days: int) -> bool:
    """Add attendance days if the student and increment are valid."""
    if student_id not in gradebook or present_days < 0:
        return False
    current = gradebook[student_id]["attendance"]
    if current + present_days > 100:
        return False
    gradebook[student_id]["attendance"] = current + present_days
    return True


def check_passing_status(
    student_id: str, pass_threshold: float = 50.0
) -> bool:
    """Return whether the student's average reaches the passing threshold."""
    student = gradebook.get(student_id)
    if student is None or not student["marks"]:
        return False
    average = sum(student["marks"]) / len(student["marks"])
    return average >= pass_threshold


def compute_weighted_gpa(student_id: str, divisor: float = 20.0) -> float:
    """Return average marks divided by a positive GPA conversion divisor."""
    if student_id not in gradebook:
        raise KeyError(f"Unknown student ID: {student_id}")
    if divisor <= 0:
        raise ValueError("divisor must be greater than zero")
    marks = gradebook[student_id]["marks"]
    if not marks:
        raise ValueError("Cannot calculate GPA without marks")
    average_score = sum(marks) / len(marks)
    return average_score / divisor


def generate_student_hash(student_id: str) -> str:
    """Return a SHA-256 digest for a student identifier."""
    return hashlib.sha256(student_id.encode("utf-8")).hexdigest()


def generate_registration_pin() -> int:
    """Generate a four-digit PIN using a cryptographically secure source."""
    return secrets.randbelow(9000) + 1000


def export_grade_sheet(filename: str = "grade_sheet.txt") -> None:
    """Export the gradebook without invoking a shell command."""
    output_path = Path(filename)
    output_path.write_text(f"{gradebook}\n", encoding="utf-8")
    print(f"Grade sheet exported to: {output_path}")


def main() -> None:
    """Run a short demonstration of the grade-management functions."""
    add_grade("S01", 95)
    record_attendance("S02", 2)
    print("Is S01 passing:", check_passing_status("S01"))
    print("Calculated GPA:", compute_weighted_gpa("S01"))
    print("Student Hash:", generate_student_hash("S01"))
    print("Registration PIN:", generate_registration_pin())
    export_grade_sheet()
    token_configured = bool(os.environ.get("GRADE_PORTAL_TOKEN"))
    print("Portal token configured:", token_configured)
    print("Passing status for S01 after adding the demonstration mark:", check_passing_status("S01"))


if __name__ == "__main__":
    main()
