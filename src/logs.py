import datetime


class CustomLogger:
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

    green = "\033[92m"

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __get_time(self):
        return datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]

    def debug(self, msg: str):
        print(f"{self.grey}[DEB] {self.__get_time()} : {msg}{self.reset}")

    def info(self, msg: str):
        print(f"{self.green}[INF] {self.__get_time()} : {msg}{self.reset}")

    def warning(self, msg: str):
        print(f"{self.yellow}[WAR] {self.__get_time()} : {msg}{self.reset}")

    def error(self, msg: str):
        print(f"{self.red}[ERR] {self.__get_time()} : {msg}{self.reset}")

    def critical(self, msg: str):
        print(f"{self.bold_red}[CRT] {self.__get_time()} : {msg}{self.reset}")


LOGGER = CustomLogger()

if __name__ == '__main__':
    LOGGER.debug("debug")
    LOGGER.info("info")
    LOGGER.warning("warning")
    LOGGER.error("error")
    LOGGER.critical("critical")
