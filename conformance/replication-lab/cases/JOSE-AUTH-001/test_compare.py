import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projects" / "jwt-auth-python"))

from compare import compare
from replica_probe import capture, sign_token_fixture_capture


def source_fixture():
    return sign_token_fixture_capture()


class JoseJwtAuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.source = source_fixture()

    def test_independent_verifier_matches_reference_fixture(self):
        report = compare(self.source, capture(self.source))
        self.assertEqual(report["result"], "match", report["errors"])

    def test_signature_verification_mutation_is_detected(self):
        self.assertEqual(compare(self.source, capture(self.source, verify_signature=False))["result"], "mismatch")

    def test_expiration_check_mutation_is_detected(self):
        self.assertEqual(compare(self.source, capture(self.source, verify_exp=False))["result"], "mismatch")

    def test_not_before_check_mutation_is_detected(self):
        self.assertEqual(compare(self.source, capture(self.source, verify_nbf=False))["result"], "mismatch")

    def test_issuer_check_mutation_is_detected(self):
        self.assertEqual(compare(self.source, capture(self.source, enforce_issuer=False))["result"], "mismatch")

    def test_audience_check_mutation_is_detected(self):
        self.assertEqual(compare(self.source, capture(self.source, enforce_audience=False))["result"], "mismatch")

    def test_algorithm_allowlist_mutation_is_detected(self):
        self.assertEqual(compare(self.source, capture(self.source, allow_hs384=True))["result"], "mismatch")

    def test_required_claim_mutation_is_detected(self):
        self.assertEqual(compare(self.source, capture(self.source, require_claims=False))["result"], "mismatch")


if __name__ == "__main__":
    unittest.main()
