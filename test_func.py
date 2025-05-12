from database_storage import DataBaseHub
from database_storage import DataBaseCreator
from server import Server
from connection_distributor import NewConnectionDistributor

ncd = NewConnectionDistributor()
# server = Server(limit=1)
while True:
    a = input('> ')
    if a == 'q':
        break

    if a == 's':
        ncd.start()

    if a == 'b':
        ncd.stop()

    if a == 'l':
        print(ncd.threads)
        print(ncd.client_list)


print("[MAIN-TEST] -- script was go")
