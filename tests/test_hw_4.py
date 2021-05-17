import pytest
from homeworks.lesson_4.hw_4_1 import fact_gen


@pytest.mark.parametrize("value, expected", [
    (0, [1]),
    (1, [1]),
    (2, [1, 2]),
    (3, [1, 2, 6]),
    (4, [1, 2, 6, 24]),
    (5, [1, 2, 6, 24, 120])
])
def test_factorial(value, expected):
    fact_gen_obj = fact_gen(value)
    for num in range(len(expected)):
        assert next(fact_gen_obj) == expected[num]
    with pytest.raises(StopIteration):
        next(fact_gen_obj)
