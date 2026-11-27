# Schema and comparison validation

The suite uses Ajv 8 with JSON Schema Draft 2020-12 and `ajv-formats`.

From the repository root:

```sh
npm install --prefix conformance/validation
npm run validate --prefix conformance/validation
npm run test:completeness --prefix conformance/validation
```

The completeness unit test covers all combinations of complete, incomplete, and undetermined capture states, checks their required combined result, and prevents faithful-replication claims when either side is incomplete or undetermined. The runner registers all versioned schemas, validates capture fixtures against `schemas/v1/capture.schema.json`, and validates comparison-report fixtures against `schemas/v1/comparison-report.schema.json`. It also checks that each comparison's combined replication-completeness result agrees with the two capture statuses. Files in each `valid/` directory must pass; files in each `invalid/` directory must fail.

Validation checks structural constraints only. It does not resolve cross-record references, prove evidence authenticity, validate semantic alignment, or recalculate comparison results. Replication-completeness consistency is checked, but the validator cannot prove that the property inventory itself is exhaustive; that requires review of the declared scope and facet requirements.
