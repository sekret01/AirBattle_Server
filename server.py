import socket


HOST = "192.168.0.226"
PORT = 9999
BUFF = 4096


class Server:
    """ Класс сокет-сервера для подключений игроков-клиентов """

    def __init__(self, limit: int):
        self.server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.limit: int = limit
        self.closed: bool = True

    def setup_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.closed = False

    def start_listen(self):
        if self.closed: self.setup_socket()
        self.server.listen(self.limit)

    def stop_listen(self):
        self.server.close()
        self.closed = True
        # self.server.shutdown(socket.SHUT_WR)

