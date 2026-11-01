import pytest

from salon_booking import arrival_status, can_book, extra_time_charge


@pytest.mark.parametrize(
    "service,duration,level,member,expected",
    [
        ("haircut", 20, "junior", False, 0),
        ("haircut", 30, "junior", False, 0),
        ("haircut", 40, "junior", False, 100),
        ("haircut", 50, "senior", True, 90),
        ("colour", 80, "junior", True, 50),
        ("spa", 100, "senior", True, 180),
        ("haircut", 100, "senior", False, 2100),
    ],
)
def test_extra_time_charge_values(service, duration, level, member, expected):
    assert extra_time_charge(service, duration, level, member) == expected


def test_unknown_service():
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("nails", 30, "junior", False)


def test_negative_duration():
    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("haircut", -1, "junior", False)


@pytest.mark.parametrize(
    "party_size,services,walk_in,expected",
    [
        (1, 1, True, True),
        (2, 1, True, True),
        (3, 1, True, False),
        (4, 2, False, True),
        (5, 1, False, False),
        (2, 3, False, False),
    ],
)
def test_booking_choices(party_size, services, walk_in, expected):
    assert can_book(party_size, services, walk_in) is expected


@pytest.mark.parametrize(
    "minutes,is_colour,weekend,expected",
    [
        (10, True, False, "open"),
        (5, False, False, "open"),
        (0, False, False, "late"),
        (-11, False, False, "closed"),
        (20, True, True, "open"),
        (5, True, True, "late"),
        (-6, True, True, "closed"),
    ],
)
def test_arrival_status(minutes, is_colour, weekend, expected):
    assert arrival_status(minutes, is_colour, weekend) == expected
