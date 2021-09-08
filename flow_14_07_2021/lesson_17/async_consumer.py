import asyncio
import aio_pika
from time import sleep

from flow_14_07_2021.lesson_15.cw import MyAsyncDbClient, DB_URL

db_client = MyAsyncDbClient(DB_URL)
db_client.setup()


async def process_message(message: aio_pika.IncomingMessage):
    await asyncio.sleep(.2)
    async with message.process():
        print(message.body)


class ConsumerAsync:
    def __init__(self, url, queue_name):
        self.url = url
        self.queue_name = queue_name
        self.connection = None

    async def setup(self):
        self.connection = await aio_pika.connect_robust(self.url)

    async def consume(self):
        # Creating channel
        channel = await self.connection.channel()

        # Declaring queue
        queue = await channel.declare_queue(self.queue_name, auto_delete=False, durable=True)

        await queue.consume(process_message)

    async def close(self):
        await self.connection.close()


async def main(loop):
    consumer = ConsumerAsync("amqp://rmquser:rmqpass@127.0.0.1/", "test_queue")
    await consumer.setup()
    await consumer.consume()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(main(loop))
    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
