import socket
import threading
import json
import time

IP = "192.168.0.226"
PORT = 9999
BUFF = 4096
COMMANDS = ['login']

def get_command():
    ...


def handle_client(client_socket: socket, address: any):
    with client_socket as sock:


        recv = sock.recv(BUFF).decode('utf-8')

        if len(recv) == 0: command = None
        else: command = json.loads(recv).get("command", None)
        if command is None:
            print("[*] just connect")
            print(f"[*] Disconnect {address[0]}:{address[1]}")
            sock.close()
            return

        print(f"[-] command: {command}")
        if not command in COMMANDS:
            data = json.dumps(False)
            sock.send(data.encode('utf-8'))
            print(f"[*] Disconnect {address[0]}:{address[1]}")
            sock.close()
            return

        if command == 'login':
            str_data = sock.recv(BUFF).decode('utf-8')
            data = json.loads(str_data)
            print(f">> new profile was login")
            print(f">> login: [{data['login']}]")
            print(f">> password: [{data['password']}]")
            data = json.dumps(True)
            sock.send(data.encode('utf-8'))
            print(f"[*] Disconnect {address[0]}:{address[1]}")
            sock.close()
            return

        print(f"[*] Disconnect {address[0]}:{address[1]}")
        sock.close()




def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5)
    print(f"[*] Listening on {IP}:{PORT}")

    while True:
        client, address = server.accept()
        print(f"Accepted connection from {address[0]}:{address[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client, address))
        client_handler.start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("[*] Stop listening")

