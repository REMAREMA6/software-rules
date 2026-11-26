# Schema validation

The validation suite uses Ajv 8 with the JSON Schema Draft 2020-12 implementation and `ajv-formats` for date-time format checks.

From the repository root:

```sh
npm install
npm run validate --prefix conformance/validation
```

The suite recursively registers versioned schemas, validates every JSON fixture against `schemas/v1/capture.schema.json`, expects files under `fixtures/valid/` to pass, and expects files under `fixtures/invalid/` to fail.

A fixture passing JSON Schema validation proves only structural validity. It does not prove that referenced IDs exist, that evidence is authentic, that the observation really occurred, or that two captures are equivalent. Those checks require later conformance and comparison work.

No claim is made that the suite has been executed in this repository environment; run it after installing dependencies.
