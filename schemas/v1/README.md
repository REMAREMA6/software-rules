# Schema v1 (Draft)

**Maturity:** Draft, not a stable release  
**JSON Schema dialect:** Draft 2020-12  
**Schema draft version:** 0.1.0 (reserved compatibility directory: v1); compatibility is not guaranteed before a stable release.

## Files

- `capture.schema.json` — capture manifest and record collections.
- `records.schema.json` — common target, coverage, scenario, execution, observation, rule, contract, and evidence definitions.
- `facet-payloads.schema.json` — union of the facet payloads.
- `facets/*.schema.json` — 15 typed facet payloads.
- `comparison-report.schema.json` — structural report envelope only; Phase 5 owns comparison semantics.

All schemas use stable URN identifiers under `urn:software-rules:schema:v1:`. The `v1` path/namespace identifies the intended major compatibility family; the current draft version is `0.1.0`, not a stable 1.0.0 release. These URNs are identifiers, not network retrieval endpoints.

## Normative distinctions

- Runtime observations require a runtime method, an execution or runtime interval, and at least one evidence reference.
- Runtime rules link to runtime observations.
- Source-derived rules use a separate record and source evidence references, plus explicit verification state.
- Declared contracts remain separate from both.
- Expected outcomes are stored on scenario definitions; actual facts are observations; evaluation is not embedded into either.
- Field-state objects distinguish observed, not observed, unknown, unavailable, not applicable, redacted, conflicting, and partial.
- Omission is not equivalent to null, false, zero, or an empty collection.
- Unknown facet-specific fields belong under `extensions`; core records reject unrecognized sibling properties.

## Deliberate limits

These schemas validate structure, not truth, execution, evidence integrity, referential integrity, semantic completeness, or equivalence. Cross-record ID resolution and temporal consistency require conformance checks beyond JSON Schema. Facet payload dimensions are intentionally mostly optional because captures may be partial; coverage and limitations must disclose gaps.

The comparison report schema does not define matching, canonicalization, tolerance, or difference classification. Those decisions belong to Phase 5.
