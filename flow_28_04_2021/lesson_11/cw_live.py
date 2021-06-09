"""
Организовать взаимодействие клиента и сервера:
клиент открывает файл (который вы создали и наполнили) и построчно читает и перекидывает по сети строки на сервер.
Сервер принимает строки и складывает их в новый файл, логируя время принятия.

Исходный файл:
123
456
789

Результирующий файл:
2021-06-09 21:49:54.657742 123
2021-06-09 21:49:54.657742 456
2021-06-09 21:49:54.657742 789
"""

# работа с сетевыми запросами в python:
import requests

# answer = requests.post("127.0.0.1")

# работа с сетью в Python
import socket  # стандартная библиотека

# КОД НА СТОРОНЕ СЕРВЕРА
# создаю сущность "отверстия" почтового ящика
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # семейство сокета и его тип
# # подробная информация содержится в оф. документации
sock.bind(("127.0.0.1", 10002))  # max port 65335  # на какой почтовый ящик прикручиваем отверстие
sock.listen(socket.SOMAXCONN)  # слушаем хост и порт и задаём макс. количество входящих соединений

conn, addr = sock.accept()  # начинаем принимать входящее клиентское соединение
# бесконечно читаем из нашего соединния
while True:
    data = conn.recv(1024)
    if not data:
        print("Ничего нет")
        break
    print(data.decode("utf-8"))
#
# conn.close()
# sock.close()


# КОД НА СТОРОНЕ КЛИЕНТА (работа с почтальоном!!!)
import socket

sock = socket.socket()
sock.connect(("127.0.0.1", 10001))  # заблокируется до тех пор, пока сервер на своей стороне
# не вызовет accept
sock.sendall("ping".encode("utf-8"))
sock.close()

# более короткая запись
sock = socket.create_connection(("127.0.0.1", 10001))
sock.sendall("ping".encode("utf-8"))
sock.close()

# А теперь можно разнести код по разным файлам и посмотреть, как один код будет
# отправлять запросы, а другой их получать

# import requests
# import json
#
# res = requests.get('https://www.avito.ru/clickstream/events/1/json')
# print(json.loads(res.content), type(json.loads(res.content)))
