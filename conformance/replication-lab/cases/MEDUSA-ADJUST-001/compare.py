import json,sys
from pathlib import Path
def compare(source,replica):
 left={x["label"]:x["output"] for x in source["scenarios"]}
 right={x["label"]:x["output"] for x in replica["scenarios"]}
 errors=[]
 if set(left)!=set(right):errors.append("scenario labels differ")
 for label,expected in left.items():
  if right.get(label)!=expected:errors.append(f"{label}: source={expected!r}; replica={right.get(label)!r}")
 return {"result":"mismatch" if errors else "match","scenarioCount":len(left),"errors":errors}
if __name__=="__main__":
 result=compare(json.loads(Path(sys.argv[1]).read_text()),json.loads(Path(sys.argv[2]).read_text()))
 print(json.dumps(result,indent=2))
 if result["errors"]:raise SystemExit(1)
