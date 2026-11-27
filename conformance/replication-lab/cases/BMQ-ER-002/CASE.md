# Case — BullMQ custom retry/backoff semantics

**Case ID:** BMQ-ER-002  
**Status:** source-derived rules captured; independent Python model/simulator/comparator tests pass CI; pinned-source runtime probe and cross-capture comparison are pending; case not passed  
**Facet(s):** Background processing; Errors and recovery  
**Source:** https://github.com/taskforcesh/bullmq  
**Source commit:** 526668f2c5e6de9d5d664df577f09a6bdccac1b4  
**Source stack:** TypeScript / Node.js with Redis-backed queue  
**Replica stack:** Python 3.12 decision-model simulation (independent of BullMQ; deliberately narrower than the queue implementation)  
**Rule:** BMQ-ER-002

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
| attempts=3; succeeds after two failures | Establish retry transition and completion | CI probe pending |
| Fixed backoff | Establish delay semantics | Not run |
| Exponential backoff | Establish exact delay sequence and resolve documentation ambiguity | Not run |
| Custom strategy returns positive delay | Establish delayed retry | CI probe pending |
| Custom strategy returns 0; attempts=2 and processor always fails | Establish immediate retry and attempt-limit boundary | CI probe pending |
| Custom strategy returns -1 | Establish no-retry terminal outcome | CI probe pending |
| Custom strategy varies by error/job data | Establish strategy inputs | Not run |
| Custom strategy is asynchronous | Establish awaited strategy semantics | Not run |
| Strategy throws/rejects/returns invalid value | Establish error path | Not run |
| Worker closes during delay | Establish shutdown interaction | Not run |

## Independent replica

A narrow independent Python implementation is committed under conformance/replication-lab/projects/retry-policy-python/. It models retry eligibility, attempt counts, custom backoff decisions, and the terminal result for the declared scenarios; it does not recreate BullMQ, Redis, queue storage, or the worker scheduler. It uses no BullMQ imports. The Python scenario simulator generates a separate replica capture, and the comparison script checks shared semantic fields against the source runtime capture.

The original eight Python decision-model tests passed in GitHub Actions. Additional simulator/comparator tests also pass in CI, including mutations to the attempt count and backoff sequence. This verifies the replica and comparator logic internally; source/runtime equivalence remains unproven until the pinned-source workflow completes and its JSON artifacts are reviewed.

Source-derived capture: examples/cross-repository/captures/bullmq-source.capture.json. It explicitly records the two rules as source-inferred and marks replication completeness incomplete.

## Comparison and mutation

The Python suite detects an off-by-one attempt-limit mutation. Comparator tests also detect changed processor-attempt counts and a mutated backoff sequence. The pinned-source workflow compares the three runtime scenarios against the independent Python capture; its result is pending. Further case completion still requires broader mutations, including ignoring the configured delay and retrying when the strategy explicitly suppresses retry.

## Current conclusion

No pass claim yet. The pinned-source runtime workflow is configured to run BullMQ 6.7.10 at the exact inspected commit with Redis 7, generate source traces for three retry scenarios, produce the Python replica capture, compare shared semantic fields, and retain artifacts. The workflow result and artifacts must be reviewed before the case can pass.
