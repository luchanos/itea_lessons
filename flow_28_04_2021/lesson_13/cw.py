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

# с точки зрения процесса ресурсами владеет именно процесс. Но процесс не знает, что там творится в потоках.
# Если поток завершить аварийно, то могут случиться неприятности (незакрытые файлы и тд).
# Поэтому в питоне нет функции аварийного завершения потока.

# Блокировки.
# import threading
#
#
# class Point:
#     def __init__(self):
#         self._mutex = threading.RLock()  # запрашиваем блокировку
#         self._x = 0
#         self._y = 0
#
#     def get(self):
#         with self._mutex:
#             return self._x, self._y
#
#     def set(self, x, y):
#         with self._mutex:
#             self._x = x
#             self._y = y

# Предположим, что используем наш класс в большом количестве потоков
# Может произойти неконсистентное состояние объекта. Также это "гонка за ресурсами"

# Другой способ
# import threading
#
# a = threading.RLock()
# b = threading.RLock()
#
#
# def foo():
#     try:
#         a.acquire()  # запрашиваем блокировку
#         b.acquire()
#     finally:
#         a.release()  # освобождаем
#         b.release()


# если мы запустим код выше в большом количестве процессов,
# то рано или поздно это приведет к ситуации, когда произойдёт взаимная блокировка (deadlock). Чтобы избежать этого
# нужно освобождать блокировки в правильной последовательности. Контекстный менеджер - это выход!

# GIL
# Глобальная блокировка интерпретатора
# Не позволяет двум потокам выполняться одновременно двум потокам. Защищает память от "разрушения".
# from threading import Thread
# import time
#
#
# def count(n):
#     while n > 0:
#         n -= 1
#
# t0 = time.time()
# count(100_00_00)
# count(100_00_00)
# print("Последовательное", time.time() - t0)
#
# # параллельное выполнение
# t0 = time.time()
# th1 = Thread(target=count, args=(100_000_000, ))
# th2 = Thread(target=count, args=(100_000_000, ))
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

# сопрограмма (корутина)
# def grep(pattern):
#     print("start grep")
#     while True:
#         line = yield  # заморозить своё состояние и ожидать ввода данных
#         if pattern in line:
#             print(line)


# g = grep("python")
# print(g)
# next(g)  # сначала всегда вызываем next или g.send(None) - запуск корутины
# g.send("golang is better")
# g.send("python is simple")

# отличие корутины от генератора:
# корутина потребляет значения, а генератор их производит

# def grep(pattern):
#     print("start grep")
#     try:
#         while True:
#             line = yield  # заморозить своё состояние и ожидать ввода данных
#             if pattern in line:
#                 print(line)
#     except GeneratorExit:
#         print("stop grep")


# g = grep("python")
# next(g)
# g.send("python is the best!")
# g.close()  # вообще он будет вызван самостоятельно сборщиком мусора, но можно и вызвать самостоятельно


#  вызов одной корутины внутри другой
# def grep_python_coroutine():
#     g = grep("python")
#     yield from g


# g = grep_python_coroutine()
# print(g)
# g.send(None)
# g.send("python wow!")


# asyncio - библиотека, которая входит в состав стандартной библиотеки python3
# собственно, проблема: предположим у нас есть необходимость работать с запросами, которые требуют времени. Например
# это могут быть запросы во внешний сервис или БД. Чтобы не заниматься ожиданием того, когда очередная задача будет
# выполнена, мы можем воспользоваться процессами и потоками. Но дело в том, что процессы слишком дорогие, а с потоками
# будет происходить вот такая петрушка:

# допустим 3 потока занимаются выполнением задачи ввода-вывода. Интерпретатор скачет между ними и дает каждому
# определенный квант времени. Назовем их Т1, Т2, Т3. Допустим Т3 завершил работу первым. Т1 и Т2 еще в "ожидании" ввода
# вывода, но при этом интерпретатор всё равно выделяет каждому из них время на процессоре, которое фактически
# выбрасывается в помойку. И только в самом конце мы переключимся на Т3, чтобы увидеть, что он закончил свою работу.

# asyncio предлагает нам другой подход - пусть у нас есть некий цикл событий, по сути просто петля, которая крутится в
# бесконечном цикле и ждёт, что ей кто-то просигнализирует о готовности.
import asyncio
from asyncio import sleep  # это асинхронный неблокирующий sleep
from time import sleep as sync_sleep  # а вот это блокирующий


# async def main():
#     # sleep(.5)
#     await sleep(.5)
#     print("Я поспал полсекунды")

# cor = main()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(cor)

# а теперь с тасками:
# async def sleepy():
#     print("Я сейчас посплю полсекундочки")
#     await sleep(2)
#     return "Я отлично поспал!"
#
#
# async def sync_sleepy():
#     print("Я сейчас посплю полсекундочки")
#     sync_sleep(2)
#     return "Я отлично поспал!"
#
#
# async def main():
#     # task_1 = sleepy()
#     # task_2 = sleepy()
#     # task_3 = sleepy()
#     task_1 = sync_sleepy()
#     task_2 = sync_sleepy()
#     task_3 = sync_sleepy()
#     result = await asyncio.gather(task_1, task_2, task_3)
#     for res in result:
#         print(res)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()


# асинхронный сервер
import asyncio


async def handle_echo(reader, writer):  # reader, writer - это обязательные параметры для корутины, которую
    # хотим использовать в сервере "из коробки"
    print("Ready for reading")
    data = await reader.read(1024)
    message = data.decode()
    addr = writer.get_extra_info("peername")
    print(f"received {message} from {addr}")
    writer.close()

loop = asyncio.get_event_loop()
# в asyncio есть сервер из коробки! нужно лишь сказать, что нужно делать с
# входящим соединением! на каждое соединение будет самостоятельно создаваться
# своя корутина на обработку пришедшей информации
coro = asyncio.start_server(handle_echo, "127.0.0.1", 10001, loop=loop)
server = loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()


# import asyncio
# import datetime
# import random
#
#
# async def my_sleep_func():
#     await asyncio.sleep(random.randint(0, 5))
#
#
# async def display_date(num, loop):
#     """
#     У нас есть асинхронная функция display_date, которая принимает число (в качестве идентификатора)
#     и цикл обработки событий в качестве параметров
#     """
#     end_time = loop.time() + 5.0
#     while True:
#         print("Loop: {} Time: {}".format(num, datetime.datetime.now()))
#         if (loop.time() + 1.0) >= end_time:
#             break
#         await my_sleep_func()
#
#
# loop = asyncio.get_event_loop()
#
# asyncio.ensure_future(display_date(1, loop))
# asyncio.ensure_future(display_date(2, loop))
#
# loop.run_forever()

# Всякий раз, когда происходит вызов await, asyncio понимает, что функции, вероятно, потребуется некоторое время.
# Таким образом, он приостанавливает выполнение, начинает мониторинг любого связанного с ним события ввода-вывода
# и позволяет запускать задачи. Когда asyncio замечает, что приостановленный ввод-вывод функции готов,
# он возобновляет функцию.

# ХОЗЯЙКЕ НА ЗАМЕТКУ! Если вы попробуете использовать неасинхронную функцию в ивент-лупе,
# то получите обычную линейно выполняющуюся программу.


# ХОЗЯЙКЕ НА ЗАМЕТКУ:
# if io_bound:
#     if io_very_slow:
#         print("Use Asyncio")
#     else:
#        print("Use Threads")
# else:
#     print("Multi Processing")
