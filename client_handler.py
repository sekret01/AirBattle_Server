import json
import socket
import threading

from task_manager import Tasks


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
                try:
                    recv = sock.recv(self.buffer_size)
                except ConnectionAbortedError:
                    print(f"client [{self.address}] :: connection was close")
                    break

                if not recv:
                    break

                data = json.loads(recv.decode())
                if not self._check_recv(data):
                    sock.send(json.dumps({'status': False, 'message': 'data is not correct'}).encode())
                    continue

                print(f"client [{self.address}] :: get command -> [{data['command']}]")
                func = Tasks.get_command(data['command'])
                if not func:
                    print(f"client [{self.address}] :: command [{data['command']}] -> NOT FOUND")
                    sock.send(json.dumps({'status': False, 'message': 'command not found'}).encode())

                try:
                    result = func(**data['data'])
                    sock.send(json.dumps(result).encode())
                    print(f"client [{self.address}] :: command [{data['command']}] was done")

                except Exception as ex:
                    print(f"client [{self.address}] :: command [{data['command']}] -> ERROR\n[{ex}]")
                    sock.send(json.dumps({'status': False, 'message': 'command closed with error'}).encode())

        print(f"client [{self.address}] disconnect")
        self.client_list.remove(self.client)
        self.threads_dict.pop(self.address)

    @staticmethod
    def _check_recv(recv: any):
        if type(recv) != dict: return False
        if not recv.get('command', None): return False
        if not recv.get("data", None): return False
        if type(recv["data"]) != dict: return False

        return True

