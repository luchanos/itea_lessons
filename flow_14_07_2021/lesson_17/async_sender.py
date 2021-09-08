import asyncio
import aio_pika

from logging import getLogger, StreamHandler
import sys

logger = getLogger(__name__)

stdout_handler = StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
logger.setLevel("DEBUG")


class SenderAsync:
    def __init__(self, url):
        self.url = url
        self.connection = None

    async def setup(self, ):
        self.connection = await aio_pika.connect_robust(
            self.url
        )

    async def send(self, routing_key, message):
        # если добавить эту строчку, то всё зависнет
        # async with self.connection:
        channel = await self.connection.channel()  # аналог cursor в psycopg2
        async with channel:
            await channel.default_exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key=routing_key,
            )
        logger.info("sended")

    async def _close(self):
        await self.connection.close()

    async def __aenter__(self):
        await self.setup()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._close()


async def main():
    sender = SenderAsync("amqp://rmquser:rmqpass@127.0.0.1/")
    # await sender.setup()

    async with sender:
        for i in range(100_000_000):
            await sender.send(routing_key="test_queue", message=str(i))
    # await sender.send(routing_key="test_queue", message="123")
    # await sender.send(routing_key="test_queue", message="123")


if __name__ == "__main__":
    asyncio.run(main())
