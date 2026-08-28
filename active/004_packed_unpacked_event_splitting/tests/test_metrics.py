import unittest
from packed_unpacked_g0.metrics import (
    READOUTS, PRIMARY_READOUTS, bootstrap_ci, _variant_bias, _focal_score
)


class MetricTests(unittest.TestCase):
    def test_bootstrap_positive(self):
        lo, hi = bootstrap_ci([0.1, 0.2, 0.3, 0.4], seed=1, n_boot=500)
        self.assertGreater(lo, 0)
        self.assertGreaterEqual(hi, lo)

    def test_variant_bias_is_side_invariant(self):
        right = {"variant_side": "right", "p_right_more": .7, "p_left_more": .2}
        left = {"variant_side": "left", "p_right_more": .2, "p_left_more": .7}
        self.assertAlmostEqual(_variant_bias(right), .5)
        self.assertAlmostEqual(_variant_bias(left), .5)

    def test_focal_score_is_side_invariant(self):
        right = {"focal_side": "right", "p_right_more": .7, "p_left_more": .2}
        left = {"focal_side": "left", "p_right_more": .2, "p_left_more": .7}
        self.assertAlmostEqual(_focal_score(right), .5)
        self.assertAlmostEqual(_focal_score(left), .5)

    def test_frequency_is_diagnostic_not_primary(self):
        self.assertIn("frequency", READOUTS)
        self.assertNotIn("frequency", PRIMARY_READOUTS)
        self.assertEqual(set(PRIMARY_READOUTS), {"probability", "decision"})


if __name__ == "__main__":
    unittest.main()
