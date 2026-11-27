import json
import sys
from pathlib import Path


def compare(source, replica):
    errors = []
    if source.get("configuration") != replica.get("configuration"):
        errors.append("configuration values differ")
    source_by_label = {item["label"]: item for item in source["scenarios"]}
    replica_by_label = {item["label"]: item for item in replica["scenarios"]}
    if set(source_by_label) != set(replica_by_label):
        errors.append("scenario sets differ")

    fields = ("status", "body", "headers", "wireBodyBytes")
    for label, expected in replica_by_label.items():
        actual = source_by_label.get(label)
        if actual is None:
            errors.append(f"{label}: missing source scenario")
            continue
        if actual["request"] != expected["request"]:
            errors.append(f"{label}.request differs")
        for field in fields:
            if actual["response"][field] != expected["response"][field]:
                errors.append(
                    f"{label}.{field}: source={actual['response'][field]!r}, "
                    f"replica={expected['response'][field]!r}"
                )

    return {
        "result": "mismatch" if errors else "match",
        "scenarioCount": len(replica_by_label),
        "comparedFields": ["configuration", "request", "response.status", "response.body", "response.headers"],
        "errors": errors,
    }


if __name__ == "__main__":
    source_path, replica_path = map(Path, sys.argv[1:3])
    report = compare(json.loads(source_path.read_text()), json.loads(replica_path.read_text()))
    print(json.dumps(report, indent=2))
    if report["errors"]:
        raise SystemExit(1)
