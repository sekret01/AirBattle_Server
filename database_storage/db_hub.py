from .db_config import DataBaseConfig
# from .profile_data import ProfileData
import sqlite3


class DataBaseHub(DataBaseConfig):
    """ класс для работы с БД """
    
    def __init__(self):
        super().__init__()

    @DataBaseConfig.connection
    def check_login_on_unique(self, cursor: sqlite3.Cursor, login: str) -> dict:
        """ Проверка уникальности логина """

        if login == "": return {'status': False, 'message': 'empty login'}
        cursor.execute("""SELECT login FROM Accounts""")
        all_logins: list[str] = [log[0] for log in cursor.fetchall()]
        if login in all_logins:
            return {'status': False, 'message': 'login already exists'}
        return {'status': True, 'message': 'ок'}

    @DataBaseConfig.connection
    def registrate_new_player(self, cursor: sqlite3.Cursor, login: str, password: str) -> dict:
        """ Регистрация нового игрока """

        if login == "" or password == "": return {'status': False, 'message': 'empty fields'}
        if not self.check_login_on_unique(login=login)['status']: return {'status': False, 'message': 'login already exists'}

        try:
            cursor.execute(f"""INSERT INTO Accounts VALUES ('{login}', '{password}')""")
            cursor.execute(f"""INSERT INTO Statistic VALUES ('{login}', 0, 0, 0)""")
        except Exception as ex:
            return {'status': False, 'message': f'[LOGIN] -- ERROR: {ex}'}
        return {'status': True, 'message': 'ok'}

    @DataBaseConfig.connection
    def logon_profile(self, cursor: sqlite3.Cursor, login: str, password: str) -> dict:
        """ Получение данных профиля и отправка статистики при правильном пароле """

        cursor.execute(f"""SELECT * FROM Accounts WHERE login = '{login}'""")
        acc_data = cursor.fetchall()  # [('login', 'password')]
        if len(acc_data) == 0:
            return {'status': False, 'message': f'no login [{login}] in database', 'profile_data': None}
        acc_data = acc_data[0]
        _login = acc_data[0]
        _password = acc_data[1]

        if password != _password:
            return {'status': False, 'message': f'Incorrect password', 'profile_data': None}
        else:
            cursor.execute(f"""SELECT * FROM Statistic WHERE login = '{login}'""")
            acc_statistic = cursor.fetchall()[0]  # [('login', 0, 0, 0)]
            _all_rounds = acc_statistic[0]
            _win_rounds = acc_statistic[1]
            _points = acc_statistic[2]

            return {
                'status': True,
                'message': 'authorization completed',
                'profile_data': {
                    'login': _login,
                    'all_rounds': _all_rounds,
                    'win_rounds': _win_rounds,
                    'points': _points
                }
            }

    @DataBaseConfig.connection
    def delete_account(self, cursor: sqlite3.Cursor, login: str) -> dict:
        """ Удаление игрового аккаунта """

        try:
            cursor.execute(f"""DELETE FROM Accounts WHERE login = '{login}'""")
            cursor.execute(f"""DELETE FROM Statistic WHERE login = '{login}'""")
            return {'status': True, 'message': f'account [{login}] was deleted'}
        except Exception as ex:
            return {'status': False, 'message': f'[DELETE-ACCOUNT] -- ERROR: {ex}'}

    @DataBaseConfig.connection
    def update_statistic(
            self,
            cursor: sqlite3.Cursor,
            login: str,
            all_rounds: int = 0,
            win_rounds: int = 0,
            points: int = 0
    ) -> dict:
        """ Обновление значений статистики игрока """

        try:
            cursor.execute(f"""
            UPDATE Statistic
            SET all_rounds = all_rounds + {all_rounds},
            win_rounds = win_rounds + {win_rounds},
            points = points + {points}
            WHERE login = '{login}'
            """)
            return {'status': True, 'message': 'statistic was upgraded'}
        except Exception as ex:
            return {'status': False, 'message': f'[UPDATE-STATISTIC] -- ERROR: {ex}'}




        
    