import json
import sys
from pathlib import Path


def compare(source, replica):
    source_by_label = {item["label"]: item for item in source["scenarios"]}
    replica_by_label = {item["label"]: item for item in replica["scenarios"]}
    errors = []
    if set(source_by_label) != set(replica_by_label):
        errors.append("scenario sets differ")
    fields = ("outcome", "errorType", "errorField")
    for label, actual in source_by_label.items():
        expected = replica_by_label.get(label)
        if expected is None:
            errors.append(f"{label}: missing replica scenario")
            continue
        for field in fields:
            if actual.get(field) != expected.get(field):
                errors.append(f"{label}.{field}: source={actual.get(field)!r}, replica={expected.get(field)!r}")
        if actual["outcome"] == "rejected" and not actual.get("isMedusaError"):
            errors.append(f"{label}: source rejection was not a MedusaError")
    return {
        "result": "mismatch" if errors else "match",
        "scenarioCount": len(source_by_label),
        "comparedFields": ["accept/reject outcome", "Medusa invalid_data category", "field-specific validation order"],
        "errors": errors,
    }


if __name__ == "__main__":
    source_path, replica_path = map(Path, sys.argv[1:3])
    report = compare(json.loads(source_path.read_text()), json.loads(replica_path.read_text()))
    print(json.dumps(report, indent=2))
    if report["errors"]:
        raise SystemExit(1)
