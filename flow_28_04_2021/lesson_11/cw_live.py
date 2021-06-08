# работа с сетью в Python
import socket  # стандартная библиотека

# КОД НА СТОРОНЕ СЕРВЕРА
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # семейство сокета и его тип
# # подробная информация содержится в оф. документации
# sock.bind(("127.0.0.1", 10002))  # max port 65335
# sock.listen(socket.SOMAXCONN)  # слушаем хост и порт и задаём макс. количество входящих соединений
#
# conn, addr = sock.accept()  # начинаем принимать входящее клиентское соединение
# # бесконечно читаем из нашего соединния
# while True:
#     data = conn.recv(1024)
#     if not data:
#         print("Ничего нет")
#         break
#     print(data.decode("utf-8"))
#
# conn.close()
# sock.close()


# КОД НА СТОРОНЕ КЛИЕНТА
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

# при работе с сокетами важно обрабатывать сетевые ошибки
