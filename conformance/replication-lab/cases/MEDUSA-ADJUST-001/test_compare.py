import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"projects"/"medusa-adjustment-python"))
from replica_probe import capture
from compare import compare
SOURCE=capture()
class AdjustmentRuleMutations(unittest.TestCase):
 def test_independent_decimal_model_matches(self):self.assertEqual(compare(SOURCE,capture())["result"],"match")
 def test_tax_inclusive_conversion_mutation(self):self.assertEqual(compare(SOURCE,capture({"skip_inclusive_tax_conversion":True}))["result"],"mismatch")
 def test_tax_exclusive_calculation_mutation(self):self.assertEqual(compare(SOURCE,capture({"skip_exclusive_tax":True}))["result"],"mismatch")
 def test_missing_amount_filter_mutation(self):self.assertEqual(compare(SOURCE,capture({"include_missing_amount":True}))["result"],"mismatch")
 def test_adjustment_own_total_mutation(self):self.assertEqual(compare(SOURCE,capture({"cumulative_adjustment_values":True}))["result"],"mismatch")
 def test_quantity_allocation_mutation(self):self.assertEqual(compare(SOURCE,capture({"skip_per_item_allocation":True}))["result"],"mismatch")
 def test_zero_quantity_fallback_mutation(self):self.assertEqual(compare(SOURCE,capture({"zero_quantity_no_fallback":True}))["result"],"mismatch")
if __name__=="__main__":unittest.main()
