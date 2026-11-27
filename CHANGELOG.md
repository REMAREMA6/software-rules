# Changelog

All notable changes to the Software Rules specification, schemas, examples, and repository structure are recorded here.

This project follows a Keep a Changelog-inspired structure. Entries describe user- or implementer-relevant changes, not every typo correction.

## Unreleased

### Added
- Pinned BullMQ source-runtime probe using the exact inspected commit and Redis, plus an independent Python scenario simulator, capture comparator, and mutation-detection tests.

### Fixed
- Cross-record integrity now accepts direct source-artifact evidence for explicitly source-inferred inventory properties while keeping runtime observations separate; added a BullMQ source capture fixture and regression tests.
- Corrected BullMQ runtime probe suppression detection and enabled shell pipeline failure propagation after artifact review exposed empty captures behind falsely green workflow results.

### Changed
- Corrected the Phase 6 handoff and source-candidate count; explicitly separated the Python model workflow from BullMQ runtime execution and retained the source capture as unverified/incomplete. Added a pinned-source runtime-to-replica execution order and bounded cross-stack portability language.

### Added
- Cross-repository replication lab scaffolding, rule-case and source-repository templates, and a Python rule-model CI workflow.
- Initial source candidates for BullMQ, Keycloak, OWASP Juice Shop, Grafana, TypeORM, n8n, Prometheus, Express, and Medusa, each pinned to an inspected commit with licence/evidence status recorded.
- BullMQ retry-policy source capture and a narrow independent Python retry-decision replica with eight test cases, including an off-by-one mutation check. This case remains incomplete pending source runtime execution and capture comparison.

### Changed
- Updated the Phase 6 tracker to record the new multi-repository work and distinguish candidate/source-derived evidence from completed cross-stack conformance.

### Changed
- Corrected Phase 6 architecture: use multiple immutable source repositories and a separate independent replication lab. One fixture is no longer expected to implement all 15 facets; each rule must pass source extraction, technology-independent capture, different-stack replication, equivalent probes, comparison, and mutation detection.

### Added
- Cross-repository Phase 6 programme with a 15-facet validation matrix, source register, replication-lab layout, evidence requirements, rule-level pass criteria, and explicit exit gate.

### Changed
- Reframed Phase 6 as an expanded multi-facet empirical capture and conformance programme. The initial Task Board result is retained as bounded baseline evidence; Phase 6 remains in progress until all applicable facets in the selected replication scope have evidence-backed inventories and cross-facet conformance. Phase 7 is blocked.

### Added
- Successful expanded Task Board probe evidence from GitHub Actions run #45858743131, including title normalization, duplicate acceptance, literal user-content rendering, long-title boundary, mixed-state counts/filters, bidirectional completion, multiple deletion, identifiers, and PATCH data samples.
- Dedicated Phase 6 expanded-conformance GitHub Actions workflow to execute the expanded Playwright probes, cross-record/evidence-link tests, schema validation, and runtime artifact upload.
- Expanded Playwright probes for title trimming, duplicate titles, HTML-like/Unicode and long inputs, mixed task-state/filter truth tables, completion toggling, deletion, and identifier samples; execution and evidence review are pending.
- Stronger cross-record integrity checks require property evidence references to be attached to linked observations and require captured properties to have observed runtime-class evidence not explicitly marked partial.
- Comparison coverage now supports explicit partial, conflicting, source-inferred, and excluded unit counts.
- Draft schema format bumped to 0.2.0 because replication-scope inventories and separate comparison-completeness reporting are incompatible additions to the 0.1.0 draft.
- Added the Playwright runtime conformance harness, retaining full computed CSS properties, DOM hierarchy, pseudo-element content, geometry, accessibility snapshots, UI-state screenshots, keyboard/validation scenarios, API traces, and pixel comparisons.
- Normative `specification/REPLICATION-COMPLETENESS.md`: replication-scope completeness is a separate requirement from agreement among the properties captured; incomplete captures cannot establish faithful replication.
- Phase 6 cross-record integrity validator and unit tests for duplicate IDs and unresolved/mismatched references across capture records.
- Phase 5 comparison specification: matching/alignment, normalization, difference classification, coverage/limitations, and a worked comparison report.
- Expanded comparison-report JSON Schema with alignment, normalization profile, result, coverage, and bounded conclusion structures.
- Comparison valid/invalid fixtures, including a schema-enforced prohibition on universal-equivalence claims.
- Phase 4 draft JSON Schema set (0.1.0) with a capture manifest, shared records, 15 typed facet payload schemas, and a structural comparison-report envelope.
- Positive and negative fixtures plus an Ajv 2020-12 validation runner and instructions.
- `specification/SCHEMA-DESIGN.md` documenting serialization choices, missingness, provenance, extensions, and validation boundaries.
- Phase 3 facet catalogue, boundary/overlap matrix, and 15 individual facet specifications with conceptual payload inventories and illustrative worked examples.
- Design decision D-010 accepting the 15-facet catalogue for the current specification draft.
- Phase 2 core specification: terminology, principles, rule classification, evidence/provenance, observation model, source-derived rules, and core model.
- Cross-facet conceptual model tests for interface layout and API request/response observations.
- Design decisions D-007 through D-009 for scenario/execution/observation separation, rule-versus-observation distinction, and expected-versus-actual outcomes.
- Repository governance documents and conventions.
- Comparative standards review and authoritative research bibliography.

