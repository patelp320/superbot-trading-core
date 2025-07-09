import unittest
import smart_position_sizer

class SmartPositionSizerTestCase(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(smart_position_sizer.size_position(10000, 1.0), 100.0)

    def test_bounds(self):
        self.assertEqual(smart_position_sizer.size_position(10000, 3.0), 200.0)
        self.assertEqual(smart_position_sizer.size_position(10000, 0.1), 50.0)

if __name__ == '__main__':
    unittest.main()
