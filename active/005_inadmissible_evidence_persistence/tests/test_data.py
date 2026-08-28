import unittest
from inadmissible_g0.data import validate_record

def good():
    return {
        "scenario_id": "case-1", "domain": "legal",
        "case_facts": "Admissible baseline facts.",
        "evidence_text": "A disputed statement points toward the target verdict.",
        "evidence_polarity": "supports_target",
        "target_verdict": "Target wins", "other_verdict": "Other wins",
        "admissible_ruling": "The evidence is admitted for the verdict.",
        "struck_ruling": "The evidence is struck and must not be considered for the verdict.",
        "exclusion_scope": "The exclusion applies to the final verdict.",
        "struck_gold": True, "must_ignore_for_verdict_gold": True,
        "neutral_evidence_text": "A neutral procedural detail.",
        "source": {"dataset": "external-demo", "record_id": "1", "license": "CC-BY",
                   "split": "test", "url": "https://example.invalid", "provenance": "external"}
    }

class DataTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(validate_record(good()).evidence_polarity, "supports_target")
    def test_custom_only_rejected(self):
        x = good(); x["source"]["provenance"] = "synthetic"
        with self.assertRaises(ValueError): validate_record(x)
    def test_struck_gold_required(self):
        x = good(); x["struck_gold"] = False
        with self.assertRaises(ValueError): validate_record(x)

if __name__ == "__main__":
    unittest.main()
