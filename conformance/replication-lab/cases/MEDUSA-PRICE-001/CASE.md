# Case — Medusa calculated-price and original-price selection

**Case ID:** MEDUSA-PRICE-001  
**Status:** Pending runtime and evidence validation.  
**Facet(s):** Business rules; data; behaviour  
**Source:** https://github.com/medusajs/medusa  
**Immutable source commit:** `6e28e10acb9676392315b3ff1a9c7147fce4b5ab`  
**Source version:** Medusa pricing module at the pinned commit  
**Source stack:** TypeScript / Node.js  
**Replica stack:** Python 3.12  
**Licence:** MIT

## Declared boundary

The case extracts and executes the exact `PricingModuleService.calculatePrices` method body from the pinned source file. Its repository dependency is replaced by a deterministic candidate-price fixture, while rule lookup and tax-preference collaborators are stubbed to return no tax inclusivity. This isolates the service's price selection and returned calculated/original price semantics. It does not test the SQL candidate filtering, quantity tiers, currency normalization, price-list activation windows, tax inclusivity, or database persistence.

## Technology-independent rules

1. A default price is the first candidate without a price-list association.
2. The original price is the first matching non-sale price-list price when present; otherwise it is the default price.
3. An override price selected as the leading price-list candidate becomes both calculated and original price.
4. A sale price is compared with the original price; the lower amount becomes the calculated price.
5. Sale prices are never used as original/reference prices.
6. If only a sale price matches and no default or override exists, the calculated price is the sale price and the original price is null.
7. The method preserves the requested price-set order and omits price sets with no candidate result.

## Probes

Nine deterministic scenarios cover default, sale below/above/equal to original, override, sale-plus-override ordering, multiple override candidates, sale-only/no-original, and a missing price set. The source method is extracted using the pinned TypeScript compiler API and executed with explicit repository/helper stubs. The Python replica independently implements the selected pricing rules.

## Mutation tests

The suite detects always-select-sale, default-as-original, allowing-sale-as-original, choosing the wrong override, and failure to omit a missing price set.

## Acceptance gate

Accept only after all nine source/replica returned-price objects match; all five deliberate mutations are detected; source method provenance and digest are retained; and Software Rules 0.2.0 captures/comparison pass schema and cross-record integrity validation. This is bounded price-selection evidence, not full commerce or business-rule facet coverage.
