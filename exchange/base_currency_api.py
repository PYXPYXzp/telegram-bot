from typing import List

import requests


class BaseCurrencyApi:

    API_URL = ""
    ORGANIZATION_OPTIONS = {}

    def get_data(self) -> dict:
        return requests.get(self.API_URL).json()

    def get_organization_objects(self, data: dict) -> List:
        pass

    def get_organizations_data(self):
        data = self.get_data()
        return self.get_organization_objects(data)

    def parse_currencies(self, currencies):
        pass