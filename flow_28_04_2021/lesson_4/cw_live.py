# f_o_lst = [open("testfile.txt", "r") for _ in range(100_000)]  # OSError: Too many open files: 'testfile.txt'
# f_o = open("testfile.txt", "r")
# print("Какая-то логика")

# try:
#     f_o = open("testfile.txt", "w")
# except Exception as err:
#     print(err)
# finally:
#     f_o.close()

# f_o = open("testfile.txt", "w")

# with open("testfile.txt", "w") as f_o:
#     print("Что-то делаю")
#     f_o.write("Что-то записываю")
# print("Закончили выполнение")


# class MyClassForContextMan:
#     def __enter__(self):
#         print(f"Вызывается метод __enter__ у экземпляра {self}")
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print(f"Вызывается метод __exit__ у экземпляра {self}")
#         if exc_val:
#             print(f"И кстати тут произошла вот такая ошибка с вот такой информацией о ней: "
#                   f"{exc_type}, {exc_val}, {exc_tb}")


# ex_for_context = MyClassForContextMan()

# # штатная работа:
# with ex_for_context:
#     print(f"Выполнение контекста для {ex_for_context}")
#     raise ValueError("Всё очень плохо")
# print("something")

# import sys
# from time import time
#
# start = time()
# num = 0
# res_list = []
# while num < 100_000_000:
#     res_list.append(num)
#     num += 1
#
# print(time() - start)
# print(sys.getsizeof(res_list))

# ФУНКЦИЯ С yield - ЭТО ГЕНЕРАТОРНАЯ ФУНКЦИЯ!!
# ОБЪЕКТ-ГЕНЕРАТОР - ЭТО РЕЗУЛЬТАТ РАБОТЫ ГЕНЕРАТОРНОЙ-ФУНКЦИИ!!!
# def oboyma_point():
    # print('a')
    # yield 1
    # print('b')
    # yield 2
    # print('c')
    # yield 3
    # print('d')
    # yield 4
    # print('e')


# oboyma = oboyma_point()
# print('x')
# print(next(oboyma))
# print('x')
# print(next(oboyma))
# print('x')
# print(next(oboyma))
# print('x')
# print(next(oboyma))
# print('x')
# print(next(oboyma))
# print('x')

# for bullet in oboyma:
#     print(bullet)


import sys
from time import time

# start = time()
# num = 0


# def get_func(cnt):
#     """Результатом этой функции будет ОБЪЕКТ-ГЕНЕРАТОР! Такая функция сохраняет состояние!"""
#     num = 0
#     while num < cnt:
#         yield num  # логика выполняется от yield до yield! yield возвращает значение!
#         num += 1
#
#
# def consumer_1(g_o):
#     val = 3
#     cnt = 0
#     received_resources = []
#     while cnt <= val:
#         received_resources.append(next(g_o))
#         cnt += 1
#     print(received_resources)
#
#
# def consumer_2(g_o):
#     val = 5
#     cnt = 0
#     received_resources = []
#     while cnt <= val:
#         received_resources.append(next(g_o))
#         cnt += 1
#     print(received_resources)
#
#
# def consumer_3(g_o):
#     val = 5
#     cnt = 0
#     received_resources = []
#     while cnt <= val:
#         try:
#             received_resources.append(next(g_o))
#         except:
#             print(received_resources)
#             break
#         cnt += 1
#     print(received_resources)
#
# g_o = get_func(10)
# consumer_1(g_o)
# consumer_2(g_o)
# consumer_3(g_o)

# g_o = get_func(10)
# print(3 in g_o)
# print(next(g_o))
# print(3 in g_o)
# print(3 in g_o)
# print(time() - start)
# print(sys.getsizeof(g_o))


# lst = [1, 2, 3, 4, 5, 6, 7]

# for el in lst:
#     print(el)

# ШАГ 1: получить объект-итератор от перебираемого объекта:
# it = iter(lst)
# print(it)
# try:
#     while True:
#         # ШАГ 2: вызывать функцию next от нашего объекта-итератора до тех пор, пока не закипит (StopIteration error)
#         print(next(it))
# except StopIteration:
#     pass


# class MyCollection:
#     def __init__(self, end_val, start_val=0):
#         self.start_val = start_val
#         self.end_val = end_val
#         self.__current = start_val
#
#     def __iter__(self):
#         """Тут надо вернуть как раз какой-то итератор! Объект-генератор - это подвид итератора!"""
#         while self.__current <= self.end_val:
#             yield self.__current
#             self.__current += 1


# ещё более экзотичная ситуация, когда нужно написать свой кастомный итератор!
# class MyIterator:
#     def __init__(self, end_val, start_val=0):
#         self.start_val = start_val
#         self.end_val = end_val
#         self.current = start_val
#
#     def __next__(self):
#         if self.current < self.end_val:
#             self.current += 1
#             return self.current
#         raise StopIteration
#
#     def to_start(self):
#         self.current = 0
#
#     def to_some_value(self, value):
#         if value < self.end_val:
#             self.current = value
#         else:
#             raise ValueError("Bad value")
#
#     def __iter__(self):
#         """Итератор сам для себя является итератором"""
#         return self


# class MyCollectionV2:
#     def __init__(self, end_val, start_val=0):
#         self.start_val = start_val
#         self.end_val = end_val
#
#     def __iter__(self):
#         """Теперь возвращаем объект нашего кастомного итератора!"""
#         return MyIterator(end_val=self.end_val, start_val=self.start_val)


# coll = MyCollectionV2(start_val=0, end_val=3)
# for el in coll:
#     print(el)

# it = iter(coll)
# print(next(it))
# print(next(it))
# print(next(it))
# it.to_start()
# print(next(it))
# print(next(it))
# print(next(it))
# it.to_some_value(-100)
# print(next(it))
# print(next(it))
# print(next(it))

from abc import ABC, abstractmethod
from os import system


# class BaseClient(ABC):
#     """Базовый клиент с методами, которые должны иметь ВСЕ клиенты-наследники"""
#
#     @abstractmethod
#     def ping(self):
#         """Каждый клиент должен иметь возможность пинговать свой ресурс"""
#         pass
#
#     @abstractmethod
#     def _get(self):
#         pass
#
#     @abstractmethod
#     def _post(self):
#         pass


# теперь представим, что у нас есть несколько сервисов, которые находятся на разных адресах
# class GoogleClient(BaseClient):
#     def __init__(self):
#         self.url = "google.com"
#
#     def ping(self):
#         print(system(f"ping -i 1 -c 1 {self.url}"))
#
#     def _get(self):
#         pass
#
#     def _post(self):
#         pass


# class YouTubeClient(BaseClient):
#     def __init__(self):
#         self.url = "youtube.com"
#
#     def ping(self):
#         print(system(f"ping -i 1 -c 1 {self.url}"))
#
#     def _get(self):
#         pass
#
#     def _post(self):
#         pass


# yt_cli = YouTubeClient()
# goocle_cli = GoogleClient()
# yt_cli.ping()
# goocle_cli.ping()
