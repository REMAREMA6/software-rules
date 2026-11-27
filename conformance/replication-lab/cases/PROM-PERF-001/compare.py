import json, math, statistics, sys
from pathlib import Path

def read(path): return json.loads(Path(path).read_text())
def compare(source, replica):
    if len(source["runs"]) != 3 or len(replica["runs"]) != 3: return ["expected exactly three runs per implementation"]
    errors=[]
    for side, data in (("source",source),("replica",replica)):
        for run in data["runs"]:
            if run["uniqueSeries"] != 200 or run["scrapes"] != 100: errors.append(f"{side}: workload dimensions differ")
            if run["totalSamples"] != 20000: errors.append(f"{side}: expected 20000 samples, got {run['totalSamples']}")
            if run["wallSeconds"] <= 0 or run["samplesPerSecond"] <= 0: errors.append(f"{side}: invalid timing measurement")
    for index,(a,b) in enumerate(zip(source["runs"],replica["runs"]),1):
        for field in ("uniqueSeries","scrapes","totalSamples"):
            if a[field] != b[field]: errors.append(f"run {index}: {field} mismatch {a[field]} != {b[field]}")
    return errors

def summary(data):
    rates=[r["samplesPerSecond"] for r in data["runs"]]
    walls=[r["wallSeconds"] for r in data["runs"]]
    return {"medianSamplesPerSecond":statistics.median(rates),"minSamplesPerSecond":min(rates),
            "maxSamplesPerSecond":max(rates),"medianWallSeconds":statistics.median(walls)}

if __name__=="__main__":
    src,rep=read(sys.argv[1]),read(sys.argv[2])
    errors=compare(src,rep)
    report={"scope":"200 unique series × 100 scrapes; three repeated runs per implementation",
            "semanticMatches":not errors,"source":summary(src),"replica":summary(rep),"errors":errors,
            "performanceComparability":"Separate runtime measurements only; cross-language speed equality is not asserted."}
    Path(sys.argv[3]).write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
    if errors: raise SystemExit(1)
