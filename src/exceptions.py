import utils


class ConfigValueNotFoundError(utils.LoggedBaseException):
    pass


class ValueIncorrectError(utils.LoggedBaseException):
    pass


class NoTokenError(utils.LoggedBaseException):
    pass


class CCAPIError(utils.LoggedBaseException):
    pass


class AccountSettingError(utils.LoggedBaseException):
    pass
