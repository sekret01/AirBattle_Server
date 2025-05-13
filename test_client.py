import json
import socket

HOST = "192.168.0.226"
PORT = 9999

if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print('connect was success')
    while True:
        a = input('> ')
        if a == 'q': break

        elif a == 'logon':
            data = {'command': 'logon', 'data': {"login": "sekret", "password": "qwerty1234"}}

        elif a == 'login':
            data = {'command': 'login', 'data': {"login": "sekret", "password": "qwerty1234"}}

        elif a == 'unique':
            data = {'command': 'check_unique', 'data': {'login': 'player_1'}}

        elif a == '':
            data = 'NoneFunc'

        else:
            data = a

        client.send(json.dumps(data).encode())
        try:
            answer = client.recv(4096)
            print(json.loads(answer.decode()))
        except Exception as ex:
            print(f"[ERROR] -- {ex}")

    client.close()