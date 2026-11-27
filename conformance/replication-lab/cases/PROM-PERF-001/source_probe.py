import json, os, re, resource, statistics, subprocess, sys, time
from pathlib import Path

binary, dataset, output = sys.argv[1:4]
out = []
for index in range(3):
    profile_dir = Path(f"/tmp/prom-perf-source-{index}")
    command = [binary, "tsdb", "bench", "write", "--metrics=200", "--scrapes=100", f"--out={profile_dir}", dataset]
    started = time.perf_counter()
    proc = subprocess.run(command, text=True, capture_output=True, check=True)
    wall = time.perf_counter() - started
    text = proc.stdout + "\n" + proc.stderr
    samples = int(re.search(r"total samples:\s*(\d+)", text).group(1))
    rate = float(re.search(r"samples/sec:\s*([0-9.eE+-]+)", text).group(1))
    rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    profiles = {p.name: p.stat().st_size for p in profile_dir.glob("*.prof")}
    out.append({"run": index + 1, "uniqueSeries": 200, "scrapes": 100, "totalSamples": samples,
                "wallSeconds": wall, "samplesPerSecond": rate, "maxChildRssKb": rss,
                "profileBytes": profiles, "stageOutput": text})
Path(output).write_text(json.dumps({"implementation":"Prometheus promtool / Go","sourceCommit":os.environ["PROM_SOURCE_COMMIT"],
    "environment":{"os":os.uname().sysname,"machine":os.uname().machine,"cpuCount":os.cpu_count()},
    "runs":out}, indent=2)+"\n")
