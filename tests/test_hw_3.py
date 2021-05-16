import pytest

from homeworks.lesson_2.hw_2_3 import Matrix


@pytest.mark.parametrize(
    "first_matrix_data, second_matrix_data, expected_matrix_data", [
        (
            [[1, 1, 1],
             [1, 1, 1],
             [1, 1, 1]],

            [[1, 1, 1],
             [1, 1, 1],
             [1, 1, 1]],

            [[2, 2, 2],
             [2, 2, 2],
             [2, 2, 2]],
        ),
        (
            [[2, 2, 2],
             [-1, -1, -1],
             [12, 12, 12]],

            [[-1, 1, 1],
             [1, 0, 1],
             [1, 1, 7]],

            [[1, 3, 3],
             [0, -1, 0],
             [13, 13, 19]],
        ),
    ])
def test_matrix_add(first_matrix_data, second_matrix_data, expected_matrix_data):
    res_matrix = Matrix(first_matrix_data) + Matrix(second_matrix_data)
    assert res_matrix == Matrix(expected_matrix_data)


@pytest.mark.parametrize("matrix_data, multiplier, expected_matrix_data", [
    (
            [[1, 1, 1],
             [1, 1, 1],
             [1, 1, 1]],

            3,

            [[3, 3, 3],
             [3, 3, 3],
             [3, 3, 3]]
     ),

    (
            [[1, 1, 1],
             [1, 1, 1],
             [1, 1, 1]],

            -2,

            [[-2, -2, -2],
             [-2, -2, -2],
             [-2, -2, -2]]
    ),
                         ])
def test_matrix_div(matrix_data, multiplier, expected_matrix_data):
    res_matrix = Matrix(matrix_data) * multiplier
    assert res_matrix == Matrix(expected_matrix_data)
