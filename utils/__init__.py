import os
import configparser

from utils.log_handling import logger


class LoggedBaseException(BaseException):
    logger = logger

    def __init__(self, message: str = None):
        super().__init__(message)

        self.logger.error(str(self))

    def __str__(self):
        return str(self.__class__).split('\'')[1]


class Config(configparser.ConfigParser):
    if 'HEROKU' in list(os.environ.keys()):
        ON_HEROKU = bool(os.environ['HEROKU'])
    else:
        ON_HEROKU = False

    if 'UNSTABLE' in list(os.environ.keys()):
        UNSTABLE = bool(os.environ['UNSTABLE'])
    else:
        UNSTABLE = False

    if 'TESTING' in list(os.environ.keys()):
        PRODUCT = not bool(os.environ['TESTING'])
    else:
        PRODUCT = True

    def __init__(self):
        super().__init__()
        self.read('CONFIG.cfg')


config = Config()
