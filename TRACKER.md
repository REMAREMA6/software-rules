# Project Tracker

**Project:** Software Rules  
**Repository:** REMAREMA6/software-rules  
**Last updated:** 2026-11-26  
**Current phase:** Phase 0 — Repository and project governance  
**Overall status:** In progress

> This file is the persistent progress record. Update it whenever task status changes. Keep the current task and next action explicit so work can resume in a new chat.

## Status key

- [ ] Not started
- [~] In progress
- [x] Completed
- [!] Blocked
- [?] Needs a decision or verification

## Current position

- **Current phase:** Phase 0 — Repository and project governance
- **Current task:** Establish and review the project roadmap and tracker.
- **Blockers:** None known.
- **Next action:** Begin Phase 1 research; review the existing standards and prior-art candidates listed in `PLAN.md`, then record findings and design implications.

## Phase tracking

| Phase | Name | Status | Notes |
|---|---|---|---|
| 0 | Repository and project governance | [~] In progress | Repository and initial README exist; plan and tracker being established. |
| 1 | Research existing standards and prior art | [ ] Not started | Research before fixing the core model. |
| 2 | Core concepts and common model | [ ] Not started | Depends on Phase 1 findings. |
| 3 | Facet specifications | [ ] Not started | Define facet boundaries and typed payloads. |
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
- [ ] Link plan and tracker from the README.
- [ ] Establish changelog and design-decision recording conventions.
- [ ] Define specification maturity labels and versioning policy.

## Phase 1 — Research existing standards and prior art

- [ ] Review requirements/specification standards (ISO/IEC/IEEE 29148).
- [ ] Review platform-independent modelling (OMG MDA).
- [ ] Review UML structural and behavioural modelling.
- [ ] Review business-rule representation (OMG SBVR).
- [ ] Review API contracts (OpenAPI).
- [ ] Review event-driven API contracts (AsyncAPI).
- [ ] Review runtime observability conventions (OpenTelemetry).
- [ ] Review web runtime inspection (DOM, CSSOM, WebDriver).
- [ ] Review native UI runtime inspection and accessibility semantics.
- [ ] Review scenario-based behaviour specification (Gherkin/BDD).
- [ ] Review JSON Schema for machine validation.
- [ ] Review design-token interchange and its limits.
- [ ] Write a comparative standards review.
- [ ] Record design decisions, rejected approaches, and unresolved questions.
- [ ] Confirm or revise the proposed facet list.

## Phase 2 — Core concepts and common model

- [ ] Define and review the canonical terminology.
- [ ] Define system boundary and facet model.
- [ ] Define runtime-rule record.
- [ ] Define source-derived-rule record.
- [ ] Define scenario, trigger, condition, input, and environment.
- [ ] Define observation, outcome, state change, and side effect.
- [ ] Define evidence and provenance.
- [ ] Define unknown, unobserved, inferred, not applicable, and contradicted states.
- [ ] Define identity, relationships, units, timestamps, and ordering.
- [ ] Define common observation envelope.
- [ ] Define versioning and compatibility.
- [ ] Review the core model against at least two unlike software facets.

## Phase 3 — Facet specifications

- [ ] Interface
- [ ] Behaviour
- [ ] Business rules
- [ ] Data
- [ ] Persistence
- [ ] API
- [ ] Messaging
- [ ] Security
- [ ] Permissions
- [ ] Background processing
- [ ] Errors
- [ ] Integrations
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
| D-001 | Keep runtime-observed rules distinct from source-derived rules. | Accepted | Project foundation; documented in README and PLAN. |
| D-002 | Use a shared core envelope with facet-specific typed payloads. | Proposed | Validate during research and core-model design. |
| D-003 | Treat comparison conclusions as bounded by captured scenarios and evidence. | Accepted | Project foundation; documented in README and PLAN. |

## Work log

### 2026-11-26
- Repository inspected; confirmed the initial README is present.
- Added the project roadmap and target layout.
- Established this tracker as the progress and handoff record.
- Next: begin standards and prior-art research before fixing the format.
