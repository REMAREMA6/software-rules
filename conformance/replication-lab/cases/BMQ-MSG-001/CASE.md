# Case — BullMQ message delivery, duplicate suppression, and consumer outcome

**Case ID:** BMQ-MSG-001  
**Status:** PASSED for the declared two-scenario scope. Pinned BullMQ+Redis and independent Python queue model match across ten facet/scenario projections; executable replica mutations, Software Rules schema validation, cross-record evidence integrity, and committed artifacts all pass.  
**Facet(s):** Messaging; Behaviour; Background processing; Errors and recovery; Data  
**Source:** https://github.com/taskforcesh/bullmq  
**Source commit:** 526668f2c5e6de9d5d664df577f09a6bdccac1b4  
**Source stack:** TypeScript / Node.js / Redis 7 / BullMQ  
**Replica stack:** Python 3.12 in-memory queue model  
**Licence:** MIT

## Declared scope

Two isolated queue scenarios:
1. Enqueue two jobs with the same custom job identifier before a worker starts. Observe whether the duplicate is suppressed, which payload remains stored, how many times the worker processes it, and the terminal acknowledgement state.
2. Enqueue a single job whose processor throws with attempts=1. Observe the failed terminal state and emitted queue event order.

## Technology-independent rules under test

- A queue identifier configured as unique within the retained job set suppresses a second enqueue using the same identifier; the existing job payload remains authoritative.
- A worker processing a queued job emits a lifecycle progression from waiting to active and then to completed on successful processing.
- A consumer failure at an attempts limit of one ends in a failed state rather than a successful acknowledgement.
- The message/event trace and terminal queue counts must agree with the actual number of jobs processed.

## Source evidence

Pinned BullMQ source repository and the Job IDs guide. The guide states that custom job IDs are unique and adding an existing ID is ignored. The runtime probe validates the Node.js queue/worker behaviour and QueueEvents trace rather than treating documentation alone as runtime evidence.

## Independent replica

The Python model implements only the declared identifier, queue lifecycle, and terminal outcome semantics. It does not use BullMQ, Redis, or BullMQ source code.

## Mutation tests

Executable mutations of the independent Python model detect duplicate processing, payload overwrite, missing completion acknowledgement, reordered queue events, and a failed consumer incorrectly marked completed.

## Result

**Passed for the declared bounded scope.** The pinned BullMQ source at commit `526668f2c5e6de9d5d664df577f09a6bdccac1b4` with Redis 7 and the independent Python 3.12 queue model match both scenarios across ten facet/scenario projections. Executable mutations detect duplicate processing, payload overwrite, missing completion acknowledgement, event reordering, and incorrect failure completion. Software Rules 0.2.0 source/replica captures and the comparison report passed schema and cross-record evidence validation in [workflow run #25](https://github.com/REMAREMA6/software-rules/actions/runs/45929249126). Raw runtime captures, structured captures, and comparison are committed under `artifacts/` at [commit ce9d0e1](https://github.com/REMAREMA6/software-rules/commit/ce9d0e1a0c62830418daa912c1a798561c897a3a). This does not establish exactly-once processing, crash redelivery, delayed jobs, or every message broker delivery guarantee.
