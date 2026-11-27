# Source record — BullMQ

**Selection status:** Accepted for one bounded retry/backoff conformance case; broader BullMQ facet coverage remains a candidate/investigation task.  
**Repository:** taskforcesh/bullmq  
**Canonical URL:** https://github.com/taskforcesh/bullmq  
**Immutable commit:** 526668f2c5e6de9d5d664df577f09a6bdccac1b4  
**Commit date:** Not yet independently recorded in this case; verify from GitHub commit metadata before final case acceptance.  
**Licence:** MIT (LICENSE at the selected commit).  
**Primary implementation:** TypeScript/Node.js. The repository also contains implementations for other runtimes; those must not be mistaken for an independent replica in this project.  
**Relevant infrastructure:** Redis-backed distributed queue; the repository README describes a queue with workers and retry/backoff support.  
**Candidate facets:** Background processing; errors and recovery; messaging/event delivery; persistence semantics (candidate only; requires separate transaction/durability analysis).

## Why selected

BullMQ contains explicit worker/job lifecycle code, a retry/backoff guide, and worker tests that exercise retry timing and custom backoff behaviour. It is a suitable source candidate for extracting background-processing and retry rules. It is not yet accepted as runtime evidence because the source tests and documentation have been inspected but not executed in this Phase 6 case.

## Selected boundary

The initial investigation is limited to one queued job processed by a worker, where the processor fails and a configured custom backoff strategy determines the next retry delay. Queue storage, scheduling, and worker state transitions are relevant only where they affect that rule.

## Inspected evidence

- README.md: describes BullMQ as a Redis-based distributed queue and links to its documentation.
- LICENSE: MIT.
- docs/gitbook/guide/retrying-failing-jobs.md: describes attempts, automatic retry, fixed/exponential/custom backoff, and custom strategy outcomes.
- src/classes/job.ts: contains attemptsMade/attemptsStarted state and shouldRetryJob logic; moveToCompleted increments attemptsMade at line 683, shouldRetryJob is at line 706, and moveToFailed increments attemptsMade at line 824.
- tests/worker.test.ts: custom-backoff tests around lines 4596–4747 exercise error-dependent, job-data-dependent, and asynchronous custom backoff strategies.
- src/classes/worker.ts: defines worker lifecycle and events including active, completed, failed, stalled, and error.

## Candidate technology-independent rules

| Rule ID | Facet | Candidate proposition | Evidence class | Status |
|---|---|---|---|---|
| BMQ-BG-001 | Background processing | A worker takes queued jobs and invokes a processor; observable lifecycle events include active, completed, failed, and stalled | Source-derived from worker interface/implementation | Pending runtime verification |
| BMQ-ER-001 | Errors and recovery | A processor failure can trigger an automatic retry when the job's attempt policy allows it | Source-derived from retry guide and job implementation | Pending boundary/runtime verification |
| BMQ-ER-002 | Errors and recovery | A custom backoff result of -1 suppresses retry, a positive delay routes to delayed, and zero routes to waiting | Source-derived plus pinned runtime/independent Python comparison for three scenarios | Bounded scenarios verified; broader branches pending |
| BMQ-ER-003 | Errors and recovery | A custom backoff strategy may inspect the error and job data, and may be asynchronous | Source-derived from worker tests | Pending runtime verification |
| BMQ-BG-002 | Background processing | A custom backoff result of -1 suppresses retry and leaves the job failed; a result of 0 requeues immediately to waiting | Source-derived plus pinned runtime/independent Python comparison | Bounded scenarios verified |\n| BMQ-DATA-001 | Data | attemptsMade increments after failed attempts and successful completion; at processor start it reflects prior failures | Source-derived from pinned Job implementation; observed in three bounded runtime scenarios | Bounded scenarios verified |

## Open questions

- Confirm exact attempt-count semantics and distinguish attempts started from attempts made.
- Confirm behaviour when attempts are omitted, equal to one, or exhausted.
- Confirm whether retry delay is measured from failure time and how delayed jobs are promoted.
- Confirm exact state and event ordering across failed, delayed, waiting, active, and completed states.
- Confirm error handling when a custom strategy throws, rejects, returns an invalid value, or returns -1/0.
- Confirm interaction with worker shutdown, stalled jobs, and duplicate processing.
- The guide's exponential-backoff example contains wording that appears internally inconsistent about the number of retry delays for attempts=3. Do not resolve by assumption; probe the implementation and retain the exact observed sequence.

## Independent replication

A deliberately narrow Python 3.12 decision-model replica exists under `conformance/replication-lab/projects/retry-policy-python/`. It has no BullMQ imports and does not recreate Redis, queue storage, or the worker scheduler. The pinned BullMQ runtime and Python model matched three scenarios in [GitHub Actions run #25](https://github.com/REMAREMA6/software-rules/actions/runs/45925568609): positive delays then completion, -1 suppression, and zero-delay retry followed by attempt-limit failure. The comparison also matched processor attempt counters, strategy arguments/results, state transitions, terminal states, and final attemptsMade values. This is not a complete BullMQ replica.

## Acceptance status

One bounded retry/backoff case has a successful pinned-source runtime-to-Python semantic comparison (run #18). The schema-native source/replica captures, comparison report, raw runtime traces, and raw comparison summary are committed under `conformance/replication-lab/cases/BMQ-ER-002/artifacts/` at [commit 513766d](https://github.com/REMAREMA6/software-rules/commit/513766df3b9d4300df4c9297b79f221b54e29e42). This does not establish full BullMQ coverage or completion of the 15-facet Phase 6 programme.


## Additional messaging case — BMQ-MSG-001

A second bounded case probes duplicate custom job identifiers, first-payload authority, queue event order, successful consumer completion, and terminal consumer failure. The independent replica is a Python 3.12 queue model; the source probe runs against the same pinned BullMQ commit with Redis 7. This is distinct from the retry/backoff case.

**Runtime status:** Passed in run #45928721261. Two scenarios and ten semantic projections matched; six mutation tests passed. Retained artifact ID 15167806675 expires 2026-12-27.

**Remaining:** Schema-native capture/report generation and evidence-integrity validation are being added. The case does not establish exactly-once delivery, redelivery after crash, or all queue lifecycle semantics.
