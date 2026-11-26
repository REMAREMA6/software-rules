# Cross-record integrity validation

**Status:** Draft — Phase 6

JSON Schema validates each record's local shape. It cannot establish that IDs referenced by one record exist elsewhere in the same capture. This validator checks that graph-level layer.

## Run

```sh
node conformance/integrity/test.mjs
node conformance/integrity/validate-integrity.mjs path/to/capture.json
```

## Checks

- Duplicate scenario, execution, observation, and evidence IDs.
- Execution → scenario and target references.
- Observation → target, execution, and evidence references.
- Observation target consistency with its linked execution.
- Runtime rule → supporting, qualifying, and contradicting observations.
- Source-derived rule → source evidence.
- Coverage → scenario and execution references.

## Boundaries

This is not a JSON Schema replacement. Run schema validation first, then this validator. It does not verify evidence authenticity, source revision reachability, semantic alignment between captures, contract correctness, or comparison result correctness. It also does not infer missing references: unresolved links are errors, not implicit absence.
