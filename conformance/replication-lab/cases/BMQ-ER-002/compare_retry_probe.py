import json
import sys
from pathlib import Path


def field_value(source_scenario, field):
    if field == "backoffResults":
        return [
            event["delayMs"]
            for event in source_scenario["trace"]
            if event["event"] == "backoff-result"
        ]
    if field == "processorAttemptsMade":
        return [
            event["attemptsMade"]
            for event in source_scenario["trace"]
            if event["event"] == "processor"
        ]
    if field == "stateTransitions":
        return [
            event["event"].removeprefix("queue:")
            for event in source_scenario["trace"]
            if event["event"] in {
                "queue:delayed",
                "queue:waiting",
                "queue:failed",
                "queue:completed",
            }
        ]
    return source_scenario[field]


def compare_captures(source, replica):
    source_by_label = {item["label"]: item for item in source["scenarios"]}
    replica_by_label = {item["label"]: item for item in replica["scenarios"]}
    fields = (
        "configuredAttempts",
        "processorAttempts",
        "processorAttemptsMade",
        "strategyAttempts",
        "backoffResults",
        "stateTransitions",
        "finalState",
    )
    errors = []
    for label, expected in replica_by_label.items():
        actual = source_by_label.get(label)
        if actual is None:
            errors.append(f"{label}: missing source scenario")
            continue
        for field in fields:
            actual_value = field_value(actual, field)
            expected_value = expected[field]
            if actual_value != expected_value:
                errors.append(
                    f"{label}.{field}: source={actual_value!r}, replica={expected_value!r}"
                )
        for field in ("terminal", "attemptsMade"):
            if actual["outcome"].get(field) != expected["outcome"].get(field):
                errors.append(
                    f"{label}.outcome.{field}: source={actual['outcome'].get(field)!r}, "
                    f"replica={expected['outcome'].get(field)!r}"
                )
        if "result" in expected["outcome"] and actual["outcome"].get("result") != expected["outcome"]["result"]:
            errors.append(f"{label}.outcome.result differs")
    if set(source_by_label) != set(replica_by_label):
        errors.append("source and replica scenario sets differ")

    return {
        "sourceCommit": source.get("sourceCommit"),
        "sourcePackageVersion": source.get("packageVersion"),
        "replica": replica.get("implementation"),
        "comparedFields": list(fields) + ["outcome.terminal", "outcome.attemptsMade"],
        "scenarioCount": len(replica_by_label),
        "result": "mismatch" if errors else "match",
        "errors": errors,
    }


if __name__ == "__main__":
    source_path, replica_path = map(Path, sys.argv[1:3])
    source = json.loads(source_path.read_text())
    replica = json.loads(replica_path.read_text())
    report = compare_captures(source, replica)
    print(json.dumps(report, indent=2))
    if report["errors"]:
        raise SystemExit(1)
