import json,sys
from pathlib import Path
def compare(source,replica):
 a={x["label"]:x for x in source["scenarios"]}; b={x["label"]:x for x in replica["scenarios"]}; errors=[]
 if set(a)!=set(b): errors.append("scenario sets differ")
 for label,x in a.items():
  y=b.get(label)
  if y is None: errors.append(f"{label}: missing replica"); continue
  if x["inputs"]!=y["inputs"]: errors.append(f"{label}: candidate input differs")
  if x["output"]!=y["output"]: errors.append(f"{label}: returned price object differs")
 return {"result":"mismatch" if errors else "match","scenarioCount":len(a),"errors":errors}
if __name__=="__main__":
 a,b=(json.loads(Path(p).read_text()) for p in sys.argv[1:3]); r=compare(a,b); print(json.dumps(r,indent=2))
 if r["errors"]: raise SystemExit(1)
