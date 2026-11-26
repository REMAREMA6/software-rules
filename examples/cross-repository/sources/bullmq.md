# Source record — BullMQ

**Selection status:** Candidate inspected; runtime capture and independent replication not yet complete.  
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
- src/classes/job.ts: contains attemptsMade/attemptsStarted state and shouldRetryJob logic; source lines around 683–830 include failure and retry decision handling.
- tests/worker.test.ts: custom-backoff tests around lines 4596–4747 exercise error-dependent, job-data-dependent, and asynchronous custom backoff strategies.
- src/classes/worker.ts: defines worker lifecycle and events including active, completed, failed, stalled, and error.

## Candidate technology-independent rules

| Rule ID | Facet | Candidate proposition | Evidence class | Status |
|---|---|---|---|---|
| BMQ-BG-001 | Background processing | A worker takes queued jobs and invokes a processor; observable lifecycle events include active, completed, failed, and stalled | Source-derived from worker interface/implementation | Pending runtime verification |
| BMQ-ER-001 | Errors and recovery | A processor failure can trigger an automatic retry when the job's attempt policy allows it | Source-derived from retry guide and job implementation | Pending boundary/runtime verification |
| BMQ-ER-002 | Errors and recovery | A configured custom backoff strategy can determine the delay before a retry | Source-derived from guide and worker tests | Pending runtime verification |
| BMQ-ER-003 | Errors and recovery | A custom backoff strategy may inspect the error and job data, and may be asynchronous | Source-derived from worker tests | Pending runtime verification |
| BMQ-BG-002 | Background processing | A custom backoff result of -1 suppresses retry and leaves the job failed; a result of 0 requests immediate requeue semantics | Source-derived from guide | Pending exact state/order verification |

## Open questions

- Confirm exact attempt-count semantics and distinguish attempts started from attempts made.
- Confirm behaviour when attempts are omitted, equal to one, or exhausted.
- Confirm whether retry delay is measured from failure time and how delayed jobs are promoted.
- Confirm exact state and event ordering across failed, delayed, waiting, active, and completed states.
- Confirm error handling when a custom strategy throws, rejects, returns an invalid value, or returns -1/0.
- Confirm interaction with worker shutdown, stalled jobs, and duplicate processing.
- The guide's exponential-backoff example contains wording that appears internally inconsistent about the number of retry delays for attempts=3. Do not resolve by assumption; probe the implementation and retain the exact observed sequence.

## Independent replication

Not started. Proposed replica: a small independent Go or Python worker/queue model, with no BullMQ imports and a separately chosen storage/queue mechanism. The exact stack will be selected after the source rule and probe matrix are finalized.

## Acceptance status

Candidate only. No runtime capture, independent replica, comparison report, or mutation result is claimed yet.
