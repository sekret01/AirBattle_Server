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
        else:
            client.send(a.encode())

    client.close()