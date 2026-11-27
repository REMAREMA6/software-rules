import json
import sys
from pathlib import Path


def compare(source, replica):
    source_by_label = {item["label"]: item for item in source["scenarios"]}
    replica_by_label = {item["label"]: item for item in replica["scenarios"]}
    errors = []
    if set(source_by_label) != set(replica_by_label):
        errors.append("scenario sets differ")
    for label, expected in source_by_label.items():
        actual = replica_by_label.get(label)
        if actual is None:
            errors.append(f"{label}: missing replica scenario")
            continue
        if expected.get("request") != actual.get("request"):
            errors.append(f"{label}: request tuple differs")
        if expected.get("decision") != actual.get("decision"):
            errors.append(f"{label}: source={expected.get('decision')}, replica={actual.get('decision')}")
    return {
        "result": "mismatch" if errors else "match",
        "scenarioCount": len(source_by_label),
        "comparedDimensions": ["subject", "resource", "action", "permit/deny decision"],
        "errors": errors,
    }


if __name__ == "__main__":
    source_path, replica_path = map(Path, sys.argv[1:3])
    report = compare(json.loads(source_path.read_text()), json.loads(replica_path.read_text()))
    print(json.dumps(report, indent=2))
    if report["errors"]:
        raise SystemExit(1)
