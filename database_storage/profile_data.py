# может быть удобен при обработке данных перед отправлением клиенту,
# пока что пусть будет

class ProfileData:
    """ Класс для хранения данных о пользователе """
    def __init__(
            self,
            login: str,
            password: str,
            all_rounds: int,
            win_rounds: int,
            points: int
    ):
        self.login = login
        self.password = password
        self.all_rounds = all_rounds
        self.win_rounds = win_rounds
        self.points = points

