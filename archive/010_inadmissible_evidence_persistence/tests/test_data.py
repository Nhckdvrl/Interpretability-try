import json
import tempfile
import unittest
from pathlib import Path
from inadmissible_g0.data import validate_record, load_scenarios
from inadmissible_g0.prompts import recognition_prompt, POLARITY_ORDERS

def good(sid="case-1-a", pair="pair-1", polarity="supports_target", evidence="A disputed statement supports the target verdict."):
    return {"scenario_id":sid,"polarity_pair_id":pair,"domain":"legal","case_facts":"Admissible baseline facts.","evidence_text":evidence,"evidence_polarity":polarity,"target_verdict":"Target wins","other_verdict":"Other wins","admissible_ruling":"The evidence is admitted for the verdict.","struck_ruling":"The evidence is struck and must not be considered for the verdict.","exclusion_scope":"The exclusion applies to the final verdict.","neutral_evidence_text":"A neutral procedural detail.","neutral_struck_ruling":"The neutral procedural detail is struck and must not be considered.","exclusion_reason_type":"procedural_truth_neutral","admitted_gold":True,"struck_gold":True,"must_ignore_for_verdict_gold":True,"evidence_polarity_gold":True,"exclusion_scope_gold":True,"baseline_excludes_evidence_gold":True,"neutral_evidence_gold":True,"neutral_control_matched_gold":True,"neutral_ruling_matched_gold":True,"content_swap_gold":True,"matched_base_gold":True,"baseline_no_dangling_reference_gold":True,"exclusion_reason_gold":True,"polarity_options_symmetric_gold":True,"pair_statistical_unit_gold":True,"source":{"dataset":"external-demo","record_id":sid,"license":"CC-BY","split":"test","url":"https://example.invalid","provenance":"external-derived"}}

class DataTests(unittest.TestCase):
    def test_valid_record(self): self.assertEqual(validate_record(good()).evidence_polarity,"supports_target")
    def test_gold_required(self):
        x=good(); x["content_swap_gold"]=False
        with self.assertRaises(ValueError): validate_record(x)
    def test_polarity_prompt_defines_target_and_other(self):
        s=validate_record(good()); p,_=recognition_prompt(s.case_facts,s.evidence_text,s.struck_ruling,s.exclusion_scope,s.target_verdict,s.other_verdict,"polarity",POLARITY_ORDERS[0],s.evidence_polarity)
        self.assertIn(s.target_verdict,p); self.assertIn(s.other_verdict,p); self.assertNotIn("A. Yes",p)
    def test_dangling_never_seen_reference_rejected(self):
        x=good(); x["case_facts"]="Apart from the statement below, facts are balanced."
        with self.assertRaises(ValueError): validate_record(x)
    def test_load_requires_matched_bidirectional_pair(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"d.jsonl"; p.write_text(json.dumps(good())+"\n")
            with self.assertRaises(ValueError): load_scenarios(p)
            a=good(); b=good("case-1-b","pair-1","supports_other","A disputed statement supports the other verdict.")
            p.write_text(json.dumps(a)+"\n"+json.dumps(b)+"\n")
            self.assertEqual(len(load_scenarios(p)),2)
            b["case_facts"]="different baseline"
            p.write_text(json.dumps(a)+"\n"+json.dumps(b)+"\n")
            with self.assertRaises(ValueError): load_scenarios(p)
if __name__=="__main__": unittest.main()
