# старый добрый клиент
import socket
from sys import argv

HOST_PORT_PAIR = ("127.0.0.1", 5000)

sock = socket.create_connection(HOST_PORT_PAIR)
client_num = argv[1]

with sock:
    while True:
        data = f"CLIENT {client_num} say:" + input(f"CLIENT {client_num} ---- Enter data or q for exit: ")
        if data.lower() == 'q':
            break
        sock.send(data.encode())
        response = sock.recv(1024)
        print("Server say:", response.decode())
