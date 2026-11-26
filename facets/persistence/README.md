# Persistence Facet

**Maturity:** Draft — Phase 3 facet specification  
**Facet ID:** `persistence`

## 1. Purpose and boundary

Durable or transactionally managed state and its lifecycle as observed through authorized runtime interaction/inspection: reads, writes, commits, rollbacks, consistency, ordering, and retention/deletion. Excludes transient in-memory state unless its persistence boundary is specifically under test.

The facet records facts established from the running target. Source declarations and contracts may guide scenarios but must be recorded with their own evidence class.

## 2. Observation unit

The primary observation unit is a **state operation / transaction**. A single execution may produce multiple observations and link to observations from other facets. Do not combine unrelated events into a single opaque record.

## 3. Observable payload dimensions

The conceptual payload should support:
- Store/resource identity.
- Operation (read/write/update/delete).
- Key/selector.
- Before/after state.
- Transaction boundary.
- Commit/rollback result.
- Consistency/visibility observation.
- Ordering.
- Durability test interval.
- Concurrency context.
- Retention/expiry.
- And evidence access method..

These are semantic dimensions, not frozen serialized field names. Phase 4 will define types, cardinality, requiredness, identifiers, and schema constraints. Preserve raw evidence and record normalization separately.

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

Link to Data for shape; Behaviour for initiating action; API for request; Messaging/Background Processing for asynchronous writes; Errors and Recovery for rollback/retry.

Cross-facet links must use shared capture/target/execution identity and explicit correlation where available. Temporal proximity alone is not proof of causality.

## 8. Worked conceptual example

Create an order through the running system, then read it through an independent authorized path after the request completes; record matching persisted state and observation timing. Illustrative only.

## 9. Research and mapping

Reuse relevant standards and platform conventions where they solve a specific part of the facet; do not treat any one of them as the complete Software Rules representation. See [standards review](../../research/STANDARDS-REVIEW.md) and [references](../../research/REFERENCES.md).

## 10. Phase 4 schema questions

Before schema freeze, resolve exact property names/types, optionality, cardinality, stable identifiers, enumerations, units, null/missing/redaction representation, extension handling, and evidence-reference constraints. The schema must preserve the semantic distinctions defined in the common model.
