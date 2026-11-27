import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"projects"/"typeorm-isolation-python"))
from replica_probe import capture
from compare import compare
SOURCE=capture()
class IsolationMutationTests(unittest.TestCase):
 def test_postgres_isolation_model_matches(self):self.assertEqual(compare(SOURCE,capture())["result"],"match")
 def test_repeatable_read_as_read_committed(self):self.assertEqual(compare(SOURCE,capture({"repeatable_read_uses_read_committed":True}))["result"],"mismatch")
 def test_serializable_write_skew_allowed(self):self.assertEqual(compare(SOURCE,capture({"serializable_allows_write_skew":True}))["result"],"mismatch")
 def test_wrong_serialization_error_category(self):self.assertEqual(compare(SOURCE,capture({"wrong_error_code":True}))["result"],"mismatch")
 def test_invariant_count_mutation(self):self.assertEqual(compare(SOURCE,capture({"wrong_invariant_count":True}))["result"],"mismatch")
if __name__=="__main__":unittest.main()
