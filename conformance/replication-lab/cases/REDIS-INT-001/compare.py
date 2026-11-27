import json
import sys
from pathlib import Path


def compare(source, replica):
    left = {item["label"]: item for item in source["scenarios"]}
    right = {item["label"]: item for item in replica["scenarios"]}
    errors = []
    if set(left) != set(right):
        errors.append("scenario sets differ")
    for label, expected in left.items():
        actual = right.get(label)
        if actual is None:
            errors.append(f"{label}: missing replica scenario")
            continue
        if expected.get("request") != actual.get("request"):
            errors.append(f"{label}: logical request differs")
        for field in ("outcome", "value"):
            if expected.get(field) != actual.get(field):
                errors.append(f"{label}.{field}: source={expected.get(field)!r}, replica={actual.get(field)!r}")
    return {"result": "mismatch" if errors else "match", "scenarioCount": len(left),
            "comparedDimensions": ["logical operation", "dependency outcome", "normalized value"], "errors": errors}


if __name__ == "__main__":
    source_path, replica_path = map(Path, sys.argv[1:3])
    report = compare(json.loads(source_path.read_text()), json.loads(replica_path.read_text()))
    print(json.dumps(report, indent=2))
    if report["errors"]:
        raise SystemExit(1)
