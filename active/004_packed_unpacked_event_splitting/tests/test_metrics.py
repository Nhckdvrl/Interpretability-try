import unittest
from packed_unpacked_g0.metrics import bootstrap_ci

class MetricTests(unittest.TestCase):
    def test_bootstrap_positive(self):
        lo, hi = bootstrap_ci([0.1, 0.2, 0.3, 0.4], seed=1, n_boot=500)
        self.assertGreater(lo, 0)
        self.assertGreaterEqual(hi, lo)

if __name__ == "__main__":
    unittest.main()
