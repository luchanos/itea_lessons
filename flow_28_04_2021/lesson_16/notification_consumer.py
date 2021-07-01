# тут мы будем слушать очередь, в которую прилетаю задачи на нотификацию
import pika
from pika import PlainCredentials
from app_2 import create_notification_task_func
import json
from time import sleep


connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost', credentials=PlainCredentials("rmquser", "rmqpass")))
channel = connection.channel()

# channel.queue_declare(queue='test_queue')

print(' [*] Waiting for notification tasks. To exit press CTRL+C')


def callback(ch, method, properties, body):
    """
    Типовое сообщение:
    {
    "message": "тестовое сообщение для пользователя в чат 362857450",
    "profile_id": 1
    }
    """

    # предположим, что для завершения работы нам нужно какое-то время и мы не держим большое количество
    # запросов сразу
    sleep(1)
    print(f"Обрабатываю следующее сообщение {body}\n")
    rmq_message_decoded = json.loads(body.decode())
    create_notification_task_func(data=rmq_message_decoded)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_message_callback=callback,
                      queue='test_queue',
                      auto_ack=False)

channel.start_consuming()
