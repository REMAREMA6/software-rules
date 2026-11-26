# Project Tracker

**Project:** Software Rules  
**Repository:** REMAREMA6/software-rules  
**Last updated:** 2026-11-26  
**Current phase:** Phase 3 — Facet specifications  
**Overall status:** In progress

> This file is the persistent progress and handoff record. Update it whenever task status changes. Keep the current task, blockers, and next action explicit so work can resume in a new chat.

## Status key

- [ ] Not started
- [~] In progress
- [x] Completed
- [!] Blocked
- [?] Needs a decision or verification

## Current position

- **Current phase:** Phase 3 — Facet specifications
- **Current task:** Validate the proposed facet taxonomy and define facet-specific capture requirements.
- **Blockers:** The 15-facet taxonomy remains provisional; boundaries and overlaps need validation against concrete examples.
- **Next action:** Define the interface facet boundary and its runtime observation payload, using the resolved DOM/layout capture workflow as the first concrete case.
- **Do not do yet:** Freeze machine schemas or claim the facet taxonomy is final. First review facet boundaries, required observations, and evidence needs.

## Phase tracking

| Phase | Name | Status | Notes |
|---|---|---|---|
| 0 | Repository and project governance | [x] Complete | Roadmap, tracker, contribution guide, changelog, decision log, maturity/versioning policy, and navigation links established. |
| 1 | Research existing standards and prior art | [x] Complete | Comparative review, authoritative references, limitations, design implications, and revised facet proposal recorded. |
| 2 | Core concepts and common model | [x] Complete | Core vocabulary, rule/evidence classes, linked observation model, source-derived model, and interface/API conceptual tests completed. Schemas remain deferred. |
| 3 | Facet specifications | [~] In progress | Validate facet boundaries and define typed payloads against concrete capture cases. |
| 4 | Machine-readable schemas | [ ] Not started | Schemas follow the agreed conceptual model. |
| 5 | Canonicalization and comparison | [ ] Not started | Define comparison semantics and limits. |
| 6 | End-to-end examples and conformance | [ ] Not started | Validate the format in realistic examples. |
| 7 | Review, release, and maintenance | [ ] Not started | Final consistency review and release. |

## Phase 0 — Repository and project governance

- [x] Create public GitHub repository.
- [x] Create initial `README.md`.
- [x] Confirm GitHub repository connection can create files.
- [x] Propose and document target repository layout.
- [x] Create project roadmap in `PLAN.md`.
- [x] Create persistent progress tracker.
- [x] Create contribution workflow in `CONTRIBUTING.md`.
- [x] Link plan and tracker and governance documents from the README.
- [x] Establish changelog and design-decision recording conventions.
- [x] Define specification maturity labels and versioning policy.

**Phase 0 exit gate: satisfied.** A new chat or contributor can find the project purpose, roadmap, progress, contribution process, decisions, change history, and versioning policy in the repository.

## Phase 1 — Research existing standards and prior art

- [x] Review requirements/specification standards (ISO/IEC/IEEE 29148).
- [x] Review platform-independent modelling (OMG MDA).
- [x] Review UML structural and behavioural modelling.
- [x] Review business-rule representation (OMG SBVR).
- [x] Review API contracts (OpenAPI).
- [x] Review event-driven API contracts (AsyncAPI).
- [x] Review runtime observability conventions (OpenTelemetry).
- [x] Review web runtime inspection (DOM, CSSOM, WebDriver).
- [x] Review native UI runtime inspection and accessibility semantics.
- [x] Review scenario-based behaviour specification (Gherkin/BDD).
- [x] Review JSON Schema for machine validation.
- [x] Review design-token interchange and its limits.
- [x] Write a comparative standards review.
- [x] Record design decisions, rejected approaches, and unresolved questions.
- [x] Revise the proposed facet list and record new candidate facets.

## Phase 2 — Core concepts and common model

- [x] Define and review canonical terminology.
- [x] Distinguish declared contracts, runtime observations, and source-derived inferences.
- [x] Separate scenario definitions, scenario executions, and individual observations.
- [x] Define external, platform-inspection, and instrumented runtime observation methods.
- [x] Define capture coverage and incomplete/unavailable dimensions.
- [x] Define system boundary, component, and facet concepts.
- [x] Define runtime-rule classification, proposition, status, and relationships.
- [x] Define source-derived-rule record and verification lifecycle.
- [x] Define scenario, trigger, condition, input, expected outcome, and actual outcome.
- [x] Define observation, outcome, state change, and side effect.
- [x] Define evidence and provenance requirements.
- [x] Distinguish unknown, not observed, unavailable, not applicable, redacted, and conflicting states.
- [x] Define identity relationships, units, timestamps, ordering, and correlation conceptually.
- [x] Define the common observation envelope and typed facet payload boundary.
- [x] Define the conceptual relationship to format versioning.
- [x] Test the model against interface resolved-layout and API request/response examples.

**Phase 2 exit gate: satisfied at the conceptual-model level.** The examples are model tests, not empirical captures or final conformance fixtures. Exact serialized fields, schemas, facet payloads, and the final facet taxonomy remain open.

## Phase 3 — Facet specifications

