import socket


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

    def _send(self, message):
        with socket.create_connection((self.host, self.port), self.timeout) as sock:
            try:
                sock.sendall(message.encode("utf8"))
                data = sock.recv(1024)
                print(data.decode())
            except socket.timeout:
                print("send data timeout")
            except socket.error as ex:
                print("send data error:", ex)

    def __call__(self, message):
        self._send(message)
        print("Отправка метрики в БД. Событие: использован метод _send.")


client = Client("127.0.0.1", 5000, timeout=15)
user_answer = ""
while user_answer != "q":
    user_answer = input("Введите данные для отправки: ")
    client(user_answer)
