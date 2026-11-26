# Project Plan

**Project:** Software Rules  
**Repository:** REMAREMA6/software-rules  
**Status:** Phase 6 — expanded multi-facet runtime capture and conformance in progress  
**Plan version:** 0.3.0  
**Last updated:** 2026-11-26

## 1. Mission

Define a technology-independent, machine-readable format for capturing the complete rules needed to reproduce a declared software scope in an independent implementation across technologies and stacks. Capture and comparison are the evidence and conformance process for that replication purpose.

The intended workflow is:

1. Identify the software system and the scenarios to examine.
2. Trigger controlled scenarios against the running reference system.
3. Capture observable results and supporting evidence in the Software Rules format.
4. Build an independent implementation in any suitable technology.
5. Run equivalent scenarios against that implementation.
6. Capture its results using the same format.
7. Normalize and compare the captures.
8. Report matches, differences, unknowns, and coverage limits.

The specification describes observable software behaviour and state. It is not a source-code translation format and does not prescribe the implementation stack.

## 2. Foundational distinctions

### 2.1 Runtime rules

A runtime rule is supported by evidence collected while the target software is executing. It must record the scenario or trigger, relevant preconditions and environment, observations, outcomes, and evidence references.

Source code may guide an investigator toward scenarios or explain what to inspect. Merely finding a declaration in source code does not make it a runtime observation.

### 2.2 Source-derived rules

A source-derived rule is a cautious inference from source code used when the relevant fact cannot be established through runtime observation. It must be stored separately, carry source provenance, and remain explicitly unverified as runtime behaviour.

### 2.3 Unknown is not false

The format must distinguish at least: observed, not observed, unknown, inferred from source, not applicable, and contradicted. Missing evidence must never silently become a negative result or a pass.

### 2.4 Comparison is bounded

A matching pair of captures demonstrates agreement only for the scenarios, inputs, environments, and observable dimensions covered by those captures. It does not prove universal equivalence.

### 2.5 Common envelope, facet-specific payloads

All rule records should share a common identity, provenance, condition, and evidence envelope. Each software facet must have its own typed payload. Do not force unrelated facets into one generic schema.

## 3. Work phases and completion gates

### Phase 0 — Repository and project governance

- [x] Create repository and initial README.
- [x] Establish this plan and persistent tracker.
- [x] Establish contribution, decision, and change-recording conventions.
- [x] Define specification maturity labels and versioning policy.
- [x] Link governance documents from the README.
- [x] Establish changelog and design-decision recording conventions.
- [x] Define initial specification maturity labels and versioning policy.

**Exit gate:** A new contributor or new chat can understand the mission, current state, next task, and where decisions are recorded. The repository has a maintained roadmap, tracker, contribution guide, changelog, decision log, and explicit maturity/versioning policy.

### Phase 1 — Research existing standards and prior art

Investigate relevant standards and formats before fixing the Software Rules model. Record each source's publication status, what it solves, what it does not solve, and whether Software Rules should reuse, map to, or deliberately differ from it.

Research areas include:

- Requirements engineering and specification quality (for example, ISO/IEC/IEEE 29148).
- Platform-independent modelling (for example, OMG MDA).
- Structural and behavioural modelling (for example, UML).
- Business vocabulary and rules (for example, OMG SBVR).
- API contracts (for example, OpenAPI).
- Event-driven and message API contracts (for example, AsyncAPI).
- Runtime telemetry and semantic conventions (for example, OpenTelemetry).
- Web interface runtime inspection and resolved style values (for example, DOM/CSSOM and WebDriver).
- Native interface inspection (for example, Android UI Automator and accessibility semantics).
- Scenario-based behavioural specification (for example, Gherkin/BDD).
- Machine-readable validation (for example, JSON Schema).
- Visual design token interchange (for example, the W3C Design Tokens Community Group format).

Deliverables:
- `research/STANDARDS-REVIEW.md`
- `research/REFERENCES.md`
- `research/DESIGN-DECISIONS.md`

- [x] Complete comparative review of all listed candidate standards.
- [x] Record publication status, scope, limitations, and project treatment for each.
- [x] Collect authoritative primary references.
- [x] Distinguish declared contracts from actual runtime observations.
- [x] Revise the working facet taxonomy and record unresolved boundaries.

**Exit gate: satisfied.** The candidate standards have been evaluated, their limits and design implications documented, authoritative references collected, and the facet taxonomy revised as a proposal. No capture schema has been frozen.

