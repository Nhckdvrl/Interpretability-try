import unittest
from inadmissible_g0.prompts import condition_text, recognition_prompt, RECOGNITION_ORDERS

class PromptTests(unittest.TestCase):
    def test_struck_context_contains_scope(self):
        ctx = condition_text("facts", "evidence", "struck", "struck", exclusion_scope="final verdict")
        self.assertIn("EXCLUSION SCOPE", ctx)
        self.assertIn("final verdict", ctx)

    def test_polarity_probe_names_verdicts(self):
        ctx = condition_text("facts", "evidence", "struck", "struck", exclusion_scope="final verdict")
        prompt, _ = recognition_prompt(ctx, "Target wins", "Other wins", "polarity", RECOGNITION_ORDERS[0], "supports_target")
        self.assertIn("TARGET VERDICT", prompt)
        self.assertIn("Target wins", prompt)
        self.assertIn("OTHER VERDICT", prompt)
        self.assertIn("Other wins", prompt)

if __name__ == "__main__":
    unittest.main()
