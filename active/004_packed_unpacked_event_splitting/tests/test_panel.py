import json
import tempfile
import unittest
from pathlib import Path
from packed_unpacked_g0.panel import evaluate_panel

class PanelTests(unittest.TestCase):
    def test_generality_requires_full_contract(self):
        rows = [
            ("Qwen", 4, True), ("Qwen", 8, True), ("Qwen", 32, True),
            ("Gemma", 12, True), ("Phi", 4, True),
            ("Llama", 8, False), ("Mistral", 24, False),
        ]
        with tempfile.TemporaryDirectory() as td:
            paths = []
            for i, (family, size, passed) in enumerate(rows):
                p = Path(td) / f"{i}.json"
                p.write_text(json.dumps({
                    "family": family, "size_b": size, "model_pass": passed,
                    "model": f"{family}-{size}"
                }))
                paths.append(str(p))
            x = evaluate_panel(paths)
            self.assertTrue(x["generality_pass"])
            self.assertIn("Qwen", x["three_size_families"])

    def test_three_families_without_size_sequence_fails(self):
        rows = [
            ("Qwen", 8, True), ("Gemma", 12, True), ("Phi", 4, True),
            ("Llama", 8, False), ("Mistral", 24, True),
        ]
        with tempfile.TemporaryDirectory() as td:
            paths = []
            for i, (family, size, passed) in enumerate(rows):
                p = Path(td) / f"{i}.json"
                p.write_text(json.dumps({
                    "family": family, "size_b": size, "model_pass": passed,
                    "model": f"{family}-{size}"
                }))
                paths.append(str(p))
            self.assertFalse(evaluate_panel(paths)["generality_pass"])

if __name__ == "__main__":
    unittest.main()
