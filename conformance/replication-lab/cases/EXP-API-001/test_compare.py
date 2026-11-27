import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projects" / "express-routing-python"))

from compare import compare
from replica_probe import capture


def captures():
    scenarios = [
        ("get-base", "GET", "/widgets", 200, "get", {"content-type": "text/html; charset=utf-8", "content-length": "3", "allow": None}),
        ("head-fallback", "HEAD", "/widgets", 200, "", {"content-type": "text/html; charset=utf-8", "content-length": "3", "allow": None}),
        ("options-auto", "OPTIONS", "/widgets", 200, "GET, HEAD, PUT", {"content-type": "text/html; charset=utf-8", "content-length": "14", "allow": "GET, HEAD, PUT"}),
        ("options-missing", "OPTIONS", "/missing", 404, "not found", {"content-type": "text/html; charset=utf-8", "content-length": "9", "allow": None}),
        ("options-explicit", "OPTIONS", "/override", 200, "GET", {"content-type": "text/html; charset=utf-8", "content-length": "3", "allow": "GET"}),
        ("case-and-trailing-slash", "GET", "/WIDGETS/", 200, "get", {"content-type": "text/html; charset=utf-8", "content-length": "3", "allow": None}),
        ("query-ignored", "GET", "/widgets?color=blue", 200, "get", {"content-type": "text/html; charset=utf-8", "content-length": "3", "allow": None}),
    ]
    source = {"configuration": {"caseSensitiveRouting": False, "strictRouting": False}, "scenarios": []}
    replica = {"configuration": {"caseSensitiveRouting": False, "strictRouting": False}, "scenarios": []}
    for label, method, path, status, body, headers in scenarios:
        item = {
            "label": label,
            "request": {"method": method, "path": path},
            "response": {"status": status, "body": body, "headers": copy.deepcopy(headers), "wireBodyBytes": 0},
        }
        source["scenarios"].append(copy.deepcopy(item))
        replica["scenarios"].append(copy.deepcopy(item))
    return source, replica


class ExpressApiComparisonTests(unittest.TestCase):
    def test_equivalent_http_observations_match(self):
        source, replica = captures()
        report = compare(source, replica)
        self.assertEqual(report["result"], "match")

    def test_head_body_mutation_is_detected(self):
        source, replica = captures()
        replica["scenarios"][1]["response"]["body"] = "get"
        self.assertEqual(compare(source, replica)["result"], "mismatch")

    def test_options_head_method_mutation_is_detected(self):
        source, replica = captures()
        replica["scenarios"][2]["response"]["headers"]["allow"] = "GET, PUT"
        self.assertEqual(compare(source, replica)["result"], "mismatch")

    def test_case_sensitive_mutation_is_detected(self):
        source, replica = captures()
        replica["scenarios"][5]["response"]["status"] = 404
        self.assertEqual(compare(source, replica)["result"], "mismatch")

    def test_strict_trailing_slash_mutation_is_detected(self):
        source, replica = captures()
        replica["scenarios"][5]["response"]["status"] = 404
        self.assertEqual(compare(source, replica)["result"], "mismatch")

    def test_query_path_matching_mutation_is_detected(self):
        source, replica = captures()
        replica["scenarios"][6]["response"]["status"] = 404
        self.assertEqual(compare(source, replica)["result"], "mismatch")


    def test_actual_head_body_mutation_is_detected(self):
        source, _ = captures()
        mutant = capture(suppress_head_body=False)
        self.assertEqual(compare(source, mutant)["result"], "mismatch")

    def test_actual_case_sensitive_mutation_is_detected(self):
        source, _ = captures()
        mutant = capture(case_sensitive=True)
        self.assertEqual(compare(source, mutant)["result"], "mismatch")

    def test_actual_strict_routing_mutation_is_detected(self):
        source, _ = captures()
        mutant = capture(strict_routing=True)
        self.assertEqual(compare(source, mutant)["result"], "mismatch")

    def test_actual_options_method_mutation_is_detected(self):
        source, _ = captures()
        mutant = capture(options_includes_head=False)
        self.assertEqual(compare(source, mutant)["result"], "mismatch")

    def test_actual_options_override_mutation_is_detected(self):
        source, _ = captures()
        mutant = capture(explicit_options_override=False)
        self.assertEqual(compare(source, mutant)["result"], "mismatch")

    def test_actual_query_matching_mutation_is_detected(self):
        source, _ = captures()
        mutant = capture(query_in_path=True)
        self.assertEqual(compare(source, mutant)["result"], "mismatch")

    def test_explicit_options_override_mutation_is_detected(self):
        source, replica = captures()
        replica["scenarios"][4]["response"]["headers"]["allow"] = "GET, HEAD, PUT"
        self.assertEqual(compare(source, replica)["result"], "mismatch")


if __name__ == "__main__":
    unittest.main()
