import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projects" / "typeorm-transaction-python"))

from compare import compare
from replica_probe import capture


def fixtures():
    source = {
        "scenarios": [
            {
                "label": "commit-success",
                "terminal": "committed",
                "callbackResult": {"postId": 1, "categoryId": 1},
                "postRows": [{"id": 1, "title": "Post #1"}],
                "categoryRows": [{"id": 1, "name": "Category #1"}],
                "postCount": 1,
                "categoryCount": 1,
            },
            {
                "label": "rollback-on-invalid-post",
                "terminal": "rolled-back",
                "errorPropagated": True,
                "errorCategory": "integrity-constraint",
                "readsVisibleBeforeFailure": True,
                "postRowsAfter": [],
                "categoryRowsAfter": [],
                "postCountAfter": 0,
                "categoryCountAfter": 0,
            },
        ]
    }
    return source


class TypeOrmTransactionComparisonTests(unittest.TestCase):
    def test_equivalent_transaction_outcomes_match(self):
        self.assertEqual(compare(fixtures(), capture())["result"], "match")

    def test_executable_no_rollback_mutation_is_detected(self):
        mutant = capture(rollback_on_error=False)
        self.assertEqual(compare(fixtures(), mutant)["result"], "mismatch")

    def test_missing_callback_error_propagation_is_detected(self):
        mutant = capture()
        mutant["scenarios"][1]["errorPropagated"] = False
        self.assertEqual(compare(fixtures(), mutant)["result"], "mismatch")

    def test_partial_commit_mutation_is_detected(self):
        mutant = capture(rollback_on_error=False)
        self.assertEqual(compare(fixtures(), mutant)["result"], "mismatch")


if __name__ == "__main__":
    unittest.main()
