import pika
from pika import PlainCredentials

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost', credentials=PlainCredentials("rmquser", "rmqpass")))
channel = connection.channel()

channel.queue_declare(queue='hello')

print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    if int(body.decode()) % 2 == 0:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(" [x] Received %r" % (body,))


channel.basic_qos(prefetch_count=2)
channel.basic_consume(on_message_callback=callback,
                      queue='hello',
                      auto_ack=False)

channel.start_consuming()
