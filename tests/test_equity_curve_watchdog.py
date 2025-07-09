import unittest

import equity_curve_watchdog

class EquityCurveWatchdogTestCase(unittest.TestCase):
    def test_alert_triggered(self):
        history = [100, 120, 110, 80]
        self.assertTrue(equity_curve_watchdog.monitor_equity_curve(history, 0.2))

    def test_no_alert(self):
        history = [100, 105, 103]
        self.assertFalse(equity_curve_watchdog.monitor_equity_curve(history, 0.2))

if __name__ == "__main__":
    unittest.main()
