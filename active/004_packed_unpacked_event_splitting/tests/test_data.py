import unittest
from packed_unpacked_g0.data import validate_record

def good():
    return {
        "scenario_id": "x1", "domain": "forecast",
        "packed_text": "A team from group X wins.",
        "packed_paraphrase": "The winner belongs to group X.",
        "source": {"dataset": "external-demo", "record_id": "1", "license": "CC-BY",
                   "split": "test", "url": "https://example.invalid", "provenance": "external"},
        "partitions": [{
            "partition_id": "p2", "branches": ["Team A wins", "Team B wins"],
            "unpacked_text": "Team A wins or Team B wins",
            "repacked_text": "One of the group-X teams wins",
            "disjoint_gold": True, "exhaustive_gold": True, "equivalent_gold": True,
            "partial_is_strict_subset": True,
        }]
    }

class DataTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(validate_record(good()).partitions[0].branch_count, 2)
    def test_custom_only_rejected(self):
        x = good(); x["source"]["provenance"] = "synthetic"
        with self.assertRaises(ValueError): validate_record(x)
    def test_relation_gold_required(self):
        x = good(); x["partitions"][0]["exhaustive_gold"] = False
        with self.assertRaises(ValueError): validate_record(x)

if __name__ == "__main__":
    unittest.main()
