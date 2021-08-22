import asyncio
import time

import aiohttp

async def main_action():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://0.0.0.0:8082") as response:
            html = await response.text()
            print(
                "Status:",
                response.status,
                "Content-type:",
                response.headers["content-type"],
                "Body:",
                html[:15],
                "...",
            )


async def main(semaphore):
    await semaphore.acquire()
    start = time.time()
    await main_action()
    sleep_time = time.time() - start
    await asyncio.sleep(1 - sleep_time if sleep_time > 0 else 1)
    await semaphore.release()


async def make_by_semaphore():
    semaphore = asyncio.Semaphore(value=10)
    await asyncio.wait([main(semaphore) for _ in range(100)])


loop = asyncio.get_event_loop()
loop.run_until_complete(make_by_semaphore())
