import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"projects"/"medusa-promotion-python"))
from replica_probe import capture
from compare import compare
SOURCE=capture()
class PromotionRuleMutations(unittest.TestCase):
 def test_independent_rule_model_matches(self):self.assertEqual(compare(SOURCE,capture())["result"],"match")
 def test_eq_every_mutation(self):self.assertEqual(compare(SOURCE,capture({"eq_uses_any":True}))["result"],"mismatch")
 def test_in_some_mutation(self):self.assertEqual(compare(SOURCE,capture({"in_uses_all":True}))["result"],"mismatch")
 def test_missing_ne_context_mutation(self):self.assertEqual(compare(SOURCE,capture({"ne_missing_fails":True}))["result"],"mismatch")
 def test_numeric_lexical_mutation(self):self.assertEqual(compare(SOURCE,capture({"lexical_numeric":True}))["result"],"mismatch")
 def test_scope_prefix_mutation(self):self.assertEqual(compare(SOURCE,capture({"skip_scope_strip":True}))["result"],"mismatch")
 def test_all_rules_conjunction_mutation(self):
  altered=capture()
  altered["scenarios"]=[dict(x) for x in altered["scenarios"]]
  altered["scenarios"][24]["output"]=True
  self.assertEqual(compare(SOURCE,altered)["result"],"mismatch")
 def test_missing_string_value_mutation(self):self.assertEqual(compare(SOURCE,capture({"keep_non_string_values":True}))["result"],"mismatch")
if __name__=="__main__":unittest.main()
