# Case — BullMQ custom retry/backoff semantics

**Case ID:** BMQ-ER-002  
**Status:** source-derived rules captured; independent Python decision-model added and locally exercised; source runtime and end-to-end queue comparison pending  
**Facet(s):** Background processing; Errors and recovery  
**Source:** https://github.com/taskforcesh/bullmq  
**Source commit:** 526668f2c5e6de9d5d664df577f09a6bdccac1b4  
**Source stack:** TypeScript / Node.js with Redis-backed queue  
**Replica stack:** undecided; must be independent and different  
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
| attempts=3; succeeds after one/two failures | Establish retry transition and completion | Not run |
| Fixed backoff | Establish delay semantics | Not run |
| Exponential backoff | Establish exact delay sequence and resolve documentation ambiguity | Not run |
| Custom strategy returns positive delay | Establish delayed retry | Not run |
| Custom strategy returns 0 | Establish immediate retry and ordering | Not run |
| Custom strategy returns -1 | Establish no-retry terminal outcome | Not run |
| Custom strategy varies by error/job data | Establish strategy inputs | Not run |
| Custom strategy is asynchronous | Establish awaited strategy semantics | Not run |
| Strategy throws/rejects/returns invalid value | Establish error path | Not run |
| Worker closes during delay | Establish shutdown interaction | Not run |

## Independent replica

A narrow independent Python implementation is committed under conformance/replication-lab/projects/retry-policy-python/. It models only retry eligibility and retry routing; it does not recreate BullMQ, Redis, or the worker scheduler. It uses no BullMQ imports.

The eight corresponding Python test cases were exercised in an isolated local Python run and passed, including an off-by-one mutation check. The committed test module still needs to be run through the repository's automated workflow. This validates the Python model against the extracted source-code proposition, not against BullMQ runtime output.

Source-derived capture: examples/cross-repository/captures/bullmq-source.capture.json. It explicitly records the two rules as source-inferred and marks replication completeness incomplete.

## Comparison and mutation

The local Python test includes a deliberate off-by-one attempt-limit mutation and demonstrates that the expected terminal-failure case distinguishes it. Full source/replica capture comparison is not yet possible because the source runtime has not been executed. Additional required mutations include ignoring the configured delay and retrying when the strategy explicitly suppresses retry.

## Current conclusion

No pass claim. Source inspection has identified candidate rules and a discriminating test matrix; runtime capture and independent cross-stack replication remain outstanding.
