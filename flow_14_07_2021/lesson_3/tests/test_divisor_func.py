from flow_14_07_2021.lesson_3.my_functions import divisor

import pytest


@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5.0),
    (5, 3, 1.6666666666666667),
    (50, 30, 1.6666666666666667),
    (15, 31, 0.4838709677419355)
])
def test_divisor(a, b, expected):
    assert divisor(a, b) == expected


# @pytest.mark.skip
@pytest.mark.parametrize("a, b, expected_exception_type", [
    ("param_1", "param_2", TypeError),
    (1, 0, ZeroDivisionError),
    ("param_1", 1, TypeError),
    (1, "param_1", TypeError)
])
def test_divisor_error(a, b, expected_exception_type):
    with pytest.raises(expected_exception_type):
        divisor(a, b)
