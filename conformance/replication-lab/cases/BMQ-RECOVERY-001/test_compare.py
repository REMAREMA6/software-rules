import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"projects"/"bullmq-stalled-python"))
from replica_probe import capture
from compare import compare
REFERENCE=capture()
class BullMQStalledRecoveryMutations(unittest.TestCase):
 def test_stalled_recovery_matches(self):self.assertEqual(compare(REFERENCE,capture())["result"],"match")
 def test_no_requeue_mutation(self):self.assertEqual(compare(REFERENCE,capture({"do_not_requeue":True}))["result"],"mismatch")
 def test_ignore_stalled_limit_mutation(self):self.assertEqual(compare(REFERENCE,capture({"ignore_stalled_limit":True}))["result"],"mismatch")
 def test_attempts_accounting_mutation(self):self.assertEqual(compare(REFERENCE,capture({"increment_attempts_on_requeue":True}))["result"],"mismatch")
 def test_stalled_counter_mutation(self):self.assertEqual(compare(REFERENCE,capture({"omit_stalled_counter":True}))["result"],"mismatch")
if __name__=="__main__":unittest.main()
