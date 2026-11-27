# Case — BullMQ message delivery, duplicate suppression, and consumer outcome

**Case ID:** BMQ-MSG-001  
**Status:** Source runtime probe, independent Python model, comparator, and mutation tests prepared; runtime recheck queued after observed QueueEvents trace reconciliation.  
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

Comparator tests detect duplicate processing, payload overwrite, missing completion acknowledgement, reordered queue events, and a failed consumer incorrectly marked completed.

## Acceptance gate

This case remains pending until the pinned BullMQ+Redis runtime, Python replica, equivalent comparisons, mutation tests, schema/integrity validation, and retained evidence all pass. It does not establish all message broker delivery guarantees or exactly-once processing.
