import copy
import unittest
from compare import compare


class BullMQMessagingTests(unittest.TestCase):
    def setUp(self):
        self.source = {"scenarios": [
            {"label": "duplicate-id-suppression", "setup": {"firstId": "stable-message-id", "secondId": "stable-message-id", "storedPayload": "first"}, "processed": ["first"], "terminal": {"state": "completed", "id": "stable-message-id", "result": "acknowledged"}, "eventNames": ["waiting", "active", "completed"], "counts": {"waiting": 0, "active": 0, "completed": 1, "failed": 0}},
            {"label": "consumer-failure", "setup": {"firstId": "failure-message-id"}, "processed": ["failure-case"], "terminal": {"state": "failed", "id": "failure-message-id", "error": "consumer-failed"}, "eventNames": ["waiting", "active", "failed"], "counts": {"waiting": 0, "active": 0, "completed": 0, "failed": 1}}
        ]}
        self.replica = copy.deepcopy(self.source)

    def test_equivalent_message_lifecycle_matches(self):
        self.assertEqual(compare(self.source, self.replica)["result"], "match")

    def test_duplicate_delivery_mutation_is_detected(self):
        self.replica["scenarios"][0]["processed"].append("second")
        self.assertEqual(compare(self.source, self.replica)["result"], "mismatch")

    def test_duplicate_payload_overwrite_is_detected(self):
        self.replica["scenarios"][0]["setup"]["storedPayload"] = "second"
        self.assertEqual(compare(self.source, self.replica)["result"], "mismatch")

    def test_missing_completion_ack_is_detected(self):
        self.replica["scenarios"][0]["terminal"]["state"] = "active"
        self.assertEqual(compare(self.source, self.replica)["result"], "mismatch")

    def test_event_order_mutation_is_detected(self):
        self.replica["scenarios"][0]["eventNames"] = ["waiting", "completed", "active"]
        self.assertEqual(compare(self.source, self.replica)["result"], "mismatch")

    def test_failed_consumer_state_is_detected(self):
        self.replica["scenarios"][1]["terminal"]["state"] = "completed"
        self.assertEqual(compare(self.source, self.replica)["result"], "mismatch")


if __name__ == "__main__":
    unittest.main()
