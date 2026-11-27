import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"projects"/"typeorm-isolation-python"))
from replica_probe import model_capture
from compare import compare
SOURCE=model_capture()
class IsolationMutationTests(unittest.TestCase):
 def test_postgres_isolation_model_matches(self):self.assertEqual(compare(SOURCE,model_capture())["result"],"match")
 def test_read_committed_snapshot_mutation(self):self.assertEqual(compare(SOURCE,model_capture({"read_committed_snapshot":True}))["result"],"mismatch")
 def test_repeatable_read_as_read_committed(self):self.assertEqual(compare(SOURCE,model_capture({"repeatable_read_uses_read_committed":True}))["result"],"mismatch")
 def test_serializable_write_skew_allowed(self):self.assertEqual(compare(SOURCE,model_capture({"serializable_allows_write_skew":True}))["result"],"mismatch")
 def test_wrong_serialization_error_category(self):self.assertEqual(compare(SOURCE,model_capture({"wrong_error_code":True}))["result"],"mismatch")
 def test_serialization_abort_without_error(self):self.assertEqual(compare(SOURCE,model_capture({"serializable_aborts_without_error":True}))["result"],"mismatch")
 def test_invariant_count_mutation(self):self.assertEqual(compare(SOURCE,model_capture({"wrong_invariant_count":True}))["result"],"mismatch")
if __name__=="__main__":unittest.main()
