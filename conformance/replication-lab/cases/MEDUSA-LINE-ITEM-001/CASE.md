# Case — Medusa line-item subtotal, tax, discount, and total calculation

**Case ID:** MEDUSA-LINE-ITEM-001  
**Status:** PASSED for all fourteen line-item scenarios. The pinned Medusa line-item, adjustment, and tax functions matched the independent Python 3.12 Decimal model; six deliberate mutations were detected; Software Rules 0.2.0 captures/comparison passed schema and evidence-integrity validation in [run #45945304370](https://github.com/REMAREMA6/software-rules/actions/runs/45945304370), artifact `15173899465` (expires 2026-12-27).  
**Facets:** Business rules; data; behaviour  
**Source:** https://github.com/medusajs/medusa  
**Immutable source commit:** `6e28e10acb9676392315b3ff1a9c7147fce4b5ab`  
**Source stack:** TypeScript  
**Replica stack:** Python 3.12 / Decimal  
**Licence:** MIT for selected community source files

## Declared boundary

The case extracts and executes Medusa's exact `getLineItemTotals`, `calculateAdjustmentTotal`, and `calculateTaxTotal` functions. It tests quantity multiplication, tax-exclusive/inclusive pricing, multiple additive tax lines, adjustments, tax on discounted amounts, original versus discounted totals, zero/fractional quantity, and per-adjustment values. It does not execute full cart aggregation, shipping, promotion discovery/eligibility, currency conversion, tax-provider calculation, persistence, or checkout.

## Technology-independent rules under test

1. Line-item base amount is unit price multiplied by quantity.
2. For tax-inclusive prices, subtotal removes the sum of tax rates from the gross amount; for tax-exclusive prices, subtotal is the gross pre-tax amount.
3. Multiple tax lines contribute additively to the tax total.
4. Adjustments are normalized to pre-tax subtotal when tax-inclusive, then tax is calculated on the remaining taxable amount.
5. Discount tax is the difference between original tax and tax after adjustments.
6. The final line-item total is current subtotal minus discount subtotal plus tax on the discounted amount.
7. Original totals remain distinct from discounted totals.
8. Each adjustment retains its own subtotal and total; fractional and zero quantities follow the source's allocation rules.

## Probe matrix

Fourteen deterministic scenarios cover no tax, exclusive/inclusive tax, multiple tax lines, exclusive/inclusive discounts, multiple/mixed adjustments, fractional and zero quantity, and empty tax context. Six deliberate mutations target inclusive conversion, additive tax, discount-tax recalculation, per-adjustment values, quantity allocation, and original-versus-discounted tax.

## Acceptance gate

Accept only after the pinned Medusa functions and independent Python Decimal model match all twelve normalized outcomes, all six mutations are detected, and Software Rules 0.2.0 captures/comparison pass schema and evidence-integrity validation. This is bounded line-item calculation evidence, not full cart totals or complete business-rule facet coverage.
