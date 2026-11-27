import json,sys
from pathlib import Path
def compare(a,b):
 x={s["label"]:s["value"] for s in a["scenarios"]};y={s["label"]:s["value"] for s in b["scenarios"]};errors=[]
 if set(x)!=set(y):errors.append("scenario labels differ")
 for label,value in x.items():
  if y.get(label)!=value:errors.append(f"{label}: source={value!r} replica={y.get(label)!r}")
 return {"result":"mismatch" if errors else "match","scenarioCount":len(x),"errors":errors}
if __name__=="__main__":
 a,b=(json.loads(Path(p).read_text()) for p in sys.argv[1:3]);r=compare(a,b);print(json.dumps(r,indent=2))
 if r["errors"]:raise SystemExit(1)
