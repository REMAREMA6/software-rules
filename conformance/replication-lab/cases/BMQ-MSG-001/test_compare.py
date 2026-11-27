import unittest
from compare import compare
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'projects' / 'messaging-python'))
from replica_probe import capture


class BullMQMessagingTests(unittest.TestCase):
    def setUp(self):
        self.source = {"scenarios": [
            {"label": "duplicate-id-suppression", "setup": {"firstId": "stable-message-id", "secondId": "stable-message-id", "storedPayload": "first", "storedState": "waiting", "queuedCount": 1}, "processed": ["first"], "terminal": {"state": "completed", "id": "stable-message-id", "result": "acknowledged"}, "eventNames": ["waiting", "active", "completed"], "counts": {"waiting": 0, "active": 0, "completed": 1, "failed": 0}},
            {"label": "consumer-failure", "setup": {"firstId": "failure-message-id", "storedState": "waiting", "queuedCount": 1}, "processed": ["failure-case"], "terminal": {"state": "failed", "id": "failure-message-id", "error": "consumer-failed"}, "eventNames": ["waiting", "active", "failed"], "counts": {"waiting": 0, "active": 0, "completed": 0, "failed": 1}}
        ]}

    def test_equivalent_message_lifecycle_matches(self):
        self.assertEqual(compare(self.source, capture())["result"], "match")

    def test_duplicate_delivery_mutation_is_detected(self):
        self.assertEqual(compare(self.source, capture(suppress_duplicate=False))["result"], "mismatch")

    def test_duplicate_payload_overwrite_mutation_is_detected(self):
        self.assertEqual(compare(self.source, capture(preserve_first_payload=False))["result"], "mismatch")

    def test_missing_completion_ack_mutation_is_detected(self):
        self.assertEqual(compare(self.source, capture(complete_after_processing=False))["result"], "mismatch")

    def test_event_order_mutation_is_detected(self):
        self.assertEqual(compare(self.source, capture(event_order_mutation=True))["result"], "mismatch")

    def test_failed_consumer_state_mutation_is_detected(self):
        self.assertEqual(compare(self.source, capture(failure_state="completed"))["result"], "mismatch")


if __name__ == "__main__":
    unittest.main()
