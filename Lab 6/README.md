# Lab 6 - Code and Branch Coverage

This folder contains the Salon Booking application and the two test suites.

## Files

- `salon_booking.py` contains the application code.
- `CodeCoverageTest_salon_booking.py` checks the main code paths and error cases.
- `BranchCoverageTest_salon_booking.py` checks the true and false outcomes of the decisions.
- `Lab 6 Code Coverage.png` shows the code coverage run.
- `Lab 6 Branch Coverage.png` shows the branch coverage run.

## Run the tests

Install the required tools with:

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

Both test suites passed against `salon_booking.py`. The code coverage run reported 100% statement coverage. The branch coverage run reported 100% coverage, with all 26 branches covered.
