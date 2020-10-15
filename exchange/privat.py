from typing import List

from exchange.currency import DollarCurrency, EuroCurrency, RublCurrency
from exchange.base_currency_api import BaseCurrencyApi


class PrivatAPI(BaseCurrencyApi):
    API_URL = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"

    CURRENCIES_CLASSES = {
        DollarCurrency.NAME: DollarCurrency,
        EuroCurrency.NAME: EuroCurrency,
        RublCurrency.NAME: RublCurrency,
    }

    def get_organization_objects(self, data) -> List:
        result = []
        for currency in data:
            currency_class = self._get_currency_class(currency)
            if currency_class:
                result.append(currency_class(bid=currency.get('buy'), ask=currency.get('sale')))
        return result

    def _get_currency_class(self, currency):
        currency_name = currency.get("ccy")
        currency_class = self.CURRENCIES_CLASSES.get(currency_name)
        return currency_class
