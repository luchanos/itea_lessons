"""
Сделать шаблоны для отображения сотрудников, заявок и департаментов и прикрутить их к соответствующим flask-методам.
Используйте 1 базовый шаблон, от которого унаследуйте все остальные. Что хотелось бы видеть:
 - навигационную панель (можно взять из классной работы или написать свою собственную)
 - удобный вывод информации (ограничение по количеству записей, выводимых на экран и использование
 списка с точками или цифрами при выводе)
"""

from time import sleep

# Пул потоков
from concurrent.futures import ThreadPoolExecutor, as_completed
from random import randrange

b = 0


# def f(a):
#     global b
#     print("This is %d" % b)
#     b += 1
#     # sleep_time = randrange(0, 10)
#     # time.sleep(sleep_time)
#     sleep_time = 1
#     sleep(sleep_time)
#     buf = b
#     return f"result {a * a} for thread {buf} which slept {sleep_time}"
#
#
# with ThreadPoolExecutor(max_workers=1) as pool:  # тут всё само сделается!
#     results = [pool.submit(f, i) for i in range(10)]  # submit - создает футуру, это объект, который обещает исполнится
#
#     for future in as_completed(results):
#         print(future.result())


# Синхронизация потоков
# Этот механизм позволяет потокам обмениваться данными между собой

# Очередь
# from queue import Queue
# from threading import Thread
#
#
# def worker(q, n):
#     while True:
#         item = q.get()
#         if item is None:
#             break  # завершаем выполнение
#         print("process data:", n, item)
#
#
# q = Queue(5)  # эта очередь будет одной сразу на 2 потока!
# th1 = Thread(target=worker, args=(q, 1))
# th2 = Thread(target=worker, args=(q, 2))
# th1.start()
# th2.start()
#
# for i in range(50):
#     q.put(i)
#
# q.put(None)
# q.put(None)
# th1.join()
# th2.join()

# с точки зрения процесса ресурсами владеет именно процесс. Но процесс не знает, что творится в потоках.
# Если поток завершить аварийно, то могут случиться неприятности (незакрытые файлы и тд).
# Поэтому в питоне нет функции аварийного завершения потока.

# Блокировки.
import threading


class Point:
    def __init__(self):
        self._mutex = threading.RLock()  # запрашиваем блокировку | палка, которой поток, работающий с конкретным
        # экземпляром точки этого класса будет отгонять другие потоки от неё до тех пор, пока сам не завершит
        # с ней работу.
        self._x = 0
        self._y = 0

    def get(self):
        with self._mutex:
            return self._x, self._y

    def set(self, x, y):
        with self._mutex:
            self._x = x
            self._y = y

# Предположим, что используем наш класс в большом количестве потоков
# Может произойти неконсистентное состояние объекта. Также это "гонка за ресурсами"

# Другой способ
# import threading

# a = threading.RLock()
# b = threading.RLock()


# def foo():
#     try:
#         a.acquire()  # запрашиваем блокировку
#         print("kek")
#         b.acquire()
#     finally:
#         a.release()  # освобождаем
#         b.release()


# если мы запустим код выше в большом количестве процессов,
# то рано или поздно это приведет к ситуации, когда произойдёт взаимная блокировка (deadlock). Чтобы избежать этого
# нужно освобождать блокировки в правильной последовательности. Контекстный менеджер - это выход!

# GIL
# Глобальная блокировка интерпретатора
# Не позволяет двум потокам выполняться одновременно. Защищает память от "разрушения".
# from threading import Thread
# import time
#
#
# def count(n):
#     while n > 0:
#         n -= 1
#
# t0 = time.time()
# count(10_000_000)
# count(10_000_000)
# print("Последовательное", time.time() - t0)

# параллельное выполнение
# t0 = time.time()
# th1 = Thread(target=count, args=(10_000_000, ))
# th2 = Thread(target=count, args=(10_000_000, ))
#
# th1.start()
# th2.start()
# th1.join()
# th2.join()
#
# print("Параллельное", time.time() - t0)

# В этом случае код, который написан с использованием потоков будет неэффективным,
# так как имеем дело с CPU-bound задачами


# если заменить CPU-задачу на I/O то будет заметен огромный прирост!

# Сопрограммы
# наша цель - фильтровать входной поток данных при помощи функции grep и дальше мы прокидываем паттерн и выводим только
# те, в которых присутствует слово python

# Асинхронность - когда задачи запускаются и завершаются независимо друг от друга

# def give_me_value():
#     print("fwef")
#     yield 123
#
#
# g_o = give_me_value()
# print(next(g_o))


# сопрограмма (корутина)
def grep(pattern):
    print("start grep")
    while True:
        line = yield  # заморозить своё состояние и ожидать ввода данных
        if pattern in line:
            print(line)


# g = grep("python")
# print(g)
# next(g)  # сначала всегда вызываем next или g.send(None) - запуск корутины
# g.send("golang is better")
# g.send("python is simple")

# отличие корутины от генератора:
# корутина потребляет значения, а генератор их производит

def grep(pattern):
    print("start grep")
    try:
        while True:
            line = yield  # заморозить своё состояние и ожидать ввода данных
            if pattern in line:
                print(line)
    except GeneratorExit:
        print("stop grep")


# g = grep("python")
# next(g)
# g.send("python is the best!")
# g.close()  # вообще он будет вызван самостоятельно сборщиком мусора, но можно и вызвать вручную


#  вызов одной корутины внутри другой
# def grep_python_coroutine():
#     g = grep("python")
#     yield from g


# g = grep_python_coroutine()
# print(g)
# g.send(None)  # это эквивалент next(g)
# g.send("python wow!")

# ЧТО ВАЖНО ЗНАТЬ:
# 1. Если видите в функции yield - значит её результат - это 100% объект-генератор
# 2. Если yield стоит ведушщим словом в строке, значит вы имеете дело с классическим генератором, который отдает
# значения по запросу. Если слово yield стоит справа от знака = (равно), то это корутина (сопрограмма) и она будет
# потреблять значения.
# 3. На сопрограммах (корутинах) построено все асинхронное взаимодействие внутри Python.
