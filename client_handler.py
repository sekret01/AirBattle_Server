import socket
import threading



class ClientHandler:
    """ Класс обработки одного клиента"""
    
    def __init__(
            self,
            client: socket.socket,
            address: str,
            client_list: list[socket.socket],
            threads_dict: dict[str, threading.Thread]
    ):
        self.client: socket.socket = client
        self.address: str = address
        self.buffer_size = 4096

        self.client_list: list[socket.socket] = client_list  # возможно сделать отдельный класс для хранения
        self.threads_dict: dict[str, threading.Thread] = threads_dict  # возможно сделать отдельный класс для хранения

    def start_loop(self):
        with self.client as sock:
            while True:
                recv = sock.recv(self.buffer_size)
                if not recv: break
                print(f"client [{self.address}] :: {recv}")

        print(f"client [{self.address}] disconnect")
        self.client_list.remove(self.client)
        self.threads_dict.pop(self.address)

