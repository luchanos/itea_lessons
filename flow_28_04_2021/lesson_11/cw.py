# вот если напишем просто так, то отвалимся с ошибкой
# from .some_directory.some_file_1 import my_shiny_func

# my_shiny_func()

# какие у нас есть варианты?
# 1. добавить наш модуль в саму папку со всеми остальными модулями (это лютый костыль-костылищще)
# 2. поиграться с sys (тоже костыль, но для разработки сгодится)
# 3. создать пакет (благородные Доны делают так)
# 4. накатить как отдельную библиотеку (... или даже так)

import sys
import os

# Метод path из модуля sys возвращает все пути для поиска модулей Python.
# print(sys.path)
# sys.path.append('/Users/nnsviridov/AcademicProjects/itea_lessons/flow_28_04_2021/lesson_11/some_directory')

# пайчарм это подсветит, но работать всё равно будет
# from some_file_1 import my_shiny_func
# my_shiny_func()

# или можно получить его как base_dir
# basedir = os.path.abspath(os.path.dirname(__file__))
# print(basedir)
# sys.path.append(basedir + "/some_directory")
# опять подсветит, но опять будет работать
# from some_file_1 import my_shiny_func
# my_shiny_func()

# чтобы превратить директорию в пакет, нужно просто создать там файл __init__
# если поставить working directory у питона на some_directory,
# from some_directory.some_file_1 import my_shiny_func
# from some_directory.some_file_1 import my_shiny_func
# from ..lesson_4.cw_live import *  # две точки - на две директории выше
# my_shiny_func()
