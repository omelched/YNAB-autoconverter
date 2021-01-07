import re
from time import strftime

import utils
import src.interface
import src.exceptions


class JSONParsable(object):

    def __init__(self, *init_structure, **kwargs):
        for dictionary in init_structure:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


class Budget(JSONParsable):
    name = None
    id = None
    accounts = []
    currency_format = {}

    def get_accounts(self):

        accounts = src.interface.interface_manager.get_accounts(self.id)

        if not accounts:
            utils.logger.warning(f'No accounts on budget {self.name}!')
            return

        for account in accounts:
            if str(account.note).find('@parsable') == -1:
                utils.logger.info(f'Account {account.name} is not parsable. Pop it!')
                continue

            if str(account.note).find('@asset:') == -1:
                raise src.exceptions.AccountSettingError('\"@asset:\" is missing')

            if str(account.note).find('@value:') == -1:
                raise src.exceptions.AccountSettingError('\"@value:\" is missing')

            account.asset = re.search(r'@asset:(.{3})', account.note).group(1)
            account.value = int(re.search(r'@value:(\d*)', account.note).group(1))
            account.budget = self
            account.balance = account.balance / 1000
            self.accounts.append(account)

    def get_set_accounts_rate(self):

        for account in self.accounts:
            account.get_set_account_rate()

    def calculate_post_diff(self):

        for account in self.accounts:
            account.calculate_post_diff()

    @property
    def get_asset_code(self):
        return self.currency_format['iso_code']

    def __str__(self):
        return self.name


class Account(JSONParsable):
    name = None
    id = None
    note = None
    balance = .0
    asset = ''
    value = 0
    rate = .0
    budget = None

    def get_set_account_rate(self):
        self.rate = src.interface.interface_manager.get_rate(self.asset, self.budget.get_asset_code)

    def calculate_post_diff(self):
        diff = self.balance - self.rate * self.value

        if not abs(diff / self.balance) > 0.005:
            utils.logger.info('Diff lower than 0.5%!')

        self.post_diff(diff)

    def post_diff(self, amount: float, payee_name: str = 'Фиксируем прибыль'):
        src.interface.interface_manager.post_transaction(self.budget.id,
                                                         self.id,
                                                         strftime("%Y-%m-%d"),
                                                         int(amount * 100) * 10,
                                                         payee_name)

    def __str__(self):
        return f'{self.name} on {self.budget.name}'
