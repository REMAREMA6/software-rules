import json, os, resource, sys, time, tracemalloc
from datetime import datetime, timezone
from pathlib import Path

metrics, scrapes, runs = 200, 100, 3
labels = [{"__name__": f"benchmark_metric_{i:04d}", "job": "software-rules", "instance": f"series-{i:04d}"} for i in range(metrics)]
unique = {tuple(sorted(item.items())) for item in labels}
results = []
for run in range(runs):
    started_at=datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
    tracemalloc.start()
    started = time.perf_counter()
    values = {series: 123456789 for series in unique}
    appended = 0
    for _ in range(scrapes):
        for series in values:
            values[series] += 1000
            appended += 1
    elapsed = time.perf_counter() - started
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    ended_at=datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
    results.append({"run":run+1,"startedAt":started_at,"endedAt":ended_at,"uniqueSeries":len(unique),"scrapes":scrapes,"totalSamples":appended,
        "wallSeconds":elapsed,"samplesPerSecond":appended/elapsed if elapsed else 0,
        "peakTracedBytes":peak,"maxRssKb":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
Path(sys.argv[1]).write_text(json.dumps({"implementation":"Independent Python 3.12 workload model",
    "environment":{"os":os.uname().sysname,"machine":os.uname().machine,"cpuCount":os.cpu_count()},
    "runs":results},indent=2)+"\n")
