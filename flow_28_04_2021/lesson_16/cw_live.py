# отправка сообщений в Телеграм с помощью обыкновенных запросов POST

TOKEN = "1818338603:AAEv3AOttf2NqRSSphapItXr-ADv3sbL0tM"
BASE_URL = 'https://api.telegram.org'
CHAT_ID = 362857450

# Телеграм говорит нам, что мы можем собрать URL по некоторому правилу и отправка сообщения
# произойдет просто по переходу по нему

sender_url = "https://api.telegram.org/bot1818338603:AAEv3AOttf2NqRSSphapItXr-ADv3sbL0tM/sendMessage?chat_id=362857450" \
             "text=ТЕСТОВОЕ СОООБЩЕНИЕ"

f"{BASE_URL}/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={notification.message}"













# Deque, Queue, Stack
# классические коллекции.

# Stack - стек, первым вошёл - последним обслужен
# l = []
# l.append(1)
# l.append(2)
# l.append(3)
#
# l.pop()
# l.pop()
# l.pop()

# Queue - очередь, первым вошёл - первым обслужен
# l = []
# l.append(1)
# l.append(2)
# l.append(3)
#
# l.pop(0)
# l.pop(0)
# l.pop(0)

# Deque - двусторонняя очередь - по сути совмещает в себе поведение Stack и Queue
# подробнее можно прочитать в книге Грокаем алгоритмы)



# Rabbit MQ - брокер сообщений
# https://habr.com/ru/post/488654/ - годная статья для понимания
# https://habr.com/ru/post/149694/


# RabbitMQ ‒ это брокер сообщений. Его основная цель ‒ принимать и отдавать сообщения. Его можно представлять себе,
# как почтовое отделение: когда Вы бросаете письмо в ящик, Вы можете быть уверены, что рано или поздно почтальон
# доставит его адресату. В этой аналогии RabbitMQ является
# одновременно и почтовым ящиком, и почтовым отделением, и почтальоном.


# поднимаю его в контейнере
# коннекчусь к штуке, которая открывает мне web-интерфейс

# Работа с брокером сообщений на стороне Python
# Имеется web-интерфейс

# Docker
import pika
from pika import PlainCredentials


# connection = pika.BlockingConnection(pika.ConnectionParameters(
#                'localhost', credentials=PlainCredentials("rmquser", "rmqpass")))
# channel = connection.channel()

# Мы подключились к брокеру сообщений, находящемуся на локальном хосте. Для подключения к брокеру, находящемуся на
# другой машине, достаточно заменить «localhost» на IP адрес этой машины.

# объявляем очередь (если будем кидать сообщение в несуществующую очередь,
# то оно будет проигнорировано)

# channel.queue_declare(queue='hello')

# кидаем в очередь сообщение
# channel.basic_publish(exchange='',
#                       routing_key='hello',
#                       body=b'Hello World!')
# print(" [x] Sent 'Hello World!'")


# накидаем очень много сообщений в очередь
# while True:
#     # кидаем в очередь сообщение
#     channel.basic_publish(exchange='',
#                           routing_key='hello',
#                           body=b'Hello World!')
#     break
#
# connection.close()

# давайте напишем штуку, которая будет кидать и слушать сообщения сама с собой:
# def callback(ch, method, properties, body):
#     print(" [x] Received %r" % (body,))
#
#
# channel.basic_consume(on_message_callback=callback,
#                       queue='hello',
#                       auto_ack=True)
# channel.start_consuming()

# идея в том, что в очередь могут писать сколько угодно консумеров, мы потом сможем спокойно разгрести
# тот пул задач, который у нас накопился. Например для того, чтобы насоздавать сообщений для отправки пользователям
