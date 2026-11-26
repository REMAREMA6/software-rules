import unittest

from retry_policy import RetryDecision, decide_retry, exponential, fixed


class RetryPolicyTests(unittest.TestCase):
    def test_attempt_limit_counts_total_attempts(self):
        self.assertEqual(decide_retry(3, 0), RetryDecision(True, 0, "waiting"))
        self.assertEqual(decide_retry(3, 1), RetryDecision(True, 0, "waiting"))
        self.assertEqual(decide_retry(3, 2), RetryDecision(False, 0, "failed"))

    def test_unrecoverable_error_suppresses_retry(self):
        self.assertEqual(
            decide_retry(3, 0, unrecoverable=True),
            RetryDecision(False, 0, "failed"),
        )

    def test_max_started_attempts_suppresses_retry(self):
        self.assertEqual(
            decide_retry(5, 0, attempts_started=2, max_started_attempts=2),
            RetryDecision(False, 0, "failed"),
        )

    def test_positive_custom_backoff_schedules_delayed_state(self):
        self.assertEqual(
            decide_retry(3, 0, backoff=fixed(1500)),
            RetryDecision(True, 1500, "delayed"),
        )

    def test_zero_backoff_requeues_immediately(self):
        self.assertEqual(
            decide_retry(3, 0, backoff=fixed(0)),
            RetryDecision(True, 0, "waiting"),
        )

    def test_minus_one_backoff_suppresses_retry(self):
        self.assertEqual(
            decide_retry(3, 0, backoff=fixed(-1)),
            RetryDecision(False, 0, "failed"),
        )

    def test_exponential_backoff_uses_one_based_attempt_number(self):
        strategy = exponential(1000)
        self.assertEqual([strategy(n) for n in (1, 2)], [1000, 2000])
        self.assertEqual(
            decide_retry(3, 0, backoff=strategy),
            RetryDecision(True, 1000, "delayed"),
        )
        self.assertEqual(
            decide_retry(3, 1, backoff=strategy),
            RetryDecision(True, 2000, "delayed"),
        )

    def test_off_by_one_mutation_is_detected(self):
        # Deliberate mutant: permits one retry beyond the configured attempt limit.
        def mutant(attempts, attempts_made):
            if attempts_made + 1 > attempts:
                return RetryDecision(False, 0, "failed")
            return RetryDecision(True, 0, "waiting")

        expected = decide_retry(3, 2)
        mutated = mutant(3, 2)
        self.assertNotEqual(mutated, expected)
        self.assertEqual(expected, RetryDecision(False, 0, "failed"))


if __name__ == "__main__":
    unittest.main()
