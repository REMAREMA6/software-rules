import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"projects"/"express-session-python"))
from replica_probe import capture
from compare import compare
REFERENCE=capture()
class SessionLifecycleMutations(unittest.TestCase):
 def test_session_lifecycle_matches(self):self.assertEqual(compare(REFERENCE,capture())["result"],"match")
 def test_save_uninitialized_mutation(self):self.assertEqual(compare(REFERENCE,capture({"emit_cookie_for_uninitialized":True}))["result"],"mismatch")
 def test_old_session_id_not_invalidated(self):self.assertEqual(compare(REFERENCE,capture({"keep_old_id_on_regenerate":True}))["result"],"mismatch")
 def test_tampered_cookie_accepted(self):self.assertEqual(compare(REFERENCE,capture({"accept_tampered_cookie":True}))["result"],"mismatch")
 def test_destroyed_session_retained(self):self.assertEqual(compare(REFERENCE,capture({"retain_destroyed_session":True}))["result"],"mismatch")
 def test_cookie_not_cleared(self):self.assertEqual(compare(REFERENCE,capture({"omit_cookie_clear":True}))["result"],"mismatch")
if __name__=="__main__":unittest.main()
