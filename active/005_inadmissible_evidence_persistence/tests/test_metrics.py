import unittest
from inadmissible_g0.metrics import bootstrap_ci

class MetricTests(unittest.TestCase):
    def test_bootstrap_positive(self):
        lo, hi = bootstrap_ci([.03, .05, .08, .10], seed=2, n_boot=500)
        self.assertGreater(lo, 0)
        self.assertGreaterEqual(hi, lo)

if __name__ == "__main__":
    unittest.main()
