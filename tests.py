import json

import unittest
from unittest.mock import patch

from currency import FinanceAPI


class TestFinanceAPI(unittest.TestCase):

    def setUp(self):
        with open('test_data_api.json') as f:
            self.api_data = json.load(f)

    @patch.object(FinanceAPI, 'get_data')
    def test_get_rate_data(self, get_data_mock):
        get_data_mock.return_value = self.api_data
        finance = FinanceAPI()
        self.assertIsNotNone(finance.get_rate_data())


if __name__ == '__main__':
    unittest.main()
