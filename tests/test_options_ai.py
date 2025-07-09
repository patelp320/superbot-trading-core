import unittest
from unittest.mock import patch
import pandas as pd
import types
import sys

# Provide dummy yfinance if needed
if 'yfinance' not in sys.modules:
    yf_dummy = types.ModuleType('yfinance')
    yf_dummy.download = lambda *args, **kwargs: pd.DataFrame()
    sys.modules['yfinance'] = yf_dummy

import options_ai

class OptionsAiTestCase(unittest.TestCase):
    @patch('options_ai.yf.download')
    def test_filter_candidate_true(self, mock_download):
        data = {
            'Open': [10]*20,
            'Close': [10]*19 + [11],
            'Volume': [1500000]*19 + [2500000]
        }
        df = pd.DataFrame(data)
        mock_download.return_value = df
        self.assertTrue(options_ai.filter_candidate('FAKE'))

    @patch('options_ai.yf.download')
    def test_filter_candidate_false_low_volume(self, mock_download):
        data = {
            'Open': [10]*20,
            'Close': [10]*20,
            'Volume': [1000]*20
        }
        df = pd.DataFrame(data)
        mock_download.return_value = df
        self.assertFalse(options_ai.filter_candidate('FAKE'))

if __name__ == '__main__':
    unittest.main()
