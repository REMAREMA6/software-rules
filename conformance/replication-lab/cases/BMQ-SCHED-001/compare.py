import json,sys
from pathlib import Path
def compare(a,b):
 x=a["scenarios"][0];y=b["scenarios"][0];errors=[]
 for group in ("scheduled","cancelled","counts"):
  if x[group]!=y[group]:errors.append(f"{group}: source={x[group]!r}; replica={y[group]!r}")
 return {"result":"mismatch" if errors else "match","scenarioCount":2,"errors":errors}
if __name__=="__main__":
 r=compare(json.loads(Path(sys.argv[1]).read_text()),json.loads(Path(sys.argv[2]).read_text()))
 print(json.dumps(r,indent=2))
 if r["errors"]:raise SystemExit(1)
