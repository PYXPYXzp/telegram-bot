from exchange.privat import PrivatAPI


class ExchangeRates:

    API_OPTIONS = {
        "privat": PrivatAPI()
    }

    def __init__(self, **kwargs):
        self.currencies = kwargs.get("currencies")
        self.organization_type = kwargs.get("organization_type")
        self.time_interval = kwargs.get("time_interval")
        self.api = kwargs.get("api", "finance")

    def _get_api(self) -> object:
        return self.API_OPTIONS[self.api]

    def get_current_exchange_rate(self) -> str:
        api = self._get_api()
        currency_data = api.get_organizations_data()
        return self.generate_message(currency_data)

    def generate_message(self, cur_data: list):
        result = []
        for currency in cur_data:
            result.append(f'{currency.NAME}: bid - {currency.bid}, ask - {currency.ask}')
        return '\n '.join(result)

    def get_graph(self):
        pass