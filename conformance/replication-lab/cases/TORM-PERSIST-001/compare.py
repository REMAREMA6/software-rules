import json
import sys
from pathlib import Path

def compare(source, replica):
    fields = {"rollback": ("error", "callbackResult", "rowsAfterRollback"), "commit": ("callbackReturn", "rowsAfterCommit")}
    differences = []
    for scenario, names in fields.items():
        for name in names:
            left, right = source["scenarios"][scenario][name], replica["scenarios"][scenario][name]
            if left != right:
                differences.append({"scenario": scenario, "field": name, "source": left, "replica": right})
    return {"result": "match" if not differences else "mismatch", "comparedFields": [f"{s}.{f}" for s, ns in fields.items() for f in ns], "differences": differences}

if __name__ == "__main__":
    source, replica = [json.loads(Path(p).read_text()) for p in sys.argv[1:3]]
    report = compare(source, replica)
    print(json.dumps(report, indent=2))
    if report["differences"]: raise SystemExit(1)
