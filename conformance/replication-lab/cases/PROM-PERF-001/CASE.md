# Case — Prometheus TSDB write workload and resource measurement

**Case ID:** PROM-PERF-001  
**Status:** PASSED for the declared 200-series × 100-scrape workload and three repetitions in [run #45938387274](https://github.com/REMAREMA6/software-rules/actions/runs/45938387274). The pinned Prometheus command and independent Python model matched all three workload/sample-count comparisons; the dropped-scrape and missing-repeat mutations were detected; Software Rules 0.2.0 source/replica captures and comparison passed schema and evidence-integrity validation. Artifact `15171587211` retained through 2026-12-27. Median observed throughput was approximately 5.64M samples/s for Prometheus and 0.95M samples/s for the Python model; these are implementation-specific measurements, not an equality claim. This is bounded workload/resource evidence, not complete performance-facet coverage.  
**Facet:** Performance and resource behaviour; behaviour; data  
**Source:** https://github.com/prometheus/prometheus  
**Immutable source commit:** `1e794b83ad0d1df86c26fc607f87197734b9d9d9`  
**Source stack:** Go 1.26 / Prometheus TSDB  
**Independent replica:** Python 3.12 workload model  
**Licence:** Apache-2.0

## Declared boundary

The source boundary is the pinned `promtool tsdb bench write` command and its TSDB append path in `cmd/promtool/tsdb.go`. The benchmark creates a fresh TSDB directory, disables compactions, loads a bounded series-label dataset, appends one sample per series per simulated scrape, and commits each scrape batch. The benchmark also records stage duration, sample throughput, and CPU/heap/block/mutex profiles.

The independent Python model reproduces the workload's observable accounting contract, not Prometheus's storage engine or internal implementation. Runtime performance values from Go and Python are recorded separately; they are not treated as numerically equivalent or compared against an arbitrary cross-language speed threshold.

## Technology-independent workload rules

1. The input dataset contributes only unique series identities.
2. A scrape appends one sample for every selected unique series.
3. For a scrape count divisible by 100, the total append count is unique series × requested scrapes.
4. Total sample throughput is total appended samples divided by measured ingestion duration.
5. Measurements must record workload cardinality, scrape count, runtime, hardware/runner context, repeat count, and resource observations.
6. Repeated measurements are summarized as distributions; a single timing is not a performance conclusion.
7. Source and replica must agree on workload identity and semantic sample counts. Runtime speed is reported per implementation, not conflated across different languages and storage architectures.

## Workload and probes

CI creates 200 unique label sets and executes 100 scrapes, producing 20,000 expected samples. Both source and replica execute three independent runs. The comparison checks workload fingerprint, unique-series count, scrape count, and total sample count. A deliberate replica mutation drops one scrape and must fail the comparison.

## Performance interpretation

The case records per-run wall time, samples/second, peak resident memory where available, and Prometheus profile file sizes. The Python model records wall time, samples/second, and peak traced allocation. These are separate implementation measurements on the same hosted runner, not a claim that Python and Prometheus have equal resource costs. No production SLO or universal performance threshold is inferred.

## Acceptance gate

Accept only after the pinned Prometheus command runs three times; the independent model runs three times; semantic workload comparisons match; the one-scrape mutation is detected; repeated measurement summaries and environment metadata are retained; Software Rules captures and comparison validate; and the limitations above remain explicit.
