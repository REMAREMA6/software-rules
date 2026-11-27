# Case — BullMQ stalled-job recovery and stalled-limit failure

**Case ID:** BMQ-RECOVERY-001  
**Status:** PASSED in [run #45943469678](https://github.com/REMAREMA6/software-rules/actions/runs/45943469678). The pinned BullMQ runtime and independent Python model matched both stalled-job outcomes, including attemptsStarted/attemptsMade/stalledCounter, events, processed values, and final queue counts. Four deliberate mutations were detected; Software Rules 0.2.0 captures/comparison passed schema, cross-record integrity, and comparison completeness validation. Artifact `15173607117` retained through 2026-12-27. This is bounded stalled-job recovery evidence, not complete BullMQ background-processing or messaging coverage.  
**Facets:** Background processing; messaging; errors and recovery; behaviour; data  
**Source:** https://github.com/taskforcesh/bullmq  
**Immutable source commit:** `526668f2c5e6de9d5d664df577f09a6bdccac1b4`  
**Source stack:** TypeScript / Node.js / Redis  
**Replica stack:** Python 3.12 state-machine model  
**Licence:** MIT

## Declared boundary

A worker is force-closed while a job is active. After its lock expires, a second worker runs BullMQ's stalled checker. The case covers one permitted stalled recovery and the terminal failure when `maxStalledCount=0`. It does not cover multiple simultaneous stalled jobs, parent/child flows, queue-wide pause, Redis failover, or process crash/power-loss semantics beyond the forced worker-close boundary.

## Technology-independent rules

1. A job left active after its worker is force-closed becomes eligible for stalled detection after its lock expires.
2. The stalled checker increments the job's stalled counter and emits a stalled event.
3. If the stalled count is within `maxStalledCount`, the job is returned to the waiting state and may be processed by another worker.
4. A recovered job can complete normally; the final job records its attempts-started, attempts-made, and stalled-counter values.
5. If the stalled count exceeds `maxStalledCount`, the job is moved to failed with the terminal reason `job stalled more than allowable limit`.

## Probes and mutations

Two scenarios cover one successful stalled recovery and immediate terminal failure at a zero stalled limit. Four deliberate mutations target no requeue, ignored stalled limit, wrong attemptsMade accounting, and missing stalled-counter increment.

## Acceptance gate

Accept only after the pinned BullMQ runtime and independent Python model match the two lifecycle outcomes and queue counts, all four mutations are detected, and Software Rules 0.2.0 captures/comparison pass schema and evidence-integrity validation. This is bounded stalled-job recovery evidence, not complete BullMQ background-processing or messaging coverage.
