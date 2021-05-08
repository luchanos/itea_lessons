from flow_28_04_2021.lesson_3 import divisor
import pytest


# декоратор принимает на вход именование аргументов для тестовой функции и их значения
@pytest.mark.parametrize("delimoe, delitel, expected", [(1, 2, .5), (100, 50, 2)])
def test_my_divisor_func(delimoe, delitel, expected):
    res = divisor(delimoe, delitel)
    assert res == expected


@pytest.mark.parametrize("exc_type, delimoe, delitel", [(ZeroDivisionError, 1, 0),
                                                        (TypeError, "1", 3)])
def test_divisor_with_error(exc_type, delimoe, delitel):
    with pytest.raises(exc_type):
        divisor(delimoe, delitel)
