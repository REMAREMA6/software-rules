import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"projects"/"viper-config-python"))
from replica_probe import capture
from compare import compare
REFERENCE=capture()
class ViperConfigurationMutations(unittest.TestCase):
 def test_precedence_matches(self):self.assertEqual(compare(REFERENCE,capture())["result"],"match")
 def test_override_precedence_mutation(self):self.assertEqual(compare(REFERENCE,capture({"ignore_override":True}))["result"],"mismatch")
 def test_flag_precedence_mutation(self):self.assertEqual(compare(REFERENCE,capture({"ignore_flag":True}))["result"],"mismatch")
 def test_environment_precedence_mutation(self):self.assertEqual(compare(REFERENCE,capture({"ignore_environment":True}))["result"],"mismatch")
 def test_empty_environment_mutation(self):self.assertEqual(compare(REFERENCE,capture({"ignore_empty_env":True}))["result"],"mismatch")
 def test_key_replacer_mutation(self):self.assertEqual(compare(REFERENCE,capture({"ignore_key_replacer":True}))["result"],"mismatch")
 def test_explicit_binding_mutation(self):self.assertEqual(compare(REFERENCE,capture({"ignore_explicit_binding":True}))["result"],"mismatch")
if __name__=="__main__":unittest.main()