- [ ] Interface
- [ ] Behaviour
- [ ] Business rules
- [ ] Data
- [ ] Persistence
- [ ] API
- [ ] Messaging
- [ ] Identity and authentication
- [ ] Authorization and permissions
- [ ] Security controls
- [ ] Background processing
- [ ] Errors and recovery
- [ ] Integrations
- [ ] Configuration
- [ ] Performance and resource behaviour
- [ ] Review facet boundaries and cross-facet relationships.

For every facet, track: scope, observable dimensions, trigger/scenario model, typed payload, evidence requirements, limitations, examples, and schema requirements.

## Phase 4 — Machine-readable schemas

- [ ] Define schema conventions and versioning.
- [ ] Manifest schema.
- [ ] Common observation schema.
- [ ] Runtime-rule schema.
- [ ] Source-rule schema.
- [ ] Evidence schema.
- [ ] Facet payload schemas.
- [ ] Comparison report schema.
- [ ] Positive and negative validation fixtures.
- [ ] Validate all examples.

## Phase 5 — Canonicalization and comparison

- [ ] Define capture alignment and identity matching.
- [ ] Define normalization without loss of meaningful distinctions.
- [ ] Define comparison categories and tolerances.
- [ ] Define missing, unknown, conflicting, and incomparable results.
- [ ] Define coverage and bounded-equivalence reporting.
- [ ] Define comparison report format.
- [ ] Create and review comparison examples.

## Phase 6 — End-to-end examples and conformance

- [ ] Interface capture example.
- [ ] Behaviour capture example.
- [ ] API capture example.
- [ ] Full-system multi-facet example.
- [ ] Source-derived rule example, clearly separated from runtime evidence.
- [ ] Equivalent capture pair.
- [ ] Capture pair containing deliberate differences.
- [ ] Automated schema validation tests.
- [ ] Conformance test cases and capture-agent usage guidance.

## Phase 7 — Review, release, and maintenance

- [ ] Check terminology consistency.
- [ ] Check common-envelope consistency across facets.
- [ ] Check provenance and evidence requirements.
- [ ] Check schema and example validity.
- [ ] Check comparison claims and limitations.
- [ ] Document known limitations and unresolved issues.
- [ ] Publish versioned specification release.
- [ ] Define maintenance and change process.

## Decision log

| ID | Decision | Status | Record |
|---|---|---|---|
| D-001 | Keep runtime-observed rules distinct from source-derived rules. | Accepted | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md) |
| D-002 | Use a shared conceptual envelope with facet-specific typed payloads. | Accepted | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md); serialization remains deferred. |
| D-003 | Bound equivalence claims to captured scenarios and evidence. | Accepted | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md) |
| D-004 | Compose existing standards; no reviewed standard supplies the complete capture-and-comparison format. | Accepted | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md) |
| D-005 | Keep declared contracts distinct from runtime observations. | Accepted | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md) |
| D-006 | Expand the facet taxonomy with configuration, performance/resource behaviour, and clearer identity/access boundaries. | Proposed | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md); validate in Phase 3. |
| D-007 | Separate scenario definitions, executions, and observations. | Accepted | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md) |
| D-008 | Treat rules as propositions supported/qualified/contradicted by observations. | Accepted | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md) |
| D-009 | Keep expected outcomes, actual outcomes, and evaluations separate. | Accepted | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md) |

## Work log

### 2026-11-26
- Completed Phase 2: added TERMINOLOGY.md, PRINCIPLES.md, RULE-CLASSIFICATION.md, EVIDENCE-AND-PROVENANCE.md, OBSERVATION-MODEL.md, SOURCE-DERIVED-RULES.md, and CORE.md.
- Defined separate scenario, execution, observation, evidence, and rule concepts; separated expected from actual outcomes; specified runtime observation methods and coverage/missingness states.
- Tested the conceptual model against interface resolved-layout and API request/response cases. These tests validate model fit conceptually, not empirical capture or schema conformance.
- Accepted D-002 and added D-007, D-008, and D-009. No machine-readable schemas or final facet payloads were created.
- Moved active work to Phase 3; next task is the interface facet specification.

### 2026-11-26
- Inspected the repository and confirmed README, plan, and tracker.
- Completed Phase 0 governance: added `CONTRIBUTING.md`, `CHANGELOG.md`, `research/DESIGN-DECISIONS.md`, and `specification/VERSIONING.md`.
- Completed Phase 1 research: added `research/STANDARDS-REVIEW.md` and `research/REFERENCES.md` using authoritative standards-body and project sources.
- Evaluated requirements engineering, platform-independent modelling, UML, SBVR, OpenAPI, AsyncAPI, OpenTelemetry, web/native UI inspection, Gherkin, JSON Schema, design tokens, and HTTP semantics.
- Recorded the limits of existing standards, distinguished declared contracts from runtime observations, and revised the facet taxonomy as a proposal.
- Verified the Phase 1 exit gate and moved active work to Phase 2.
- Completed Phase 2: created the core conceptual documents and tested the shared model against interface layout and API request/response cases. These are illustrative model tests, not empirical system captures.
- Accepted D-002 and recorded D-007 through D-009. Machine schemas, facet payloads, and the final facet taxonomy remain open.
- Moved active work to Phase 3. Next: define and validate the interface facet boundary and its runtime capture requirements.
