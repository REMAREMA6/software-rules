import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projects" / "medusa-price-date-python"))

from compare import compare
from replica_probe import capture


def source_fixture():
    return {
        "scenarios": [
            {"label": "omitted-both", "outcome": "accepted", "errorType": None, "errorField": None, "isMedusaError": False},
            {"label": "null-both", "outcome": "accepted", "errorType": None, "errorField": None, "isMedusaError": False},
            {"label": "empty-string-both", "outcome": "accepted", "errorType": None, "errorField": None, "isMedusaError": False},
            {"label": "valid-start-iso", "outcome": "accepted", "errorType": None, "errorField": None, "isMedusaError": False},
            {"label": "valid-end-iso", "outcome": "accepted", "errorType": None, "errorField": None, "isMedusaError": False},
            {"label": "invalid-start", "outcome": "rejected", "errorType": "invalid_data", "errorField": "starts_at", "isMedusaError": True},
            {"label": "invalid-end", "outcome": "rejected", "errorType": "invalid_data", "errorField": "ends_at", "isMedusaError": True},
            {"label": "date-object-start", "outcome": "accepted", "errorType": None, "errorField": None, "isMedusaError": False},
            {"label": "reversed-range", "outcome": "accepted", "errorType": None, "errorField": None, "isMedusaError": False},
            {"label": "both-invalid-start-first", "outcome": "rejected", "errorType": "invalid_data", "errorField": "starts_at", "isMedusaError": True},
        ]
    }


class MedusaPriceDateRuleTests(unittest.TestCase):
    def test_equivalent_date_validation_matches(self):
        self.assertEqual(compare(source_fixture(), capture())["result"], "match")

    def test_empty_string_rejection_mutation_is_detected(self):
        self.assertEqual(compare(source_fixture(), capture(empty_string_is_missing=False))["result"], "mismatch")

    def test_ends_at_validation_omission_is_detected(self):
        self.assertEqual(compare(source_fixture(), capture(validate_end=False))["result"], "mismatch")

    def test_chronology_check_mutation_is_detected(self):
        self.assertEqual(compare(source_fixture(), capture(enforce_order=True))["result"], "mismatch")

    def test_validation_order_mutation_is_detected(self):
        self.assertEqual(compare(source_fixture(), capture(start_first=False))["result"], "mismatch")


if __name__ == "__main__":
    unittest.main()
