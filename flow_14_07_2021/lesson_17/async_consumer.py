import asyncio
import aio_pika


class ConsumerAsync:
    def __init__(self, url, queue_name):
        self.url = url
        self.queue_name = queue_name
        self.connection = None

    async def setup(self):
        self.connection = await aio_pika.connect_robust(self.url)

    async def consume(self):
        async with self.connection:
            # Creating channel
            channel = await self.connection.channel()

            # Declaring queue
            queue = await channel.declare_queue(self.queue_name, auto_delete=False, durable=True)

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        print(message.body)
                        await asyncio.sleep(.2)
                        if queue.name in message.body.decode():
                            break


async def main():
    consumer = ConsumerAsync("amqp://rmquser:rmqpass@127.0.0.1/", "test_queue")
    await consumer.setup()
    await consumer.consume()


if __name__ == "__main__":
    asyncio.run(main())
