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
            "partial_text": "Team A wins",
            "complement_text": "A team outside group X wins",
            "complement_branches": ["Team C wins", "Team D wins"],
            "complement_unpacked_text": "Team C wins or Team D wins",
            "disjoint_gold": True, "exhaustive_gold": True, "equivalent_gold": True,
            "partial_is_strict_subset": True, "partial_strictly_lower_probability_gold": True,
            "complement_gold": True, "complement_partition_gold": True,
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

    def test_strict_subset_needs_lower_probability_gold(self):
        x = good(); x["partitions"][0]["partial_strictly_lower_probability_gold"] = False
        with self.assertRaises(ValueError): validate_record(x)

    def test_focal_alternative_branch_counts_are_matched(self):
        x = good(); x["partitions"][0]["complement_branches"].append("Team E wins")
        with self.assertRaises(ValueError): validate_record(x)


if __name__ == "__main__":
    unittest.main()
