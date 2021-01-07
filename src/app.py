import utils
import src.exceptions
import src.interface
import re


class Application(object):
    # Init parameters
    _YNAB_TOKEN = ''
    _CCAPI_TOKEN = ''

    # Attributes
    ynab_token = ''
    ccapi_token = ''

    budgets = []

    def __init__(self):

        # 0:
        # ...

        # 1:
        self.initialize_parameters()

        # 2:
        self.parse_parameters()
        src.interface.interface_manager.set_tokens(self.ynab_token, self.ccapi_token)

        # 3:
        self.get_budgets()

        for budget in self.budgets:

            # 4:
            budget.get_accounts()

            # 5:
            budget.get_set_accounts_rate()

            # 6:
            budget.calculate_post_diff()

    def initialize_parameters(self):

        try:
            self._YNAB_TOKEN = getattr(utils.config, 'YNAB_TOKEN')
        except AttributeError:
            try:
                self._YNAB_TOKEN = utils.config['COMMON']['YNAB_TOKEN']
            except KeyError:
                raise src.exceptions.ConfigValueNotFoundError('YNAB_TOKEN')

        try:
            self._CCAPI_TOKEN = getattr(utils.config, 'CCAPI_TOKEN')
        except AttributeError:
            try:
                self._CCAPI_TOKEN = utils.config['COMMON']['CCAPI_TOKEN']
            except KeyError:
                raise src.exceptions.ConfigValueNotFoundError('CCAPI_TOKEN')

    def parse_parameters(self):

        self.ynab_token = str(self._YNAB_TOKEN)
        self.ccapi_token = str(self._CCAPI_TOKEN)

        if not self.ynab_token:
            raise src.exceptions.NoTokenError('YNAB_TOKEN')

        if not self.ccapi_token:
            raise src.exceptions.NoTokenError('CCAPI_TOKEN')

    def get_budgets(self):

        self.budgets = src.interface.interface_manager.get_all_budgets()

        if not self.budgets:
            raise src.exceptions.ValueIncorrectError(f'len(budgets): {len(self.budgets)}')

