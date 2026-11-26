# Changelog

All notable changes to the Software Rules specification, schemas, examples, and repository structure are recorded here.

This project follows a Keep a Changelog-inspired structure. Entries describe user- or implementer-relevant changes, not every typo correction.

## Unreleased

### Added
- Phase 2 core specification: terminology, principles, rule classification, evidence/provenance, observation model, source-derived rules, and core model.
- Cross-facet conceptual model tests for interface layout and API request/response observations.
- Design decisions D-007 through D-009 for scenario/execution/observation separation, rule-versus-observation distinction, and expected-versus-actual outcomes.
- Repository governance documents and conventions.
- Comparative standards review and authoritative research bibliography.

### Changed
- Completed Phase 1 and moved the tracker to Phase 2.
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
