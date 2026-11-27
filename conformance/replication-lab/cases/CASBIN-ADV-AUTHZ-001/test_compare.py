import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"projects"/"casbin-advanced-python"))
from replica_probe import capture
from compare import compare

REFERENCE=capture()
class AdvancedAuthorizationMutations(unittest.TestCase):
 def test_independent_model_matches(self): self.assertEqual(compare(REFERENCE,capture())["result"],"match")
 def test_domain_isolation_mutation_detected(self): self.assertEqual(compare(REFERENCE,capture({"ignore_domain":True}))["result"],"mismatch")
 def test_abac_owner_mutation_detected(self): self.assertEqual(compare(REFERENCE,capture({"ignore_owner":True}))["result"],"mismatch")
 def test_deny_override_mutation_detected(self): self.assertEqual(compare(REFERENCE,capture({"ignore_deny":True}))["result"],"mismatch")
 def test_policy_mutation_propagation_detected(self): self.assertEqual(compare(REFERENCE,capture({"ignore_policy_mutation":True}))["result"],"mismatch")
if __name__=="__main__": unittest.main()