### Phase 2 — Core concepts and common model

Define the language and shared structure before designing facet payloads.

Tasks:
- Define system, boundary, component, facet, rule, observation, scenario, trigger, condition, outcome, evidence, provenance, and comparison.
- Define the distinction between declared contracts, runtime observations, and source-derived inferences.
- Decide whether scenario executions and individual observations are separate entities.
- Define capture method classes, including external observation, platform inspection, and runtime instrumentation.
- Define capture coverage and the meaning of incomplete or unavailable dimensions.
- Define runtime versus source-derived rule classes.
- Define rule identity and relationships.
- Define preconditions, inputs, environment, execution context, and time/order.
- Define observed state, emitted outputs, side effects, and evidence references.
- Define confidence and verification states without conflating them.
- Define unknown, unavailable, not applicable, and not observed.
- Define how multiple observations support, qualify, or contradict a rule.
- Define conceptual identity, time/order/correlation, and value/unit provenance; defer identifier syntax and canonicalization mechanics to Phases 4–5.
- Define the relationship between capture format version and target build/version; defer schema compatibility mechanics to Phase 4.

Deliverables:
- `specification/TERMINOLOGY.md`
- `specification/PRINCIPLES.md`
- `specification/RULE-CLASSIFICATION.md`
- `specification/EVIDENCE-AND-PROVENANCE.md`
- `specification/OBSERVATION-MODEL.md`
- `specification/CORE.md`
- `specification/SOURCE-DERIVED-RULES.md`
- `specification/VERSIONING.md`

**Exit gate: satisfied (conceptual model).** The vocabulary and linked entity model distinguish scenario definitions, executions, observations, evidence, runtime rules, source-derived rules, and declared contracts. The common model has been exercised against two unlike conceptual cases (resolved interface layout and API request/response behaviour) without flattening their facet-specific payloads. This validates the conceptual envelope, not a final serialization, empirical capture, or complete facet taxonomy. Machine schemas and facet payloads remain deferred.

### Phase 3 — Facet specifications

Design each facet as its own specification with explicit scope, observable dimensions, scenario requirements, payload fields, evidence requirements, limitations, and examples.

Proposed facets, revised after Phase 1 research:

1. Interface — web/native hierarchy, visual properties, geometry, stacking, accessibility, assets, and UI states.
2. Behaviour — triggers, preconditions, transitions, observable outputs, and side effects.
3. Business rules — domain constraints, decisions, calculations, policies, and rule outcomes.
4. Data — runtime data shapes, fields, types, relationships, transformations, and validation outcomes.
5. Persistence — durable state, reads/writes, transactions, consistency, and lifecycle observations.
6. API — synchronous request/response interfaces and actual runtime exchanges.
7. Messaging — channels, messages, publishing, receiving, delivery, and processing outcomes.
8. Identity and authentication — identity context, authentication events, and outcomes.
9. Authorization and permissions — roles, capabilities, policy decisions, and access outcomes.
10. Security controls — security-relevant runtime outcomes and authorized test observations.
11. Background processing — jobs, schedules, retries, lifecycle, and outcomes.
12. Errors and recovery — validation failures, exposed exceptions, retries, recovery, and failure outcomes.
13. Integrations — interactions and contracts with external systems.
14. Configuration — runtime configuration values and changes that affect behaviour.
15. Performance and resource behaviour — duration, throughput, latency, resource use, and performance outcomes.

The Phase 3 review accepts the 15 facets as the working normative catalogue for this draft. Facets are observation perspectives, may overlap in one execution, and are not required to exist in every system. Their boundaries and cross-facet relationships are documented in `facets/FACET-BOUNDARIES.md`. Each facet specification defines scope, observation unit, conceptual payload dimensions, scenario requirements, evidence, limitations, cross-facet links, and a worked conceptual example.

Deliverables:
- `facets/README.md` catalogue.
- `facets/FACET-BOUNDARIES.md` taxonomy and overlap rules.
- `facets/<facet>/README.md` for each of the 15 facets.
- Worked conceptual examples in each facet specification.

**Exit gate: satisfied at the facet-specification level.** All 15 facets have defined boundaries, conceptual typed payload inventories, evidence requirements, limitations, cross-facet relationships, and reviewed illustrative examples. These are not empirical captures. Exact machine schemas remain Phase 4; empirical end-to-end captures and conformance fixtures remain Phase 6.

### Phase 4 — Machine-readable schemas

