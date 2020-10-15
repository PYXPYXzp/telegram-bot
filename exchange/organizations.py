class BaseExchangerOrganization:
    def __init__(self, currencies: list):
        self.currencies_list = currencies


class Bank(BaseExchangerOrganization):
    ORGANIZATION_NAME = "bank"


class Exchanger(BaseExchangerOrganization):
    ORGANIZATION_NAME = "exchanger"