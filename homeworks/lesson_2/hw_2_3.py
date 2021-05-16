"""
3. Реализовать класс матрицы произвольного типа. При создании экземпляра передаётся вложенный список. Для объектов
класса реализовать метод сложения и вычитания матриц, а также умножения, деления матрицы на число и user-friendly вывода
матрицы на экран.
"""


class Matrix:
    def __init__(self, matrix_data):
        self.matrix_data = matrix_data

    def __add__(self, other):
        total_res = []
        for i in range(len(self.matrix_data)):
            str_res = []
            for j in range(len(self.matrix_data[0])):
                str_res.append(self.matrix_data[i][j] + other.matrix_data[i][j])
            total_res.append(str_res)
        return Matrix(total_res)

    def __sub__(self, other):
        total_res = []
        for i in range(len(self.matrix_data)):
            str_res = []
            for j in range(len(self.matrix_data[0])):
                str_res.append(self.matrix_data[i][j] - other.matrix_data[i][j])
            total_res.append(str_res)
        return Matrix(total_res)

    def __mul__(self, num):
        total_res = []
        for i in range(len(self.matrix_data)):
            str_res = []
            for j in range(len(self.matrix_data[0])):
                str_res.append(self.matrix_data[i][j] * num)
            total_res.append(str_res)
        return Matrix(total_res)

    def __truediv__(self, num):
        total_res = []
        for i in range(len(self.matrix_data)):
            str_res = []
            for j in range(len(self.matrix_data[0])):
                str_res.append(self.matrix_data[i][j] / num)
            total_res.append(str_res)
        return Matrix(total_res)

    def __eq__(self, other):
        return self.matrix_data == other.matrix_data

    def __str__(self):
        res_str = ""
        for el in self.matrix_data:
            res_str += f"{el}\n"
        return res_str

    def __repr__(self):
        res_str = ""
        for el in self.matrix_data:
            res_str += f"{el}\n"
        return res_str
