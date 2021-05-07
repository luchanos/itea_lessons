from flow_28_04_2021.lesson_3 import divisor
import pytest


@pytest.mark.parametrize("a, b, expected_result", [
    (1, 2, 0.5),
    (100, 50, 2),
],)
def test_divisor(a, b, expected_result):
    res = divisor(a, b)
    assert res == expected_result


def test_divisor_with_error():
    with pytest.raises(ZeroDivisionError):
        divisor(1, 0)
