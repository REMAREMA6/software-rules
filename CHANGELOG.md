# Changelog

All notable changes to the Software Rules specification, schemas, examples, and repository structure are recorded here.

This project follows a Keep a Changelog-inspired structure. Entries describe user- or implementer-relevant changes, not every typo correction.

## Unreleased

### Added
- Draft schema format bumped to 0.2.0 because replication-scope inventories and separate comparison-completeness reporting are incompatible additions to the 0.1.0 draft.
- Reopened Phase 6 conformance with required replication-scope property inventories, evidence-linked property states, separate comparison completeness results, and integrity checks against false completeness claims.
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
- Original Phase 6 completion is withdrawn pending redo; Task Board captures now explicitly report incomplete replication scope despite matching selected observations.
- Phase 7 started: the replication-completeness requirement is now an explicit review and conformance obligation.
- Phase 6 now distinguishes completed structural cross-record validation from outstanding empirical runtime captures; no browser evidence is represented as collected.
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

## 2026-11-26 — Phase 6 conformance examples

- Added reference, independent, and deliberately mutated Task Board applications.
- Added empirical interface, behavior, and deterministic adapter API captures, plus raw API events.
- Added an unverified source-derived rule with retained source excerpt.
- Added bounded equivalent and actual-mismatch comparison reports.
- Added schema fixtures and cross-record integrity checks for all captures; documented the in-memory adapter and other test limits.
