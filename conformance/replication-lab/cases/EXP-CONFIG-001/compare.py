import json, sys
from pathlib import Path

def index(raw):
    return {(s["label"],d["path"]):d["status"] for s in raw["scenarios"] for d in s["decisions"]}
def compare(a,b):
    x,y=index(a),index(b); errors=[]
    if set(x)!=set(y): errors.append("scenario/path sets differ")
    for key,value in x.items():
        if y.get(key)!=value: errors.append(f"{key}: source={value}, replica={y.get(key)}")
    return {"result":"mismatch" if errors else "match","observationCount":len(x),"errors":errors}
if __name__=="__main__":
    a,b=(json.loads(Path(p).read_text()) for p in sys.argv[1:3])
    result=compare(a,b); print(json.dumps(result,indent=2))
    if result["errors"]: raise SystemExit(1)
