# import asyncio
#
#
# async def some_func():
#     print("Тестовое сообщение")
#     some_func_2()
#     await some_func_3()  # это команда означает "делаю, жду результат и только потом иду дальше,
#     # при этом, если у меня есть какие-то другие задачи, то я могу тоже взять их в работу
#
#
# def some_func_2():
#     print("Тестовое сообщение из some_func_2")
#
#
# async def some_func_3():
#     print("Выполняю запрос с длительным ожиданием во внешний сервис")
#
#
# # c = some_func()
# # print(c)
#
# if __name__ == "__main__":
#     # создаём ивент-луп или цикл событий (карусель)
#     loop = asyncio.get_event_loop()
#     print(loop)
#     loop.run_until_complete(some_func())  # отдали нашу корутину (или task)



# import asyncio
# from asyncio import sleep as asleep  # это асинхронный неблокирующий sleep
# from time import sleep as sync_sleep  # а вот это блокирующий
#
#
# # async def main():
# #     # sleep(.5)
# #     await asleep(.5)
# #     print("Я поспал полсекунды")
# #
# # cor = main()
# # loop = asyncio.get_event_loop()
# # loop.run_until_complete(cor)
#
# # а теперь с тасками:
# async def sleepy():
#     print("Я сейчас посплю 2 секундочки")
#     await asleep(2)
#     return "Я отлично поспал!"
#
#
# async def sync_sleepy():
#     print("Я сейчас посплю 2 секундочки")
#     sync_sleep(2)
#     return "Я отлично поспал!"


# async def main():
#     # task_1 = sleepy()
#     # task_2 = sleepy()
#     # task_3 = sleepy()
#     task_1 = sync_sleepy()  # первая задача
#     task_2 = sync_sleepy()  # вторая задача
#     task_3 = sync_sleepy()  # третья задача
#     result = await asyncio.gather(task_1, task_2, task_3)
#     for res in result:
#         print(res)

# loop = asyncio.get_event_loop()
# # task_1 = sync_sleepy()  # первая задача
# # task_2 = sync_sleepy()  # вторая задача
# # task_3 = sync_sleepy()  # третья задача
# task_1 = sleepy()  # первая задача
# task_2 = sleepy()  # вторая задача
# task_3 = sleepy()  # третья задача
# res = loop.run_until_complete(asyncio.gather(task_1, task_2, task_3))
# loop.close()

import asyncio


async def handle_echo(reader, writer):  # reader, writer - это обязательные параметры для корутины, которую
    # хотим использовать в сервере "из коробки"
    print("SERVER ---- Ready for reading")
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
