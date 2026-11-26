# Authorization and Permissions Facet

**Maturity:** Draft — Phase 3 facet specification  
**Facet ID:** `authorization-permissions`

## 1. Purpose and boundary

Runtime decisions about whether an identified/authenticated principal or service may perform an operation on a resource. Covers roles, permissions, capabilities, policy evaluation outcomes, and enforcement. Excludes proving who the principal is (Identity/Authentication).

The facet records facts established from the running target. Source declarations and contracts may guide scenarios but must be recorded with their own evidence class.

## 2. Observation unit

The primary observation unit is a **access decision**. A single execution may produce multiple observations and link to observations from other facets. Do not combine unrelated events into a single opaque record.

## 3. Observable payload dimensions

The conceptual payload should support:
- Principal identity reference.
- Authentication context reference.
- Action.
- Resource.
- Environment/context attributes.
- Policy/role/capability evidence where exposed.
- Decision (permit/deny/indeterminate).
- Enforcement point.
- Response/side effect.
- And reason/evidence when available..

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

Link to Identity/Authentication for principal establishment; Security Controls for enforcement safeguards; API/Interface for observed denial; Business Rules only when domain eligibility is distinct from access permission.

Cross-facet links must use shared capture/target/execution identity and explicit correlation where available. Temporal proximity alone is not proof of causality.

## 8. Worked conceptual example

Use two test principals against the same protected operation and record permit/deny outcomes with identical resource/action context; do not infer complete role policy from two cases. Illustrative only.

## 9. Research and mapping

Reuse relevant standards and platform conventions where they solve a specific part of the facet; do not treat any one of them as the complete Software Rules representation. See [standards review](../../research/STANDARDS-REVIEW.md) and [references](../../research/REFERENCES.md).

## 10. Phase 4 schema questions

Before schema freeze, resolve exact property names/types, optionality, cardinality, stable identifiers, enumerations, units, null/missing/redaction representation, extension handling, and evidence-reference constraints. The schema must preserve the semantic distinctions defined in the common model.
