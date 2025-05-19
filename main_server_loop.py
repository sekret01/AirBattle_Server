from database_storage import DataBaseHub
from database_storage import DataBaseCreator
from server import Server
from connection_distributor import NewConnectionDistributor
import os

VERSION = "0.1.3"

def test_server():
    os.system('cls')
    print(f"VERSION: {VERSION}\nCOMMANDS: \n  > start - start server listening\n  > stop - stop server listening\n  > exit - exit program\n{'=' * 40}\n")
    ncd = NewConnectionDistributor()
    while True:
        a = input('')
        if a == 'exit':
            break

        if a == 'start':
            ncd.start()

        if a == 'stop':
            ncd.stop()

        if a == 'list':
            print(ncd.threads)
            print(ncd.client_list)


    print("[MAIN-TEST] -- script stopped")


def set_bd():
    db_creator = DataBaseCreator()
    db_creator._create_database()


if __name__ == "__main__":
    # set_bd()
    test_server()
