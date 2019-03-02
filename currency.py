import requests

class Currency:
    FINANCE_API_URL = 'http://resources.finance.ua/ru/public/currency-cash.json'
    CURRENCY_EXCHANGE = 2
    BANKS = 1
    USD = 'USD'
    EUR = 'EUR'


    def __init__(self):
        self.dict_of_currency_in_banks = {self.USD: [], self.EUR: []}
        self.dict_of_currency_in_exchanges = {self.USD: [], self.EUR: []}
        self.currency_by_organizations_types = {
            self.BANKS: self.dict_of_currency_in_banks, 
            self.CURRENCY_EXCHANGE: self.dict_of_currency_in_exchanges
        }
    
    def get_average_currency(self):
        currency_data = self.get_currency_data()
        self.parse_currency_data(currency_data)
        return self.get_message()
        
    
    def get_currency_data(self):
        return requests.get(self.FINANCE_API_URL).json()

    def parse_currency_data(self, currency_data):
        organizations_currency = currency_data.get('organizations')
        if not organizations_currency:
            return None
        for organization in organizations_currency:
            self.add_to_dict_by_organization_type(organization)
    

    def add_to_dict_by_organization_type(self, organization):
        organization_type = organization.get('orgType')
        currencies_USD = organization['currencies'].get(self.USD)
        currencies_EUR = organization['currencies'].get(self.EUR)
        self.currency_by_organizations_types[organization_type][self.USD].append(currencies_USD)
        self.currency_by_organizations_types[organization_type][self.EUR].append(currencies_EUR)
    
    def get_message(self):
        
        exchanges_ask_eur = self.get_avg_сurrency([float(x['ask']) for x in self.currency_by_organizations_types[self.CURRENCY_EXCHANGE][self.EUR] if x])
        exchanges_bid_eur = self.get_avg_сurrency([float(x['bid']) for x in self.currency_by_organizations_types[self.CURRENCY_EXCHANGE][self.EUR] if x])
        exchanges_ask_usd = self.get_avg_сurrency([float(x['ask']) for x in self.currency_by_organizations_types[self.CURRENCY_EXCHANGE][self.USD] if x])
        exchanges_bid_usd = self.get_avg_сurrency([float(x['bid']) for x in self.currency_by_organizations_types[self.CURRENCY_EXCHANGE][self.USD] if x])
        banks_ask_eur = self.get_avg_сurrency([float(x['ask']) for x in self.currency_by_organizations_types[self.BANKS][self.EUR] if x])
        banks_bid_eur = self.get_avg_сurrency([float(x['bid']) for x in self.currency_by_organizations_types[self.BANKS][self.EUR] if x])
        banks_ask_usd = self.get_avg_сurrency([float(x['ask']) for x in self.currency_by_organizations_types[self.BANKS][self.USD] if x])
        banks_bid_usd = self.get_avg_сurrency([float(x['bid']) for x in self.currency_by_organizations_types[self.BANKS][self.USD] if x])
        exchanges = f'Менялы EUR покупка {exchanges_bid_eur:.2f} продажа {exchanges_ask_eur:.2f}, USD покупка {exchanges_bid_usd:.2f} продажа {exchanges_ask_usd:.2f}' + '\n'
        banks = f'Банки EUR покупка {banks_bid_eur:.2f} продажа {banks_ask_eur:.2f}, USD покупка {banks_bid_usd:.2f} продажа {banks_ask_usd:.2f}'
        return exchanges + '\n' + banks

    
    def get_avg_сurrency(self, currency_list):
        return sum(currency_list) / float(len(currency_list))

