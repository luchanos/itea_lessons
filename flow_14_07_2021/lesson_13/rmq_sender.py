import time

from pika import PlainCredentials, ConnectionParameters, BlockingConnection

# это просто синтаксис для создания подключения к Кролику
connection = BlockingConnection(ConnectionParameters(
               'localhost', credentials=PlainCredentials("rmquser", "rmqpass")))

# создаём канал для передачи данных
channel = connection.channel()

# channel.basic_publish(exchange='',  # это точка доступа к очередям (почтамт)
#                       routing_key='test_queue',  # это название очереди, куда отправляем сообщение
#                       body=b'Hello World!')
# print(" [x] Sent 'Hello World!'")

# for num in range(100):


import json

product_data = [("Репчатый лук от отечественного производителя", 100),
                ("Капуста белокочанная высшего сорта", 200),
                ("Картофель молодой", 300, "Картофель"),
                ("Свекла сахарная импортная", 50),
                ("Яйцо куриные высшей категории", 70)]

for _ in range(10):
    for product in product_data:
        d = dict()
        d["description"] = product[0]
        d["quantity"] = product[1]
        channel.basic_publish(exchange='',
                              routing_key='test_queue',
                              body=f'{json.dumps(d)}'.encode())
        print(f" [x] Sent '{d}'")
        time.sleep(.5)

connection.close()
