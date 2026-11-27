# Observation Model

**Maturity:** Draft — Software Rules specification 0.3.0.  
**Purpose:** Define the shared conceptual structure for capturing rules and supporting observations across unlike facets.  
**Important:** The current draft JSON Schema mapping is version 0.2.0 under `schemas/v1/`. This document defines conceptual meaning; the schema defines current serialized field names, types, cardinalities, and structural requiredness. Neither establishes that a particular capture's property inventory is exhaustive.

## 1. Model overview

Software Rules separates the reusable scenario, one actual execution, the facts recorded, the evidence retained, and the rule inferred from those facts.

~~~text
Capture
├── Target identity and system boundary
├── Scope, environment, configuration, and coverage
├── Scenario definitions
│   └── Scenario executions
│       ├── Actual context, inputs, triggers, and actions
│       ├── Execution status and timing
│       └── Observations
│           ├── Raw values
│           ├── Optional normalized values
│           └── Evidence references
├── Runtime rules
│   ├── Applicability conditions and proposition
│   └── Supporting / qualifying / contradicting observations
├── Source-derived rules
│   └── Source artifacts and inference provenance
└── Declared contracts
    └── Artifact identity, version, and scope
~~~

This is a logical relationship model; it does not require one physical file per entity.

## 2. Core entities

### Capture
Top-level bounded collection. Identifies capture ID, format version, purpose, scope, target, boundary, build/revision, environment/configuration, capture times, collector, included facets, planned coverage, linked records, and known limitations. A capture may be partial.

### Target and system boundary
Target identity describes the specific instance/build examined, not merely the product name. Boundary states what is inside the target and what remains an external actor or dependency.

### Scenario
Reusable examination description: ID/purpose, facet and subject, preconditions/initial state, actor/initiator, trigger and ordered actions, inputs, expected outcomes and their source, observable questions/dimensions, and stopping criteria. A scenario is not evidence that it ran.

### Scenario execution
One actual attempt, with its own identity. Records scenario reference, target/build/environment actually used, actual initial conditions, actor/trigger/inputs/actions, start/end times, sequence/correlation, execution status, observations/evidence, and deviations from the scenario definition. A scenario can have many executions; repetitions may reveal nondeterminism or state dependence.

### Observation
One bounded finding tied to an execution or explicitly identified runtime interval. Records observation ID, execution reference, subject/component/facet, method class and concrete method, time/sequence, facet-specific kind/payload, raw value or evidence reference, optional normalized value/transformation, relevant conditions, and limitations/status. Keep observations as atomic as practical; facets define atomicity for structures such as a DOM tree or trace.

### Rule
Reusable proposition supported by observations or separately inferred from source artifacts. Records rule ID/class, facet/subject scope, proposition, applicability conditions/trigger, claimed response/constraint/transition, status/history, supporting/qualifying/contradicting references, and coverage limitations. One rule may have many observations; one observation may support multiple rules.

### Evidence artifact
Retained material supporting an observation or source inference. It may be embedded or externally referenced and carries type, origin, capture time, integrity, redaction, and access/retention metadata as appropriate.

### Declared contract
Independent artifact describing intended/permitted behaviour. It can be linked to scenarios, rules, and observations. A runtime mismatch must remain visible without altering either record.

## 3. Expected outcome, actual outcome, and evaluation

Keep three things separate:
1. **Expected outcome:** predeclared prediction, requirement, or oracle with its origin.
2. **Actual outcome:** what observations establish.
3. **Evaluation:** comparison between expected and actual, including method and limitations.

Evaluation may be pass, fail, inconclusive, or not evaluated. It must not overwrite the underlying observation.

## 4. Observation method classes

| Class | What it observes | Example | Main limitation |
|---|---|---|---|
| External black-box | Behaviour exposed at system boundary | User action and visible result; request/response; output file | Hidden state/side effects may remain unknown |
| Platform/runtime inspection | Actual state/structure exposed by executing platform | DOM/computed style; accessibility tree; runtime database state | Limited to exposed fields and access |
| Runtime instrumentation | Events/operations collected from executing target | Trace/span; structured event; metric | Sampling, instrumentation gaps, observer effects |

All three are runtime methods when evidence is tied to actual execution. Source code/static configuration/contracts are source or declaration evidence, not runtime methods.

## 5. Conditions and execution context

Record conditions needed to reproduce, interpret, or compare an observation. Depending on the facet, these may include target build, feature flags, platform/browser/device/runtime version, configuration, locale/timezone, actor role/permissions, initial state/data, dependency state, network conditions, inputs, and timing constraints.

Do not record every conceivable detail indiscriminately. If a potentially relevant condition is unknown, mark it unknown rather than assuming a default.

## 6. State, outputs, and side effects

Facet observations may describe:
- Value or structure exposed by the target.
- State snapshot at a point in time.
- State transition/delta between identified points.
- Returned/emitted output.
- Published event/message.
- Durable or externally visible side effect.
- Error/failure/recovery action.
- Measurement with unit and measurement method.

