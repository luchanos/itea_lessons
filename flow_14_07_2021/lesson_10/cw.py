import socket
import time
from datetime import datetime
from logging import getLogger

from flow_14_07_2021.lesson_10.const import HOST_PORT_PAIR

logger = getLogger(__name__)
logger.setLevel("DEBUG")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # семейство сокета и его тип
# подробная информация содержится в оф. документации
sock.bind(HOST_PORT_PAIR)  # max port 65335
sock.listen(socket.SOMAXCONN)  # слушаем хост и порт и задаём макс. количество входящих соединений

while True:
    conn, addr = sock.accept()  # начинаем принимать входящее клиентское соединение
    # conn.settimeout(0)  # таймаут в секундах для ожидания сервера, что подсоединившийся клиент что-то даст
    logfile = open("logfile.txt", "a")

    # 0 - неблокирующий режим. None - это бесконечное ожидание, что данные прочитают
    with conn, sock, logfile:
        while True:
            received_data = conn.recv(1024)
            # обратите внимание, что данные прилетают в виде байтов!
            # print(datetime.now(), received_data.decode("utf-8"), file=logfile)
            logger.error(f"{datetime.now()}, {received_data.decode('utf-8')}")
            time.sleep(1)
            if not received_data:
                break
