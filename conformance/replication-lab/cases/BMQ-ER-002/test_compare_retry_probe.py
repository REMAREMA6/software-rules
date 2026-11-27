import copy
import unittest

from compare_retry_probe import compare_captures


def source_capture():
    return {
        "sourceCommit": "pinned",
        "packageVersion": "6.7.10",
        "scenarios": [
            {
                "label": "retry",
                "configuredAttempts": 3,
                "processorAttempts": 3,
                "processorAttemptsMade": [0, 1, 2],
                "strategyAttempts": [1, 2],
                "backoffResults": [40, 80],
                "stateTransitions": ["delayed", "waiting", "delayed", "waiting", "completed"],
                "outcome": {"terminal": "completed", "attemptsMade": 3, "result": "ok"},
                "finalState": "completed",
                "trace": [
                    {"event": "queue:waiting", "data": {"jobId": "1"}},
                    {"event": "processor", "attemptsMade": 0},
                    {"event": "backoff-result", "delayMs": 40},
                    {"event": "queue:delayed"},
                    {"event": "queue:waiting", "data": {"prev": "delayed"}},
                    {"event": "processor", "attemptsMade": 1},
                    {"event": "backoff-result", "delayMs": 80},
                    {"event": "queue:delayed"},
                    {"event": "queue:waiting"},
                    {"event": "processor", "attemptsMade": 2},
                    {"event": "queue:completed"},
                ],
            }
        ],
    }


def replica_capture():
    return {
        "implementation": "independent Python model",
        "scenarios": [
            {
                "label": "retry",
                "configuredAttempts": 3,
                "processorAttempts": 3,
                "processorAttemptsMade": [0, 1, 2],
                "strategyAttempts": [1, 2],
                "backoffResults": [40, 80],
                "stateTransitions": ["delayed", "waiting", "delayed", "waiting", "completed"],
                "outcome": {"terminal": "completed", "attemptsMade": 3, "result": "ok"},
                "finalState": "completed",
            }
        ],
    }


class CaptureComparisonTests(unittest.TestCase):
    def test_equivalent_captures_match(self):
        report = compare_captures(source_capture(), replica_capture())
        self.assertEqual(report["result"], "match")
        self.assertEqual(report["scenarioCount"], 1)

    def test_mutated_attempt_limit_is_detected(self):
        mutant = replica_capture()
        mutant["scenarios"][0]["processorAttempts"] = 4
        report = compare_captures(source_capture(), mutant)
        self.assertEqual(report["result"], "mismatch")
        self.assertTrue(any("processorAttempts" in error for error in report["errors"]))

    def test_mutated_state_transition_is_detected(self):
        mutant = replica_capture()
        mutant["scenarios"][0]["stateTransitions"] = ["waiting", "waiting", "completed"]
        report = compare_captures(source_capture(), mutant)
        self.assertEqual(report["result"], "mismatch")
        self.assertTrue(any("stateTransitions" in error for error in report["errors"]))

    def test_mutated_backoff_sequence_is_detected(self):
        mutant = replica_capture()
        mutant["scenarios"][0]["backoffResults"] = [40, 40]
        report = compare_captures(source_capture(), mutant)
        self.assertEqual(report["result"], "mismatch")
        self.assertTrue(any("backoffResults" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