Formalize the serialized capture model without beginning normalization or comparison semantics.

Tasks:
- Define JSON Schema Draft 2020-12 conventions, schema identifiers, draft version, and extension policy.
- Define the capture manifest and common target, coverage, scenario, execution, observation, evidence, contract, runtime-rule, and source-rule records.
- Require runtime method/procedure and evidence references for runtime observations.
- Keep source-derived rules and declared contracts structurally separate.
- Define one typed payload schema for each of the 15 facets.
- Define a structural comparison-report envelope only; defer match classifications and equivalence semantics to Phase 5.
- Add positive and negative fixtures.
- Provide a repeatable automated validation command.
- Document validation limits, schema evolution, and compatibility.

Deliverables:
- `specification/SCHEMA-DESIGN.md`
- `schemas/v1/*.schema.json` (draft schema version 0.1.0; not a stable 1.0.0 release)
- `schemas/v1/fixtures/valid/` and `schemas/v1/fixtures/invalid/`
- `conformance/validation/`

**Exit gate:** All schemas parse and resolve their references; the valid fixture passes; every negative fixture fails for the intended structural reason; validation instructions are reproducible. Cross-record referential integrity and evidence truth are explicitly outside JSON Schema validation.

### Phase 5 — Canonicalization and comparison

Specify how independently produced captures are aligned and compared without erasing meaningful differences or exceeding evidence.

Tasks:
- [x] Define capture, scenario, execution, subject, observation, and rule alignment.
- [x] Define identity evidence, ambiguity, and one-to-many/many-to-one alignment constraints.
- [x] Define normalization profiles and preserve raw observations/evidence.
- [x] Define rules for identifiers, timestamps, units, numbers, ordering, text, structured values, geometry, and performance measurements.
- [x] Define exact, normalized, semantic, and tolerance-based comparison bases.
- [x] Define match, mismatch, missing, additional, unknown, conflicting, and not-comparable classifications.
- [x] Define decision ordering so missing evidence cannot become a match.
- [x] Define coverage counts and bounded conclusions.
- [x] Expand the comparison-report JSON Schema.
- [x] Add a valid comparison example and an invalid universal-equivalence fixture.
- [x] Validate capture and comparison fixtures in CI.

Deliverables:
- `comparison/COMPARISON-MODEL.md`
- `comparison/NORMALIZATION.md`
- `comparison/MATCHING-RULES.md`
- `comparison/DIFFERENCE-CLASSIFICATION.md`
- `comparison/COVERAGE-AND-LIMITATIONS.md`
- `comparison/examples/`
- Updated `schemas/v1/comparison-report.schema.json`

