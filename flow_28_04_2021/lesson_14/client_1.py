# старый добрый клиент
import socket
from time import sleep

while True:
    sock = socket.create_connection(("127.0.0.1", 10001))
    data = input("CLIENT 1 ---- Enter data: ")
    sock.send(data.encode())
