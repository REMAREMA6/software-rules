import json,sys
from pathlib import Path
def compare(a,b):
 x={v["label"]:v for v in a["scenarios"]};y={v["label"]:v for v in b["scenarios"]};errors=[]
 if set(x)!=set(y):errors.append("scenario labels differ")
 for label,value in x.items():
  if y.get(label)!=value:errors.append(f"{label}: source={value!r}; replica={y.get(label)!r}")
 return {"result":"mismatch" if errors else "match","scenarioCount":len(x),"errors":errors}
if __name__=="__main__":
 r=compare(json.loads(Path(sys.argv[1]).read_text()),json.loads(Path(sys.argv[2]).read_text()))
 print(json.dumps(r,indent=2))
 if r["errors"]:raise SystemExit(1)
