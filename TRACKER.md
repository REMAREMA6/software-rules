# Project Tracker

**Project:** Software Rules  
**Repository:** REMAREMA6/software-rules  
**Last updated:** 2026-11-26  
**Current phase:** Phase 6 — Expanded multi-facet capture and conformance  
**Overall status:** Phase 6 in progress; initial interface/behaviour/API fixture exists, but multi-facet completeness is not established

> This file is the persistent progress and handoff record. Update it whenever task status changes. Keep the current task, blockers, and next action explicit so work can resume in a new chat.

## Status key

- [ ] Not started
- [~] In progress
- [x] Completed
- [!] Blocked
- [?] Needs a decision or verification

## Current position

- **Current phase:** Phase 6 — Expanded multi-facet capture and conformance
- **Current task:** Complete the Task Board capture record and comparison updates; then establish a richer full-stack reference target for facets absent from the Task Board.
- **Blockers:** The Task Board is a limited fixture. Its in-memory adapter does not demonstrate durable persistence or production server behaviour; it has no identity, authorization, messaging, integrations, background processing, or application configuration. A richer reference target has not yet been selected or created.
- **Next action:** Review the latest supplemental artifact and update the capture records/comparisons. Then add a richer target that actually implements persistence, messaging, identity/authentication, authorization, security, background jobs, integrations, and application configuration.
- **Existing result:** The initial reference/independent Task Board baseline is pixel-identical across seven tested UI states at 1280×800 in Chromium 159.0.8154.6 on Linux; the deliberate mutation produces a 272-pixel visual mismatch. This is bounded evidence, not proof of complete interface capture or whole-system replication.

## Phase tracking

| Phase | Name | Status | Notes |
|---|---|---|---|
| 0 | Repository and project governance | [x] Complete | Roadmap, tracker, contribution guide, changelog, decision log, maturity/versioning policy, and navigation links established. |
| 1 | Research existing standards and prior art | [x] Complete | Comparative review, authoritative references, limitations, design implications, and revised facet proposal recorded. |
| 2 | Core concepts and common model | [x] Complete | Core vocabulary, rule/evidence classes, linked observation model, source-derived model, and interface/API conceptual tests completed. Schemas remain deferred. |
| 3 | Facet specifications | [x] Complete | Accepted 15-facet draft catalogue; all facets have boundaries, conceptual payload dimensions, scenario/evidence requirements, limitations, cross-facet links, and illustrative worked examples. Not empirical captures. |
| 4 | Machine-readable schemas | [x] Complete | Draft v0.2.0 schemas; 15 typed facets; positive/negative fixtures; Ajv 2020-12 CI passed. |
| 5 | Canonicalization and comparison | [x] Complete | Matching, normalization, classifications, coverage, bounded conclusions, report schema, example, and CI validation completed. |
| 6 | End-to-end multi-facet capture and conformance | [~] In progress | Initial interface/behaviour/API fixture exists. Audit interface evidence, then expand behaviour, business rules, data, and the remaining applicable facets. Phase 6 is not complete. |
| 7 | Review, release, and maintenance | [ ] Not started | Blocked until the expanded Phase 6 exit gate is satisfied. |

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

- [x] Interface — resolved hierarchy, presentation, geometry, stacking, accessibility, assets, and UI states.
- [x] Behaviour — triggers, conditions, transitions, outputs, and side effects.
- [x] Business rules — domain decisions, constraints, calculations, and policy outcomes.
- [x] Data — runtime structures, values, validation, and transformations.
- [x] Persistence — durable state, transactions, consistency, and lifecycle.
- [x] API — synchronous request/response exchanges.
- [x] Messaging — asynchronous message/event delivery and processing.
- [x] Identity and authentication — principal establishment and credential/session lifecycle.
- [x] Authorization and permissions — runtime access decisions and enforcement.
- [x] Security controls — security-relevant mechanisms and outcomes under authorized tests.
- [x] Background processing — queued, scheduled, and worker lifecycle.
- [x] Errors and recovery — failures, retries, fallbacks, compensation, and recovery.
- [x] Integrations — external-system interactions and dependency outcomes.
- [x] Configuration — effective runtime configuration and changes.
- [x] Performance and resource behaviour — measured workload and resource characteristics.
- [x] Review facet boundaries and cross-facet relationships.
- [x] Create a catalogue and explicit boundary/overlap matrix.
- [x] Define observation unit, conceptual payload dimensions, scenario requirements, evidence, limitations, and cross-facet links for every facet.
- [x] Add a worked conceptual example to every facet specification.

