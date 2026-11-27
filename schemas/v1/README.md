# Schema v1 (Draft)

**Maturity:** Draft, not a stable release  
**JSON Schema dialect:** Draft 2020-12  
**Schema draft version:** 0.2.0 (reserved compatibility directory: v1); compatibility is not guaranteed before a stable release.
**Overall specification release:** 0.3.0 Draft. The schema and specification versions are independent.

## Files

- `capture.schema.json` — capture manifest and record collections.
- `records.schema.json` — common target, coverage, scenario, execution, observation, rule, contract, and evidence definitions.
- `facet-payloads.schema.json` — union of the facet payloads.
- `facets/*.schema.json` — 15 typed facet payloads.
- `comparison-report.schema.json` — comparison report structure, alignments, normalization profile, result classifications, coverage, and bounded conclusion.

All schemas use stable URN identifiers under `urn:software-rules:schema:v1:`. The `v1` path/namespace identifies the intended major compatibility family; the current draft version is `0.2.0`, not a stable 1.0.0 release. The corresponding overall specification snapshot is `0.3.0` Draft. These URNs are identifiers, not network retrieval endpoints.

## Normative distinctions

- Runtime observations require a runtime method, an execution or runtime interval, and at least one evidence reference.
- Runtime rules link to runtime observations.
- Source-derived rules use a separate record and source evidence references, plus explicit verification state.
- Declared contracts remain separate from both.
- Expected outcomes are stored on scenario definitions; actual facts are observations; evaluation is not embedded into either.
- Field-state objects distinguish observed, not observed, unknown, unavailable, not applicable, redacted, conflicting, and partial.
- Every capture requires `replicationScope`, including a declared property inventory and an explicit completeness assessment. Captured/partial items link to runtime observations and evidence.
- Replication completeness is separate from schema validity, record integrity, and agreement among compared observations. A structurally valid capture may still be explicitly incomplete.
- Omission is not equivalent to null, false, zero, or an empty collection.
- Unknown facet-specific fields belong under `extensions`; core records reject unrecognized sibling properties.

## Comparison boundary

The report schema validates local structure and classification constraints. It does not verify that referenced captures, observations, alignments, normalization operations, or evidence IDs exist or are semantically compatible. It does not calculate results. Cross-record integrity and comparison correctness require conformance procedures beyond JSON Schema.

See `comparison/` for the normative comparison model and limitations.
