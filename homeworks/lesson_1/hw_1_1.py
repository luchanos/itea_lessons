"""
1. Написать декоратор, который будет печатать на экран время работы функции.
"""
from datetime import datetime


def func_timer(func):
    def inner(*args, **kwargs):
        start = datetime.now()
        func(*args, **kwargs)
        print(datetime.now() - start)
    return inner
