import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pi_ri_g0 import classify_key, parse_mapping, score_case
from longmemeval_audit import audit_prediction, chronological_sessions


class PIRITest(unittest.TestCase):
    def test_parse_mapping(self):
        text = "bird: robin\ncity: tokyo"
        self.assertEqual(parse_mapping(text, ["bird", "city"]), {"bird": "robin", "city": "tokyo"})

    def test_latest_intrusion_classes(self):
        values = ["emu", "robin", "sparrow"]
        self.assertEqual(classify_key("sparrow", values, "latest")["class"], "correct")
        self.assertEqual(classify_key("emu", values, "latest")["class"], "primacy_intrusion")
        self.assertEqual(classify_key("robin", values, "latest")["class"], "stale_intrusion")

    def test_matched_case_score(self):
        case = {
            "keys": ["bird", "city"],
            "history": {"bird": ["emu", "robin"], "city": ["osaka", "tokyo"]},
            "target": "latest",
        }
        score = score_case(case, "bird: emu\ncity: tokyo")
        self.assertEqual(score["class_counts"]["primacy_intrusion"], 1)
        self.assertEqual(score["class_counts"]["correct"], 1)
        self.assertAlmostEqual(score["accuracy"], 0.5)


class LongMemEvalAuditTest(unittest.TestCase):
    def _row(self):
        return {
            "question_id": "q1",
            "question_type": "knowledge-update",
            "question": "Where do I live now?",
            "answer": "Tokyo",
            "question_date": "2026-01-03",
            "haystack_session_ids": ["s2", "s1"],
            "haystack_dates": ["2026-01-02", "2026-01-01"],
            "answer_session_ids": ["s1", "s2"],
            "haystack_sessions": [
                [{"role": "user", "content": "I moved to Tokyo."}],
                [{"role": "user", "content": "I live in Osaka."}],
            ],
        }

    def test_sessions_are_sorted(self):
        sessions = chronological_sessions(self._row())
        self.assertIn("Osaka", sessions[0]["text"])
        self.assertIn("Tokyo", sessions[1]["text"])

    def test_high_precision_stale(self):
        audited = audit_prediction(self._row(), "Osaka")
        self.assertFalse(audited["deterministic_correct"])
        self.assertTrue(audited["high_precision_stale_intrusion"])
        self.assertEqual(audited["stale_source_session_indices"], [0])


if __name__ == "__main__":
    unittest.main()
