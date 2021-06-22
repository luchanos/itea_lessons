import asyncio
from asyncio import sleep


async def tcp_echo_client(message, loop):
    await sleep(1)
    reader, writer = await asyncio.open_connection("127.0.0.1", 10001, loop=loop)
    print(f"send from async client: {message}")
    writer.write(message.encode())
    writer.close()


async def many_sending_tasks(loop):
    tasks = [tcp_echo_client(loop=loop, message=str(x)) for x in range(30)]
    await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
message = "hello world"
# loop.run_until_complete(tcp_echo_client(message, loop))
loop.run_until_complete(many_sending_tasks(loop))
loop.close()
