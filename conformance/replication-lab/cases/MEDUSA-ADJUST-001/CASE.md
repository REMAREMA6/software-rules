# Case — Medusa adjustment, discount, and tax allocation rules

**Case ID:** MEDUSA-ADJUST-001  
**Status:** Pending runtime and evidence validation.  
**Facets:** Business rules; data; behaviour  
**Source:** https://github.com/medusajs/medusa  
**Immutable source commit:** `6e28e10acb9676392315b3ff1a9c7147fce4b5ab`  
**Source version:** Medusa source at pinned commit  
**Source stack:** TypeScript  
**Replica stack:** Python 3.12 / Decimal  
**Licence:** MIT for selected community source files

## Declared boundary

The case extracts and executes the exact `calculateAdjustmentTotal` function from `packages/core/utils/src/totals/adjustment/index.ts`. It compares adjustment amount allocation, tax-inclusive versus tax-exclusive adjustment conversion, aggregation, per-item allocation, missing amounts, and zero/fractional quantity behaviour. It does not execute the full cart service, line-item tax calculator, promotions engine, discount eligibility, discount stacking precedence, cart persistence, or checkout lifecycle.

## Technology-independent rules under test

1. An adjustment with no defined amount is ignored.
2. If a tax rate exists and an adjustment is tax-inclusive, its pre-tax subtotal is amount divided by one plus the tax rate.
3. If a tax rate exists, tax is computed from the adjustment subtotal and added to form the adjustment total.
4. If no tax rate exists, the adjustment amount is used as both subtotal and total, even if marked tax-inclusive.
5. Aggregate subtotal, tax, and total are sums over all defined adjustments.
6. Each adjustment retains its own subtotal and total; an adjustment must not be assigned the cumulative running sum.
7. Aggregate totals are allocated per item using the quantity; a missing or zero quantity follows the source's fallback-to-one behaviour.

## Probe matrix

Nine scenarios cover empty adjustments, exclusive/inclusive tax, multiple and mixed adjustments, missing amount, zero and fractional quantity, and absent tax context. Six deliberate mutations must be detected: inclusive-tax conversion, exclusive-tax application, missing-amount filtering, per-adjustment versus cumulative values, per-item allocation, and zero-quantity fallback.

## Acceptance gate

Accept only after the pinned source function and independent Python Decimal implementation match all nine normalized outputs, all six mutations are detected, and Software Rules 0.2.0 captures/comparison pass schema and evidence-integrity validation. This is bounded adjustment-calculation evidence, not full Medusa commerce or complete business-rule facet coverage.