### Changed
- Phase 6 was reopened because the original selected observations were not replication-sufficient. The redo now completes every required property in the declared Task Board scope; all three captures report complete, and comparison completeness remains separate from observed agreement.
- Phase 6 runtime conformance now verifies seven pixel-identical baseline UI states at 1280×800 in Chromium 159.0.8154.6 on Linux, detects the deliberate 272-pixel mutation, and compares keyboard, validation, API, and HTTP 503 failure outcomes.
- Phase 6 schema fixtures and cross-record integrity checks pass after updating the validator to require complete Task Board inventories while retaining the incomplete minimal fixture. Phase 7 review is now active.
- Completed Phase 5 and advanced active work to Phase 6 after GitHub Actions run #4 validated both capture and comparison fixtures.
- Extended automated validation to run on comparison specification changes and validate comparison-report fixtures alongside capture fixtures.
- Completed Phase 4 and advanced active work to Phase 5 after the Ajv 2020-12 GitHub Actions validation passed the valid fixture and all three negative fixtures.
- Phase 4 schema design formalizes the common record envelope; comparison semantics and cross-record conformance remain deferred to Phases 5–6.
- Completed Phase 3 and moved active work to Phase 4 (machine-readable schemas). The facet examples are illustrative; empirical end-to-end captures remain Phase 6 work.
- Completed Phase 1 and moved the tracker to Phase 2; subsequently completed Phase 2 and moved active work to Phase 3.
- Revised the working facet taxonomy to separate identity/authentication from authorization and add configuration and performance/resource behaviour.
- Recorded the distinction between declared contracts and actual runtime observations.
- Completed Phase 2's conceptual model and accepted the shared-envelope/facet-payload approach (D-002). Machine schemas and facet payloads remain deferred.

### Deprecated
- None.

### Removed
- None.

### Fixed
- None.

## Change-recording rules

- Add an entry when a change affects meaning, format structure, schema behaviour, compatibility, examples, or repository navigation.
- Group entries under Added, Changed, Deprecated, Removed, Fixed, or Security as appropriate.
- Reference the relevant decision ID (for example, D-004) when a change follows a recorded design decision.
- Keep entries concise and describe the effect of the change.
- Do not use this file as the task tracker; use [TRACKER.md](TRACKER.md) for progress.
- When a version is released, replace the relevant Unreleased entries with a dated version heading and keep prior release entries unchanged.

## 2026-11-26 — Phase 6 conformance examples and replication-completeness redo

- Added reference, independent, and deliberately mutated Task Board applications, plus evidence-linked per-property replication inventories.
- Added the Playwright runtime capture harness and retained screenshots, full computed CSS maps, DOM/geometry/accessibility snapshots, keyboard outcomes, validation outcomes, API traces, and HTTP 503 failure evidence.
- Verified exact pixel identity between reference and independent baseline across seven declared UI states; the deliberate pluralization mutation produces a 272-pixel mismatch.
- Updated all three capture records and schema fixtures to complete for the declared Task Board scope; updated equivalent and mismatch reports to report completeness separately from agreement.
- Added runtime and schema/integrity CI. The runtime conformance run and final schema/integrity run passed; the runtime artifact is linked from `examples/task-board/README.md` and expires after 30 days.
- Retained explicit exclusions for responsive variants, durable persistence, production network/server behavior, authentication, and authorization; no universal cross-stack equivalence claim is made.


## 2026-11-26 — Phase 6 multi-facet expansion

- Updated the roadmap and tracker to make Phase 6 cover the complete multi-facet capture objective, in sequence: interface audit, behaviour/functionality, business rules, data, persistence, API/messaging/integrations, identity/authorization/security, background processing/errors/configuration/performance, and cross-facet validation.
- Reclassified the existing Task Board result as bounded baseline evidence rather than completion of the overall Phase 6 objective.
- Explicitly recorded that its deterministic in-memory API adapter does not establish production API or persistence behaviour, and that facets absent from this fixture remain unverified rather than globally not applicable.
- Blocked Phase 7 release work until the expanded Phase 6 exit gate is satisfied.


### Correction — Phase 6 status

The initial Task Board completeness result was subsequently re-audited and reclassified. The captures now report incomplete coverage, with seven required properties marked partial across font rendering, business rules, and data. The earlier bounded pixel and workflow comparison results remain valid for the tested conditions, but the earlier claim that the Task Board captures were complete is superseded.


### Phase 6 expanded probe result — 2026-11-26

- Corrected the strict-mode filter selector issue and achieved a successful expanded runtime, integrity, and schema-validation run (#45858743131).
- Updated all three captures and comparison reports with the verified expanded evidence. Inventory counts are now 34 properties per capture: 28 captured, two partial, one not applicable, and three optional exclusions.
- Retained the expanded 41-file evidence archive as artifact #15136459580. The two remaining partial properties are broader font-rendering conditions and the maximum title-length constraint.

- Follow-up validation runs #45859279008 and #45859552354 passed after updating the 34-property captures, comparison coverage, and project documentation.

- Expanded the Task Board runtime capture with responsive/focus/hover/colour-scheme UI states, SVG/script injection-shaped title probes, create/update/delete HTTP 503 failure outcomes, and navigation/paint/resource measurements. Run #45860499892 passed all 13 screenshot comparisons, integrity checks, and schema validation; artifact #15137373210 retains 65 files.
- Added a 15-facet applicability assessment that distinguishes Task Board's implemented facets from full-stack facets absent from its declared boundary.

- Corrected the pointer-driven update/delete screenshot race and passed the complete expanded runtime, integrity, and schema/comparison workflow in run #45861726449. The final Task Board capture inventories contain 38 entries each (33 captured, two partial, one not applicable, two excluded); the 13-state baseline remains pixel-identical and the deliberate mutation remains detectable.
