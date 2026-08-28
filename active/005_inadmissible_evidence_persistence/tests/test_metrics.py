import unittest
from inadmissible_g0.metrics import bootstrap_ci, _neutral_ok

class MetricTests(unittest.TestCase):
    def test_bootstrap_positive(self):
        lo,hi=bootstrap_ci([.03,.05,.08,.10],seed=2,n_boot=500); self.assertGreater(lo,0); self.assertGreaterEqual(hi,lo)
    def test_neutral_control_must_be_small_relative_to_signal(self):
        cfg={"max_neutral_struck_abs_shift":.05,"min_struck_directional_residual":.05,"max_neutral_to_struck_ratio":.5}
        self.assertTrue(_neutral_ok(.02,.10,cfg)); self.assertFalse(_neutral_ok(.045,.06,cfg))
if __name__=="__main__": unittest.main()
