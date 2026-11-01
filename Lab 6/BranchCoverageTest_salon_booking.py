import pytest

from salon_booking import arrival_status, can_book, extra_time_charge


@pytest.mark.parametrize(
    "service,duration,level,member,expected",
    [
        ("unknown", 30, "junior", False, "unknown service"),
        ("haircut", -1, "junior", False, "invalid duration"),
    ],
)
def test_invalid_charge_inputs(service, duration, level, member, expected):
    with pytest.raises(ValueError, match=expected):
        extra_time_charge(service, duration, level, member)


@pytest.mark.parametrize(
    "service,duration,level,member,expected",
    [
        ("haircut", 30, "junior", False, 0),
        ("haircut", 31, "junior", False, 10),
        ("haircut", 31, "senior", False, 18),
        ("haircut", 91, "junior", False, 1098),
        ("haircut", 91, "senior", False, 1830),
        ("haircut", 40, "junior", True, 0),
        ("spa", 91, "senior", True, 18),
    ],
)
def test_charge_decision_branches(service, duration, level, member, expected):
    assert extra_time_charge(service, duration, level, member) == expected


@pytest.mark.parametrize(
    "party_size,services,walk_in,expected",
    [
        (2, 1, True, True),
        (3, 1, True, False),
        (4, 2, False, True),
        (5, 1, False, False),
        (4, 3, False, False),
    ],
)
def test_booking_decision_branches(party_size, services, walk_in, expected):
    assert can_book(party_size, services, walk_in) is expected


@pytest.mark.parametrize(
    "minutes,is_colour,weekend,expected",
    [
        (20, True, False, "open"),
        (10, True, False, "open"),
        (0, True, False, "late"),
        (-6, True, False, "closed"),
        (15, False, True, "open"),
        (0, False, True, "late"),
        (-11, False, True, "closed"),
    ],
)
def test_arrival_decision_branches(minutes, is_colour, weekend, expected):
    assert arrival_status(minutes, is_colour, weekend) == expected
