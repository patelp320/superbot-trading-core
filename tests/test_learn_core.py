import unittest
from unittest.mock import patch
import pandas as pd
import sys
import types

# Provide a dummy yfinance module if it's not installed
if 'yfinance' not in sys.modules:
    yf_dummy = types.ModuleType('yfinance')
    yf_dummy.download = lambda *args, **kwargs: pd.DataFrame()
    sys.modules['yfinance'] = yf_dummy

if 'requests' not in sys.modules:
    requests_dummy = types.ModuleType('requests')
    requests_dummy.get = lambda *args, **kwargs: types.SimpleNamespace(text='S')
    sys.modules['requests'] = requests_dummy

import learn_core

class LearnCoreTestCase(unittest.TestCase):
    @patch('learn_core.yf.download')
    def test_low_volume_returns_none(self, mock_download):
        df = pd.DataFrame({
            'Close': [10, 11, 12, 13, 14],
            'Volume': [1000, 2000, 1500, 1200, 1300]
        })
        mock_download.return_value = df
        result = learn_core.process_ticker('FAKE')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
