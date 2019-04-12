import json

import unittest
from unittest.mock import patch

from currency import FinanceAPI, ExchangeRates


class TestFinanceAPI(unittest.TestCase):

    def setUp(self):
        with open('test_data_api.json') as f:
            self.api_data = json.load(f)

    @patch.object(FinanceAPI, 'get_data')
    def test_get_rate_data(self, get_data_mock):
        get_data_mock.return_value = self.api_data
        rates = ExchangeRates()
        print(rates.get_avg_message())
        self.assertIsNotNone(rates.get_avg_message())


if __name__ == '__main__':
    unittest.main()
