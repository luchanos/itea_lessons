import aiohttp
import asyncio


async def send_message_to_tg(url, session):
    async with session.get(url) as response:
        print(await response.read())


TOKEN = "1818338603:AAEv3AOttf2NqRSSphapItXr-ADv3sbL0tM"


async def main_4():
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id=362857450&text=1234'
    tasks = []

    session = aiohttp.ClientSession()
    async with session:
        for i in range(10):
            cor = send_message_to_tg(url, session)
            task = asyncio.create_task(cor)
            tasks.append(task)

        await asyncio.gather(*tasks)
        print("Закончили main_4!")


loop = asyncio.get_event_loop()
loop.run_until_complete(main_4())
