import json,sys
from pathlib import Path
def compare(a,b):
 x={v["label"]:v["output"] for v in a["scenarios"]};y={v["label"]:v["output"] for v in b["scenarios"]}
 errors=[]
 if set(x)!=set(y):errors.append("scenario labels differ")
 for k,v in x.items():
  if y.get(k)!=v:errors.append(f"{k}: source={v!r}; replica={y.get(k)!r}")
 return {"result":"mismatch" if errors else "match","scenarioCount":len(x),"errors":errors}
if __name__=="__main__":
 r=compare(json.loads(Path(sys.argv[1]).read_text()),json.loads(Path(sys.argv[2]).read_text()))
 print(json.dumps(r,indent=2))
 if r["errors"]:raise SystemExit(1)
