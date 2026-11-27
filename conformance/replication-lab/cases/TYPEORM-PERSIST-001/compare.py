import json
import sys
from pathlib import Path


def compare(source, replica):
    source_by_label = {item["label"]: item for item in source["scenarios"]}
    replica_by_label = {item["label"]: item for item in replica["scenarios"]}
    errors = []
    if set(source_by_label) != set(replica_by_label):
        errors.append("scenario sets differ")

    fields = {
        "commit-success": (
            "terminal", "callbackResult", "postRows", "categoryRows", "postCount", "categoryCount"
        ),
        "rollback-on-invalid-post": (
            "terminal", "errorPropagated", "errorCategory", "readsVisibleBeforeFailure",
            "postRowsAfter", "categoryRowsAfter", "postCountAfter", "categoryCountAfter"
        ),
    }
    for label, compared in fields.items():
        actual = source_by_label.get(label)
        expected = replica_by_label.get(label)
        if actual is None or expected is None:
            errors.append(f"{label}: missing source or replica scenario")
            continue
        for field in compared:
            if actual.get(field) != expected.get(field):
                errors.append(f"{label}.{field}: source={actual.get(field)!r}, replica={expected.get(field)!r}")

    return {
        "result": "mismatch" if errors else "match",
        "scenarioCount": len(replica_by_label),
        "comparedFields": [
            "callback return value",
            "persisted rows after commit",
            "error propagation",
            "rows visible inside the transaction before failure",
            "persisted rows after rollback",
            "semantic integrity-constraint category",
        ],
        "errors": errors,
    }


if __name__ == "__main__":
    source_path, replica_path = map(Path, sys.argv[1:3])
    report = compare(json.loads(source_path.read_text()), json.loads(replica_path.read_text()))
    print(json.dumps(report, indent=2))
    if report["errors"]:
        raise SystemExit(1)
