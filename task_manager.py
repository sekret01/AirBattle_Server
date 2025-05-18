from typing import Union

from database_storage import DataBaseHub


class Tasks:
    """ Класс для определения нужной функции исходя из запроса клиента """

    db_hub = DataBaseHub()
    _commands: dict[str, callable] = {
        'login': db_hub.registrate_new_player,
        'logon': db_hub.logon_profile,
        'check_unique': db_hub.check_login_on_unique,
        'save_statistic': db_hub.save_statistic,
        'update_statistic': db_hub.update_statistic,
        'leaderboard': db_hub.get_leaderboard
    }

    @staticmethod
    def get_command(command: str) -> Union[callable, None]:
        """ Определение функции по команде """
        return Tasks._commands.get(command, None)