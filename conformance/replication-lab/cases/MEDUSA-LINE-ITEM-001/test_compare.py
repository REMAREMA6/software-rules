import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"projects"/"medusa-line-item-python"))
from replica_probe import capture
from compare import compare
SOURCE=capture()
class LineItemMutationTests(unittest.TestCase):
 def test_decimal_line_item_model_matches(self):self.assertEqual(compare(SOURCE,capture())["result"],"match")
 def test_inclusive_conversion_mutation(self):self.assertEqual(compare(SOURCE,capture({"skip_inclusive_conversion":True}))["result"],"mismatch")
 def test_additive_tax_mutation(self):self.assertEqual(compare(SOURCE,capture({"max_tax_rate":True}))["result"],"mismatch")
 def test_discount_tax_recalculation_mutation(self):self.assertEqual(compare(SOURCE,capture({"tax_not_recalculated_after_discount":True}))["result"],"mismatch")
 def test_adjustment_individual_value_mutation(self):self.assertEqual(compare(SOURCE,capture({"cumulative_adjustment":True}))["result"],"mismatch")
 def test_original_tax_basis_mutation(self):self.assertEqual(compare(SOURCE,capture({"original_tax_uses_discounted_base":True}))["result"],"mismatch")
 def test_quantity_allocation_mutation(self):
  changed=capture();changed["scenarios"][8]["output"]["total"]=0
  self.assertEqual(compare(SOURCE,changed)["result"],"mismatch")
if __name__=="__main__":unittest.main()
