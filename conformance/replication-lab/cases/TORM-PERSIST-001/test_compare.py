import unittest
from compare import compare

class TypeORMTransactionComparisonTests(unittest.TestCase):
    def setUp(self):
        self.source = {"scenarios": {
            "rollback": {"error": {"name": "Error", "message": "forced-transaction-failure"}, "callbackResult": None, "rowsInsideCallback": [{"id": 1, "value": "rolled-back"}], "rowsAfterRollback": []},
            "commit": {"callbackReturn": "callback-result", "rowsAfterCommit": [{"id": 1, "value": "committed"}]}
        }}
        self.replica = {"scenarios": {
            "rollback": {"error": {"name": "Error", "message": "forced-transaction-failure"}, "callbackResult": None, "rowsAfterRollback": []},
            "commit": {"callbackReturn": "callback-result", "rowsAfterCommit": [{"id": 1, "value": "committed"}]}
        }}

    def test_equivalent_transaction_outcomes_match(self):
        self.assertEqual(compare(self.source, self.replica)["result"], "match")

    def test_missing_rollback_is_detected(self):
        self.replica["scenarios"]["rollback"]["rowsAfterRollback"] = [{"id": 1, "value": "rolled-back"}]
        self.assertEqual(compare(self.source, self.replica)["result"], "mismatch")

    def test_error_swallowing_is_detected(self):
        self.replica["scenarios"]["rollback"]["error"] = None
        self.assertEqual(compare(self.source, self.replica)["result"], "mismatch")

    def test_read_your_writes_mutation_is_detected(self):
        self.replica["scenarios"]["rollback"]["rowsInsideCallback"] = []
        self.assertEqual(compare(self.source, self.replica)["result"], "mismatch")

    def test_commit_loss_is_detected(self):
        self.replica["scenarios"]["commit"]["rowsAfterCommit"] = []
        self.assertEqual(compare(self.source, self.replica)["result"], "mismatch")

    def test_callback_return_loss_is_detected(self):
        self.replica["scenarios"]["commit"]["callbackReturn"] = None
        self.assertEqual(compare(self.source, self.replica)["result"], "mismatch")

if __name__ == "__main__":
    unittest.main()