**Phase 3 exit gate: satisfied at the specification level.** All 15 facets have a boundary, conceptual typed payload inventory, evidence model, limitations, and illustrative worked example. These examples are not empirical captures. Machine schemas remain Phase 4; empirical end-to-end examples and conformance fixtures remain Phase 6.

## Phase 4 — Machine-readable schemas

- [x] Define schema conventions, dialect, identifiers, draft version, and extension policy.
- [x] Capture manifest schema.
- [x] Common target, coverage, scenario, execution, and observation record schemas.
- [x] Separate runtime-rule, source-derived-rule, and declared-contract schemas.
- [x] Evidence/provenance schema.
- [x] Typed payload schemas for all 15 facets.
- [x] Structural comparison-report envelope (comparison semantics deferred to Phase 5).
- [x] Positive and negative validation fixtures.
- [x] Automated validation runner and instructions.
- [x] Execute validation and verify expected fixture outcomes.
- [x] Document schema evolution and validation boundaries.

**Phase 4 exit gate: satisfied.** GitHub Actions run [#2](https://github.com/REMAREMA6/software-rules/actions/runs/45792470335) completed successfully on 2026-11-26. Ajv 2020-12 validated the valid fixture and rejected all three negative fixtures for the expected structural reasons. The schemas remain Draft version 0.1.0 in the intended v1 compatibility family; they are not a stable release. Cross-record reference integrity and evidence authenticity remain outside JSON Schema validation.

## Phase 5 — Canonicalization and comparison

- [x] Define capture alignment and identity matching.
- [x] Define normalization without loss of meaningful distinctions.
- [x] Define comparison bases: exact, normalized, semantic, and tolerance-based.
- [x] Define match, mismatch, missing, additional, unknown, conflicting, and not-comparable results.
- [x] Define missingness decision order; missing evidence never becomes a match.
- [x] Define coverage and bounded-equivalence reporting.
- [x] Expand comparison report schema.
- [x] Create and review a comparison example.
- [x] Add valid and invalid comparison fixtures to automated CI.

**Phase 5 exit gate: satisfied.** GitHub Actions run [#4](https://github.com/REMAREMA6/software-rules/actions/runs/45793398830) passed the capture and comparison fixture suites. The valid comparison example passed; the invalid report claiming universal equivalence was rejected. The example is illustrative, not empirical. Active work moved to Phase 6.

## Phase 6 — Cross-repository, cross-stack replication and conformance

**Status: [~] In progress.** Phase 6 uses multiple source repositories and a separate independent replication project. One application is not expected to implement all 15 facets. See [the full programme](examples/CROSS-REPOSITORY-REPLICATION-PROGRAM.md).

### Agreed operating model
- [x] Each facet may use a different source repository.
- [x] A separate independent replication project is required.
- [x] Rules must be extracted into a technology-independent specification before implementation.
- [x] Equivalent source/replica probes, comparison, and mutation detection are required.
- [ ] Create the replication-lab skeleton and case manifest.
- [ ] Select and inspect immutable source repositories for all 15 facets.
- [ ] Implement and validate independent cross-stack cases for every facet.
- [ ] Complete the final evidence and coverage audit.

### Existing bounded evidence
- [x] Task Board reference, independent, and deliberately mutated implementations.
- [x] 13-state interface comparison, including three viewport widths, focus, hover, and colour-scheme preference, pixel-identical under recorded CI conditions.
- [x] Initial behaviour, business-rule, data, in-memory API adapter, error, limited security-output, and performance samples.
- [x] Runtime artifact and integrity/schema/comparison workflows recorded in the Task Board audit.
- [ ] Resolve Task Board's remaining partial properties if still in its declared scope; otherwise explicitly constrain that fixture's scope with evidence and justification.

### Fifteen-facet cross-repository programme
- [ ] 1. Interface — screen/state capture and independent UI-stack replication.
- [ ] 2. Behaviour — triggers, transitions, side effects, ordering, and failure replication.
- [ ] 3. Business rules — conditions, constraints, calculations, precedence, and boundary replication.
- [ ] 4. Data — shapes, types, nullability, relationships, transformations, and serialization.
- [ ] 5. Persistence — durable state, transactions, rollback, concurrency, and consistency.
- [ ] 6. API — request/response, protocol, validation, and failure semantics.
- [ ] 7. Messaging — publish/consume, delivery, acknowledgement, ordering, retries, and idempotency.
- [ ] 8. Identity/authentication — principal, credential/session lifecycle, expiry, and logout.
- [ ] 9. Authorization — actor/resource/action policy matrix and enforcement.
- [ ] 10. Security — authorized control, bypass, and containment scenarios.
- [ ] 11. Background processing — enqueue, worker lifecycle, retry, cancellation, and terminal outcomes.
- [ ] 12. Errors/recovery — failure classes, retry/fallback/compensation, and recovered-state replication.
- [ ] 13. Integrations — external dependency contracts and controlled failure outcomes.
- [ ] 14. Configuration — defaults, precedence, invalid/missing values, and runtime changes.
- [ ] 15. Performance/resources — repeatable workload, latency distributions, throughput, and resource behaviour.

### Rule-level completion checklist
- [ ] Source repository, immutable commit, licence, runtime, and system boundary recorded.
- [ ] Runtime observations, source-derived inferences, and declared contracts distinguished.
- [ ] Technology-independent rule and facet payload captured.
- [ ] Independent replica implemented in a different stack.
- [ ] Equivalent normal, boundary, negative, and failure scenarios executed where applicable.
- [ ] Captures compared with no unexplained required mismatch or coverage gap.
- [ ] Meaningful mutation detected.
- [ ] Evidence, provenance, cross-facet links, and reproduction instructions retained.

**Current blocker:** the replication lab and multi-repository case set have not yet been built. The earlier Task Board-only approach is superseded as the overall Phase 6 strategy. Do not claim Phase 6 complete until the 15-facet cross-repository exit gate passes.

## Phase 7 — Review, release, and maintenance

**Status: [ ] Not started — blocked by Phase 6.**

- [ ] Review terminology, facet boundaries, provenance, schemas, and examples.
- [ ] Verify completeness and comparison claims against evidence.
- [ ] Document known limitations and unresolved issues.
- [ ] Publish a versioned specification release.
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
| D-012 | Use evidence-backed alignment, loss-aware normalization, explicit result classes, and bounded comparison conclusions. | Accepted | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md) |\n| D-013 | Require evidence-backed, replication-sufficient captures for the declared scope; completeness is separate from observed agreement. | Accepted | [DESIGN-DECISIONS.md](research/DESIGN-DECISIONS.md) |

## Work log

### 2026-11-26
- Completed Phase 4: added the draft 0.1.0 capture and record schemas, all 15 typed facet payload schemas, and validation fixtures. GitHub Actions run #2 passed the four fixture expectations using Ajv 2020-12.
- Completed Phase 5: defined matching, normalization, comparison bases, result classification, coverage, and bounded conclusions; expanded the report schema and added comparison fixtures. GitHub Actions run #4 passed the capture and comparison fixture suites. The comparison example is illustrative, not empirical. Active work moved to Phase 6.
- Completed Phase 0 governance: added the contribution guide, changelog, design-decision log, and versioning policy.
- Completed Phase 1 research: reviewed candidate standards and prior art, collected authoritative references, documented limitations, and proposed the revised facet taxonomy.
- Completed Phase 2: added the core conceptual documents; separated scenario definitions, executions, observations, evidence, runtime rules, source-derived rules, and declared contracts; tested the model against interface and API examples.
- Accepted D-002 and recorded D-007 through D-009.
- Completed Phase 3: added the 15-facet catalogue, boundary/overlap matrix, and an individual specification for every facet. Each facet includes its scope, observation unit, conceptual payload dimensions, scenario requirements, evidence expectations, limitations, cross-facet links, and an illustrative worked example.
- Accepted D-010, the 15-facet catalogue for this specification draft. Phase 3 examples are illustrative model tests, not empirical captures. Machine schemas remain Phase 4; empirical end-to-end captures remain Phase 6.
- Verified the Phase 3 files and project navigation on GitHub. Active work moved to Phase 4: machine-readable schemas.



### Phase 6 initial completeness work — 2026-11-26

- [x] Record the Replication Completeness Rule as an accepted project requirement.
- [x] Require a declared replication scope and per-property inventory in the capture schema.
- [x] Require comparisons to report replication completeness separately from observed agreement.
- [x] Add cross-record integrity checks for unique inventory IDs, facet declarations, observation/evidence references, and false complete claims.
- [x] Add Task Board inventories for interface, behaviour, and API properties.
- [x] Bump the incompatible draft capture/report format from 0.1.0 to 0.2.0 and update the valid fixtures.
- [x] Audit all three inventories: 22 properties each; every required property is captured or explicitly not applicable, and optional exclusions have reasons.
- [x] Add tests rejecting a complete status when required properties are partial or unresolved.
- [x] Expand reference, independent, and mutated runtime captures to cover all required properties in the declared Task Board scope.
- [x] Capture full per-element computed CSS properties, DOM hierarchy, pseudo-element content, geometry, accessibility snapshots, and screenshots for every declared UI state.
- [x] Compare reference and independent baseline screenshots pixel-for-pixel across seven states; all seven comparisons have zero differing pixels.
- [x] Preserve and detect the deliberate mutation; its one-active screenshot differs by 272 pixels.
- [x] Execute empty/whitespace validation, keyboard-only create/filter/complete/delete, API success, and HTTP 503 failure scenarios.
- [x] Update all three capture records, schema fixtures, and both comparison reports with runtime evidence and completeness conclusions.
- [x] Re-run schema validation and cross-record integrity checks; both pass.

**Phase 6 redo result:** Complete for the declared Task Board replication scope. The three captures each account for all 22 inventory properties: 18 captured, one explicitly not applicable, and three optional dimensions explicitly excluded. The reference and independent baseline are pixel-identical in seven tested UI states at 1280×800 CSS px under Chromium 159.0.8154.6 on Linux. Keyboard, validation, API request/response, and failure outcomes agree. The mutated implementation remains fully captured but comparison correctly reports its deliberate pluralization mismatch. Runtime evidence: [successful Playwright run #45855076741](https://github.com/REMAREMA6/software-rules/actions/runs/45855076741), [capture artifact](https://github.com/REMAREMA6/software-rules/actions/runs/45854435953/artifacts/15136130524). Final schema and integrity validation: [run #45855135858](https://github.com/REMAREMA6/software-rules/actions/runs/45855135858).

**Boundary:** This proves completeness and pixel identity only for the declared Task Board scope and captured environment. It does not prove universal equivalence across every stack, browser, operating system, viewport, or arbitrary software system. Phase 7 is now active.


### Phase 6 expansion — 2026-11-26

- Reframed Phase 6 as the complete multi-facet empirical capture and conformance programme, rather than treating the initial Task Board fixture as the final scope.
- Kept the existing interface/behaviour/API runtime work as a bounded baseline. It does not establish complete interface capture or coverage of other software facets.
- Ordered the remaining work: interface evidence audit; behaviour/functionality; business rules; data; persistence; API/messaging/integrations; identity/authorization/security; background processing/errors/configuration/performance; cross-facet completeness.
- Phase 7 is blocked until the expanded Phase 6 exit gate is satisfied.
- Next action: extend the Playwright harness with title boundary cases, duplicate titles, mixed-task state/count truth tables, repeated toggles/deletes, malformed/unknown-ID API operations, and exact request/response data-shape capture.


### Phase 6A audit result — 2026-11-26

- Inspected the three capture inventories, evidence records, observation payloads, and integrity validator.
- Confirmed that the old reference interface observation itself explicitly reported partial completeness for its main-control snapshot; the later Playwright archive contains richer detail, but the inventory had no separate property for the font-rendering limitation.
- Added an explicit partial font-rendering property and partial business-rule/data observations to each Task Board capture. These include only the facts supported by the existing one-task workflow and in-memory API samples.
- Added six further partial rule/data properties across title normalization, initial completion state, summary counts, task record shape, identifier generation, and PATCH field-preservation semantics.
- Updated all three captures to 29 inventory entries: 18 captured, seven partial, one not applicable, and three optional exclusions. Completeness is now incomplete.
- Updated equivalent and deliberate-difference reports to preserve observed comparison results while reporting incomplete-both.
- Updated integrity tests to expect the Task Board captures to remain incomplete.
- Audit finding: the integrity validator checks reference existence, facet labels, and declared statuses; it does not verify that the linked evidence semantically proves the property or that the inventory is exhaustive. This limitation is now explicit. Stronger evidence-quality checks remain active work.


### Phase 6B probe implementation — 2026-11-26

- Added an expanded Playwright probe sequence to the runtime harness for leading/trailing whitespace normalization, duplicate titles, HTML-like/Unicode title safety, 512-character titles, mixed active/completed records, filter counts, completion toggle-back, deletion, and identifier samples.
- Added request/response synchronization and explicit outcome assertions so the test does not mistake a click for a completed asynchronous operation.
- The harness retains the probe results in the per-variant runtime output. This initial implementation was subsequently executed successfully in run #45858743131; verified results are recorded in the later work-log entry.


- Added .github/workflows/phase6-expanded-conformance.yml to run the expanded Playwright capture, evidence-link integrity tests, schema validation, and artifact upload on relevant pushes and pull requests. The workflow has been added; its first execution result still needs verification.


### Phase 6 expanded probe execution — 2026-11-26

- Corrected a Playwright strict-mode selector ambiguity found in the first workflow attempt; filter button locators now require exact accessible-name matches.
- Successful run: [GitHub Actions #45858743131](https://github.com/REMAREMA6/software-rules/actions/runs/45858743131). Runtime capture, cross-record/evidence-link integrity, and JSON Schema/comparison validation all passed.
- Retained 41 runtime artifact files in [artifact #15136459580](https://github.com/REMAREMA6/software-rules/actions/runs/45858743131/artifacts/15136459580), including three variant captures and expanded probe results.
- All three variants agreed on title trimming, duplicate acceptance, literal HTML-like/Unicode rendering, 512-character title acceptance, mixed-state counts/filters, completion toggle-back, PATCH field preservation, and three-task deletion.
- Updated all three captures with the new scenario, execution, evidence, and observations. Inventory now has 34 entries per capture: 28 captured, two partial, one not applicable, and three optional exclusions.
- Updated comparison coverage to 28 observed/captured units and two partial units; all reports remain incomplete-both.
- Remaining partial properties: font rendering beyond the recorded Chromium/Linux conditions and maximum title-length constraint.


- Updated the Phase 6 facet-expansion document with current 6B–6D progress and a clear statement of which facets the Task Board does not exercise.
- The latest documentation/capture validation run #45859552354 also completed successfully.

- Post-update verification: [run #45859279008](https://github.com/REMAREMA6/software-rules/actions/runs/45859279008) passed after the 34-entry capture inventories and comparison reports were updated; [run #45859552354](https://github.com/REMAREMA6/software-rules/actions/runs/45859552354) also passed after the latest documentation/plan updates.


### Supplemental Phase 6 probe expansion — 2026-11-26

- Expanded the runtime harness with responsive viewports (320×720, 768×900, 1920×1080), focus/hover/dark-colour-scheme states, SVG/script-shaped input probes, HTTP 503 failures for create/update/delete, and browser navigation/paint/resource measurements.
- Successful runtime workflow: [#45860499892](https://github.com/REMAREMA6/software-rules/actions/runs/45860499892). All 13 baseline UI screenshot comparisons were pixel-identical; the deliberate mutation remained detectable at 272 differing pixels.
- Runtime results: no horizontal overflow at the three tested widths; focus and hover states were reached; no disabled controls exist in the fixture; SVG/script-shaped titles were rendered literally with no injected SVG/script/image and no payload execution; all three failed API operations returned 503 and produced unhandled page errors with no user-facing recovery UI.
- Single-run local performance samples were recorded: navigation load event end 8.1–8.9 ms, first contentful paint 16 ms, and 14 resources per variant. These are CI-host measurements, not performance guarantees.
- Artifact: [#15137373210](https://github.com/REMAREMA6/software-rules/actions/runs/45860499892/artifacts/15137373210), 65 files, 30-day retention.
- Added `examples/task-board/FACET-APPLICABILITY.md`. It explicitly separates the five facets exercised by Task Board from facets absent from this fixture. It does not mark the project-wide Phase 6 complete.

- Task Board supplemental evidence now spans eight facets: interface, behaviour, business rules, data, API adapter, errors/recovery, limited security output encoding, and single-run performance. The three captures contain 38 inventory entries each (33 captured, two partial, one not applicable, two excluded) and remain explicitly incomplete.

- Corrected an intermittent screenshot race by waiting for PATCH/DELETE responses and the resulting DOM state before saving the pointer workflow. [Run #45861726449](https://github.com/REMAREMA6/software-rules/actions/runs/45861726449) passed runtime capture, cross-record integrity, and schema/comparison validation. Artifact #15137768292 contains the corrected 65-file evidence archive.
