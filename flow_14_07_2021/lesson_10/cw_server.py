# КОД НА СТОРОНЕ СЕРВЕРА
import socket
import sys

from logging import getLogger, StreamHandler

# logger = getLogger(__name__)
# stdout_handler = StreamHandler(sys.stdout)
# logger.addHandler(stdout_handler)
# logger.setLevel("DEBUG")
from flow_14_07_2021.lesson_10.const import HOST_PORT_PAIR

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # семейство сокета и его тип
# подробная информация содержится в оф. документации
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
sock.bind(HOST_PORT_PAIR)  # max port 65335
sock.listen(socket.SOMAXCONN)  # слушаем хост и порт и задаём макс. количество входящих соединений

while True:
    conn, addr = sock.accept()  # начинаем принимать входящее клиентское соединение
    # бесконечно читаем из нашего соединния
    conn.settimeout(5)  # таймаут в секундах для ожидания сервера, что подсоединившийся клиент что-то даст
    # None - это бесконечное ожидание, что данные прочитают
    with conn, sock:
        while True:
            received_data = conn.recv(1024)
            # обратите внимание, что данные прилетают в виде байтов!
            # logger.info(f"I am received that data: {received_data}")
            print(received_data.decode("utf-8"))
            if not received_data:
                break

# если юзаем менеджер контекста, то не нужно
# conn.close()
# sock.close()
