import json,sys
from pathlib import Path
def compare(source,replica):
 a={x["label"]:x["output"] for x in source["scenarios"]}
 b={x["label"]:x["output"] for x in replica["scenarios"]}
 errors=[]
 if set(a)!=set(b):errors.append("scenario labels differ")
 for label,value in a.items():
  if b.get(label)!=value:errors.append(f"{label}: source={value!r}; replica={b.get(label)!r}")
 return {"result":"mismatch" if errors else "match","scenarioCount":len(a),"errors":errors}
if __name__=="__main__":
 r=compare(json.loads(Path(sys.argv[1]).read_text()),json.loads(Path(sys.argv[2]).read_text()))
 print(json.dumps(r,indent=2))
 if r["errors"]:raise SystemExit(1)
