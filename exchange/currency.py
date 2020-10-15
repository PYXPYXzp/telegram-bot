class BaseCurrency:

    NAME = ""

    def __init__(self, bid: float, ask: float):
        self.bid = bid
        self.ask = ask


class DollarCurrency(BaseCurrency):
    NAME = "USD"


class EuroCurrency(BaseCurrency):
    NAME = "EUR"


class YuanCurrency(BaseCurrency):
    NAME = "CNY"


class RublCurrency(BaseCurrency):
    NAME = "RUR"


class BitCoinCurrency(BaseCurrency):
    NAME = "BTC"
