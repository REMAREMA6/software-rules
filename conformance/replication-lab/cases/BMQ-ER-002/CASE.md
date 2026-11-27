# Case — BullMQ custom retry/backoff semantics

**Case ID:** BMQ-ER-002  
**Status:** pinned-source runtime and independent Python comparison match for three scenarios in run #18; Software Rules schema-native captures and evidence-integrity validation are pending; broader retry cases remain untested  
**Facet(s):** Background processing; Errors and recovery  
**Source:** https://github.com/taskforcesh/bullmq  
**Source commit:** 526668f2c5e6de9d5d664df577f09a6bdccac1b4  
**Source stack:** TypeScript / Node.js with Redis-backed queue  
**Replica stack:** Python 3.12 decision-model simulation (independent of BullMQ; deliberately narrower than the queue implementation)  
**Rules:** BMQ-ER-001 (bounded attempt-limit branch), BMQ-ER-002 (custom backoff routing), BMQ-ER-003 (attemptsMade counter semantics)

## Declared scope

A queued job is processed by a worker. The processor fails and the configured custom backoff strategy determines whether and when the job is retried. This case does not yet cover the full BullMQ lifecycle or all queue semantics.

## Current source-derived rule hypothesis

A job with a configured retry-attempt policy can be retried after processor failure. A custom backoff strategy may calculate the retry delay; source tests demonstrate strategies that inspect the thrown error, inspect/update job data, and return an asynchronous result.

This is a source-derived hypothesis, not yet an established runtime rule in this project.

## Evidence inspected

- Retry guide: docs/gitbook/guide/retrying-failing-jobs.md.
- Implementation: src/classes/job.ts, especially shouldRetryJob and failure handling around source lines 683–830.
- Worker lifecycle: src/classes/worker.ts.
- Tests: tests/worker.test.ts around lines 4596–4747.

Source code and tests are pinned to the immutable commit above. See the associated source record for limitations and unresolved questions.

## Required source probe matrix

| Scenario | Purpose | Status |
|---|---|---|
| No attempts option; processor fails | Establish default failure/no-retry behaviour | Not run |
| attempts=1; processor fails | Establish minimum attempt boundary | Not run |
| attempts=3; processor always fails | Establish total attempts and terminal state | Not run |
| attempts=3; succeeds after two failures | Establish retry transition, completion, and final attemptsMade count | Passed in [run #18](https://github.com/REMAREMA6/software-rules/actions/runs/45924520050) |
| Fixed backoff | Establish delay semantics | Not run |
| Exponential backoff | Establish exact delay sequence and resolve documentation ambiguity | Not run |
| Custom strategy returns positive delay | Establish delayed retry | Passed in run #18 |
| Custom strategy returns 0; attempts=2 and processor always fails | Establish immediate retry and attempt-limit boundary | Passed in run #18 |
| Custom strategy returns -1 | Establish no-retry terminal outcome | Passed in run #18 |
| Custom strategy varies by error/job data | Establish strategy inputs | Not run |
| Custom strategy is asynchronous | Establish awaited strategy semantics | Not run |
| Strategy throws/rejects/returns invalid value | Establish error path | Not run |
| Worker closes during delay | Establish shutdown interaction | Not run |

## Independent replica

A narrow independent Python implementation is committed under conformance/replication-lab/projects/retry-policy-python/. It models retry eligibility, attempt counts, custom backoff decisions, and the terminal result for the declared scenarios; it does not recreate BullMQ, Redis, queue storage, or the worker scheduler. It uses no BullMQ imports. The Python scenario simulator generates a separate replica capture, and the comparison script checks shared semantic fields against the source runtime capture.

The original eight Python decision-model tests passed in GitHub Actions. Additional simulator/comparator tests also pass in CI, including mutations to the attempt count and backoff sequence. This verifies the replica and comparator logic internally; source/runtime equivalence remains unproven until the pinned-source workflow completes and its JSON artifacts are reviewed.

Source-derived capture: examples/cross-repository/captures/bullmq-source.capture.json. It explicitly records the two rules as source-inferred and marks replication completeness incomplete.

## Comparison and mutation

The Python suite detects an off-by-one attempt-limit mutation. Comparator tests also detect changed processor-attempt counts, backoff sequences, and state transitions. The pinned BullMQ runtime and independent Python model matched all three scenarios in [run #18](https://github.com/REMAREMA6/software-rules/actions/runs/45924520050). The comparison includes processor-start attemptsMade values and the terminal attemptsMade counter. The follow-up workflow generates Software Rules 0.2.0 source/replica captures and a comparison report, then validates schemas and cross-record evidence integrity. Further case completion still requires broader mutations and additional probes for attempts omitted/1, fixed/exponential strategies, custom strategy failures, asynchronous behaviour, and worker shutdown.

## Current conclusion

The three-scenario raw runtime-to-replica comparison passes. This is a bounded result, not a full BullMQ retry-policy pass. The formal Software Rules captures and comparison report must still pass schema and cross-record validation before this case is accepted. The broader retry probe matrix and mutation set remain incomplete.
