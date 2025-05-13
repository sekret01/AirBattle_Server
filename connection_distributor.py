import socket
import threading
from client_handler import ClientHandler
from server import Server


class NewConnectionDistributor:
    """ Класс для хранения подключений и распределения их по потокам """

    def __init__(self):
        self.limit = 10
        self.server: Server = Server(self.limit)
        self.main_server_thread: threading.Thread | None = None
        self.stop_main_loop: bool = False

        self.client_list: list[socket.socket] = []  # возможно сделать отдельный класс для хранения
        self.threads: dict[str, threading.Thread] = {}


    def _start_accept_connections(self) -> None:
        """ Функция для принятия новых подключений """

        self.server.start_listen()
        print(f"[*S] -- начало прослушивания")

        while True:
            try:
                client, address = self.server.server.accept()
                print(f"[*S] -- новое подключение - [{address[0]}:{address[1]}]")

                client_address = f"{address[0]}:{address[1]}"
                client_handler = ClientHandler(
                    client=client,
                    address=client_address,
                    client_list=self.client_list,
                    threads_dict=self.threads
                )
                client_handler_thread = threading.Thread(name='client_address', target=client_handler.start_loop)
                client_handler_thread.start()

                self.client_list.append(client)
                self.threads[client_address] = client_handler_thread

            except OSError:
                print(f"[**S] -- сервер закрыт")
                return


    def start(self):
        """ Старт прослушивания подключений. Функция будет вызвана в отдельном потоке """
        self.main_server_thread = threading.Thread(name='main server thread', target=self._start_accept_connections, daemon=True)
        self.main_server_thread.start()

    def stop(self):
        """ Остановить поток с функцией прослушивания подключений """
        if self.main_server_thread and self.main_server_thread.is_alive():
            self.server.stop_listen()
            for client in self.client_list:
                client.close()

        else: print(self.main_server_thread.is_alive())
