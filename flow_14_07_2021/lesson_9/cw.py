from time import sleep


def one():
    two()
    sleep(2)


def two():
    sleep(2)


# Синхронность - задачи выполняются друг за другом
# one()
# two()

# Асинхронность - когда задачи запускаются и завершаются независимо друг от друга

# Конкурентность - это когда я пишу письмо и периодически переключаюсь на разговор по телефону
# Параллельность - когда я пишу письмо, а рядом сидит друг, который за меня разговаривает по телефону

# Процесс - программа, которая запущена в оперативной памяти компьютера. Другими словами, процесс - это набор
# инструкций, которые выполняются последовательно (в общем случае). В реальности всё немного не так просто.
# характеристики процесса:
# - PID - идентификатор процесса
# - Объём оперативной памяти, который занимает процесс
# - Стек (для вызова функций и переменных)
# - Список открытых файлов
# - Ввод/вывод

# TOP - команда, которая покажетю какие процессы сейчас запущены (запускаем команду в терминале)
# Кажется, что все процессы работают одновременно, но это не так. На самом деле планировщик выделяет каждому
# процессу небольшой квант времени, в ходе которого процесс выполняется, а потом происходит переключение.

# ЗАПУСТИМ НАШ ПЕРВЫЙ ПРОЦЕСС
# import time
# import os
#
# pid = os.getpid()  # получаем id процесса, в котором запущена программа
#
# while True:
#     print(pid, time.time())
#     time.sleep(2)

# ps axu - покажет информацию о процессах, запущенных в системе
# ps axu | grep lesson_2.py

# последовательность команд, которые выполняет процесс:
# процесс делает такую штуку, как системный вызов. Системный вызов выполняется ядром ОС, а результат возвращается
# в процесс, который этот системный вызов совершил. Пример системного вызова - вывод информации в консоль.

# чтобы посмотреть, какие системные вызовы делает наш процесс, мы можем запустить команду в терминале:
# strace -p <номер процесса>

# список открытых процессом файлов:
# lsof -p <номер процесса>

# перенаправление вывода в файл python cw_alchemy.py > log.txt


# СОЗДАНИЕ ПРОЦЕССОВ
# import time
# import os
#
# pid = os.fork()  # создать точную копию родительского процесса, полностью
# # копирует все ресурсы родителя
# cnt = 0
# if pid == 0:  # id дочернего процесса будет всегда 0
#     # этот код будет исполнен в дочернем процессе
#     while True:
#         print("child:", os.getpid())
#         time.sleep(1)
#         cnt += 1
#         if cnt == 5:
#             break
# else:
#     # while True:
#     #     print("parent:", os.getpid())
#     #     time.sleep(2)
#     # этот код будет исполнен в родительском процессе
#     print("parent:", os.getpid())
#     os.wait()  # дожидаемся завершения всех дочерних процессов

# РАБОТА ПАМЯТИ В ПРОЦЕССАХ
# import os
#
# foo = "bar"
#
# if os.fork() == 0:  # память целиком будет скопирована для дочернего процесса
#     # код будет выполнен в дочернем процессе
#     foo = "baz"
#     print("child", foo)
# else:
#     sleep(1)
#     # код будет выполнен в родительском процессе
#     print("parent:", foo)  # то, что в дочке поменялось значение никак не повлияет на родителя
#     os.wait()

# аналогично с файловыми дескрипторами:
# import os
#
# f = open("data.txt")
# foo = f.readline()  # считали одну строчку
#
# if os.fork() == 0:
#     # код будет выполнен в дочернем процессе
#     foo = f.readline()  # считали ещё одну строчку
#     print("child", foo)
# else:
#     # код будет выполнен в родительском процессе
#     foo = f.readline()  # считали ещё одну строчку
#     print("parent", foo)


# В питон для создания процессов и работы с ними используют модель multiprocessing
# from multiprocessing import Process
# import os
#
#
# def f(name):
#     print("hello", name, "from", os.getpid())
#
#
# print(os.getpid())
# p = Process(target=f, args=("Bob", ))  # создаём объект, в котором хотим запустить функцию с параметрами
# p.start()  # тут будет под капотом форкнут процесс и в нём выполнена функция с параметрами
# p.join()  # ожидание завершения всех дочерних процессов

# ХОЗЯЙКЕ НА ЗАМЕТКУ: не во всех системах есть системные вызовы fork, поэтому юзать multiprocessing - это хорошо!
# Все делают за нас!


# Альтернативный способ создания процессов:
# from time import sleep
# from multiprocessing import Process
# num_list = [x for x in range(10)]
#
#
# class MyShinyProcess(Process):
#     def __init__(self, name):
#         super().__init__()
#         self.name = name
#
#     def run(self):
#         global num_list
#         proc_num = num_list.pop()
#         print("hello", self.name, proc_num)
#         sleep(1)
#         if len(num_list) != 0:
#             p = MyShinyProcess("Mike")
#             p.start()
#             p.join()  # важно ждать завершения работы дочернего процесса, чтобы контролировать
#             # распределение ресурсов
#         print("%d FINISHED!" % proc_num)
#
#
# p = MyShinyProcess("Mike")
# p.start()
# p.join()

# простое применение - хотим читать файл параллельно в нескольких процессах и что-то делать с прочитанными данными

# ПОТОКИ
# Потоки напоминают процессы.
# - у потока своя последовательность инструкций
# - каждый поток имеет свой стек
# - потоки принадлежат процессу (если процесс один, то все потоки принадлежат ему)
# - потоки разделяют память и ресурсы процесса
# - управлением потоками руководит ОС
# - в Python потоки имеют ограничения, связанные с GIL (об этом позже)

from threading import Thread


# def f(name):
#     print("hello", name)
#
#
# th = Thread(target=f, args=("Bob", ))
# th2 = Thread(target=f, args=("Bob", ))
# th.start()  # запускаем поток на исполнение
# th2.start()
# th.join()  # дожидаемся выполнения всех созданных потоков
# th2.join()

# альтернатива:
# from threading import Thread
#
#
# class MyShinyThread(Thread):
#     def __init__(self, name):
#         super().__init__()
#         self.name = name
#
#     def run(self):
#         print("hello", self.name)
#
#
# th = MyShinyThread("Bob")
# th.start()  # запускаем поток на исполнение
# th.join()  # дожидаемся выполнения всех созданных потоков

# простое применение - хотим читать файл с общим прогрессом и что-то делать с вычитанными данными
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from random import randrange
#
# b = 0
#
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
# with ThreadPoolExecutor(max_workers=10) as pool:  # тут всё само сделается!
#     results = [pool.submit(f, i) for i in range(10)]  # submit - создает футуру, это объект, который обещает исполнится
#
#     for future in as_completed(results):
#         print(future.result())


# старый добрый клиент
import socket
from time import sleep

while True:
    sock = socket.create_connection(("127.0.0.1", 10001))
    res = sock.recv(1024)
    data = input("CLIENT 1 ---- Enter data: ")
    sock.send(data.encode())
