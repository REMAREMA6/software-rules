import json

from retry_policy import decide_retry


def simulate(label, attempts, backoff, success_after_failures=None):
    processor_attempts = 0
    processor_attempts_made = []
    failures = 0
    strategy_attempts = []
    backoff_results = []
    state_transitions = []

    while True:
        processor_attempts += 1
        processor_attempts_made.append(failures)
        if success_after_failures is not None and failures >= success_after_failures:
            outcome = {
                "terminal": "completed",
                # BullMQ increments attemptsMade after a successful completion too.
                "attemptsMade": failures + 1,
                "result": "ok",
            }
            state_transitions.append("completed")
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
            state_transitions.append("failed")
            final_state = "failed"
            break

        if decision.state == "delayed":
            state_transitions.append("delayed")
        state_transitions.append("waiting")

    return {
        "label": label,
        "configuredAttempts": attempts,
        "processorAttempts": processor_attempts,
        "processorAttemptsMade": processor_attempts_made,
        "strategyAttempts": strategy_attempts,
        "backoffResults": backoff_results,
        "stateTransitions": state_transitions,
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
