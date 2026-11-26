# Schema and comparison validation

The suite uses Ajv 8 with JSON Schema Draft 2020-12 and `ajv-formats`.

From the repository root:

```sh
npm install
npm run validate --prefix conformance/validation
```

The runner registers all versioned schemas, validates capture fixtures against `schemas/v1/capture.schema.json`, and validates comparison-report fixtures against `schemas/v1/comparison-report.schema.json`. Files in each `valid/` directory must pass; files in each `invalid/` directory must fail.

Validation checks structural constraints only. It does not resolve cross-record references, prove evidence authenticity, validate semantic alignment, or recalculate comparison results.
