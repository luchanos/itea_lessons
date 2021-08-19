# синхронный код
from time import sleep

# cnt = 0

# def make_request():
#     global cnt
#     print(f"Делаю запрос {cnt} на внешний сервис!")
#     cnt += 1
#     sleep(.1)


# for _ in range(100):
#     make_request()


# from time import sleep
import asyncio

cnt = 0


# корутина - по сути это задача, которую вы планируете поставить перед event loop
async def make_request():
    global cnt
    current = cnt
    print(f"Делаю запрос {current} на внешний сервис!")
    cnt += 1
    await asyncio.sleep(1)
    print(current, "поспал и работу закончил!")



# for _ in range(100):
#     print(make_request())


async def main():
    tasks = [asyncio.create_task(make_request()) for _ in range(100)]
    res = asyncio.gather(*tasks)
    await res
    a = 1


# cor = make_request()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
