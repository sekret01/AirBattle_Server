import sqlite3


class DataBaseConnectError(Exception):
    def __init___(self, message: str | None = None, python_exception_info: str | None = None):
        super().__init__(message)
        self.message = message if message else "unknown"
        self.python_exception_info = python_exception_info if python_exception_info else "unknown"
        
    def __repr__(self):
        return f"Connect error: {self.message}\n============  PYTHON ==============\n{self.python_exception_info}"
    
    def __str__(self):
        return f"Connect error: {self.message}\n============  PYTHON ==============\n{self.python_exception_info}"
        


class DataBaseConfig:
    """ Базовый класс для работы с БД. Использовать как родительский """
    
    def __init__(self):
        self.DB_PATH: str = "database_storage/database.sql"
        self.status_connect: bool = False
        self.setup_connection()
        
    def setup_connection(self, message_output: bool = False):
        try:
            con = sqlite3.connect(self.DB_PATH)
            con.close()
            self.status_connect = True
        except Exception as ex:  # sqlite3Exception
            self.status_connect = False
            if message_output:
                print(ex)
    
    
    def connection(func: callable):
        """ использовать как декоратор """

        
        def wrapped(self, *args, **kwargs):
            if not self.status_connect:
                raise Exception("database connect status is FALSE. Try to reload connect status (<setup_connection>).") # raise DataBaseConnectError("database connect status is FALSE. Try to reload connect status (<setup_connection>).")

            con = sqlite3.connect(self.DB_PATH)
            cursor = con.cursor()

            try:
                res = func(self, cursor=cursor, *args, **kwargs)
                con.commit() 
            except Exception as ex:
                print("ERROR: ", ex)
                res = ex
            con.close()
            return res
        
        return wrapped
        
        

            
            
            
