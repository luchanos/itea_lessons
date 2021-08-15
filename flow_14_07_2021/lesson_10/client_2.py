# старый добрый клиент
import socket

from flow_14_07_2021.lesson_10.const import HOST_PORT_PAIR

sock = socket.create_connection(HOST_PORT_PAIR)

with sock:
    while True:
        data = input("CLIENT 2 ---- Enter data or q for exit: ")
        if data.lower() == 'q':
            break
        sock.send(data.encode())
