# Case — BullMQ delayed-job rescheduling and cancellation

**Case ID:** BMQ-SCHED-001  
**Status:** PASSED for delayed-job rescheduling and cancellation. Pinned BullMQ 6.7.10/Redis 7 matched the independent Python state machine; six deliberate mutations were detected; Software Rules 0.2.0 captures/comparison passed schema and evidence-integrity validation in [run #45945262230](https://github.com/REMAREMA6/software-rules/actions/runs/45945262230), artifact `15174920212` (expires 2026-12-27).  
**Facets:** Background processing; behaviour; messaging; errors and recovery  
**Source:** https://github.com/taskforcesh/bullmq  
**Immutable source commit:** `526668f2c5e6de9d5d664df577f09a6bdccac1b4`  
**Source version:** BullMQ 6.7.10  
**Source stack:** TypeScript / Node.js with Redis 7  
**Replica stack:** Python 3.12 state-machine model  
**Licence:** MIT

## Declared boundary

The case executes BullMQ delayed-job creation, `Job.changeDelay`, worker activation/completion, and delayed-job removal against Redis 7. It does not cover repeatable/cron jobs, parent-child flows, multiple workers, lock contention, graceful shutdown, or distributed scheduler failover.

## Technology-independent rules under test

1. A job added with a positive delay enters the delayed state.
2. Changing a delayed job's delay preserves the delayed state and updates its due time.
3. When due, the job becomes active, is processed once, and reaches completed state.
4. Worker lifecycle events preserve active-before-completed ordering.
5. Removing a delayed job removes it from the queue and prevents execution.
6. Queue counts reflect the terminal and remaining delayed states.

## Probe matrix

Two source-runtime scenarios cover rescheduling to an earlier due time and cancellation before due time. Six deliberate mutations test ignored rescheduling, incorrect state transitions, removal failure, execution after cancellation, event-order reversal, and missing active events.

## Acceptance gate

Accept only after pinned BullMQ/Redis and independent Python state-machine outcomes match, all six mutations are detected, and Software Rules 0.2.0 captures/comparison pass schema and evidence-integrity validation. This is bounded delayed-job lifecycle evidence, not complete background-processing or messaging coverage.
