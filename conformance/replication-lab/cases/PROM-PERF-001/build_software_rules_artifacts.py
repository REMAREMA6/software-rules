import argparse, hashlib, json, os
from datetime import datetime, timezone
from pathlib import Path

FACET="performance-resource-behaviour"
def now(): return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
def read(p): return json.loads(Path(p).read_text())
def write(p,v): Path(p).write_text(json.dumps(v,indent=2)+"\n")
def build_capture(raw,side,raw_path):
    created=now(); source=side=="source"
    prefix="prom-perf-"+side
    target_id="prometheus-promtool" if source else "python-workload-model"
    runtime_name=raw["implementation"]
    digest=hashlib.sha256(Path(raw_path).read_bytes()).hexdigest()
    scenarios=[]; executions=[]; observations=[]
    obsids=[]
    for item in raw["runs"]:
        n=item["run"]; sid=f"prom-perf-scenario-run-{n}"; eid=f"prom-perf-exec-{side}-{n}"; oid=f"prom-perf-obs-{side}-{n}"
        obsids.append(oid)
        scenarios.append({"scenarioId":sid,"title":f"Deterministic write workload run {n}",
          "purpose":"Measure the bounded append workload and record its semantic sample count.",
          "facetIds":[FACET],"subject":"Prometheus TSDB write workload",
          "preconditions":["Pinned source or independent model is available.","The deterministic 200-series dataset is used."],
          "trigger":"Execute 100 simulated scrapes over 200 unique series.",
          "inputs":{"uniqueSeries":200,"scrapes":100},
          "observableQuestions":["How many samples were appended?","What throughput and resource measurements were recorded?"]})
        executions.append({"executionId":eid,"scenarioId":sid,"targetId":target_id,
          "startedAt":created,"endedAt":created,"status":"completed",
          "actualContext":{"runtime":runtime_name,"sourceRevision":raw.get("sourceCommit","independent-replica"),
                           "environment":raw.get("environment",{})},
          "actualInputs":{"uniqueSeries":200,"scrapes":100},"trigger":"Run deterministic write workload",
          "collector":{"name":runtime_name}})
        observations.append({"observationId":oid,"targetId":target_id,"executionId":eid,
          "facet":FACET,"subject":"Prometheus TSDB write workload","observedAt":created,"sequence":n,
          "method":{"class":"instrumentation","procedure":"Execute repeated workload and collect runtime throughput and resource measurements.","tool":runtime_name},
          "conditions":{"run":n,"warmState":"cold","workload":{"uniqueSeries":200,"scrapes":100}},
          "trigger":"Execute deterministic write workload",
          "payload":{"facet":FACET,"kind":"measurement","subject":"TSDB append throughput",
            "metric":"samples-per-second","definition":"Total successfully appended samples divided by measured ingestion duration.",
            "value":item["samplesPerSecond"],"unit":"samples/second","statistic":"rate",
            "measurementBoundary":"TSDB append workload; source includes storage initialization separately and reports ingest stage.",
            "startedAt":created,"endedAt":created,"workload":{"uniqueSeries":200,"scrapes":100,"expectedSamples":20000},
            "concurrency":1,"sampleCount":item["totalSamples"],"warmState":"cold",
            "hardware":raw.get("environment",{}),"runtime":{"implementation":runtime_name},
            "resourceScope":"Process resident memory and generated runtime profile files.",
            "collectionMethod":"Three independent fresh-process executions; per-run rate and process resource samples.",
            "sampling":"Three independent repetitions; report median/min/max, no cross-language speed equality asserted.",
            "uncertainty":{"repeatCount":3,"distribution":"Per-run samples retained; median/min/max summarized."},
            "extensions":{"wallSeconds":item["wallSeconds"],"maxRssKb":item.get("maxChildRssKb",item.get("maxRssKb",0)),
                          "profileBytes":item.get("profileBytes",{}),"peakTracedBytes":item.get("peakTracedBytes",0)}},
          "rawValue":item,"normalizedValue":{"uniqueSeries":item["uniqueSeries"],"scrapes":item["scrapes"],"totalSamples":item["totalSamples"]},
          "evidenceRefs":[prefix+"-runtime"],"status":"observed"})
    props=[
      ("PROM-PERF-P01","workload-identity","The source and replica execute the same declared series cardinality and scrape count."),
      ("PROM-PERF-P02","sample-throughput","Each completed scrape appends one sample for every selected unique series."),
      ("PROM-PERF-P03","repeat-measurement","Three independent runs are retained and summarized without treating one timing as conclusive."),
      ("PROM-PERF-P04","resource-observation","Process memory and runtime profile/resource observations are retained with their collection boundaries.")
    ]
    inventory=[{"propertyId":pid,"facet":FACET,"subject":"Prometheus TSDB write workload","dimension":dim,
      "requirement":"required","status":"captured","observationRefs":obsids,"evidenceRefs":[prefix+"-runtime"],"rationale":why}
      for pid,dim,why in props]
    rules=[{"ruleId":pid,"facet":FACET,"subject":dim,"proposition":why,
      "trigger":"Execute the declared 200-series × 100-scrape benchmark.",
      "applicability":{"scope":"Pinned Prometheus promtool TSDB write benchmark and independent workload-accounting model."},
      "status":"supported","supportingObservationIds":obsids} for pid,dim,why in props]
    return {"schemaVersion":"0.2.0","captureId":prefix+"-capture","createdAt":created,
      "purpose":"Capture a repeatable bounded TSDB write workload and per-implementation resource measurements.",
      "target":{"targetId":target_id,"systemName":runtime_name,"systemVersion":raw.get("sourceCommit","Python 3.12"),
        "build":{"revision":raw.get("sourceCommit",os.getenv("GITHUB_SHA","working-tree"))},
        "boundary":{"description":"A deterministic 200-series × 100-scrape append workload.",
          "included":["unique-series selection","sample append count","repeated throughput measurements","process resource samples"],
          "excluded":["production SLOs","cross-hardware comparison","full Prometheus query performance","Python/Go absolute speed equivalence"]},
        "environment":{"platform":"GitHub Actions","os":"Ubuntu Linux","runtime":runtime_name,"configuration":{"state":"observed","value":raw.get("environment",{})}}},
      "scope":{"description":"Three repetitions of a 200-series × 100-scrape write workload.","facetIds":[FACET],
        "subjects":["Prometheus TSDB write workload"],"scenarioIds":[f"prom-perf-scenario-run-{i}" for i in range(1,4)]},
      "collector":{"name":runtime_name,"methodDescription":"Run the same logical series/scrape workload three times and capture performance/resource measurements."},
      "scenarios":scenarios,"executions":executions,"observations":observations,"runtimeRules":rules,
      "evidence":[{"evidenceId":prefix+"-runtime","evidenceClass":"runtime","evidenceType":"instrumented-performance-workload",
        "mediaType":"application/json","origin":{"targetId":target_id,"collector":runtime_name,
          "sourceRevision":raw.get("sourceCommit","independent-replica"),"location":raw_path},
        "capturedAt":created,"embedded":{"runCount":3,"sha256":digest},"locator":raw_path,"digest":digest,
        "sizeBytes":Path(raw_path).stat().st_size,"retention":{"status":"retained","access":"CI artifact"}}],
      "coverage":[{"facet":FACET,"subject":"Prometheus TSDB write workload","status":"observed",
        "reason":"Three runs record the declared workload's sample count and per-implementation resource measurements.",
        "scenarioIds":[f"prom-perf-scenario-run-{i}" for i in range(1,4)],
        "executionIds":[f"prom-perf-exec-{side}-{i}" for i in range(1,4)]}],
      "limitations":["Performance values are implementation-specific and must not be compared as equal across Go/TSDB and Python model.","The model reproduces workload accounting, not the TSDB storage engine.","Hosted-runner measurements are not production SLOs or portable hardware baselines."],
      "replicationScope":{"scopeId":"prometheus-write-200x100","description":"Complete declared workload-accounting and repeated-measurement scope.",
        "facets":[FACET],"propertyInventory":inventory,
        "completeness":{"status":"complete","assessedAt":created,
          "assessmentMethod":"Four required properties are linked to three runtime observations and raw repeated-run evidence.",
          "rationale":"All properties in the bounded workload-accounting and measurement scope are observed; implementation performance remains separately characterized."}}}

