import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"projects"/"medusa-price-selection-python"))
from replica_probe import capture
from compare import compare
REFERENCE=capture()
class PricingRuleMutations(unittest.TestCase):
 def test_independent_price_selection_matches(self): self.assertEqual(compare(REFERENCE,capture())["result"],"match")
 def test_sale_always_wins_mutation_detected(self): self.assertEqual(compare(REFERENCE,capture({"always_choose_sale":True}))["result"],"mismatch")
 def test_default_as_original_mutation_detected(self): self.assertEqual(compare(REFERENCE,capture({"default_as_original":True}))["result"],"mismatch")
 def test_sale_as_original_mutation_detected(self): self.assertEqual(compare(REFERENCE,capture({"sale_as_original":True}))["result"],"mismatch")
 def test_highest_override_mutation_detected(self): self.assertEqual(compare(REFERENCE,capture({"highest_override":True}))["result"],"mismatch")
 def test_missing_price_set_inclusion_mutation_detected(self): self.assertEqual(compare(REFERENCE,capture({"include_missing_set":True}))["result"],"mismatch")
if __name__=="__main__": unittest.main()
