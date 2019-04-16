import requests


class BaseCurrency:

    NAME = ''

    def __init__(self, bid: float, ask: float):
        self.bid = bid
        self.ask = ask


class DollarCurrency(BaseCurrency):
    NAME = 'USD'


class EuroCurrency(BaseCurrency):
    NAME = 'EUR'


class YuanCurrency(BaseCurrency):
    NAME = 'CNY'


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BaseExchangerOrganization:

    def __init__(self, currencies: list):
        self.currencies_list = currencies


class Bank(BaseExchangerOrganization):
    ORGANIZATION_NAME = 'bank'


class Exchanger(BaseExchangerOrganization):
    ORGANIZATION_NAME = 'exchanger'


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class BaseCurrencyApi:

    API_URL = ''
    ORGANIZATION_OPTIONS = {}

    def get_data(self) -> dict:
        return requests.get(self.API_URL).json()

    def get_organization_objects(self, data: dict):
        pass

    def get_organizations_data(self):
        data = self.get_data()
        return self.get_organization_objects(data)

    def parse_currencies(self, currencies):
        pass


class FinanceAPI(BaseCurrencyApi):

    API_URL = 'http://resources.finance.ua/ru/public/currency-cash.json'
    ORGANIZATION_OPTIONS = {
        1: Bank,
        2: Exchanger
    }
    CURRENCIES_CLASSES = [DollarCurrency, EuroCurrency, YuanCurrency]

    def get_organization_objects(self, data: dict) -> dict:
        organization_objects = []
        organizations_data = data.get('organizations')
        for org_data in organizations_data:
            currencies = self.parse_currencies(currencies=org_data['currencies'])
            organization_class = self.ORGANIZATION_OPTIONS[org_data['orgType']]
            organization_objects.append(organization_class(currencies))
        return organization_objects

    def parse_currencies(self, currencies: dict) -> list:
        currencies_result = []
        if currencies:
            for currency_class in self.CURRENCIES_CLASSES:
                currency_api_data = currencies.get(currency_class.NAME)
                if currency_api_data:
                    currencies_result.append(
                        currency_class(
                            bid=currency_api_data['bid'],
                            ask=currency_api_data['ask']
                        )
                    )
        return currencies_result

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ExchangeRates:

    API_OPTIONS = {
        'finance': FinanceAPI(),
    }

    def __init__(self, **kwargs):
        self.currencies = kwargs.get('currencies')
        self.organization_type = kwargs.get('organization_type')
        self.time_interval = kwargs.get('time_interval')
        self.api = kwargs.get('api', 'finance')

    def _get_api(self) -> object:
        return self.API_OPTIONS[self.api]

    def get_avg_message(self) -> str:
        api = self._get_api()
        organizations_data = api.get_organizations_data()
        return self.generate_avg_message(org_data=organizations_data)

    def generate_avg_message(self, org_data):
        exchanges = (
            f"Менялы \nEUR покупка {self.get_average_currency(org_data=org_data, currency_name='EUR', exchange_type='exchanger', transaction_type='bid')} "
            f"продажа {self.get_average_currency(org_data=org_data, currency_name='EUR', exchange_type='exchanger', transaction_type='ask')} \n"
            f"USD покупка {self.get_average_currency(org_data=org_data, currency_name='USD', exchange_type='exchanger', transaction_type='bid')} "
            f"продажа {self.get_average_currency(org_data=org_data, currency_name='USD', exchange_type='exchanger', transaction_type='ask')} \n"
            f"CNY покупка {self.get_average_currency(org_data=org_data, currency_name='CNY', exchange_type='exchanger', transaction_type='bid')} "
            f"продажа {self.get_average_currency(org_data=org_data, currency_name='CNY', exchange_type='exchanger', transaction_type='ask')}\n"
        )
        banks = (
            f"Банки \nEUR покупка {self.get_average_currency(org_data=org_data, currency_name='EUR', exchange_type='bank', transaction_type='bid')} "
            f"продажа {self.get_average_currency(org_data=org_data, currency_name='EUR', exchange_type='bank', transaction_type='ask')} \n"
            f"USD покупка {self.get_average_currency(org_data=org_data, currency_name='USD', exchange_type='bank', transaction_type='bid')} "
            f"продажа {self.get_average_currency(org_data=org_data, currency_name='USD', exchange_type='bank', transaction_type='ask')} \n"
            f"CNY покупка {self.get_average_currency(org_data=org_data, currency_name='CNY', exchange_type='bank', transaction_type='bid')} "
            f"продажа {self.get_average_currency(org_data=org_data, currency_name='CNY', exchange_type='bank', transaction_type='ask')}"
        )
        return exchanges + '\n' + banks

    def get_average_currency(
        self,
        org_data: list,
        currency_name: str,
        exchange_type: str,
        transaction_type: str,
    ):
        default_value = 0.0
        result_list = []
        for organization in org_data:
            if exchange_type == organization.ORGANIZATION_NAME:
                for currency in organization.currencies_list:
                    if currency_name == currency.NAME:
                        result_list.append(
                            float(getattr(currency, transaction_type))
                        )
        if len(result_list):
            return round(get_avg_сurrency(result_list), 2)
        return default_value

    def get_graph(self):
        pass


def get_avg_сurrency(currency_list):
    return sum(currency_list) / float(len(currency_list))
