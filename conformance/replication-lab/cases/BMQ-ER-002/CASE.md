# Case — BullMQ custom retry/backoff semantics

**Case ID:** BMQ-ER-002  
**Status:** PASSED for the declared three-scenario scope. Pinned-source runtime, independent Python replica, 12 semantic comparisons, mutation tests, Software Rules schema validation, and cross-record evidence integrity all pass; broader BullMQ retry behaviour remains out of scope.  
**Facet(s):** Background processing; Errors and recovery  
**Source:** https://github.com/taskforcesh/bullmq  
**Source commit:** 526668f2c5e6de9d5d664df577f09a6bdccac1b4  
**Source stack:** TypeScript / Node.js with Redis-backed queue  
**Replica stack:** Python 3.12 decision-model simulation (independent of BullMQ; deliberately narrower than the queue implementation)  
**Rules:** BMQ-ER-001 (bounded attempt-limit branch), BMQ-ER-002 (custom backoff routing), BMQ-ER-003 (attemptsMade counter semantics)

## Declared scope

A single queued job is processed by a BullMQ worker under a deterministic custom backoff strategy. This case covers exactly three scenarios: (1) two failures with positive delays followed by success; (2) a custom backoff result of -1 suppressing retry; and (3) zero-delay retry followed by failure at an attempts=2 limit. It validates processor-start and terminal attemptsMade values, backoff inputs/results, ordered queue state events, and terminal job state. It does not cover the full BullMQ retry policy or worker lifecycle.

## Current source-derived rule hypothesis

A job with a configured retry-attempt policy can be retried after processor failure. A custom backoff strategy may calculate the retry delay; source tests demonstrate strategies that inspect the thrown error, inspect/update job data, and return an asynchronous result.

This is a source-derived hypothesis, not yet an established runtime rule in this project.

## Evidence inspected

- Retry guide: docs/gitbook/guide/retrying-failing-jobs.md.
- Implementation: src/classes/job.ts, especially shouldRetryJob and failure handling around source lines 683–830.
- Worker lifecycle: src/classes/worker.ts.
- Tests: tests/worker.test.ts around lines 4596–4747.

Source code and tests are pinned to the immutable commit above. See the associated source record for limitations and unresolved questions.

## In-scope runtime probe matrix

| Scenario | Purpose | Result |
|---|---|---|
| attempts=3; two failures with positive delays, then success | Delayed retries, one-based strategy attempts, successful terminal state, and final attemptsMade | Pass — run [#25](https://github.com/REMAREMA6/software-rules/actions/runs/45925568609) |
| attempts=3; custom strategy returns -1 | Retry suppression and terminal failed state | Pass — run #25 |
| attempts=2; custom strategy returns 0; processor always fails | Immediate requeue and attempt-limit boundary | Pass — run #25 |

## Explicitly out-of-scope extensions

These are not required for this bounded case and remain unverified: no attempts option; attempts=1; attempts=3 with permanent failure; fixed backoff; exponential backoff (including the guide's wording ambiguity); strategy decisions based on error/job data; asynchronous custom strategy; strategy throws/rejections/invalid values; worker shutdown during delay; unrecoverable errors; maxStartedAttempts; stalled-job recovery; and other worker lifecycle paths.

## Independent replica

A narrow independent Python implementation is committed under conformance/replication-lab/projects/retry-policy-python/. It models retry eligibility, attempt counts, custom backoff decisions, and the terminal result for the declared scenarios; it does not recreate BullMQ, Redis, queue storage, or the worker scheduler. It uses no BullMQ imports. The Python scenario simulator generates a separate replica capture, and the comparison script checks shared semantic fields against the source runtime capture.

The original eight Python decision-model tests passed in GitHub Actions. Additional simulator/comparator tests also pass in CI, including mutations to the attempt count and backoff sequence. This verifies the replica and comparator logic internally; source/runtime equivalence remains unproven until the pinned-source workflow completes and its JSON artifacts are reviewed.

Source-derived capture: examples/cross-repository/captures/bullmq-source.capture.json. It explicitly records the two rules as source-inferred and marks replication completeness incomplete.

## Comparison and mutation

The Python suite detects an off-by-one attempt-limit mutation. Comparator tests detect changed processor-attempt counts, backoff sequences, and state transitions. The pinned BullMQ runtime and independent Python model matched all three scenarios in run #25. The comparison includes processor-start attemptsMade values, terminal attemptsMade, state transitions, and backoff results. The generated Software Rules 0.2.0 captures and comparison report passed schema and cross-record evidence validation. Additional retry modes and worker lifecycle paths are explicitly out of scope for this case.

## Current conclusion

**Passed for the declared bounded scope.** The pinned BullMQ source runtime and independent Python model match across three scenarios and 12 facet/scenario projections. The source and replica Software Rules 0.2.0 captures each contain 12 observations across four facets, three supported runtime rules, and six captured inventory properties. The comparison report records agreement within scope and complete-both completeness for this case. Schema and cross-record evidence validation passed in [workflow run #25](https://github.com/REMAREMA6/software-rules/actions/runs/45925568609), and all six raw/structured evidence artifacts were committed at [commit 513766d](https://github.com/REMAREMA6/software-rules/commit/513766df3b9d4300df4c9297b79f221b54e29e42). The wider BullMQ retry policy remains incomplete and must not be inferred from this result.
