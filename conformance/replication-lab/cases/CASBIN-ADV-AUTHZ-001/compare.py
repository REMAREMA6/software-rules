import json,sys
from pathlib import Path

def compare(a,b):
    x={s["label"]:s for s in a["scenarios"]}; y={s["label"]:s for s in b["scenarios"]}; errors=[]
    if set(x)!=set(y): errors.append("scenario sets differ")
    for label,expected in x.items():
        actual=y.get(label)
        if actual is None: errors.append(f"{label}: missing replica"); continue
        if expected["request"]!=actual["request"]: errors.append(f"{label}: request differs")
        if expected["modelClass"]!=actual["modelClass"]: errors.append(f"{label}: model class differs")
        if expected["decision"]!=actual["decision"]: errors.append(f"{label}: source={expected['decision']} replica={actual['decision']}")
    return {"result":"mismatch" if errors else "match","scenarioCount":len(x),"errors":errors}
if __name__=="__main__":
    a,b=(json.loads(Path(p).read_text()) for p in sys.argv[1:3]); r=compare(a,b); print(json.dumps(r,indent=2))
    if r["errors"]: raise SystemExit(1)
