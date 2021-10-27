import pika
from pika import PlainCredentials
import json
from time import sleep

from flow_14_07_2021.lesson_7.app_example import MyDbClient


connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost', credentials=PlainCredentials("rmquser", "rmqpass")))
channel = connection.channel()

# channel.queue_declare(queue='test_queue', durable=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

# DB_URL = 'postgresql://postgres:dbpass@127.0.0.1:5432/postgres'
# my_db_client = MyDbClient(DB_URL)
# my_db_client.setup()


# def create_product(ch, method, properties, body):
#     product_data = json.loads(body.decode())
#     my_db_client.insert_new_product(description=product_data["description"],
#                                     quantity=product_data["quantity"])
#     sleep(1)
#     print(f"Принял новый продукт! - {product_data}")
#     ch.basic_ack(delivery_tag=method.delivery_tag)


# def callback(ch, method, properties, body):
#     if int(body.decode()) % 2 != 0:
#         ch.basic_ack(delivery_tag=method.delivery_tag)
#     print(" [x] Received %r" % (body,))



def func_1():
    print("Первая функция - создание")


def func_2():
    print("Вторая функция - редактирование")


def func_3():
    print("Третья функция - удаление")


func_mapper = {
    "create": func_1,
    "update": func_2,
    "delete": func_3,
    "patch": lambda: print("Четвёртая функция")
}


def choose_context(ch, method, properties, body):
    """
    Принимаю из кролика сообщение вида:

    {"action": "<действие>", "meta": "<какая-то метаинформация>", ...}
    """
    try:
        rmq_data = json.loads(body.decode())
        func_to_be_executed = func_mapper[rmq_data["action"]]
        func_to_be_executed()
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Приняли сообщение: {rmq_data}. Запустили функцию: {func_to_be_executed}")
    except:
        print("Ошибка!")


# создаём базовый консумер (консумер = потребитель сообщений)
channel.basic_consume(on_message_callback=choose_context,
                      queue='test_queue',
                      auto_ack=False,
                      consumer_tag="my_shiny_consumer")

channel.start_consuming()