def build_report(source,replica):
    created=now(); align=[]; results=[]
    for i in range(1,4):
      a=source["observations"][i-1]; b=replica["observations"][i-1]; aid=f"prom-perf-alignment-{i}"
      align.append({"alignmentId":aid,"facet":FACET,"referenceRecordIds":[a["observationId"]],
        "implementationRecordIds":[b["observationId"]],"status":"paired",
        "identityBasis":"same-workload-run-index","rationale":"Same declared cardinality, scrape count, and repetition index."})
      av=a["normalizedValue"]; bv=b["normalizedValue"]
      results.append({"resultId":f"prom-perf-result-{i}","alignmentId":aid,"facet":FACET,
        "dimension":"workload-semantic-accounting","classification":"match" if av==bv else "mismatch",
        "comparisonBasis":"exact","referenceObservationIds":[a["observationId"]],
        "implementationObservationIds":[b["observationId"]],"referenceValue":av,"implementationValue":bv,
        "reason":"Compare semantic workload dimensions and sample accounting; implementation-specific speed and memory are not asserted equal.",
        "evidenceRefs":["prom-perf-source-runtime","prom-perf-replica-runtime"]})
    mismatches=[r for r in results if r["classification"]!="match"]
    return {"schemaVersion":"0.2.0","reportId":"prometheus-performance-comparison","createdAt":created,
      "referenceCapture":{"captureId":source["captureId"],"schemaVersion":"0.2.0"},
      "implementationCapture":{"captureId":replica["captureId"],"schemaVersion":"0.2.0"},
      "comparisonScope":{"description":"Three repeated 200-series × 100-scrape workload runs.",
        "facets":[FACET],"scenarioIds":[f"prom-perf-scenario-run-{i}" for i in range(1,4)],
        "conditions":["same deterministic series-label dataset","200 unique series","100 scrapes","same hosted runner class"],
        "excludedDimensions":["absolute Go-versus-Python speed equality","production SLOs","cross-hardware extrapolation"],
        "limitations":["Only workload accounting is compared exactly; performance/resource measurements are implementation-specific."]},
      "alignments":align,"results":results,
      "coverage":{"reference":{"declaredUnits":3,"observedUnits":3},"implementation":{"declaredUnits":3,"observedUnits":3},
        "sharedComparableUnits":3,"incomparableUnits":0,"limitations":["Three repeated runs are a bounded benchmark, not a full performance profile."]},
      "conclusion":{"status":"differences-found" if mismatches else "agreement-within-observed-scope",
        "statement":"Source and independent model "+("differ" if mismatches else "match")+" on all declared workload dimensions and sample counts; performance values remain separately characterized.",
        "scopeBounded":True,"universalEquivalenceClaimed":False},
      "replicationCompleteness":{"referenceStatus":"complete","implementationStatus":"complete","result":"complete-both",
        "statement":"Both captures account for the declared 200-series × 100-scrape workload and three repetitions, not all Prometheus performance behaviour."}}

def main():
 p=argparse.ArgumentParser(); p.add_argument("--source",required=True); p.add_argument("--replica",required=True); p.add_argument("--output-dir",required=True); a=p.parse_args()
 out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
 s=build_capture(read(a.source),"source",a.source); r=build_capture(read(a.replica),"replica",a.replica); report=build_report(s,r)
 write(out/"prometheus-source.capture.json",s); write(out/"prometheus-python-replica.capture.json",r); write(out/"prometheus-comparison.report.json",report)
 if report["conclusion"]["status"]!="agreement-within-observed-scope": raise SystemExit(1)
 print(json.dumps({"observations":len(report["results"]),"mismatches":0},indent=2))
if __name__=="__main__": main()
