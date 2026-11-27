# Source candidate — Prometheus

**Repository:** prometheus/prometheus  
**URL:** https://github.com/prometheus/prometheus  
**Immutable inspected commit:** 1e794b83ad0d1df86c26fc607f87197734b9d9d9  
**Licence:** Apache License 2.0  
**Primary stack:** Go  
**Candidate facets:** Performance and resource behaviour; data; API; persistence; errors/recovery.

## Evidence inspected

- CHANGELOG.md at the pinned commit records performance changes and benchmark-related measurements, including sample throughput/query improvements.
- storage/remote/read_handler_test.go contains remote-read handler tests and metric assertions.
- These entries identify candidate measurements and behaviours but do not define a reproducible workload or establish runtime performance characteristics.

## Candidate rule areas

Select one benchmarkable query or ingestion workload. Record dataset, cardinality, concurrency, warm/cold state, hardware/runtime, measurement method, latency distribution, throughput, allocations, and resource use. Compare only under equivalent workload/environment conditions.

**Selected Phase 6 case:** [PROM-PERF-001](../../conformance/replication-lab/cases/PROM-PERF-001/CASE.md). The immutable source boundary is `cmd/promtool/tsdb.go` at the pinned commit, specifically `promtool tsdb bench write`. CI builds the exact source commit and runs a deterministic 200-series × 100-scrape workload three times. The independent Python implementation models the workload-accounting contract; it does not replicate the Prometheus TSDB engine. The case passed three pinned source runs, three independent model runs, three semantic comparisons, mutation tests, and Software Rules schema/integrity validation in [run #45938387274](https://github.com/REMAREMA6/software-rules/actions/runs/45938387274), artifact `15171587211`. This is bounded workload/resource evidence, not complete performance-facet coverage.
