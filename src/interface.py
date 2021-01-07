import typing

import requests

import src.exceptions
import src.classes
import utils


class InterfaceManager(object):
    _ynab_token = ''
    _ccapi_token = ''

    def set_tokens(self, ynab_token: str, ccapi_token: str):

        self._ynab_token = ynab_token
        self._ccapi_token = ccapi_token

        if not self._ynab_token:
            raise src.exceptions.ValueIncorrectError(f'ynab_token: {ynab_token}')
        if not self._ccapi_token:
            raise src.exceptions.ValueIncorrectError(f'ccapi_token: {ccapi_token}')

    def get_assets_codes(self) -> typing.List[str]:

        endpoint = 'https://free.currconv.com/api/v7/currencies'

        utils.logger.debug(f'GET {endpoint}')

        r = requests.get(f'{endpoint}?apiKey={self._ccapi_token}')

        utils.logger.debug(f'{r.status_code}: {r.text}')

        if not r.status_code == 200:
            raise src.exceptions.CCAPIError(f'Status code: {r.status_code}')

        return list(r.json()['results'].keys())

    def get_all_budgets(self) -> typing.List[src.classes.Budget]:
        endpoint = 'https://api.youneedabudget.com/v1/budgets'
        headers = {'Authorization': f'Bearer {self._ynab_token}'}

        utils.logger.debug(f'GET {endpoint}')

        r = requests.get(endpoint, headers=headers)

        utils.logger.debug(f'{r.status_code}: {r.text}')

        if not r.status_code == 200:
            raise src.exceptions.CCAPIError(f'Status code: {r.status_code}')

        return [src.classes.Budget(budget_data) for budget_data in r.json()['data']['budgets']]

    def get_accounts(self, budget_id: str) -> typing.List[src.classes.Account]:
        endpoint = f'https://api.youneedabudget.com/v1/budgets/{budget_id}/accounts'
        headers = {'Authorization': f'Bearer {self._ynab_token}'}

        utils.logger.debug(f'GET {endpoint}')

        r = requests.get(endpoint, headers=headers)

        utils.logger.debug(f'{r.status_code}: {r.text}')

        if not r.status_code == 200:
            raise src.exceptions.CCAPIError(f'Status code: {r.status_code}')

        return [src.classes.Account(account_data) for account_data in r.json()['data']['accounts']]

    def get_rate(self, base_asset: str, quote_asset: str) -> float:

        endpoint = f'https://free.currconv.com/api/v7/convert?q={base_asset}_{quote_asset}&compact_ultra'

        utils.logger.debug(f'GET {endpoint}')

        r = requests.get(f'{endpoint}&apiKey={self._ccapi_token}')

        utils.logger.debug(f'{r.status_code}: {r.text}')

        if not r.status_code == 200:
            raise src.exceptions.CCAPIError(f'Status code: {r.status_code}')

        return r.json()['results'][f'{base_asset}_{quote_asset}']['val']

    def post_transaction(self, budget_id: str, account_id: str, date: str, amount: float, payee_name):
        endpoint = f'https://api.youneedabudget.com/v1/budgets/{budget_id}/transactions'
        headers = {'Authorization': f'Bearer {self._ynab_token}'}

        utils.logger.debug(f'POST {endpoint}')

        r = requests.post(endpoint, headers=headers, data={
            'transaction':
                {
                    'account_id': account_id,
                    'date': date,
                    'amount': amount,
                    'payee_name': payee_name,
                    'memo': 'via YNAB-autoconverter'
                }
        })

        utils.logger.debug(f'{r.status_code}: {r.text}')

        if not r.status_code == 201:
            raise src.exceptions.CCAPIError(f'Status code: {r.status_code}')


interface_manager = InterfaceManager()
