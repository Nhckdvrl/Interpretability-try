import unittest
from packed_unpacked_g0.metrics import bootstrap_ci, threshold_auc, max_monotonicity_violation

class MetricTests(unittest.TestCase):
    def test_bootstrap_positive(self):
        lo, hi = bootstrap_ci([0.1, 0.2, 0.3, 0.4], seed=1, n_boot=500)
        self.assertGreater(lo, 0)
        self.assertGreaterEqual(hi, lo)

    def test_threshold_auc_orders_higher_event_higher(self):
        thresholds = [0.1, 0.3, 0.5, 0.7, 0.9]
        low = threshold_auc(thresholds, [0.8, 0.4, 0.1, 0.02, 0.01])
        high = threshold_auc(thresholds, [0.99, 0.95, 0.8, 0.5, 0.1])
        self.assertGreater(high, low)

    def test_monotonicity_violation_detected(self):
        self.assertGreater(max_monotonicity_violation([0.1, 0.3, 0.5], [0.9, 0.4, 0.8]), 0.3)

if __name__ == "__main__":
    unittest.main()
