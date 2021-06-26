import pika

from pika import PlainCredentials
import json


connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost', credentials=PlainCredentials("rmquser", "rmqpass")))
channel = connection.channel()

for num in range(100):
    message_to_send = {
        "message": f"{num} тестовое сообщение для пользователя 1 в чат",
        "profile_id": 1
    }
    message_for_rmq = json.dumps(message_to_send).encode()
    channel.basic_publish(exchange='',
                          routing_key='notification_tasks',
                          body=message_for_rmq)
    print("sended...")


connection.close()
