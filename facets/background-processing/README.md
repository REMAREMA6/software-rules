# Background Processing Facet

**Maturity:** Draft — Software Rules specification 0.3.0  
**Facet ID:** `background-processing`

## 1. Purpose and boundary

Work executed outside the initiating synchronous interaction: scheduled tasks, queues, workers, deferred jobs, batch operations, and asynchronous lifecycle. Excludes message transport itself (Messaging) and synchronous request handling (API).

The facet records facts established from the running target. Source declarations and contracts may guide scenarios but must be recorded with their own evidence class.

## 2. Observation unit

The primary observation unit is a **job lifecycle**. A single execution may produce multiple observations and link to observations from other facets. Do not combine unrelated events into a single opaque record.

## 3. Observable payload dimensions

The conceptual payload should support:
- Job/task identity.
- Trigger/source.
- Schedule/time basis.
- Enqueue/acceptance.
- Worker identity/version.
- Lifecycle states.
- Attempt count.
- Start/end.
- Inputs/reference.
- Output.
- Side effects.
- Timeout/cancellation.
- Retry/backoff.
- Terminal result.
- correlation to initiating operation.

These dimensions describe the facet's semantic inventory. The current serialization mapping is in [`schemas/v1/facets/`](././schemas/v1/facets/); the JSON Schema defines the draft 0.2.0 wire structure, while this document defines the intended meaning. The schema does not prove that a particular capture inventoried every property required by its declared replication scope. Preserve raw evidence and record normalization separately.

## 4. Scenario requirements

A useful scenario identifies:
- Target/build, environment, relevant configuration, and system boundary.
- Initial state, actor/principal, and preconditions.
- Trigger and ordered actions or events.
- Inputs and relevant external dependency state.
- Observable questions and stopping/settling condition.
- Expected outcome only when an independent oracle/contract exists.

Record one execution per attempt. Repeated runs must remain separately identifiable.

## 5. Evidence requirements

Use evidence appropriate to the facet and identify the actual runtime method: external black-box observation, platform/runtime inspection, or runtime instrumentation. Record tool/protocol/version, time/order, sampling, permissions, redaction, and known limitations. Link raw records where possible. A source file or declared contract is not runtime evidence.

## 6. Missingness and limitations

Distinguish observed empty/zero/false from unknown, not observed, unavailable, not applicable, redacted, partial, and conflicting. State which dimensions were not captured and why. Do not infer absence from missing telemetry or a single execution.

## 7. Cross-facet relationships

Link to Messaging for queue delivery; Persistence for durable job state/results; API/Behaviour for initiation; Errors and Recovery for retries/failure.

Cross-facet links must use shared capture/target/execution identity and explicit correlation where available. Temporal proximity alone is not proof of causality.

## 8. Worked conceptual example

Trigger a report-generation task and observe enqueue, start, completion, output artifact, and any retry. A single completion does not establish scheduling guarantees. Illustrative only.

## 9. Research and mapping

Reuse relevant standards and platform conventions where they solve a specific part of the facet; do not treat any one of them as the complete Software Rules representation. See [standards review](././research/STANDARDS-REVIEW.md) and [references](././research/REFERENCES.md).

## 10. Serialization mapping and remaining limits

The corresponding typed payload schema is maintained in `schemas/v1/facets/`. Schema validation checks the declared serialization shape; it does not determine whether the inventory is exhaustive, whether the observation is true, or whether evidence is semantically sufficient. Those determinations remain governed by the common model, the Replication Completeness Rule, and the conformance review process.