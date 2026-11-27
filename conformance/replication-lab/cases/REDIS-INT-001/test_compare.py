import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projects" / "redis-client-python"))
from replica_probe import capture
from compare import compare


class RedisIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.reference = capture()

    def test_independent_client_matches_reference_fixture(self):
        self.assertEqual(compare(self.reference, capture())["result"], "match")

    def test_skipped_write_is_detected(self):
        self.assertEqual(compare(self.reference, capture({"skip_set": True}))["result"], "mismatch")

    def test_missing_value_mutation_is_detected(self):
        self.assertEqual(compare(self.reference, capture({"missing_as_value": True}))["result"], "mismatch")

    def test_wrongtype_suppression_is_detected(self):
        self.assertEqual(compare(self.reference, capture({"wrongtype_as_success": True}))["result"], "mismatch")

    def test_zero_ttl_mutation_is_detected(self):
        self.assertEqual(compare(self.reference, capture({"ttl_as_zero": True}))["result"], "mismatch")

    def test_connection_failure_suppression_is_detected(self):
        self.assertEqual(compare(self.reference, capture({"connection_as_success": True}))["result"], "mismatch")


if __name__ == "__main__":
    unittest.main()
