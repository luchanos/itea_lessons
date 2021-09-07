import asyncio
from random import randint

n = 0


async def sleepy():
    global n
    await asyncio.sleep(.2)
    print(f"сплю {n}")
    n += 1
    return 1 / randint(0, 1)


async def main():
    # автоматичекая обёртка корутин в тасочки
    tasks = [sleepy() for _ in range(100)]
    # параметр return_exceptions позволяет нам кастомизировать поведение при возникновении исключений
    res = await asyncio.gather(*tasks, return_exceptions=True)
    c = 1

asyncio.run(main())
