# Case — Medusa price-list date validation

**Case ID:** MEDUSA-BR-001  
**Status:** Pinned source utility and helpers inspected; independent Python model prepared; runtime comparison pending  
**Facet(s):** Business rules; Data; Behaviour; Errors and recovery  
**Source:** https://github.com/medusajs/medusa  
**Source commit:** 6e28e10acb9676392315b3ff1a9c7147fce4b5ab  
**Pricing module version:** 2.23.1  
**Source stack:** TypeScript / Node.js  
**Replica stack:** Python 3.12  
**Licence:** MIT for the selected source files

## Declared scope

Validate optional `starts_at` and `ends_at` fields using the pinned Medusa `validatePriceListDates` utility and its pinned `isDate`/ `MedusaError` helpers. Probe missing, null, empty, valid ISO, invalid ISO, Date-object, reversed-range, and dual-invalid inputs.

The case is deliberately limited to ISO-8601 strings and Date objects. It does not claim equivalence for every string accepted by JavaScript's permissive `Date` parser.

## Source evidence

- `packages/modules/pricing/src/utils/validate-price-list-dates.ts`: each truthy `starts_at` and `ends_at` value is independently checked with `isDate`; invalid values throw `MedusaError.Types.INVALID_DATA`. The function does not compare start and end chronology.
- `packages/core/utils/src/common/is-date.ts`: `isDate` accepts a value when `new Date(value).valueOf()` is not NaN (except null).
- `packages/core/utils/src/common/errors.ts`: defines `MedusaError` and the `invalid_data` error type.
- `packages/modules/pricing/src/services/pricing-module.ts` around line 1780: the pricing service invokes `validatePriceListDates` before normalizing the date fields.

The source harness transpiles these three exact source files from the pinned commit and resolves the framework utility import to the same pinned helper implementations through a temporary module shim. It does not run the complete Medusa application or pricing database service.

## Rules under test

1. Missing, null, and empty-string date fields bypass validation.
2. Each non-empty start/end field must be parseable as a valid date.
3. Invalid values raise a Medusa error with type `invalid_data`.
4. Start validation occurs before end validation when both are invalid.
5. The validator does not enforce `starts_at <= ends_at`.

## Independent replica

The Python 3.12 implementation uses ISO-8601 parsing and the same declared optional-field and validation-order semantics. It does not import Medusa or TypeScript code.

## Mutation tests

The Python replica is deliberately mutated to reject empty strings, skip end-date validation, enforce chronological ordering, or validate end dates before start dates. Each mutation must produce a comparison mismatch.

## Acceptance gate

Accept only after the pinned source utility runtime and independent Python implementation match all ten probes, executable mutation tests detect each incorrect variant, and Software Rules 0.2.0 captures plus comparison report pass schema and cross-record evidence validation.