The common model names these categories; the facet payload defines their exact structure and semantics.

## 7. Coverage model

Coverage is declared against scope, not represented only as an unexplained percentage. It should describe facets/subjects in scope; scenarios planned, attempted, completed, skipped; conditions/inputs exercised; observable dimensions captured; and sampling, filtering, redaction, instrumentation gaps, and exclusions.

Coverage states:
- **Planned:** intended for examination.
- **Attempted:** execution or inspection initiated.
- **Observed:** evidence recorded for the dimension.
- **Partial:** some evidence exists but the dimension is incompletely captured.
- **Unavailable:** could not be obtained.
- **Not observed:** no observation recorded; reason may be unknown.
- **Not applicable:** dimension does not apply to stated scope.

A completed scenario does not imply full facet coverage. A DOM snapshot may cover the captured tree while omitting later states, routes, network effects, or other viewport conditions.

## 8. Missingness and conflict

Distinguish an observed empty/absent value from not observed, unknown, unavailable, not applicable, redacted/withheld, and conflicting evidence. Do not collapse these into null, false, zero, or an empty collection unless the facet explicitly defines that meaning.

## 9. Cross-facet model tests

These are illustrative conceptual tests, not captures from a real product and not final schemas.

### Interface: resolved runtime layout

**Scenario:** Open a page at a specified viewport and inspect a named region after a defined ready condition.

**Execution context:** Target build, browser/version, operating system, viewport dimensions, device scale factor, locale, and relevant user state.

**Trigger:** Navigate to the page and wait for the defined ready condition.

**Observations:** Platform/runtime inspection records the rendered element hierarchy; capture-local node identity and parent relationships; resolved/computed style values; geometry; visibility; stacking order/context; accessibility semantics; and asset references where available. A screenshot may be retained as evidence but does not replace structured hierarchy and resolved values.

**Rule proposition:** Under the specified target and viewport conditions, the named region renders with the captured hierarchy and resolved layout properties.

**Evidence:** DOM/runtime snapshot, computed-style data, geometry, accessibility snapshot, screenshot, and capture metadata.

**Coverage limits:** One execution covers only the captured route, state, viewport, and time. It does not establish all breakpoints, interactive states, browser engines, or asynchronous states.

### API: request/response behaviour

**Scenario:** Send a request with specified method, path, headers, identity context, and body to a named endpoint.

**Execution context:** Target build, endpoint/environment, authentication context, relevant configuration, and dependency state.

**Trigger:** Submit the request.

**Observations:** External observation records the request actually sent and response status, headers, and body. Runtime instrumentation may separately record server operation spans and dependency calls. An authorized runtime inspection may observe relevant durable state before/after. Timing measurements include units and measurement boundaries.

**Rule proposition:** Under the stated request and execution conditions, the endpoint returns the captured response and any observed side effects.

**Evidence:** Raw request/response, trace/span references, timing record, and state diff where applicable.

**Coverage limits:** One request does not establish all input classes, authorization contexts, concurrency cases, retries, or dependency failures. A response alone does not prove a durable write occurred.

### Shared and facet-specific concepts

| Concept | Interface | API |
|---|---|---|
| Target | Application build | Service build/deployment |
| Scenario | Load page at viewport | Send request to endpoint |
| Execution | One page-load attempt | One request attempt |
| Trigger | Navigation | HTTP request |
| Conditions | Browser, viewport, route, user state | Headers, identity, config, dependency state |
| Observation | DOM/layout/accessibility fact | Status/header/body/timing fact |
| Method | Platform/runtime inspection | External observation and/or instrumentation |
| Evidence | DOM snapshot, screenshot, geometry | Request/response, trace, state diff |
| Rule | Conditional rendering/layout proposition | Conditional request/response proposition |
| Coverage limit | States/routes/viewports not exercised | Inputs/auth contexts/failures not exercised |

The shared model works because both examples identify target, scenario, execution, conditions, trigger, observation, method, evidence, rule, and coverage. Their payloads remain facet-specific. This supports a shared conceptual envelope without forcing a universal observation payload.

## 10. Remaining design limits

The current draft has serialized common records and 15 typed facet payloads, plus versioned normalization, matching, comparison, and conformance rules. The following remain explicit pre-stable work rather than uncompleted Phase 2–5 tasks:

- Add a distinct `specificationVersion` field to capture manifests; the current captures identify schema version 0.2.0 and rely on release provenance for the overall specification version.
- Expand platform-specific adapters and facet payloads as new source-backed property classes are encountered.
- Continue testing identifier alignment, semantic evaluators, and tolerance profiles against new independent implementations.
- Keep completeness inventory exhaustiveness as an expert scope-review responsibility; structural validators cannot prove that no relevant property was omitted.
- Define stable 1.0.0 compatibility, migration, and formal conformance levels only after the readiness criteria in `specification/VERSIONING.md` are met.
