import socket

HOST_PORT_PAIR = ("127.0.0.1", 5000)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET - интернет протокол 4й версии,
# SOCK_STREAM - поддержка протокола TCP который лежит в основе протокола HTTP
# система после завершения скрипта какое-то время не позволит использовать порт, потому что хочет, чтобы данные дошли
# до своего адресата
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)  # настройка для того, чтобы фиксануть реюз порта
server_socket.bind(HOST_PORT_PAIR)
server_socket.listen()  # слушать входящие подключения

while True:
    print('Before accept')
    client_socket, addr = server_socket.accept()  # принмаем входящее подключение - читает данные из входящего буфера
    # в случае, если что-то прилетело, то возвращается кортеж: объект клиентского сокета и адрес
    print('Connection from', addr)  # сообщили о том, что приняли входящее подключение

    while True:
        try:
            print('before recv')
            request = client_socket.recv(4096)  # принимаем из клиентского сокета сообщение

            if not request:
                break
            else:
                response = 'Hello, world!\n'.encode()
                client_socket.send(response)
        except ConnectionResetError:
            print("Connection reset by peer!")
    print('Outside inner while loop')
    client_socket.close()  # закрываем, а то клиент может подумать что мы медленно отвечаем


# для коннекта с сервером используем утилиту nc и пишем в терминале nc localhost:5000
