import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"projects"/"axios-http-python"))
from replica_probe import capture
from compare import compare
REFERENCE=capture()
class AxiosIntegrationMutations(unittest.TestCase):
 def test_http_contract_matches(self): self.assertEqual(compare(REFERENCE,capture())["result"],"match")
 def test_http_status_mutation(self): self.assertEqual(compare(REFERENCE,capture({"treat_http_errors_as_success":True}))["result"],"mismatch")
 def test_timeout_mutation(self): self.assertEqual(compare(REFERENCE,capture({"ignore_timeout":True}))["result"],"mismatch")
 def test_json_fallback_mutation(self): self.assertEqual(compare(REFERENCE,capture({"strict_malformed_json":True}))["result"],"mismatch")
 def test_header_mutation(self): self.assertEqual(compare(REFERENCE,capture({"drop_custom_header":True}))["result"],"mismatch")
 def test_redirect_mutation(self): self.assertEqual(compare(REFERENCE,capture({"disable_redirect":True}))["result"],"mismatch")
 def test_query_encoding_mutation(self): self.assertEqual(compare(REFERENCE,capture({"query_percent20":True}))["result"],"mismatch")
if __name__=="__main__": unittest.main()
