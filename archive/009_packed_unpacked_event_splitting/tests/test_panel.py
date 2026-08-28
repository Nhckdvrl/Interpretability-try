import json
import tempfile
import unittest
from pathlib import Path
from packed_unpacked_g0.panel import evaluate_panel

class PanelTests(unittest.TestCase):
    def _eval(self, rows):
        with tempfile.TemporaryDirectory() as td:
            paths=[]
            for i,(family,size,passed,verdict) in enumerate(rows):
                p=Path(td)/f"{i}.json"; p.write_text(json.dumps({"family":family,"size_b":size,"model_pass":passed,"verdict":verdict,"model":f"{family}-{size}"})); paths.append(str(p))
            return evaluate_panel(paths)
    def test_generality_requires_full_contract(self):
        rows=[("Qwen",4,True,"PASS-TO-PANEL"),("Qwen",8,True,"PASS-TO-PANEL"),("Qwen",32,True,"PASS-TO-PANEL"),("Gemma",12,True,"PASS-TO-PANEL"),("Phi",4,True,"PASS-TO-PANEL"),("Llama",8,False,"FAIL-MODEL-G0"),("Mistral",24,False,"FAIL-MODEL-G0")]
        x=self._eval(rows); self.assertTrue(x["generality_pass"]); self.assertIn("Qwen",x["three_size_families"])
    def test_hold_does_not_count(self):
        rows=[("Qwen",4,True,"PASS-TO-PANEL"),("Qwen",8,True,"PASS-TO-PANEL"),("Qwen",32,True,"PASS-TO-PANEL"),("Gemma",12,True,"HOLD-ARTIFACT-CONTROLS"),("Phi",4,True,"PASS-TO-PANEL"),("Llama",8,False,"FAIL-MODEL-G0"),("Mistral",24,False,"FAIL-MODEL-G0")]
        x=self._eval(rows); self.assertNotIn("Gemma",x["passed_families"]); self.assertFalse(x["generality_pass"])
    def test_unknown_families_cannot_replace_frozen_panel(self):
        rows=[("A",1,True,"PASS-TO-PANEL"),("B",2,True,"PASS-TO-PANEL"),("C",3,True,"PASS-TO-PANEL"),("D",4,True,"PASS-TO-PANEL"),("E",5,True,"PASS-TO-PANEL")]
        self.assertFalse(self._eval(rows)["full_panel_attempted"])
if __name__=="__main__": unittest.main()
