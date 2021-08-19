# синхронный пример
import requests
from time import time

url = 'https://loremflickr.com/320/240'


def get_file(url):
    return requests.get(url, allow_redirects=True)


def write_file(response):
    filename = response.url.split('/')[-1]
    with open(filename, 'wb') as file:
        file.write(response.content)


def main():
    t0 = time()
    for i in range(50):
        write_file(get_file(url))
    print(time() - t0)


# if __name__ == '__main__':
#     main()

# асинхронный пример
import asyncio
import aiohttp
from time import time

# все запросы надо делать через созданную сессию


# @retry(10)  # декоратор, который повторно запустит эту же самую функцию, если прилетит ошибка
# @metrics
async def fetch_content(url, session, main_id):
    async with session.get(url, allow_redirects=True) as response:
        print(f"Делаю запрос из {main_id}")
        data = await response.read()
        write_image(data)


def write_image(data):
    filename = 'file-{}.jpeg'.format(int(time() * 1000))
    with open(filename, 'wb') as file:
        file.write(data)


async def main_4():
    url = 'https://loremflickr.com/320/240'
    tasks = []

    session = aiohttp.ClientSession()
    async with session:
        for i in range(50):
            cor = fetch_content(url, session, 4)
            task = asyncio.create_task(cor)
            tasks.append(task)

        await asyncio.gather(*tasks)
        print("Закончили main_4!")


async def main_3():
    url = 'https://loremflickr.com/320/240'
    tasks = []

    session = aiohttp.ClientSession()
    async with session:
        for i in range(50):
            cor = fetch_content(url, session, 3)
            task = asyncio.create_task(cor)
            tasks.append(task)

        await asyncio.gather(*tasks)
        print("Закончили main_3!")


async def main_2():
    task_1 = asyncio.create_task(main_4())
    task_2 = asyncio.create_task(main_3())
    await asyncio.gather(task_1, task_2)
    print("Основной main завершён!")


if __name__ == '__main__':
    t0 = time()
    asyncio.run(main_2())
    print(time() - t0)
