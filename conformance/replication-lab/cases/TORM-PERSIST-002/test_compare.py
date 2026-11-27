import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"projects"/"typeorm-durability-python"))
from replica_probe import capture
from compare import compare
REFERENCE=capture()
class TypeORMDurabilityMutations(unittest.TestCase):
 def test_file_backed_durability_matches(self):self.assertEqual(compare(REFERENCE,capture())["result"],"match")
 def test_lost_commit_mutation(self):self.assertEqual(compare(REFERENCE,capture({"lose_commit":True}))["result"],"mismatch")
 def test_rollback_leak_mutation(self):self.assertEqual(compare(REFERENCE,capture({"leak_rollback":True}))["result"],"mismatch")
 def test_lost_update_mutation(self):self.assertEqual(compare(REFERENCE,capture({"lose_update":True}))["result"],"mismatch")
 def test_partial_constraint_commit_mutation(self):self.assertEqual(compare(REFERENCE,capture({"partial_constraint_commit":True}))["result"],"mismatch")
if __name__=="__main__":unittest.main()
