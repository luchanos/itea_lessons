import asyncio


class Server:
    # todo надо сделать метод, который бы дополнял словарь с метриками, и выдавал лист по запросу всех метрик
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.metric_dict = dict()

    def _msg_proccessor(self, message):
        """Обрабатывает поступившее сообщение и запускает либо метод post или get"""
        if message[0] == 'put':
            return self.put(message=message)
        elif message[0] == 'get':
            return self.get(message=message)

    def get(self, message):
        "Метод для выдачи метрик клиенту"
        return 'ok\n{data}'.format(data=self.metric_dict[message[1]]) + '\n\n'

    def put(self, message):
        """Метод для сохранения метрик от клиента"""
        if message[1] in self.metric_dict.keys():
            self.metric_dict[message[1]].append([message[2], message[3]])
        else:
            self.metric_dict[message[1]] = [[message[2], message[3]]]
        return 'ok\n\n'

    async def handle_echo(self, reader, writer):
        data = await reader.read(1024)  # считывает данные из сокета. writer - для записи в сокет
        message = data.decode()
        # message = message[:-2].split(' ')
        #
        # answer_to_client = self._msg_proccessor(message=message)  # обрабатываем сообщение и либо пишем либо выдаем метрику

        addr = writer.get_extra_info('peername')
        print(addr)
        print('received %r from %r' % (message, addr))

        # writer.write(answer_to_client.encode())
        writer.write(message.encode())
        writer.close()

    def run_server(self):
        """Запускает сервер в вечном цикле"""
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(client_connected_cb=self.handle_echo, host=self.host, port=self.port,
                                    loop=loop)  # передали параметры
        loop.run_until_complete(coro)

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass


serv = Server(host='127.0.0.1', port=5000)
serv.run_server()
