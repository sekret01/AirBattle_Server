import configparser


class ConfigGetter:
    """ Класс для предоставления конфигураций программы модулям """

    conf_path = "configs/config.ini"
    parser = configparser.ConfigParser()

    @staticmethod
    def _read() -> None:
        ConfigGetter.parser.read(ConfigGetter.conf_path)

    @staticmethod
    def get_host() -> tuple[str,int]:
        ConfigGetter._read()
        ip: str = ConfigGetter.parser["SERVER"]["IP"]
        port: int = int(ConfigGetter.parser["SERVER"]["PORT"])
        return ip, port

