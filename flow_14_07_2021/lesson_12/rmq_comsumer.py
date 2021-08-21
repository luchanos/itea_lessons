import pika
from pika import PlainCredentials

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost', credentials=PlainCredentials("rmquser", "rmqpass")))
channel = connection.channel()

channel.queue_declare(queue='test_queue', durable=True)

print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    if int(body.decode()) % 2 != 0:
        ch.basic_ack(delivery_tag=method.delivery_tag)
    print(" [x] Received %r" % (body,))


# создаём базовый консумер (консумер = потребитель сообщений)
channel.basic_consume(on_message_callback=callback,
                      queue='test_queue',
                      auto_ack=False,
                      consumer_tag="my_shiny_consumer")

channel.start_consuming()
