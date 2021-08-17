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


# 1: у нас есть N задач на то, чтобы получить данные из внешнего сервиса.
# 2: мы - ивент луп. Наша задача брать в работу задачи и выполнять их. При этом, если мы в рамках исполнения задачи
# увидим, что нужно переключить контекст, то мы сделаем это и уйдем делать другую задачу.
# 3: когда мы бросаем запрос, то со стороны Питона работаем под капотом с объектами типа "сокет". Но питонячий сокет
# это лишь ОБВЯЗКА вокруг системного сокета (так же, как и в случае с работой с файлами)
# 4: когда мы даём команду питончьему сокету бросить запрос во внешний сервис и сталкиваемся в этот же момент с
# требованием переключить контекст, то происходит следующее:
# - Питон дает команду сетевому сокету уже в ОПЕРАЦИОННОЙ СИСТЕМЕ сделать внешний запрос. То есть Питон уже не управляет
# процессом запроса, а лишь сообщает ОС, что требуется сделать и эта задача выполняется уже не интерпретатором, а ОС.
# Иначе говоря, наш Питонячий сокет сообщил ОС, что нужно на сетевом сокете операционной системы сделать запрос.
# - После того, как было выдано задание для ОС, мы на стороне питона откладываем в сторону нашу задачу с сохранённым
# контекстом исполнения (так как работаем с сопрограммой/корутиной)
# 5: дальше мы будем опрашивать наши задачи на предмет завершения их выполнения. Важно!!! Мы не будем выделять какой-то
# там квант времени, мы просто будем спрашивать о готовности ту или иную задачу (корутину/сопрограмму)
# 6: когда сокет в ОС получит данные, то эта информация будет отражена в статусе нашей задачи на стороне питона, т.к.
# при получении данных в сокете об этом узнает сокет-обвязка, которую мы дёргаем в нашей программе.


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
async def sleepy():
    print("Я сейчас посплю полсекундочки")
    await sleep(2)
    return "Я отлично поспал!"


# async def sync_sleepy():
#     print("Я сейчас посплю полсекундочки")
#     sync_sleep(.5)
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
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()


# асинхронный сервер
# import asyncio
#
#
# async def handle_echo(reader, writer):  # reader, writer - это обязательные параметры для корутины, которую
#     # хотим использовать в сервере "из коробки"
#     print("Ready for reading")
#     data = await reader.read(1024)
#     message = data.decode()
#     addr = writer.get_extra_info("peername")
#     print(f"received {message} from {addr}")
#     writer.close()

# loop = asyncio.get_event_loop()
# в asyncio есть сервер из коробки! нужно лишь сказать, что нужно делать с
# входящим соединением! на каждое соединение будет самостоятельно создаваться
# своя корутина на обработку пришедшей информации
# coro = asyncio.start_server(handle_echo, "127.0.0.1", 10001, loop=loop)
# server = loop.run_until_complete(coro)

# try:
#     loop.run_forever()
# except KeyboardInterrupt:
#     pass
#
# server.close()
# loop.run_until_complete(server.wait_closed())
# loop.close()


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
