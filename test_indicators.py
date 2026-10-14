import unittest
from nexora_engine.indicators import ema, rsi
from nexora_engine.signal_engine import analyze

class IndicatorTests(unittest.TestCase):
    def test_ema_needs_enough_data(self):
        self.assertIsNone(ema([1,2,3], 5))
    def test_ema_increasing(self):
        self.assertGreater(ema(list(range(1,31)), 9), ema(list(range(1,31)), 21))
    def test_rsi_uptrend(self):
        self.assertGreater(rsi(list(range(1,40))), 90)
    def test_short_data_is_no_signal(self):
        self.assertEqual(analyze([{"close":1} for _ in range(20)])["signal"], "NO SIGNAL")

if __name__ == "__main__":
    unittest.main()
