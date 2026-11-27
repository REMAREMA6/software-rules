import json
from pathlib import Path

from retry_policy import decide_retry, fixed


def simulate(label, attempts, backoff, success_after_failures=None):
    processor_attempts = 0
    failures = 0
    strategy_attempts = []
    backoff_results = []

    while True:
        processor_attempts += 1
        if success_after_failures is not None and failures >= success_after_failures:
            outcome = {
                "terminal": "completed",
                "attemptsMade": failures,
                "result": "ok",
            }
            final_state = "completed"
            break

        failures += 1
        decision = decide_retry(
            attempts=attempts,
            attempts_made=failures - 1,
            backoff=lambda attempt: (
                strategy_attempts.append(attempt) or
                backoff_results.append(backoff(attempt)) or
                backoff_results[-1]
            ),
        )
        if not decision.retry:
            outcome = {
                "terminal": "failed",
                "attemptsMade": failures,
                "error": "processor failure",
            }
            final_state = "failed"
            break

    return {
        "label": label,
        "configuredAttempts": attempts,
        "processorAttempts": processor_attempts,
        "strategyAttempts": strategy_attempts,
        "backoffResults": backoff_results,
        "outcome": outcome,
        "finalState": final_state,
    }


scenarios = [
    simulate(
        "positive-backoff-completes",
        attempts=3,
        backoff=lambda attempt: attempt * 40,
        success_after_failures=2,
    ),
    simulate(
        "minus-one-suppresses-retry",
        attempts=3,
        backoff=lambda _attempt: -1,
    ),
    simulate(
        "zero-delay-respects-attempt-limit",
        attempts=2,
        backoff=lambda _attempt: 0,
    ),
]

capture = {
    "implementation": "independent Python retry-policy model",
    "scenarios": scenarios,
}
print(json.dumps(capture, indent=2))
