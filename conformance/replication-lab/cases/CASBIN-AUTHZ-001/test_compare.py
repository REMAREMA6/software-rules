import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projects" / "casbin-rbac-python"))
from replica_probe import capture
from compare import compare

REFERENCE = capture()


class CasbinAuthorizationTests(unittest.TestCase):
    def test_independent_replica_matches_reference_fixture(self):
        self.assertEqual(compare(REFERENCE, capture())["result"], "match")

    def test_role_link_removal_is_detected(self):
        self.assertEqual(compare(REFERENCE, capture({"ignore_roles": True}))["result"], "mismatch")

    def test_resource_matcher_removal_is_detected(self):
        self.assertEqual(compare(REFERENCE, capture({"ignore_resource": True}))["result"], "mismatch")

    def test_action_matcher_removal_is_detected(self):
        self.assertEqual(compare(REFERENCE, capture({"ignore_action": True}))["result"], "mismatch")

    def test_default_allow_mutation_is_detected(self):
        self.assertEqual(compare(REFERENCE, capture({"default_allow": True}))["result"], "mismatch")


if __name__ == "__main__":
    unittest.main()
