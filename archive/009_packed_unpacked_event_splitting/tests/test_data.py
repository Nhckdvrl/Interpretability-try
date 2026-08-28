import unittest
from packed_unpacked_g0.data import validate_record

def good():
    return {"scenario_id":"x1","domain":"forecast","packed_text":"A team from group X wins.","packed_paraphrase":"The winner belongs to group X.","source":{"dataset":"external-demo","record_id":"1","license":"CC-BY","split":"test","url":"https://example.invalid","provenance":"external"},"partitions":[{"partition_id":"p2","branches":["Team A wins","Team B wins"],"unpacked_text":"Team A wins or Team B wins","reordered_unpacked_text":"Team B wins or Team A wins","repacked_text":"One of the group-X teams wins","partial_text":"Team A wins","complement_text":"A team outside group X wins","complement_branches":["Team C wins","Team D wins"],"complement_unpacked_text":"Team C wins or Team D wins","focal_length_control_text":"A team that belongs to group X is the winner","complement_length_control_text":"A team that does not belong to group X is the winner","branch_count_family":"team-taxonomy","disjoint_gold":True,"exhaustive_gold":True,"equivalent_gold":True,"partial_is_strict_subset":True,"partial_strictly_lower_probability_gold":True,"complement_gold":True,"complement_partition_gold":True,"reordered_equivalent_gold":True,"length_controls_equivalent_gold":True,"length_controls_matched_gold":True,"branch_count_comparable_gold":True}]}
class DataTests(unittest.TestCase):
    def test_valid(self): self.assertEqual(validate_record(good()).partitions[0].branch_count_family,"team-taxonomy")
    def test_custom_only_rejected(self):
        x=good();x["source"]["provenance"]="synthetic"
        with self.assertRaises(ValueError):validate_record(x)
    def test_relation_gold_required(self):
        x=good();x["partitions"][0]["length_controls_matched_gold"]=False
        with self.assertRaises(ValueError):validate_record(x)
    def test_reordered_form_must_change_surface_order(self):
        x=good();x["partitions"][0]["reordered_unpacked_text"]=x["partitions"][0]["unpacked_text"]
        with self.assertRaises(ValueError):validate_record(x)
if __name__=="__main__":unittest.main()
