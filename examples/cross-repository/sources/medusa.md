# Source candidate — Medusa

**Repository:** medusajs/medusa  
**URL:** https://github.com/medusajs/medusa  
**Immutable inspected commit:** 6e28e10acb9676392315b3ff1a9c7147fce4b5ab  
**Pricing module version:** 2.23.1  
**Licence:** MIT for the selected community pricing/core utility files. Enterprise-only paths are excluded.  
**Primary stack:** TypeScript / Node.js commerce platform.  
**Candidate facets:** Business rules; data; behaviour; errors and recovery. Other Medusa facets remain candidates only.

## Evidence inspected

- `packages/modules/pricing/src/utils/validate-price-list-dates.ts`: truthy `starts_at` and `ends_at` values are independently validated with `isDate`; invalid values throw `MedusaError.Types.INVALID_DATA`. The function does not compare start/end chronology.
- `packages/core/utils/src/common/is-date.ts`: `isDate` accepts a non-null value when `new Date(value).valueOf()` is not NaN.
- `packages/core/utils/src/common/errors.ts`: defines `MedusaError` and the `invalid_data` error type.
- `packages/modules/pricing/src/services/pricing-module.ts` around line 1780: the pricing service invokes `validatePriceListDates` before date normalization.

## Selected bounded rule

For optional price-list date fields:
1. Missing, null, and empty-string values bypass validation because the validator checks truthiness.
2. Each truthy start/end value must parse as a valid date.
3. Invalid values throw a Medusa error with type `invalid_data`.
4. Start is checked before end.
5. This validator does not enforce `starts_at <= ends_at`.

## Independent replica

A Python 3.12 ISO-8601 validator is prepared under `conformance/replication-lab/projects/medusa-price-date-python/`. The source harness transpiles the exact pinned validator, `isDate`, and `MedusaError` source files and resolves their utility import to those same source-derived helpers through a temporary module shim. It does not run the complete Medusa application.

## Boundary

The case covers ten inputs: omitted, null, empty, valid/invalid ISO values, Date object, reversed range, and both-invalid precedence. Other JavaScript Date parser formats, database persistence, price-list activation, and full pricing calculations are excluded.

## Status

Pinned source logic and helper implementations are inspected; the independent Python model, executable mutation tests, source harness, capture generator, and workflow are prepared. Runtime comparison and Software Rules evidence validation are pending.