**Exit gate: satisfied (2026-11-26).** The illustrative report demonstrates alignment, a matched dimension, an excluded/not-comparable dimension, separate per-capture coverage, and an inconclusive scope-bounded conclusion. GitHub Actions run [#4](https://github.com/REMAREMA6/software-rules/actions/runs/45793398830) passed the capture fixtures and comparison-report fixtures, including rejection of a universal-equivalence claim. The example is a model demonstration, not an empirical system capture.

### Phase 6 — End-to-end multi-facet capture and conformance

Phase 6 is the empirical implementation of the complete-capture objective across the 15-facet catalogue. It is **not complete** when one facet or one small example is complete. The existing Task Board is an initial conformance fixture, not the project's universal target and not evidence for facets it does not implement.

#### Work sequence

**6A — Audit the existing interface baseline**
- [x] Build the initial browser runtime capture and pixel-comparison harness.
- [x] Audit the retained capture records and evidence references; distinguish actual property-level observations from generic artifact references.
- [x] Downgrade unsupported font-rendering coverage and add partial business-rule/data observations rather than asserting complete capture.
- [ ] Expand interface scenarios to all relevant states, responsive conditions, focus/hover/disabled/loading/error states, and supported environment variations for the declared fixture.
- [ ] Keep any untested or unsupported interface dimension unresolved rather than marking it complete.

**6B — Behaviour and functionality**
- [x] Add an initial discriminating Playwright probe set for title normalization, duplicate titles, HTML-like/Unicode content, long titles, mixed task states, filter truth tables, completion toggling, deletion, and identifier samples.
- [x] Execute the expanded probe set through the dedicated Phase 6 GitHub Actions workflow and inspect the retained outputs before promoting supported properties.
- [ ] Build an explicit operation/trigger inventory from the running target.
- [ ] Capture preconditions, actors, ordered actions, state before/after, outputs, side effects, timing/order, and termination outcomes.
- [x] Exercise the initial title, duplicate, mixed-state, toggle, and multiple-delete boundary cases in the Task Board fixture.
- [ ] Extend probes to malformed, interrupted, repeated, and failure paths.
- [ ] Compare independently captured behaviour and ensure every rule is evidence-linked.

**6C — Business rules**
- [x] Identify initial task-title normalization, duplicate acceptance, initial completion defaults, and summary-count decisions.
- [x] Probe initial rules with duplicate titles and a three-task mixed completion/filter truth table.
- [ ] Extend the inventory to all domain decisions, conditions, constraints, calculations, defaults, and branch outcomes.
- [ ] Design further scenario sets for maximum title length, additional constraints, precedence, and exception cases.
- [ ] Capture boundary values, combinations, precedence, and contradictory/exception cases.
- [ ] Keep domain rules separate from UI validation, generic behaviour, and authorization.

**6D — Data**
- [~] Capture the initial task record fields/types, identifier sequence within the adapter session, JSON serialization, and PATCH field-preservation behaviour.
- [ ] Extend capture to nullability, missing-vs-empty distinctions, relationships, malformed values, unknown fields, and broader constraints.
- [ ] Extend probes to null/missing fields, malformed values, unknown identifiers, and full constraint boundaries.
- [ ] Record observed values separately from inferred schemas and source declarations.
- [ ] Link data observations to the operations and API exchanges that produced them.

**6E — Persistence**
- [ ] Observe durable reads/writes, transaction boundaries, commit/rollback, visibility, consistency, ordering, retention, and deletion.
- [ ] Test across reloads, sessions, concurrent operations, and failure boundaries where supported.
- [ ] Do not treat an in-memory test adapter as persistence evidence.

**6F — API, messaging, and integrations**
- [ ] Capture real request/response exchanges, protocol details, payloads, status, headers, timing, retries, and transport failures.
- [ ] Capture asynchronous publication, delivery, acknowledgement, ordering, duplication, and processing where present.
- [ ] Identify external dependencies and capture their actual interactions and failure outcomes.
- [ ] Distinguish a test adapter or mock from a real service boundary.

**6G — Identity, authorization, and security**
- [ ] Capture identity establishment, credentials/session lifecycle, expiry, logout, and failure outcomes.
- [ ] Exercise role/resource/action combinations and record authorization decisions and enforcement points.
- [ ] Define authorized security scenarios and capture detection, prevention, limitation, and containment outcomes.
- [ ] Never infer security properties from the absence of an observed failure.

**6H — Background processing, errors/recovery, configuration, and performance**
- [ ] Capture queued/scheduled/worker lifecycles, retries, cancellation, and terminal outcomes.
- [ ] Capture failures, fallbacks, compensation, recovery, and user/system-visible consequences.
- [ ] Record effective runtime configuration and controlled configuration changes.
- [ ] Measure performance/resource behaviour under reproducible workloads and declared measurement conditions.

**6I — Cross-facet completeness and replication validation**
- [ ] Reconcile the facet inventory against the actual system boundary and all relevant workflows/states.
- [ ] Verify every required property has adequate evidence, not merely a schema-valid record or generic observation reference.
- [ ] Validate cross-facet links, provenance, uncertainty, exclusions, and conflicting observations.
- [ ] Compare reference and independent implementations facet by facet.
- [ ] Report observed agreement separately from replication-scope completeness.
- [ ] Reject a complete/faithful-replication claim while any required property remains unresolved.

#### Current fixture boundary

The Task Board fixture currently supports empirical work on interface, behaviour, a limited set of domain rules, data, and a deterministic in-memory API adapter. Its adapter does not establish production API, persistence, identity, authorization, security, messaging, integrations, background processing, or performance properties. These facets remain unverified for this fixture; they are not globally declared irrelevant to the Software Rules format.

Where a facet is genuinely absent from a selected target, record the evidence and rationale for not-applicable status. Where a target does not expose enough evidence, record unknown/unavailable/partial. Do not manufacture coverage by adding generic inventory rows.

#### Phase 6 exit gate

Phase 6 exits only when the selected target's complete replication scope is explicit; every applicable facet has a reviewed property inventory; each required property is supported by adequate, traceable evidence; unresolved properties prevent a complete claim; independent captures and comparisons exercise the relevant dimensions; and conformance checks enforce these conditions. Passing CI is necessary for the implemented checks, not proof that the inventory itself is exhaustive.

### Phase 7 — Review, release, and maintenance

Phase 7 is blocked until the expanded Phase 6 exit gate is satisfied.

- [ ] Review the full specification for contradictions and omissions.
- [ ] Enforce the Replication Completeness Rule across every applicable facet.
- [ ] Verify schema, examples, conformance checks, and evidence provenance.
- [ ] Review comparison claims and limitations.
- [ ] Document unresolved questions and known limitations.
- [ ] Publish a versioned specification release and maintenance process.

**Exit gate:** The expanded Phase 6 conformance programme is complete, the release checklist is satisfied, known limitations are documented, and the specification version is clearly identified.

## 4. Target repository layout

~~~text
software-rules/
├── README.md
├── PLAN.md
├── TRACKER.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── specification/
│   ├── CORE.md
│   ├── TERMINOLOGY.md
│   ├── PRINCIPLES.md
│   ├── RULE-CLASSIFICATION.md
│   ├── EVIDENCE-AND-PROVENANCE.md
│   ├── OBSERVATION-MODEL.md
│   ├── SOURCE-DERIVED-RULES.md
│   └── VERSIONING.md
├── facets/
│   ├── interface/
│   ├── behavior/
│   ├── business-rules/
│   ├── data/
│   ├── persistence/
│   ├── api/
│   ├── messaging/
│   ├── identity-authentication/
│   ├── authorization-permissions/
│   ├── security-controls/
│   ├── background-processing/
│   ├── errors-recovery/
│   ├── integrations/
│   ├── configuration/
│   └── performance-resource-behaviour/
├── schemas/
│   └── v1/
├── comparison/
├── examples/
│   ├── PHASE-6-FACET-EXPANSION.md
│   ├── interface/
│   ├── behavior/
│   ├── api/
│   └── full-system/
├── conformance/
│   ├── fixtures/
│   ├── validation/
│   └── test-cases/
├── research/
│   ├── STANDARDS-REVIEW.md
│   ├── DESIGN-DECISIONS.md
│   └── REFERENCES.md
~~~

This is the target layout, not a statement that every planned file has already been created. Directories will appear in Git when their first tracked file is added.

## 5. Working rules for this project

1. Research before standardizing. Do not invent a term or structure where a relevant established standard already provides a suitable one.
2. Do not adopt an existing standard blindly. Explain its scope and limitations and why it fits.
3. Keep runtime observations and source-derived inferences separate in both data and documentation.
4. Describe observed outcomes, not presumed implementation intent.
5. Keep the core model small and shared; keep facet-specific details in facet specifications.
6. Every normative field must have a defined meaning, type, constraints, and evidence expectations.
7. Every important rule must have examples and validation tests.
8. Never silently treat missing observations as false, absent, or passing.
9. Never claim universal equivalence from finite test captures.
10. Update `TRACKER.md` whenever work starts, changes status, is blocked, or is completed.
11. Update `CHANGELOG.md` when a meaningful specification or structure change is made.
12. Record consequential design choices in `research/DESIGN-DECISIONS.md` using permanent decision IDs and explicit statuses.
13. Keep this plan as the roadmap. If the roadmap changes, update it rather than relying on chat history.
14. Apply the maturity labels and versioning policy in `specification/VERSIONING.md` to substantial specification and schema documents.
15. Follow `CONTRIBUTING.md` for the repository change and review workflow.

## 6. How to resume in a new chat

At the beginning of a new chat, provide this repository URL:

`https://github.com/REMAREMA6/software-rules`

The assistant should read, in order:
1. `README.md` — project purpose and core distinctions.
2. `PLAN.md` — full roadmap, structure, and working rules.
3. `TRACKER.md` — exact current progress, active task, blockers, and next action.
4. Any files listed under the active task in the tracker.

The tracker is the operational source of truth for progress. The plan is the source of truth for intended scope and sequence. If chat history conflicts with these repository documents, inspect the repository and resolve the discrepancy explicitly.

## 7. Immediate next work

Continue Phase 6 by probing the remaining title-length boundary and API/data edge cases (malformed payloads, unknown identifiers, null/missing fields, repeated operations, and update/delete failures). Continue the interface state/viewport audit. Then select or extend a richer controlled target for persistence, identity, authorization, security, integrations, and background processing. Keep Phase 7 blocked until the expanded Phase 6 exit gate is satisfied.
