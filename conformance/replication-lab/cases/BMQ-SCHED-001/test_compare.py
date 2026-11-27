import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"projects"/"bullmq-scheduling-python"))
from replica_probe import capture
from compare import compare
SOURCE=capture()
class SchedulingMutationTests(unittest.TestCase):
 def test_delayed_reschedule_and_cancel_match(self):self.assertEqual(compare(SOURCE,capture())["result"],"match")
 def test_ignored_reschedule(self):self.assertEqual(compare(SOURCE,capture({"ignore_change_delay":True}))["result"],"mismatch")
 def test_reschedule_state_mutation(self):self.assertEqual(compare(SOURCE,capture({"change_delay_sets_waiting":True}))["result"],"mismatch")
 def test_cancel_remove_mutation(self):self.assertEqual(compare(SOURCE,capture({"ignore_remove":True}))["result"],"mismatch")
 def test_cancelled_job_execution(self):self.assertEqual(compare(SOURCE,capture({"process_cancelled_job":True}))["result"],"mismatch")
 def test_event_order_mutation(self):self.assertEqual(compare(SOURCE,capture({"complete_before_active":True}))["result"],"mismatch")
 def test_missing_active_event(self):self.assertEqual(compare(SOURCE,capture({"skip_active_event":True}))["result"],"mismatch")
if __name__=="__main__":unittest.main()
