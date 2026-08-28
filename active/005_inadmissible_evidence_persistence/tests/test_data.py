import unittest
from inadmissible_g0.data import validate_record
from inadmissible_g0.prompts import recognition_prompt, RECOGNITION_ORDERS

def good():
    return {"scenario_id":"case-1","domain":"legal","case_facts":"Admissible baseline facts.","evidence_text":"A disputed statement points toward the target verdict.","evidence_polarity":"supports_target","target_verdict":"Target wins","other_verdict":"Other wins","admissible_ruling":"The evidence is admitted for the verdict.","struck_ruling":"The evidence is struck and must not be considered for the verdict.","exclusion_scope":"The exclusion applies to the final verdict.","neutral_evidence_text":"A neutral procedural detail.","neutral_struck_ruling":"The neutral procedural detail is struck and must not be considered.","admitted_gold":True,"struck_gold":True,"must_ignore_for_verdict_gold":True,"evidence_polarity_gold":True,"exclusion_scope_gold":True,"baseline_excludes_evidence_gold":True,"neutral_evidence_gold":True,"neutral_control_matched_gold":True,"neutral_ruling_matched_gold":True,"source":{"dataset":"external-demo","record_id":"1","license":"CC-BY","split":"test","url":"https://example.invalid","provenance":"external"}}
class DataTests(unittest.TestCase):
    def test_valid(self):self.assertEqual(validate_record(good()).evidence_polarity,"supports_target")
    def test_gold_required(self):
        x=good();x["evidence_polarity_gold"]=False
        with self.assertRaises(ValueError):validate_record(x)
    def test_polarity_prompt_defines_target_and_other(self):
        s=validate_record(good());p,_=recognition_prompt(s.case_facts,s.evidence_text,s.struck_ruling,s.exclusion_scope,s.target_verdict,s.other_verdict,"polarity",RECOGNITION_ORDERS[0],s.evidence_polarity)
        self.assertIn(s.target_verdict,p);self.assertIn(s.other_verdict,p)
if __name__=="__main__":unittest.main()
