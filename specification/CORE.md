# Software Rules Core Model

**Maturity:** Draft — Software Rules specification 0.3.0.

## 1. Purpose

The core model defines the minimum shared structure for capturing and comparing software behaviour without prescribing a programming language, framework, runtime, or deployment architecture. Facet payloads belong in their own specifications.

## 2. Conceptual record groups

1. **Capture identity:** format version, capture ID, purpose, scope, and capture time.
2. **Target identity:** system, boundary, build/revision, environment, and relevant configuration.
3. **Coverage:** facets, subjects, scenarios, conditions, and observable dimensions examined or omitted.
4. **Scenario definition:** reusable preconditions, triggers, actions, inputs, expected outcomes, and observable questions.
5. **Scenario execution:** one actual attempt with actual context, timing, actions, status, and deviations.
6. **Observation:** bounded runtime finding with subject, facet, method, time/order, raw value, optional normalized value, and limitations.
7. **Evidence:** artifacts supporting observations or source-derived inferences.
8. **Runtime rule:** scoped proposition supported, qualified, or contradicted by runtime observations.
9. **Source-derived rule:** separate proposition inferred from source artifacts.
10. **Declared contract:** independently identified statement of intended/permitted behaviour.

Not every partial capture contains every group. Requiredness depends on record class and declared scope. Absence must be represented honestly.

A replication-oriented capture additionally declares a **replication scope** and a **property inventory**. The inventory enumerates the rules and properties required to reproduce that scope, records each item's capture state, and links captured items to runtime observations and evidence. Its completeness assessment is separate from ordinary observation coverage.

## 3. Relationship requirements

The model must express:
- A capture references targets, scenarios, executions, observations, rules, contracts, evidence, and coverage.
- A scenario has zero or more executions.
- An execution occurs against one identified target/build and has zero or more observations.
- An observation belongs to one execution or explicitly scoped runtime interval.
- An observation links to evidence, unless evidence retention is explicitly unavailable and recorded.
- A runtime rule is supported, qualified, or contradicted by runtime observations.
- A source-derived rule links to source artifacts and its inference.
- A declared contract links to its artifact and may be compared with runtime observations/rules.
- Cross-facet records may be correlated where evidence supports the relationship.
- Every comparison result is scoped to identified captures and coverage.

## 4. Common observation envelope

Every facet observation should conceptually provide:

| Group | Meaning |
|---|---|
| Identity | Stable observation ID and record type. |
| Scope | Capture, target, subject/component, and facet. |
| Execution | Scenario execution or declared runtime interval. |
| Conditions | Relevant preconditions and execution context. |
| Trigger | Trigger/action/event relevant to the observation. |
| Method | Runtime observation class and concrete capture method. |
| Time/order | Observation time/interval and sequence/correlation where available. |
| Payload | Typed facet-specific observed fact. |
| Raw evidence | Raw value or evidence artifact reference. |
| Normalization | Optional normalized value and transformation provenance. |
| Status/limits | Missingness, partiality, uncertainty, redaction, and known limitations. |

This is a conceptual checklist, not a frozen list of serialized properties. Facets may add fields. If a field cannot be established or is not applicable, record that distinction.

## 5. Evidence-class separation

Runtime observations, source-derived inferences, and declared contracts must have distinguishable record types and provenance paths. No generic evidence field may erase the distinction between an observed runtime value, a source inference, and a declared contract.

## 6. Comparison boundary

Before records can be compared, establish target/scope alignment, scenario/condition alignment, facet/dimension compatibility, normalization compatibility, and sufficient coverage/evidence. For replication claims, assess both observed agreement and each capture's replication-scope completeness. Otherwise report unknown or not comparable rather than passing by default.

## 7. Versioning

A capture identifies the Software Rules format/schema version. Target build/version is a separate identity. Future schemas may add fields/facets; tools claiming lossless handling must preserve unknown extension data. Compatibility rules will be formalized with machine schemas in Phase 4.
