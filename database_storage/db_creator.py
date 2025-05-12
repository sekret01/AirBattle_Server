from .db_config import DataBaseConfig
import sqlite3


class DataBaseCreator(DataBaseConfig):
    """ Класс используется для создания БД """

    def __init__(self):
        super().__init__()

    @DataBaseConfig.connection
    def _create_database(self, cursor: sqlite3.Cursor):
        create_account_table = """
        CREATE TABLE IF NOT EXISTS Accounts (
        login text NOT NULL PRIMARY KEY,
        password text NOT NULL
        )
        """
        
        create_statistic_table = """
        CREATE TABLE IF NOT EXISTS Statistic (
        login text,
        all_rounds int,
        win_rounds int,
        points int,
        FOREIGN KEY (login) REFERENCES Accounts (login)
        )
        """
        
        cursor.execute(create_account_table)
        cursor.execute(create_statistic_table)

        print(f"[CREATOR] -- tables was create")
    
    @DataBaseConfig.connection
    def _drop_tables(self, cursor: sqlite3.Cursor):
        cursor.execute("""DROP TABLE Accounts""")
        cursor.execute("""DROP TABLE Statistic""")

        print("[CREATOR] -- tables was dropped")
    
    
