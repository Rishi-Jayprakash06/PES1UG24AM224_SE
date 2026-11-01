# Lab 6 - Code and Branch Coverage

This folder contains the two test suites for the Salon Booking exercise.

## Files

- `CodeCoverageTest_salon_booking.py` checks the main code paths and error cases.
- `BranchCoverageTest_salon_booking.py` checks the true and false outcomes of the decisions.
- `code_coverage_output.png` shows the line coverage run.
- `branch_coverage_output.png` shows the branch coverage run.

## Run the tests

Keep these files in the same folder as the assigned `salon_booking.py` file. Install the tools with:

```bash
python -m pip install pytest coverage
```

Run code coverage:

```bash
coverage run -m pytest -q CodeCoverageTest_salon_booking.py
coverage report -m salon_booking.py
```

Run branch coverage:

```bash
coverage erase
coverage run --branch -m pytest -q BranchCoverageTest_salon_booking.py
coverage report -m salon_booking.py
```

## Results

Both test suites passed locally against the assigned `salon_booking.py` file. The code coverage run reported 100% statement coverage. The branch coverage run reported 100% coverage, with all 26 branches covered.
