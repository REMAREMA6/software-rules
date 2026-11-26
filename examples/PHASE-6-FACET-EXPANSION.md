# Phase 6 — Multi-facet capture programme

**Status:** Active  
**Parent:** Project plan (../PLAN.md) and project tracker (../TRACKER.md)  
**Purpose:** Turn the 15-facet catalogue into an evidence-backed runtime capture and independent comparison process.

## Operating rule

A facet name in a capture is not evidence that the facet's rules were discovered. Every required property needs a concrete observation, an evidence reference that directly supports it, and a validation method. Generic observations, source declarations, schema validity, and passing CI cannot substitute for property-level evidence.

Keep these states distinct:
- **Captured:** directly observed or inspected using an identified method, with adequate evidence.
- **Partial:** some dimensions or conditions are evidenced, but the property is not fully established.
- **Unknown / not observed / unavailable:** no adequate evidence; do not infer absence.
- **Source-derived:** inferred from source and explicitly not runtime-verified.
- **Not applicable:** demonstrated to be outside the target's actual behaviour/boundary, with a reason and supporting evidence.
- **Excluded:** deliberately outside the declared replication scope, with justification and impact.

## Ordered work

| Stage | Facet(s) | Required investigation | Status |
|---|---|---|---|
| 6A | Interface | Audit retained artifacts property by property; extend states, responsive conditions, and interaction conditions | In progress |
| 6B | Behaviour and functionality | Triggers, preconditions, actions, transitions, outputs, side effects, ordering, boundary/failure paths | Not started |
| 6C | Business rules | Domain conditions, constraints, decisions, calculations, defaults, precedence, boundary combinations | Not started |
| 6D | Data | Runtime structures, types, nullability, relationships, constraints, transformations, defaults, serialization | Not started |
| 6E | Persistence | Durable reads/writes, transaction outcomes, consistency, visibility, retention, deletion | Not started |
| 6F | API, messaging, integrations | Actual protocol exchanges, delivery/acknowledgement, external dependency behaviour and failures | Not started |
| 6G | Identity, authorization, security | Principal/session lifecycle, permission matrices, enforcement, authorized security outcomes | Not started |
| 6H | Background processing, errors/recovery, configuration, performance | Job lifecycle, failure/recovery, effective settings, reproducible workload measurements | Not started |
| 6I | Cross-facet completeness | Inventory reconciliation, evidence graph, independent capture, comparison, completeness decision | Not started |

## Current Task Board fixture: evidence boundary

The Task Board can support initial investigation of:
- Interface: browser-rendered hierarchy, styles, geometry, semantics, and tested UI states.
- Behaviour: task creation, completion, filtering, deletion, keyboard interaction, and observed failure behaviour.
- Business rules: candidate rules such as trimming/rejecting blank titles, initial completion state, filter selection, and summary counts. Each must be tested across discriminating inputs before it can be treated as established.
- Data: candidate runtime task shape (id, title, completed), field values/types, defaults, and serialization. These need property-specific runtime evidence.
- API: only the deterministic in-memory Playwright route adapter is currently evidenced.

The fixture does not currently establish durable persistence, production server behaviour, messaging, identity, authorization, security, external integrations, background workers, or production performance. Those are **unverified for this fixture**. Do not mark them not applicable merely because the toy application lacks them; choose a suitable target or explicitly record the fixture's boundary.

## Immediate probe backlog: behaviour, business rules, and data

The following are hypotheses/questions, not established rules until executed and evidenced:

### Behaviour and functionality
- Does submission preserve the same outcome for keyboard and pointer activation?
- What happens for empty, whitespace-only, leading/trailing whitespace, duplicate, very long, and Unicode titles?
- Can completion be toggled both ways? What is the exact transition and resulting visible state?
- Does each filter produce the correct subset for zero, one, and multiple tasks with mixed completion states?
- What happens when deletion is repeated, targets an unknown identifier, or races with an update?
- What is the observable outcome when create/update/delete requests fail?

### Business rules
- Is title normalization exactly trim, and is it applied before the request or by the service?
- Is a blank title rejected by browser constraint validation, application logic, service logic, or more than one layer?
- Are duplicate titles permitted?
- Is a new task always incomplete?
- Are total and active counts derived from all records or only visible records?
- Are there any title length, character, or uniqueness constraints? Do not assume constraints that have not been probed.

### Data
- What exact fields are present in create, update, and delete request/response bodies?
- What are the observed types and null/missing behaviour of each field?
- How are identifiers generated, represented, and scoped to a session?
- Does a PATCH preserve unspecified fields or replace the record?
- What happens for malformed payloads, unknown fields, invalid field types, and unknown identifiers?
- Are HTML-like and Unicode titles preserved as data and safely rendered as text?

## Evidence record template

For every property, record:
1. Stable property/rule ID and facet.
2. Exact proposition being tested (one claim per property where possible).
3. Scope, actor, initial state, environment, trigger, inputs, and controlled variables.
4. Probe matrix, including boundary and negative cases.
5. Observation method and tool/version.
6. Raw evidence path/hash and exact evidence location.
7. Result: captured, partial, unknown, unavailable, conflicting, source-derived, not applicable, or excluded.
8. Confidence/limitations and any competing hypothesis not yet ruled out.
9. Cross-facet links (execution, data, API, UI, persistence, etc.).
10. Independent implementation probe and comparison method.

## Completion rule

A stage is not complete because its checklist is populated or a CI job passes. The investigator must review whether the inventory itself is exhaustive for the declared target and whether each claimed property has adequate, direct evidence. A stage can finish with explicit unresolved properties only if the overall replication scope remains marked incomplete. Phase 6 completes only after the 6I cross-facet gate passes.
