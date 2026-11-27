import json
import sys
from pathlib import Path

FIELDS = {
    "duplicate-id-suppression": ("setup", "processed", "terminal", "eventNames", "counts"),
    "consumer-failure": ("setup", "processed", "terminal", "eventNames", "counts"),
}

def compare(source, replica):
    source_by = {item["label"]: item for item in source["scenarios"]}
    replica_by = {item["label"]: item for item in replica["scenarios"]}
    differences = []
    if set(source_by) != set(replica_by):
        differences.append({"field": "scenario-set", "source": sorted(source_by), "replica": sorted(replica_by)})
    for label, fields in FIELDS.items():
        if label not in source_by or label not in replica_by:
            continue
        for field in fields:
            left, right = source_by[label][field], replica_by[label][field]
            if left != right:
                differences.append({"scenario": label, "field": field, "source": left, "replica": right})
    return {"result": "match" if not differences else "mismatch", "comparedFields": [f"{s}.{f}" for s, fs in FIELDS.items() for f in fs], "differences": differences}

if __name__ == "__main__":
    source, replica = [json.loads(Path(path).read_text()) for path in sys.argv[1:3]]
    report = compare(source, replica)
    print(json.dumps(report, indent=2))
    if report["differences"]:
        raise SystemExit(1)
