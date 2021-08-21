import asyncio
import time

num = 0


async def sleepy(semaphore):
    await semaphore.acquire()
    global num
    start = time.time()
    num += 1
    sleep_time = 1 - (time.time() - start)
    print(f"Выполнил увеличение каунтера! Теперь он - {num}. Спать будем - {sleep_time}")
    await asyncio.sleep(sleep_time if sleep_time > 0 else 1)
    await semaphore.release()


async def make_by_semaphore():
    semaphore = asyncio.Semaphore(value=10)
    await asyncio.wait([sleepy(semaphore) for _ in range(100)])


loop = asyncio.get_event_loop()
loop.run_until_complete(make_by_semaphore())
